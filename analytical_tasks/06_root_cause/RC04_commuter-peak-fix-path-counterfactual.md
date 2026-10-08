# RC04 — Which of five delay causes on the commuter line gets this winter's one fix, when the cause that loses the most time is mostly recovered before the terminal

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Supply Chain & Logistics · commuter rail timetable performance |
| Mirrors | Latency attribution along multi-hop paths (an early slow hop whose delay the pipeline's slack absorbs against a short late hop that makes a call miss its batch window, a late linehaul leg recovered by sort slack against a dock overrun that makes parcels miss their wave at a hub), where per-hop latency points at the hop with the most waiting and only a replay of the path shows which hop decides the deadline |
| Decision shape | Which of N root causes gets the fix: one intervention budget this winter |
| Committed call | The cause fixed, the late peak arrivals at the terminal its fix would have avoided this autumn, and the same figure for the runner-up |
| Gap · Pattern | Gap 4 (rule) over Gap 3 (objective) · Pattern B (the published controls pin a path replay) carrying E22 (the deciding comparison is a set of isolated counterfactuals), with E21 (a saturated tie) at rung 1 |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution |
| Measured traps engaged | #20 leaves the deciding comparison unstated · #1 reports a failed back-test, ships anyway · #19 breaks a big tie instead of questioning it |
| Calibration form | Published control set with a reproduction clause: twelve certified fault-free punctuality figures for closed disruptions on the line |
| Driving force | Read segment by segment, the single-track loop loses the most time: since the autumn re-timing a third of inbound trains are held at the meet. The double-track section after the loop carries the timetable's last recovery allowance, which makes up much of each wait. The dwell overruns at the interchange are small but fall after that allowance, and each also holds the following train outside the platform. Only replaying each train's path in timetable order, with the allowances, the preceding train's departure and the opposing train's clearance as inputs, sets the overruns' effect on late arrivals against the loop's, and that comparison reverses the ranking. |

## 1. Situation

A regional commuter line's morning-peak inbound punctuality at the capital terminal (arrival within three minutes) fell from 94.0% last autumn to
86.0% this autumn: 151 late arrivals out of 1,080 trains. Five causes are on the table: conflicts in the terminal throat (A), a bridge speed
restriction imposed in June (B), meets at the single-track loop, re-timed in the autumn timetable (C), dwell overruns at the interchange station,
growing with a new housing district's ridership (D), and conflicts with long-distance trains at the junction (E). There is money for one fix this
winter. The infrastructure manager's performance standard governs how an investment case attributes punctuality.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the train-running records, the delay codes, the working timetable and the twelve published fault-free
  figures. Each cause's gained delay is measured correctly, and no stakeholder's reading of their own numbers is overturned. The difficulty is
  that the decision turns on whole counterfactual autumns that no segment-level or train-level figure contains.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the director's belief, both voices and the licensed basis. The running records still put the largest gained delay at
  the loop, and the delay codes still put it at the terminal.
* **Instrument repair.** Suspect file: the delay-cause code, which records where a train's lateness crossed three minutes, as the terminal saw
  it. Repaired so that every late train carries the seconds each cause added along its path, knock-on credited to its source, rung 0's minutes
  on late trains name C (560 against the throat's 430, D 330); netting the allowance names A (430 against D's 330), and each late train's
  largest cause names C (52 trains against A's 44, D 18). Rungs 1 and 2 read the running records, which are complete, and still name B and C.
  None returns D: a 75-second overrun is rarely a late train's largest cause, and only the replay shows which late arrivals each removal brings
  back under three minutes.
* **Lens swap.** The gained-delay ranking describes where this autumn's trains lost time. The answer is a set of counterfactual autumns, one
  per fix: different trains are late in each, so it is not one population under another lens.

## 3. The driving force

A strong solver knows delay is noticed at the terminal and gained upstream, so it computes delay gained per segment and per dwell, and the loop
wins clearly: since the autumn re-timing, a third of inbound trains are held at the loop's entry signal, four minutes on average. That reading
takes each segment one at a time. The double-track section after the loop carries the working timetable's last recovery allowance, so a train
held at the loop with nothing else against it makes up most of the wait before the interchange, and the loop's waits become late arrivals mostly
on trains that something else also delays. The interchange overruns are small, 75 seconds on average, but they fall after that allowance, so
every second reaches the terminal, and each overrun also holds the following train outside the platform. The comparison that decides the fix is
between whole autumns: each train's path replayed in timetable order with one cause removed, the allowances absorbing what they can, the
preceding train setting the platform release and the opposing train setting the meet. Replayed that way, removing the overruns avoids 96 late
arrivals and removing the loop's waits 61.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Minutes on late trains by the delay-cause code recorded at the terminal | A, terminal throat (610 min) | The codes are the operator's own attribution, and they are complete | The coding guide records a cause where a train's lateness crosses three minutes, at the point of observation; the published controls reproduce 0 of 12 under coded minutes |
| 1 | Incidence: share of late trains that lost at least 30 s at each location; A and B tie at 100%, and the standard's filed two-level tie-break (first the location further upstream, then the larger mean loss per affected train) settles it at level one and names B | B, bridge restriction | It is the standard's own incidence measure, settled by the standard's own filed tie-break | The working timetable under-times both locations against recovery allowances, so every train loses time there by design; incidence reproduces 2 of 12 controls |
| 2 | Gross delay gained per segment and per dwell, summed over the peak | C, single-track loop (1,320 min) | Delay is attributed where it is gained, the textbook correction | The controls: gross subtraction reproduces 7 of 12, missing every disruption ahead of the double-track allowance and every one whose trains were followed within the platform headway |
| 3 | **Decisive:** for each cause, every peak train's path replayed in timetable order without that cause, and the late arrivals avoided compared across causes | **D, interchange dwell overruns (96 avoided)** (5th of 5 on rung 0) | — | — |

* **Position table.** D ranks 5th on rung 0, 4th on rung 1 and 3rd on rung 2, and leads only rung 3. Rung 0's leader beats its runner-up by
  1.61×, rung 2's by 1.47× and rung 3's by 1.57× (96 against the loop's 61). Rung 1 is a designed exact tie (1.00×): A and B sit at 100% under
  every cut-off from 15 to 60 s. The standard's filed two-level tie-break decides it at level one, the location further upstream, and names B,
  the bridge restriction, 14 km upstream of the throat; level two (mean loss per affected train) is never reached. The third candidate trails
  at 73% (1.37×) and D at 55% (1.82×).
* **Discriminator dominance.** The loop carries a 1.78× gross-gain advantage into rung 3 (1,320 against 742 minutes). Late arrivals avoided
  per gained minute are 0.129 for D and 0.046 for C, an edge of 2.80×, 1.31 times the required 1.2 × 1.78 = 2.14; the net margin is 1.57×.
* **Partial correction priced (L3).** Each half-built replay names the loop. Replaying with the allowances but without the platform headway
  credits D only with the trains that overran, 50 avoided, and names C at 61 (1.22×). Replaying with the knock-on but on observed running times,
  so that a train relieved of a wait does not use the allowance it used in fact, credits the loop with every wait in full and names C, 112
  against D's 96 (1.17×).
* **Grid.** Gross attribution (coded, incidence, gross) or a replay, the replay toggled on headway knock-on (off, on) and running (observed,
  recovering to the timetable's minimum), gives seven distinct builds. Coded, incidence and gross name A, B and C; the three incomplete replays
  all name C; only the full replay names D, and it alone reproduces all twelve controls. The nearest wrong cell is the observed-running replay,
  which needs the recovery rule the controls pin.
* **The deciding comparison (#20).** 96 late arrivals avoided by fixing the overruns against 61 by fixing the loop is the sentence the board
  note has to carry; no segment-level table contains it.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The standard requires reproduction of the published figures and does not say how they were produced. No document
   describes recovery, headway knock-on or a replay.
2. **The controls pin a construction, not a menu.** The full replay reproduces 12 of 12 published figures to 0.1 point; the best rival (replay
   without headway) reproduces 9, the observed-running replay 8, gross subtraction 7, incidence 2. Every rival's misses understate the
   punctuality the line would have had, so none reconciles on the twelve-control total either. The replay has no parameter: its inputs are the
   working timetable's running times, allowances, minimum dwells and headways, and the observed positions of the trains around each train.
3. **No arithmetic symptom.** Gained delay sums to each train's terminal lateness net of recovery on every rung; train counts, codes and
   segments reconcile.
4. **Not a row predicate.** Each train's counterfactual depends on the train ahead of it at the interchange, the opposing train at the loop and
   the allowance left after the loop, so it needs trains ordered within the peak and events replayed in sequence.
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
  within the platform headway, so each overrun also held the train behind outside the platform, while in CP-03 the following trains ran more
  than a headway behind. Only the replay reproduces both.
* **Every rule exercised.** One control is a loop disruption whose waits the double-track allowance absorbed in full, one an overrun with no
  following train inside the headway, and one a terminal-throat disruption with no allowance after it, so each element of the replay is tested
  on its own.
* **Resemblance points at the decoy.** This autumn's loss pattern, long waits at the loop, most resembles CP-05, a loop disruption whose
  published gain is the largest in the set.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The board's investment rule: an intervention is judged on the late arrivals at the terminal it would have avoided over the
  autumn peak. The standard's reproduction clause, one sentence. The standard's two-level tie-break for its incidence measure: tied locations
  are ordered first by distance upstream of the terminal, then by mean seconds lost per affected train. The working timetable (running times,
  allowances, minimum dwells, the interchange headway, the planned meets).
* **Empirical pins.** The headway knock-on and recovery to the timetable's minimum running time, both recovered from the controls; timetabled
  meet order holds throughout.
* **Voices.** The operations manager: "Everything bunches in the throat; that's where we lose the trains." The infrastructure planner: "The loop
  is the bottleneck. Since the timetable change trains have stood there every morning."
* **Licensed wrong basis.** The standard records that the operator's performance team attributes punctuality loss by the cause codes
  recorded at the terminal and will present that attribution at the board.

## 8. Determinism by construction

* **Lateness.** Late means arrival at the terminal more than 180 s after schedule; the peak is origin departures from 06:30 to 09:00; cancelled
  trains are outside the measure under the standard.
* **Counterfactual.** Removing a cause sets its excess over the working timetable to zero at its own location only; every later event is
  replayed in timetable order. A late train runs at the timetable's minimum running time, using the allowances, no train leaves a station before
  its booked time, and a train on time keeps its observed running.
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
* Location order inbound: bridge, loop, double-track section carrying the last recovery allowance (2.5 min), interchange, junction, throat.
  330 inbound trains are held at the loop's entry signal, 4.0 min on average, 110 of them among the late trains; overruns average 75 s on 55% of
  trains; the interchange headway is three minutes.
* Repaired attribution on the late trains: minutes C 560, A 430, D 330, E 260, B 160 (1,740, of which the allowance recovers 320); net of the
  allowance A 430, D 330, C 300, E 260, B 100; largest cause per train C 52, A 44, E 25, D 18, B 12.
* Incomplete replays: without the headway C 61, D 50; on observed running C 112, D 96.
* The twelve controls: replay 12/12, no-headway 9/12, observed-running replay 8/12, gross 7/12, incidence 2/12, all misses one way.
* CP-03 and CP-09 are identical on every published column.
* Passenger-count unit rows and short-terminated trips touch no train in the punctuality measure's replay.

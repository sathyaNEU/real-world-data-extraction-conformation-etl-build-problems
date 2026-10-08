# DS15 — Which steel-plant line to enrol in the interruptible programme, when five lines tie at a perfect record that the utility's settled baseline breaks

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Economics · industrial energy procurement |
| Mirrors | Admitting a resource into a firm-capacity product on a performance record measured against a friendlier baseline than the one the product settles on (Google and Meta data-centre demand response, cloud spot-capacity commitments judged on usual load, Amazon carrier programmes admitted on self-reported on-time rates) |
| Decision shape | Hold, forced by a blocking quantity: one line enrolled at the service point next season, or none |
| Committed call | The line enrolled, or that the plant sits the season out; and the number of the 18 test events the best line actually met |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · measured #19's architecture (a saturated tie that the utility's settled baseline rule breaks, the rule recovered by reproduction from the ledger), answered by a hold, with finer controls (#12) at rung 2 and hygiene at rung 1 |
| Gate G mechanism | signal_vs_noise_or_hold, with method_or_model_selection |
| Measured traps engaged | #19 breaks a big tie instead of questioning it · #12 stops at the first control that passes · #4 never tests its reading against the control · #9 picks from the offered options when none passes |
| Calibration form | Settled-transaction ledger: the utility's settlements of last season's 18 test events at the service point, with each event's settled baseline and 15-minute event load |
| Driving force | The plant enrols a line only if it delivered its commitment in every test event. Against the programme guide's ten-day baseline five lines did, and the guide's tie-break picks the largest. The utility settles against the lower of the ten-day average and the load in the hour before dispatch, a rule its own ledger reproduces in 18 of 18 events where the ten-day average reproduces 12. After each day-ahead notice, operators trimmed load in that hour, so lines that ran close to their commitment fall short on the settled baseline: no line meets all 18, and the best two meet 17. |

## 1. Situation

A steel plant can enrol one process line at its service point in the utility's interruptible-load programme next season, and it earns a
capacity credit on the line's committed megawatts. The procurement policy is to enrol only a line that delivered its commitment in every
one of last season's 18 test events, in which the plant took part as a whole. If several did, the plant takes the programme guide's
tie-break (largest commitment). If none did, it sits the season out, because non-performance penalties exceed the credit. Six lines are
candidates. The plant has its SCADA historian (hourly averages), revenue-grade 15-minute submeters on every line, the utility's dispatch log
and day-ahead notices, the programme guide with its worked baseline example, and the settlement ledger. The energy manager says four or
five lines have a perfect record.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct and no stakeholder read is overturned. The historian, the submeters, the dispatch log, the
  guide's worked example and the ledger are all right, and the plant did deliver every event as a whole. The difficulty is that a perfect
  line record is an artefact of the friendlier baseline, and the utility's baseline has to be recovered from its own settlements.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the energy manager's view and the historian. Fifteen-minute submeters on the dispatch windows against the guide's
  baseline still leave three lines at 18 of 18, and the tie-break still enrols the oxygen plant.
* **Instrument repair.** The suspect file is the historian, which carried the melt-shop feeder under two tags for three weeks after the
  SCADA migration. De-duplicated, relabelled, or replaced outright by the revenue-grade submeters, rung 0 enrols the rolling mill, rung 1 the
  rolling mill and rung 2 the oxygen plant; no lower rung holds. No other file is suspect: the submeters, the dispatch log, the notices and
  the ledger are complete and exact, and a baseline is a counterfactual no meter records. The hold still needs the ledger's rule applied
  line by line.
* **Lens swap.** The naive record measures each line against its usual load on ten earlier days. The answer measures it against the lower of
  that and its own load in the hour before dispatch: a different baseline moment, the hour the operators had already trimmed.

## 3. The driving force

A strong solver distrusts the hourly extract. It removes the historian's duplicated feeder tag, moves to 15-minute submeter readings, and
aligns event windows to the dispatch log, because the ledger's interval stamps follow dispatch, not clock hours. Each step is competent, and
three lines still show 18 of 18 against the guide's ten-day baseline, so the tie-break enrols the oxygen plant. But the tie itself is the
warning. The ledger settles the service point against a baseline the guide never states. The ten-day average reproduces 12 of the 18
settled baselines, high-five-of-ten reproduces 9, and the lower of the ten-day average and the load in the hour before dispatch reproduces
all 18. The utility notifies test events a day ahead, and on several event days operators trimmed load before the dispatch minute. On the
settled rule the hour before dispatch becomes the baseline. The oxygen plant delivers 8.70 MW against 9.0 in one interval of event 4, the
ladle preheat 5.88 against 6.0 in event 15, and the compressed-air line falls short in events 9 and 13. No line meets all 18, so the plant
sits out.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Historian hourly averages against the guide's ten-day baseline on clock-hour windows; five lines meet 18 of 18; the guide's tie-break | A, EAF melt shop (24 MW) | The energy manager's extract and the guide's own baseline and tie-break | The historian's tag map: for three weeks after the SCADA migration the melt-shop feeder was recorded under two tags, doubling its baseline days before event 7 |
| 1 | Duplicate tag removed (hygiene); four lines at 18 of 18 | B, rolling mill (14 MW) | Clean data and an unbroken tie | The dispatch log and the ledger's interval stamps: windows start at the dispatched minute (#12), and the roll change in event 12's last 20 minutes falls inside them |
| 2 | 15-minute submeter readings on dispatch windows, guide's baseline; three lines at 18 of 18 | C, oxygen plant (9 MW) | Matches the ledger's 144 event intervals and every window boundary | The ledger's settled baselines: the ten-day average reproduces 12 of 18, and the lower of it and the hour before dispatch reproduces 18 |
| 3 | **Decisive:** each line's baseline as the lower of its ten-day average and its own load in the hour before the dispatched minute; every interval of every event tested | **Hold: no line meets 18 of 18; the oxygen plant and the ladle preheat meet 17** | — | — |

* **Position table.** Rung leaders are the EAF, the rolling mill and the oxygen plant, chosen by the tie-break on commitments of 24, 14 and
  9 MW (margins 1.71× and 1.56×, with the next at 6 MW). On rung 3 the oxygen plant and the ladle preheat lead at 17, so the hold refuses the
  leaders rather than breaking a new tie.
* **Blocking quantity.** The best record on the settled baseline is 17 of 18 (94.4%), and the policy requires 18. Events failed: EAF 3,
  rolling mill 2, oxygen plant 1 (event 4, 8.70 MW against 9.0), ladle preheat 1 (event 15, 5.88 against 6.0), compressed air 2, water
  treatment 5.
* **Falsifiability.** The oxygen plant would have been enrolled had its load in the hour before event 4's dispatch stood at its ten-day
  level, 0.6 MW higher. Any line with every interval of all 18 events at or above commitment on the settled baseline would have been the
  pick.
* **Partial correction priced (L3).** Taking the settled rule's pre-dispatch hour as the clock hour before the event, instead of the hour
  before the dispatched minute, catches only a third of the trimming that began at 13:40 for a 14:20 dispatch,
  clears event 4 and enrols the oxygen plant again. Applying the settled rule only at the service point and sharing its delivered reduction
  by commitment passes every line and enrols the EAF. Applying it to the clean hourly historian averages the 15-minute shortfalls away and
  enrols the rolling mill. Each half-insight lands on a pick.
* **Grid.** Data and windows (historian raw, historian clean, submeters on clock hours, submeters on dispatch windows) × baseline (the guide's
  ten-day average, the settled lower-of rule) gives 8 cells. On the guide's baseline they enrol A, B, B and C; on the settled rule A, B, B
  and, in the full cell only, hold. The nearest pick is the settled rule on dispatch windows with a clock-hour baseline hour (the oxygen
  plant), and it costs one slip: the hour before the dispatched minute.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The tariff says delivered reduction is measured "against the customer baseline load as the utility settles it". The
   guide's only worked example uses the ten-day average. No document states the lower-of rule or says the five-way tie is an artefact.
2. **The reproducing rule is a construction, not a menu.** The lower-of rule reproduces 18 of 18 settled service-point baselines; the
   ten-day average 12 and high-five-of-ten 9, each overstating the baseline in the events after a trimmed hour. *In every settled event the
   service point delivered more than the plant's 25 MW commitment, because its flexible load is three times that,* so the ledger shows "met"
   for all 18 under every baseline and cannot show any line's record. The rule has to be recovered at the service point and rebuilt on each
   line's own meter.
3. **No arithmetic symptom.** Submeters sum to the service-point load within their accuracy class, and every event's total ties to the
   ledger under every rung.
4. **Not a row predicate.** It needs each line's ten-day average per interval, its own pre-dispatch hour from the dispatched minute, the
   lower of the two, the reduction per interval, and an every-interval test across each event.
5. **The enumeration is arithmetic.** No column records a line's settled baseline or delivered reduction. Both are constructed.
6. **No cutover date.** The rule applied all season, and the SCADA migration is decoy material that rung 1 cleans.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The settlement ledger: the 18 test events with the utility's settled service-point baseline and 15-minute event load for every
  interval of each window, end-stamped as its dictionary states, and the delivered reduction against the plant's 25 MW commitment.
* **What it certifies.** The event windows (144 intervals, matched only by dispatch-minute windows) and the baseline rule (18 of 18).
* **What it is blind to.** Any single line's record (property 2).
* **Twin pair.** Events 4 and 11 are identical on every visible ledger and historian column: dispatched at 14:20 for two hours, the same
  ten-day baseline (93.0 MW) and the same event load (31.0 MW). Their settled reductions are 31.0 and 62.0 MW (2.0×). Only the lower-of rule
  separates them: before event 4 the plant had trimmed to 62.0 MW in the hour before dispatch.
* **Every rule exercised.** Two events began mid-hour, which tests the dispatched minute. Seven events followed a trimmed hour and eleven did
  not, so both arms of the lower-of rule are exercised.
* **Resemblance points at the decoy.** The oxygen plant's continuous-process profile resembles the lines that settled perfectly in the
  utility's published programme case studies.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The procurement policy: enrol only a line that delivered its commitment in every test event; if several did, apply the
  guide's tie-break; if none did, do not enrol this season. The programme guide: the tie-break is the largest commitment. The tariff:
  delivered reduction is measured per 15-minute interval against the baseline the utility settles. One sentence each.
* **Empirical pins.** Dispatch windows and the lower-of rule, from the ledger.
* **Voices.** The energy manager: "Four or five of our lines never missed an event." The melt-shop superintendent: "The furnace is the
  biggest lever we have." The finance lead: "Every season we sit out is a credit we don't earn."
* **Licensed wrong basis.** The policy records that the parent company's energy committee reviews enrolments on the historian's hourly
  records against the guide's baseline and will see that basis.

## 8. Determinism by construction

* **Windows.** Dispatches fall on interval boundaries, so every window holds exactly eight whole 15-minute intervals, and the hour before
  dispatch is the four intervals ending at the dispatched minute.
* **Ten-day average.** The same intervals on the ten prior non-event weekdays, the only definition the ledger reproduces.
* **Margins.** Every failing interval sits at least 0.10 MW (1.7%) under commitment on the settled baseline, and every passing one at least
  0.08 MW over it, beyond the submeters' 0.2% accuracy class.
* **Commitments.** Each line's committed MW is filed in the draft enrolment form.

## 9. Prompt sketch and deliverables

> We can enrol one of our lines in the utility's interruptible programme next season, but only one that held its commitment in every test
> event, and the energy manager says several did. Tell me which line we enrol, or that we sit the season out, in one sentence for the plant
> leadership meeting, with how many of the 18 test events the best line really met. Send `enrolment_case.xlsx`, a chart `event_record.png`,
> and a one-page `enrolment_note.pdf`.

* `enrolment_case.xlsx` — each line's events met under each construction, the energy-intensity sheet (ask A), the stops sheet (ask B) and
  the baseline sheet (ask C).
* `event_record.png` — a grid of six lines × 18 events coloured met or failed on the settled baseline, the oxygen plant's event 4 inset
  with its ten-day baseline, its pre-dispatch hour, its event load and the commitment as labelled lines, and each line's tally at the row
  end.
* `enrolment_note.pdf` — the hold, the blocking quantity, and what would have enrolled the oxygen plant.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each line and quarter of last year, energy per tonne of product. *Device:* the production log
  books a heat in progress at month-end to the month it taps, as its dictionary documents. Allocating tonnes by heat start misstates the
  melt shop's and the ladle preheat's January and July figures.
* **Ask B (device-carried).** For each line, unplanned stops longer than 30 minutes last season. *Device:* the maintenance log splits a stop
  across a shift change into two records with a continuation flag. Counting records overstates the two continuous-process lines by about a
  quarter.
* **Ask C (validity).** The ledger's 18 settled baselines under the three baseline rules (hits), and each line's events met under the four
  rung constructions.
* **Decoupling.** Clearing the settled rule changes no figure in asks A or B. Production heats and maintenance stops never enter an interval
  reading or a baseline.

## 11. Rubric arithmetic

6 lines × 4 rung constructions (events met) + 3 baseline rules' hits + 6 lines' worst-interval shortfall (ask C) + 6 lines × 4 quarters
(ask A) + 6 stop counts (ask B) + the hold, the blocking quantity and the falsifier + 4 named chart parts + 3 files ≈ 70 criteria.

## 12. World-building constraints

* Commitments: EAF 24, rolling mill 14, oxygen plant 9, ladle preheat 6, compressed air 6, water treatment 3 MW. The plant's last-season
  service-point commitment is 25 MW, and its delivered reduction exceeds it in all 18 events under every baseline.
* Settled baselines: lower-of rule 18 of 18, ten-day average 12, high-five-of-ten 9. Seven events followed a trimmed pre-dispatch hour.
* On the settled baseline: oxygen plant 17 (event 4, 8.70 MW against 9.0), ladle preheat 17 (event 15, 5.88 against 6.0), compressed air
  16 (events 9 and 13), rolling mill 16, EAF 15, water treatment 13. On the guide's baseline the oxygen plant, ladle preheat and compressed
  air are 18 of 18.
* Events 4 and 11 are identical on every visible ledger and historian column. Heats and maintenance records never touch meter readings.

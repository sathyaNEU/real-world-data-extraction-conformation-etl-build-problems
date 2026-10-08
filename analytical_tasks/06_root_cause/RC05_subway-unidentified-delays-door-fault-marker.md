# RC05 — Which delay cause gets the subway's one remediation programme, when the biggest cause is hiding in the unidentified incidents

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Policy & Education · public transit administration |
| Mirrors | Incident attribution where a large share of incidents closes unclassified (SRE tickets closed as "unknown" at cloud platforms, warehouse exceptions coded "other", hardware returns with no fault found at Apple and Google), and the cause is recoverable only from a downstream repair record |
| Decision shape | Which of N root causes gets the fix: one remediation programme for the coming year |
| Committed call | The programme funded, and the weekday peak delay minutes its cause accounted for over the last twelve months |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · Pattern B (the counterparty's settled acknowledgements pin the assignment) carried by E19 (a latent attribution marker), with E18 (the segment coarsened) at rung 1 |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution |
| Measured traps engaged | #17 guesses an attribution the data can settle · #14 coarsens the segment it was asked about · #4 never tests its reading against the control |
| Calibration form | Counterparty acknowledgement file: the train manufacturer's accepted and rejected warranty delay claims for four closed quarters |
| Driving force | 38% of peak delay minutes are filed "unidentified", because station staff cannot see why a train will not leave. Most of them are door faults on the new fleet. Nothing on the delay record says so. The marker runs through three other records: the train occupying the platform at that minute, its removal from service before the end of the trip, and the depot repair order that closes that removal's defect ticket with a door defect. The nearer records point elsewhere: the set-out log files most of these removals under "train control", the screen message a door that will not prove closed produces. The manufacturer's acknowledgements follow the full chain exactly. |

## 1. Situation

A city subway's delay minutes rose almost 90% on last year. The agency launched a programme against passenger-related incidents, its most frequent
code, and the chief operating officer points to two multi-hour switch failures. The board will fund one remediation programme from a catalogue of
five: passenger-incident response (A), door remediation on the new train fleet (B), signal-system remediation (C), switch and track renewal (D) and
crew availability (E). The service standard sets how a programme is judged. The fleet is under the manufacturer's warranty, which pays for delay
the manufacturer acknowledges as its own.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: incident counts, coded minutes, the monthly report's group table, the platform occupancy log, the set-out
  log, the repair orders and the acknowledgements. "Unidentified" is an honest code for what staff could see. No stakeholder's reading of their
  own numbers is overturned; the task is to settle an attribution the delay file never carried.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the passenger programme, the operating officer's view and the licensed basis. The coded peak minutes still name the
  signal system, and the unidentified minutes still sit in a code no programme covers.
* **Instrument repair.** Give station staff perfect diagnostics and the delay file would code door faults directly, but the decision would
  still run on the last twelve months as filed. The assignment the manufacturer settled is reproducible from records already in the pack, so the
  difficulty is constructing it, not repairing it.
* **Lens swap.** The naive build counts incidents by the code staff chose; the answer counts minutes by the defect the depot found: different
  incidents land in each programme.

## 3. The driving force

A strong solver moves from counts to minutes, and from the weekday table to the peak periods the standard names. On coded peak minutes the
signal system leads. The 19,000 unidentified peak minutes are then either dropped (no programme owns that code), spread pro rata, or handed to
the signal system on the intuition that unexplained holds on automated lines are signalling. All three keep the signal system in front. The
manufacturer's acknowledgement file is the only settled statement of which unidentified incidents were train defects. Its acceptances follow a
chain no column states: the train standing at that platform at that minute (from the occupancy log), that train set out of service before the
end of its trip (from the set-out log), and the depot repair order that closes that set-out's defect ticket with a door defect, a median of 19
days later when the part is fitted. Neither nearer record says door. A door that will not prove closed leaves the train without departure
authority, so the controller files the set-out under "train control", and that night's exam downloads the train-control fault log before any
door work. Applied to the last twelve months, 14,600 of the unidentified peak minutes are door faults, 1,000 are onboard train-control defects
(signal-system scope) and 3,400 stay unassigned.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Weekday incidents by code, counted | A, passenger incidents (5,200) | The agency's own reading, and the code is by far the most frequent | The service standard judges a programme on delay minutes, not incidents |
| 1 | Weekday delay minutes by code from the monthly report's table, mapped to programmes | D, switches and track (27,000 min) | Minutes, from the published table, through the catalogue's own codes | The standard names the weekday peak periods (07:00–10:00, 16:00–19:00), and the two long switch failures ran mostly before 07:00 |
| 2 | Weekday peak delay minutes by code, unidentified minutes left out or spread pro rata | C, signal system (12,500; 19,364 pro rata) | The standard's own measure at its own grain, every coded minute accounted for | The acknowledgement file: the manufacturer accepted 61% of closed-quarter unidentified incidents as train defects |
| 3 | **Decisive:** unidentified peak minutes assigned through the occupancy, set-out and repair-order chain the acknowledgements follow | **B, new-fleet doors (17,700 min)** (5th of 5 on rung 0) | — | — |

* **Position table.** B ranks 5th on rungs 0 and 1 and 4th on rung 2, and leads only rung 3. Rung leaders beat their runners-up by 4.73×,
  1.29×, 1.30× and 1.31×.
* **Discriminator dominance.** The signal system carries a 4.03× lead on coded peak minutes into rung 3 (12,500 against 3,100). The chain
  assigns 14,600 unidentified minutes to B and 1,000 to C, an edge of 14.6×, above the required 1.2 × 4.03 = 4.84; as a swing, 13,600 minutes
  against a 9,400-minute lead, 1.45×. The net margin is 1.31×.
* **Partial correction priced (L3).** Every half-built chain overshoots onto C, rung 2's answer. Following the train to its set-out but
  reading the set-out log's own reason, not the ticket's repair order, files 12,400 of the 14,600 door minutes under "train control": C 25,900
  against A's 9,600 (2.70×), B 5,300. Skipping the set-out and taking the unit's next repair order picks up the overnight train-control
  download that precedes the door order for 13,900 of the door minutes: C 27,400 against A's 9,600 (2.85×), B 3,800. Spreading the
  unidentified minutes pro rata gives C 19,364 against A's 14,872 (1.30×), B 4,802; handing the two automated lines' unidentified minutes to
  the signal system gives C 23,900 against A's 9,600 (2.49×).
* **Grid.** Grain (weekday, peak) × measure (counts, minutes) × unidentified (dropped, pro rata, by line, by set-out reason, by next repair
  order, by chain) gives fourteen feasible builds, counts taking only "dropped". Every weekday build names A, C or D (the weekday chain gives B
  23,000 against D's 27,000), every peak build short of the full chain names A (counts) or C (minutes), and only the peak chain names B.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The delay guide defines "unidentified" as a code staff use when no cause is visible. The warranty contract says the
   manufacturer reviews each claim. No document says what the manufacturer checks or that set-outs and repair orders identify door faults.
2. **The corpus pins a construction, not a menu.** The chain reproduces 1,860 of 1,860 acknowledgements. Accepting on the door code alone
   reproduces 1,212, on the set-out log's recorded reason 1,296, and on the unit's next repair order 1,251. The rule is a three-hop join
   through other entities' records (two temporal hops, then the set-out's defect ticket), not a parameter.
3. **No arithmetic symptom.** Minutes, incidents and codes reconcile under every rung; unidentified minutes are a complete, legitimate code.
4. **Not a row predicate.** The delay record has no train or unit id. The train comes from platform occupancy at that station and minute, the
   unit from the train's formation, and the defect from a repair order dated after the incident.
5. **The enumeration is arithmetic.** No column marks an unidentified incident as a door fault; 14,600 minutes are built from four files.
6. **No cutover date.** Door faults rose with the fleet's mileage across the year; the dated events (the switch failures, the passenger
   programme's launch) are the decoys.
7. **Survives deletion.** With every voice gone, coded peak minutes still name the signal system.

## 6. The calibration corpus

* **Form.** The manufacturer's acknowledgement file: 1,860 incidents claimed in four closed quarters (coded door faults plus unidentified
  incidents on new-fleet trains), each accepted or rejected, with the occupancy, set-out and repair records for those quarters.
* **What it pins.** The assignment rule (above). The two chain fragments miss one way: each rejects door claims the manufacturer accepted,
  the set-out reason because it reads "train control" and the next repair order because the overnight download comes first, so neither
  reconciles to the quarters' accepted minutes; both understate them in every quarter.
* **Twin pair.** Quarters Q1 and Q3 carried identical claim profiles: incidents by code, minutes by line, new-fleet share and peak share. The
  manufacturer accepted 3,940 minutes in Q1 and 1,880 in Q3 (2.1×). Only the chain reproduces both; every code-, line- or share-based rule
  returns the same figure for each.
* **Every rule exercised.** Q2 holds set-outs for brake defects (rejected), door repair orders raised at routine inspection with no
  set-out (rejected) and train-control set-outs whose ticket closed on a door defect (accepted), so each link of the chain is tested on its
  own.
* **Resemblance points at the decoy.** This year's unidentified minutes concentrate on the two automated lines, the profile of Q3, the quarter
  with the fewest accepted door claims.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The service standard: a remediation programme is judged on the weekday peak-period delay minutes its cause accounted for
  over the last twelve months, the peak periods being 07:00–10:00 and 16:00–19:00. The programme catalogue lists each programme's codes.
* **Empirical pins.** The assignment chain, from the acknowledgement file.
* **Voices.** The customer services director: "Passenger alarms are most of our incidents, so that's where the minutes go." The signals
  engineer: "Unidentified holds on the automated lines are the signal system; you can watch them on the control screen."
* **Licensed wrong basis.** The standard records that the board's finance committee reviews remediation on the monthly report's weekday
  minutes by code group and will present that table.

## 8. Determinism by construction

* **Peak minutes.** Incidents crossing a peak boundary are split by minute; every delay record carries a start time and duration.
* **Train identity.** One train occupies a platform at a time, so the occupancy join is unique for every unidentified incident.
* **Set-out and repair.** A set-out counts when it precedes the end of the same trip; the repair order is the one that closes the set-out's
  defect ticket, matched on the ticket number; both resolve without a tolerance.
* **Window.** Twelve complete months, ending before the extract; every repair order for the window is closed.
* **Rounding.** Minutes are filed to the nearest hundred and the committed figure sits mid-bin.

## 9. Prompt sketch and deliverables

> Delay minutes on the subway are up almost 90% on last year and the board will fund one remediation programme. Our chief operating officer
> is sure it's the two switch failures. Tell me which programme we fund and how many peak delay minutes its cause cost us over the last
> twelve months, to the nearest hundred, in one sentence for the board pack. Send `delay_cause_case.xlsx`, a chart `peak_minutes_by_cause.png`
> and a short `remediation_memo.pdf`.

* `delay_cause_case.xlsx` — the five causes under each construction, the service-hours sheet (ask A), the lift and escalator sheet (ask B)
  and the acknowledgement reproduction (ask C).
* `peak_minutes_by_cause.png` — stacked horizontal bars per cause, coded peak minutes and assigned unidentified minutes as separate segments,
  with the weekday total as a ghost bar behind each, the unassigned remainder as its own bar, and the funded cause highlighted.
* `remediation_memo.pdf` — the funded programme, its minutes, and why the other four are not it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the four lines and each of the last twelve months, scheduled and operated train-hours.
  *Device:* gap trains inserted by control appear in the operations log with a gap flag and no timetable id, as the service summary's notes
  document; including them in scheduled hours overstates two lines' scheduled service by about 4%.
* **Ask B (device-carried).** For the 20 busiest stations, lift and escalator outage events and outage hours over the twelve months.
  *Device:* an outage running past midnight is written as one row per calendar day, later rows carrying a continuation flag, as the asset
  log's schema documents; counting rows as events inflates events at eleven stations.
* **Ask C (validity).** For each closed quarter, accepted minutes under each of the four assignment rules; and each cause's peak minutes under
  each of the four rung constructions.
* **Decoupling.** Clearing the chain changes no figure in asks A or B; neither touches a delay record.

## 11. Rubric arithmetic

4 lines × 12 months × 2 figures (ask A) + 20 stations × 2 figures (ask B) + 4 quarters × 4 rules + 5 causes × 4 constructions (ask C) + the
funded programme, its minutes and the runner-up's + 5 named chart parts + 3 files ≈ 185 criteria.

## 12. World-building constraints

* Weekday counts A 5,200, E 1,100, C 900, D 700, B 600; weekday coded minutes D 27,000, A 21,000, C 15,000, E 8,800, B 5,400; peak coded
  minutes C 12,500, A 9,600, D 6,800, B 3,100, E 2,600; 19,000 unidentified peak minutes, of which the chain gives B 14,600 and C 1,000
  and leaves 3,400 unassigned (1,100 brake and traction set-outs, 2,300 with no set-out). Rung 3: B 17,700, C 13,500, A 9,600, D 6,800, E 2,600.
* Of the 14,600 door minutes, 12,400 were set out under "train control" and 2,200 under "doors"; for 13,900 the overnight train-control
  download preceded the door order. Door orders are raised a median of 19 days after the set-out.
* The two switch failures run 9,000 minutes, mostly between 05:00 and 07:00. Of the 30,000 weekday unidentified minutes, 17,600 are door
  faults, 14,600 of them in the peaks.
* Acknowledgements: chain 1,860/1,860; door code 1,212; set-out reason 1,296; next repair order 1,251. Q1 and Q3 identical on every claim-profile
  column.
* Gap trains and outage continuation rows touch no delay record, occupancy row, set-out or repair order.

# AD04 — Which pump gets the outage's one bearing overhaul, when five pumps tie at the top of the vibration standard and only one tie survives the run counters

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Supply Chain & Logistics · utility asset maintenance |
| Mirrors | Breaking a saturated priority tie by reconciling what each monitoring record actually evidences (data-centre disk replacement queues where many drives report the maximum health warning, airline engine-shop slots when several engines sit at the top alert level, conveyor maintenance windows in large fulfilment networks) |
| Decision shape | Which of N gets one scarce thing: the November outage's single crane crew and spare bearing cartridge |
| Committed call | The one duty pump overhauled in the November outage |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · a saturated tie broken by reconciliation across files of record (E21), with Pattern B (the close-outs' settled shares pin the reconciliation) and a stale status flag at the lower rung (E33) |
| Gate G mechanism | method_or_model_selection, with signal_vs_noise_or_hold support |
| Measured traps engaged | #19 breaks a big tie instead of questioning it · #5 takes the population a flag or filter suggests · #4 never tests its reading against the control |
| Calibration form | Prior-period close-out: the close-out reports of the last three outages, with each duty pump's settled zone-D share and the as-found damage of every pump opened |
| Driving force | The standard ranks duty pumps by the share of their running hours spent in vibration zone D, and the platform's export computes it over the snapshots it received. Five pumps read 100%, a natural ceiling, and the documented tie-break picks among them. Gateway outages left running hours that no snapshot covers, which shows only when snapshots are laid against the PLC run counters; counted as nothing, those hours break the tie, and only one pump's 100% survives. |

## 1. Situation

A water utility's reliability team has one crane crew and one spare bearing cartridge for the November outage, enough to overhaul a single
pump across nine pumping sets, each a duty pump with a standby. Its prioritisation standard gives the slot to the duty pump with the
highest share of its 180-day running hours in vibration zone D, ties to the higher criticality class and then to more hours since the
last overhaul. The condition-monitoring platform exports that share for every pump, and five read 100%. The asset register, the operations
changeover log, the PLC run counters, the snapshot file and the close-outs of the last three outages ship with it.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: each snapshot's zone, the platform's share over the snapshots it received, the run counters and the
  close-outs. The platform labels its share as computed over received snapshots. Nothing reported is overturned and no stakeholder's
  read is corrected; the difficulty is that the standard's quantity is a share of running hours, which the export only equals where
  coverage is complete.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the reliability lead's view and the platform export. Computing the share from the snapshot file, the natural
  build, still gives five pumps at 100% and the tie-break still picks a wrong pump.
* **Instrument repair.** Give every pump a perfect sensor and a perfect gateway from now on; the window has already happened, and the
  hours the gateways missed carry no zone. A better instrument of the received snapshots changes none of the five 100% readings.
* **Lens swap.** The naive read is a share of received snapshots; the answer is a share of PLC running hours, a different denominator
  population, at the pumps the changeover log shows on duty rather than those the register lists.

## 3. The driving force

A strong solver applies the standard, notices the register's duty flags are stale for two sets and rebuilds the population from the
changeover log, sees the five-way tie and, distrusting a criticality tie-break, separates the tied pumps by an uncapped severity, mean overall
velocity. Each step is competent. But the tie is not a property of the pumps. Every sensor reports every two hours while its pump runs,
and the platform divides zone-D snapshots by snapshots received. At two stations the cellular gateway was down for 19 and 31 days in
August and September, and at a third for 9 days; the pumps ran, as the PLC counters show, and nothing was received. Those hours are in the
standard's denominator and in no snapshot. Counted at the lowest value the records allow, none of them evidenced in zone D, four of the
five 100% readings fall, to between 61% and 84%. The settled shares in the last three close-outs reproduce only under that
reconciliation.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The platform's share for the nine pumps the asset register flags as duty; five at 100%; tie-break by criticality class, then hours since overhaul | A (class 1, 41,200 h; 1.22× B) | The standard and its documented tie-break, executed on the platform's own figure | The operations changeover log: A has run as standby since 14 June, when its set changed over, and a standby pump is overhauled without an outage |
| 1 | Duty pumps from the changeover log, the platform's share, the documented tie-break | B (class 1, 33,900 h; 1.22× C) | The right population, the standard's metric, the standard's tie-break | The 2025 close-out: the tie-break's pick was found with 0.3 mm² of spalling while a tied pump failed in service in March |
| 2 | Duty pumps from the changeover log; the tie separated by mean overall velocity over the window | C (9.8 mm/s; 1.21× D) | An uncapped physical severity that splits a tie the close-out shows is not real | The 2025 close-out's settled shares: the four pumps the export tied at 100% were settled at 100%, 92.4%, 81.3% and 67.0% |
| 3 | **Decisive:** running hours evidenced in zone D (each snapshot covering the two hours it closes) over PLC running hours, unevidenced hours counted as none | **E (100%)** (5th of 9 on rung 0) | — | — |

* **Position table.** E ranks 5th on rung 0 (class 2, 19,500 h), 4th on rung 1 and 3rd on rung 2 (7.6 mm/s), and leads only rung 3, where it
  is the one pump left at 100%, 1.19× D (84.0%).
* **Discriminator dominance.** C carries a 1.29× velocity advantage over E into rung 3 (9.8 against 7.6 mm/s). On the reconciled share E
  holds 100% to C's 61.4%, an edge of 1.63× against the 1.2 × 1.29 = 1.55 required; net 1.26×.
* **Partial correction priced (L3).** A solver who reconciles against the run counters but fills unevidenced hours at each pump's own
  received share keeps all five at 100% and is back at the tie-break's B. A solver who reconciles but keeps the register's duty flags names
  A, whose 100% sits in May, before its changeover, with full coverage.
* **Grid.** Population (register or changeover log) × share (received snapshots or running hours) × tie handling (tie-break or velocity)
  gives eight cells. Register cells name A; changeover-log cells on received snapshots name B or C; running-hours cells need no tie
  handling and name E with the changeover-log population or A with the register's. The nearest wrong cell (A) needs the stale flag kept.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The standard defines the share in words and gives the tie-break. No document says the export divides by received
   snapshots, that gateways failed, which file holds running hours, or how hours with no snapshot count. The run counters are reached by
   no earlier rung.
2. **The corpus pins a construction, not a menu.** The reconciled share reproduces all 27 settled shares in the three close-outs to 0.1%;
   the export's share reproduces 16 of 27 and overstates every one it misses (by 6.3 points on average), so it fails in aggregate too. The
   reproducing rule is a construction: hours evidenced per pump come from aligning two-hourly snapshots with daily run counters, and no
   column holds them.
3. **No arithmetic symptom.** The export recomputes exactly from the snapshot file, the run counters tie to the station energy meters, and
   the snapshot file has no duplicates or gaps flagged; a gap shows only against a different file's hours.
4. **Not a row predicate.** It needs a time alignment of snapshots to each pump's running intervals, a sum of covered hours, and a ratio
   against a counter from another system.
5. **The enumeration is arithmetic.** Which pumps keep 100% is computed per pump; no field marks coverage.
6. **No cutover date.** Gateway outages are scattered across three stations and do not step any vibration series; the only dated event in
   the ladder, A's June changeover, sits under the decoy.
7. **Survives deletion.** With every voice and the export removed, the answer and the difficulty are unchanged.

## 6. The calibration corpus

* **Form.** The close-out reports of the 2023, 2024 and 2025 outages: for each of the nine duty pumps at the time, the settled zone-D share
  to 0.1%, the slot decision, and the as-found spalling of every pump opened in the outage or after an in-service failure.
* **What it pins.** The reconciled share reproduces 27 of 27 settled shares; the received-snapshot share 16 of 27; a calendar-hours
  denominator 8 of 27. In every outage the slot went to a pump at a settled 100%.
* **Twin pair.** In the 2025 close-out, pumps P4 and P7 are identical on the export's share (100%), criticality class, model, duty, hours
  since overhaul and mean velocity. Their settled shares were 100% and 81.0%, and their as-found spalling 6.4 mm² and 3.1 mm² (2.06×).
* **Every rule exercised.** One 2024 pump's gap fell while it was stopped, so it costs nothing; one 2023 pump ran only on the counter's
  last day before the window, so the window cut is exercised; one 2025 set changed duty mid-window.
* **Resemblance points at the decoy.** E's profile (class 2, recent overhaul, moderate velocity) resembles the pumps found with mild damage
  in past outages; C's high velocity resembles the 2024 slot pump, found badly spalled.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The standard: the slot goes to the duty pump with the highest share of its 180-day running hours in vibration zone D,
  ties to the higher criticality class and then to more hours since the last overhaul. The standard's scope: a standby pump is overhauled
  without an outage. The operations manual: the changeover log is the record of which pump in a set is on duty.
* **Empirical pins.** The run counter as the denominator and unevidenced hours counted as none, both from the close-outs' settled shares.
* **Voices.** The reliability lead: "The platform rates every pump the same way; I'd go with whatever it rates worst." The station
  supervisor at C: "You can hear C from the car park. It's the one that'll go."
* **Licensed wrong basis.** The standard records that the insurer's engineering surveyor ranks pumps on mean overall velocity and will
  review the outage plan on that basis.

## 8. Determinism by construction

* **Snapshot cover.** Every sensor reports every two hours while running, so each snapshot evidences the two hours it closes and no
  interval convention exists. Run counters are daily and snapshots are timestamped, and no gateway outage starts or ends inside a running
  interval.
* **Window.** The 180 days end at the extract; 150- and 210-day windows leave E alone at 100%.
* **Duty.** The changeover log and the run counters agree on one duty pump per set on every day of the window except the two changeover
  days, which fall outside the zone-D hours.
* **Rounding.** Settled shares are quoted to 0.1% and every reconciled share in the live window sits at least 0.5 points from any other.

## 9. Prompt sketch and deliverables

> Our November outage has one crane crew and one bearing cartridge, enough to overhaul a single pump. The reliability lead would give it to
> whichever pump the monitoring platform rates worst. Name the pump in a sentence I can put in the outage plan, and send `outage_slot.xlsx`
> with the sheets below, a chart `zone_d_coverage.png`, and a short `slot_decision.md`.

* `outage_slot.xlsx` — the prioritisation build for the nine sets, the lubrication sheet (ask A), the station energy sheet (ask B) and the
  close-out reproduction (ask C).
* `zone_d_coverage.png` — for each duty pump, a timeline of the 180 days showing PLC running hours, zone-D snapshots and gateway gaps,
  with the received-snapshot and running-hour shares printed side by side and the slot pump highlighted.
* `slot_decision.md` — the committed pump and why each of the other tied pumps falls away.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the nine duty pumps, lubrication orders completed in the last twelve months and grease
  applied in grams. *Device:* a lubrication round is one parent work order with a child line per pump, and grease is booked on the parent
  and apportioned by the route sheet, as the maintenance-system guide says. Booking the parent's quantity to its first child gives one
  pump per route the whole round's grease.
* **Ask B (device-carried).** For each station, energy per megalitre delivered last quarter. *Device:* three stations return part of their
  outlet flow to the well through a separately metered recirculation line, shown on the hydraulic schematics. Dividing by outlet flow
  instead of delivery understates their kWh per megalitre.
* **Ask C (validity).** For each of the three close-outs, the settled shares each of the four constructions reproduces out of 9.
* **Decoupling.** Clearing the reconciliation and the duty correction changes no figure in asks A or B.

## 11. Rubric arithmetic

9 pumps × 2 (ask A) + 9 stations × 2 (energy and delivery, ask B) + 3 close-outs × 4 constructions (ask C) + the committed pump, its
reconciled share and the margin over D + 5 named chart parts + 3 files ≈ 59 criteria.

## 12. World-building constraints

* Five pumps read 100% on the export (A, B, C, D, E); reconciled, E stays at 100% and D, B and C fall to 84.0%, 79.0% and 61.4%.
* A's set changed over on 14 June; A's 100% is May's running hours. A second set changed over in July with no effect on the tie.
* Gateway outages: 19 and 31 days at the stations of B and C, 9 days at D's; E's gateway never failed.
* Tie-break values: A 41,200 h, B 33,900 h, C 27,800 h (class 2), E 19,500 h (class 2). Velocities: C 9.8, D 8.1, E 7.6, B 6.9 mm/s.
* The close-outs hold 27 settled shares; P4 and P7 are identical on every export-visible column.
* Lubrication routes and recirculation lines never touch the snapshot file or the run counters.

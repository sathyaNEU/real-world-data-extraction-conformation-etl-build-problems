# AD04 — Which pump gets the outage's one bearing overhaul, when most of the worst pump's zone-D hours are ones a new bearing would not remove

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Supply Chain & Logistics · utility asset maintenance |
| Mirrors | Sending one repair where it removes the most of a condition the repair can actually fix (drive replacements in hyperscale fleets where read errors come from controllers, airline engine-shop slots where vibration is installation-driven, conveyor maintenance in fulfilment networks where jams are load-driven) |
| Decision shape | Which of N gets one scarce thing: the November outage's single crane crew and spare bearing cartridge |
| Committed call | The one duty pump overhauled in the November outage |
| Gap · Pattern | Gap 3 (objective) over Gap 2 (population) · a serviceable share behind a join (E06): only the zone-D hours inside each pump's preferred operating region, reached through the flow log, the drive log and the pump curves, are hours a bearing overhaul removes; a stale duty flag at the lower rung (E33) |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #7 uses the ready-made measure · #5 takes the population a flag or filter suggests · #4 never tests its reading against the control |
| Calibration form | Prior-period close-out: the close-outs of the last three outages and of every bearing overhaul since 2023, eleven in all, each with the pump's zone-D running hours in the 180 days before and after |
| Driving force | The standard sends the overhaul where it will take the most running hours out of vibration zone D, and a careful analyst counts each duty pump's zone-D running hours. A new bearing cartridge removes only the vibration a bearing causes. Below about 55% of a pump's best-efficiency flow, recirculation holds it in zone D whatever its bearing, and 82% of C's zone-D hours are night running at low flow; 92% of E's sit inside its preferred operating region, where only the bearing explains them. Classifying every zone-D snapshot by the pump's flow against its best-efficiency flow at that hour's drive speed, a join of the snapshots to the flow log, the drive log and the pump curves, is the construction the close-outs reproduce. |

## 1. Situation

A water utility's reliability team has one crane crew and one spare bearing cartridge for the November outage, enough to overhaul a single
pump across nine pumping sets, each a duty pump with a standby. Its prioritisation standard gives the slot to the duty pump whose overhaul
will take the most running hours out of vibration zone D over the year after the outage. The condition-monitoring platform exports each
pump's share of two-hourly snapshots in zone D. The asset register (with duty flags and each pump's manufacturer curve), the operations
changeover log, the PLC run counters, the pumps' discharge-flow log, the drive log, the snapshot file and the overhaul close-outs ship with it.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: each snapshot's zone, the platform's share, the run counters, the flows, the drive speeds, the pump
  curves and the close-outs. C's zone-D hours are real zone-D hours. Nothing reported is overturned and no stakeholder's read is corrected;
  the difficulty is which zone-D hours a bearing overhaul can take away.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the platform export. Counting zone-D running hours per duty pump from the snapshot file, the
  natural careful build, still names C.
* **Instrument repair.** Suspect files: the asset register's duty flags, stale since two changeovers, and the snapshot file, which reads
  each pump every two hours. Repaired, with current duty on every pump and a reading every minute, rung 0 becomes rung 1 and names B (84%),
  rung 1 still names B and rung 2 still names C (2,730 h), because C's low-flow nights and E's in-region running each last hours at a
  stretch. The run counters, flows, drive speeds and curves are complete, and a perfect vibration sensor still reads recirculation as zone
  D. No field records which zone-D hours a bearing causes, so the split by flow against the speed-scaled best-efficiency flow is still
  needed for E.
* **Lens swap.** The naive population is every zone-D running hour; the answer's is the hours a new bearing would remove, those inside each
  pump's preferred operating region at that hour's speed: a different population of hours, under a fifth of C's total.

## 3. The driving force

A strong solver refuses the register's stale duty flags and rebuilds the duty population from the changeover log, then sees that the
standard counts running hours, not shares: B's 84% sits on 1,100 night hours. It counts each duty pump's zone-D running hours and names C,
with 2,730. Each step is competent. But the standard asks for the hours the overhaul takes out, and a bearing cartridge removes only
bearing vibration. When a pump runs well below its best-efficiency flow, internal recirculation shakes it into zone D whatever its bearing;
C feeds a reservoir at night against a throttled valve, and 82% of its zone-D hours are at low flow. Inside the preferred operating region
the hydraulics are quiet, and a zone-D reading there is the bearing. The flow that decides it is relative to the best-efficiency flow at
the speed the pump was running, so each snapshot has to be joined to the flow log, the drive log and the pump curve rescaled by the
affinity laws. E, a variable-speed pump, has 92% of its 1,664 zone-D hours inside that region, and its 1,531 removable hours lead.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The platform's zone-D share for the nine pumps the asset register flags as duty | A (100%; 1.19× B) | The platform's own figure, on the register's own duty list | The operations changeover log: A has run as standby since 14 July, and a standby pump is overhauled without an outage |
| 1 | Duty pumps from the changeover log, the platform's zone-D share | B (84%; 1.20× C) | The right population and the platform's measure | The run counters: the standard counts running hours, and B's 84% sits on 1,100 night hours |
| 2 | Zone-D running hours per duty pump, snapshots times the two hours each closes, tied to the run counters | C (2,730 h; 1.22× D) | The standard's unit, on the right population, every hour evidenced | The close-outs: overhauls removed the zone-D hours inside the pump's preferred operating region and none of those at low flow, and 82% of C's are at low flow |
| 3 | **Decisive:** zone-D hours whose snapshot flow lies inside 70–120% of the pump's best-efficiency flow at that hour's drive speed, summed per duty pump | **E (1,531 h)** (5th of 9 on rung 0) | — | — |

* **Position table.** E ranks 5th on rung 0 (52%), 4th on rung 1 and 3rd on rung 2 (1,664 h), and leads only rung 3, 1.96× D (781 h).
  Intermediate leaders hold margins of 1.19×, 1.20× and 1.22×.
* **Discriminator dominance.** C carries a 1.64× advantage over E into rung 3 (2,730 against 1,664 hours). The operating-region split keeps
  0.92 of E's hours and 0.18 of C's, an edge of 5.11 against the 1.2 × 1.64 = 1.97 required, 2.60× headroom.
* **Partial correction priced (L3).** A solver who keeps only the in-region hours but ranks them as a share of running hours names B
  (58.8% against E's 47.8%, 1.23×), because B runs few hours. A solver who judges flow against each pump's full-speed best-efficiency flow,
  ignoring the drive log, reads E's slow running as low flow, cuts E to 650 hours, and names D (781 against E's 650, 1.20×), with F next
  at 756. A solver who applies the split but keeps the register's duty flags names A (1,805 against E's 1,531, 1.18×), whose bearing is
  genuinely worn but which, as a standby, is overhauled without an outage. No half lands on E.
* **Grid.** Population (register or changeover log) × unit (share or hours) × hours kept (all zone-D, in-region at full speed, in-region at
  running speed) gives twelve cells. Register cells name A except all-hours (C); changeover-log share cells name B; all-hours cells name C;
  full-speed hours name D. Only changeover-log hours in-region at running speed name E, and the nearest wrong cell (D) needs only the drive
  log left unjoined.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The standard counts hours the overhaul takes out of zone D. Nothing says a bearing removes only bearing vibration,
   and the pump curves sit in the asset register for duty-point planning.
2. **The corpus pins a construction, not a menu.** In-region hours at running speed reproduce the hours removed by 11 of 11 overhauls
   within 3%; all zone-D hours reproduce 4 of 11 and in-region hours at full speed 7, and each rival misses in one direction (all hours
   over-predict every low-flow pump, full speed under-predicts every variable-speed pump), so each also misses the corpus total. The split is
   a construction: a snapshot's place against a speed-scaled best-efficiency flow exists in no column.
3. **No arithmetic symptom.** Snapshots tie to the run counters, flows to the station meters and speeds to the drive log; every zone-D hour
   is a genuine zone-D hour.
4. **Not a row predicate.** It needs each snapshot aligned to the pump's flow and drive speed at that minute, the best-efficiency flow
   rescaled to that speed through the pump curve, and the hours summed per pump.
5. **The enumeration is arithmetic.** Which zone-D hours an overhaul removes is computed per snapshot; no field marks a cause.
6. **No cutover date.** Low-flow running follows the network's night demand every day; no series steps. The only dated event, A's July
   changeover, sits under rung 0.
7. **Survives deletion.** With every voice and the platform export removed, the answer and the difficulty are unchanged.

## 6. The calibration corpus

* **Form.** The close-outs of the 2023, 2024 and 2025 outages and of every other bearing overhaul since 2023 (standby pumps and in-service
  failures): eleven overhauls, each with the pump's zone-D running hours in the 180 days before and after and that period's flows and
  drive speeds.
* **What it pins.** Hours removed equal the in-region zone-D hours before the overhaul, 11 of 11 within 3%. All zone-D hours reproduce 4 of
  11; in-region hours at full speed 7.
* **Twin pair.** Overhauls O-4 and O-9 are identical on the platform's share (71%), running hours (3,100), model, class, hours since the
  last overhaul and mean velocity. O-4 removed 1,180 zone-D hours and O-9 560 (2.1×): O-4's zone-D hours were 92% inside the operating
  region and O-9's 44%.
* **Every rule exercised.** Two overhauled pumps had variable-speed drives, so the speed scaling is tested; one ran at low flow only in
  winter, so the split is tested across seasons.
* **Resemblance points at the decoy.** C's profile (high share, long hours, constant speed) most resembles O-4, the corpus's largest removal.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The standard: the slot goes to the duty pump whose overhaul will take the most running hours out of vibration zone D over
  the year after the outage; a standby pump is overhauled without an outage. The operations manual: the changeover log is the record of
  which pump in a set is on duty.
* **Empirical pins.** The removable band, 70–120% of best-efficiency flow at running speed, from the close-outs.
* **Voices.** The reliability lead: "The platform rates every pump the same way; I'd go with whatever it rates worst." The station
  supervisor at C: "You can hear C from the car park. It's the one that'll go."
* **Licensed wrong basis.** The standard records that the insurer's engineering surveyor ranks pumps on zone-D running hours and will
  review the outage plan on that basis.

## 8. Determinism by construction

* **Band.** No zone-D snapshot falls between 55% and 75% of the pump's best-efficiency flow at its speed, and none above 108%, so any lower
  bound from 55% to 75% and any upper bound from 110% to 130% give the same split.
* **Speed.** The drive log records speed every minute and each snapshot takes its minute's speed; fixed-speed pumps run at rated speed.
* **Window.** The 180 days end at the extract; 150- and 210-day windows keep E first by at least 1.7×.
* **Duty.** The changeover log and the run counters agree on one duty pump per set on every day of the window except the two changeover
  days, which hold no zone-D snapshot.

## 9. Prompt sketch and deliverables

> Our November outage has one crane crew and one bearing cartridge, enough to overhaul a single pump. The reliability lead would give it to
> whichever pump the monitoring platform rates worst. Name the pump in a sentence I can put in the outage plan, and send `outage_slot.xlsx`
> with the sheets below, a chart `zone_d_by_flow.png`, and a short `slot_decision.md`.

* `outage_slot.xlsx` — the prioritisation build for the nine sets, the lubrication sheet (ask A), the insulation-test sheet (ask B) and the
  close-out reproduction (ask C).
* `zone_d_by_flow.png` — for each duty pump, zone-D hours stacked by flow as a share of best-efficiency flow at running speed, the operating
  region shaded, the empty band from 55% to 75% marked, and the slot pump highlighted.
* `slot_decision.md` — the committed pump and why A, B, C and D fall away.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the nine duty pumps, lubrication orders completed in the last twelve months and grease
  applied in grams. *Device:* a lubrication round is one parent work order with a child line per pump, and grease is booked on the parent
  and apportioned by the route sheet, as the maintenance-system guide says. Booking the parent's quantity to its first child gives one
  pump per route the whole round's grease.
* **Ask B (device-carried).** For each of the nine sets, motor insulation-resistance tests in the last year and the share below the alarm
  level. *Device:* the test instrument exports one row per winding phase, three rows per test, with the test's serial in each, as its
  export guide documents. Counting rows triples every test and leaves the share unchanged only by accident.
* **Ask C (validity).** For each of the four rung constructions, the overhauls whose removed hours it reproduces within 3%, out of 11.
* **Decoupling.** Clearing the operating-region split and the duty correction changes no figure in asks A or B.

## 11. Rubric arithmetic

9 pumps × 2 (ask A) + 9 sets × 2 (ask B) + 4 constructions (ask C) + the committed pump, its removable hours and the margin over D + 5 named
chart parts + 3 files ≈ 51 criteria.

## 12. World-building constraints

* Running hours: A 1,900 (1 April to 14 July), B 1,100, C 3,900, D 3,600, E 3,200, F 2,800, G 3,000, H 2,500, I 3,400; J, A's set-mate,
  1,700 (from 14 July). Platform shares: A 100%, B 84%, C 70%, D 62%, E 52%, F 45%, G 30%, H 25%, I 20%, J 12%.
* In-region share of zone-D hours: A 0.95, B 0.70, C 0.18, D 0.35, E 0.92, F 0.60, G 0.70, H 0.50, I 0.80, J 0.50. Removable hours: A 1,805
  (standby), E 1,531, D 781, F 756, B 647, G 630, I 544, C 491.
* E and G have drives; E runs at about 72% speed, so full-speed classification cuts E to 650 hours. No other pump moves rank under it.
* Rung leaders are A, B, C, E. E is 5th / 4th / 3rd / 1st; intermediate margins are at least 1.19×; E leads rung 3 by 1.96×.
* The corpus holds eleven overhauls; O-4 and O-9 are identical on every platform-visible column.
* Lubrication routes and insulation tests never touch the snapshot file, the flows or the drive log.

# RC13 — How many bleed-valve removals the member fleets will see next pool year, when the alert that raised the question counts flying hours

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Supply Chain & Logistics · aviation spares and reliability |
| Mirrors | Spares and capacity provisioning from failure alerts (AWS and Google data-centre replacement pools, Apple repair-part forecasting, airline rotable pools), where the alert's exposure unit stops tracking the failure driver once the usage mix shifts |
| Decision shape | One figure committed at a date (a component): the bleed valve's forward removals, filed for the exchange-pool contract |
| Committed call | Unscheduled removals of the bleed-air pressure-regulating valve across member fleets over the next pool year, to the nearest ten |
| Gap · Pattern | Gap 1 (time) over Gap 2 (population) · Pattern A (past exceedance against forward yield, the moderator in how a schedule period flies the aircraft), with E02 (the unit not stored: removals, not report rows) at rung 1 |
| Gate G mechanism | forecasting, with method_or_model_selection |
| Measured traps engaged | #2 counts file rows instead of the real unit · #13 validates on one population, applies to another · #7 uses the ready-made measure |
| Calibration form | Revision log: the service-difficulty revision log, every report and its supplements for three closed years, with the working group's published removal counts |
| Driving force | The valve fails per pressurisation cycle, one per flight, not per flying hour. In every closed year members flew 1.1-hour sectors on average, so cycles and hours moved in lockstep and the alert's per-hour rate projected perfectly. Next year's filed schedules open long domestic routes and stretch the average sector to 1.6 hours. Only the cross-section of operators, whose sector lengths range from 0.8 to 2.3 hours, shows the per-cycle law that the schedule change makes decisive. |

## 1. Situation

An industry reliability working group placed the bleed-air pressure-regulating valve on its alert list after removals rose with fleet growth. The OEM
runs an exchange pool for the valve and sizes it each year from the working group's figure for the coming pool year, filed with the pool contract
on the 1st. One large domestic member files service-difficulty reports far more often than the rest, and the draft alert list ranked components on
report growth. Members' schedules for next year are filed with the group, and two growing carriers are opening long domestic routes.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: report rows and supplements, the published removal counts, each operator's hours and cycles, the alert
  rate (labelled in-file as a statement about the trailing twelve months, not a forecast) and next year's schedules. Nothing reported is
  overturned; the figure is a forward quantity that last year's correct rate does not describe.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the chair's view, the OEM's practice and the licensed basis. The per-hour rate still back-tests perfectly on every
  closed year, and the hour-based projection still looks sound.
* **Instrument repair.** Suspect file: the service-difficulty reports, in which 340 of last year's 1,690 rows are supplements to earlier
  reports. Repaired to one row per removal, rung 0 returns 1,713, as rung 1 does, and rung 2 1,560; none returns 1,180. The utilisation records
  hold every operator's hours and cycles, and next year's schedules are filed. Perfect records still leave each operator's hours and cycles in
  lockstep through the closed years, so only the cross-section of operators separates the per-cycle law, and only next year's longer sectors
  make it matter.
* **Lens swap.** The alert describes last year's fleet flying short sectors; the answer is next year's fleet flying longer ones: a different
  exposure profile at a different time.

## 3. The driving force

A strong solver distrusts the report growth, counts removals rather than report rows, and projects within each operator so the high-reporting
carrier's mix cannot distort it. Every step is right and the projection still uses flying hours, the alert programme's unit, as its exposure.
It back-tests perfectly: across the three closed years each operator kept its own sector length (within 2%) and the members' pooled average
stayed at 1.10 hours, so through time per-hour and per-cycle rates were the same law in disguise. Across operators they are not. A carrier flying 0.85-hour hops removes valves twice as often per
hour as one flying 1.8-hour sectors, and both remove them at the same rate per cycle (0.572 per thousand). Next year's schedules lift the
members' average sector from 1.10 to 1.59 hours: 27% more hours but 12% fewer cycles. The removals follow the cycles.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Report rows per thousand flight hours, trailing twelve months, × next year's filed hours | 2,145 removals (+81%) | It is the alert programme's own rate, projected on the members' own schedules | The revision log: 340 of last year's 1,690 rows are supplements to earlier reports, and the published counts reproduce only on removals |
| 1 | Removal events (supplement chains collapsed to their original report) per thousand hours × next year's hours | 1,713 (+45%) | The working group's published unit, reproduced exactly for three years | The cross-section: the high-reporting carrier's rate per hour is twice the others', so a pooled rate depends on next year's operator mix |
| 2 | Each operator's removals per hour × its own next-year hours, summed | 1,560 (+32%) | Within-operator projection, immune to reporting mix, back-tested on every closed year | The operators' rates per cycle are equal while their rates per hour vary 2.6× with sector length, and next year's sectors are longer |
| 3 | **Decisive:** removals per cycle × next year's filed cycles | **1,180 removals** | — | — |

* **Figure shape.** Every correction walks the figure down (−20%, −9%, −24% per step), and the answer is the minimum cell, so every partial
  application oversizes the pool.
* **Partial correction priced (L3).** A solver who senses sector length matters but converts hours to cycles with the OEM manual's design ratio
  (1.5 hours a cycle, a constant) rescales both years alike and lands back on 1,713 (+45%), further than rung 2.
* **Grid.** Unit (rows, removals) × aggregation (pooled, by operator) × exposure (hours, cycles) gives eight cells: 2,145, 1,953, 1,713, 1,560,
  1,482 (twice) and 1,184 (twice, because once the law is per cycle the operator mix no longer matters). The nearest wrong cell is 1,482
  (+25%), which needs report rows counted after the decisive move.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The alert programme states its unit (per thousand flight hours); the OEM manual quotes reliability in hours. No
   document says the valve fails per cycle.
2. **Corpus blind for a computable reason.** *In every closed year each operator flew the same sector length as in the other closed years
   (within 2%), so each operator's hours and cycles moved in lockstep and per-hour and per-cycle projections back-test within 1.5% of each
   other.* The revision log certifies the
   removal unit and the within-operator projection, and cannot choose between the laws.
3. **No arithmetic symptom.** Removals, reports, hours and cycles reconcile; every back-test passes under both laws.
4. **Not a row predicate.** The law is recovered across 14 operators (rate per cycle flat, rate per hour falling with sector length) and
   applied to a schedule-derived cycle count.
5. **The enumeration is arithmetic.** Next year's cycles are built route by route from the filed schedules; no column carries "removals next
   year".
6. **No cutover date.** The long routes start across the coming year route by route; nothing steps in any closed series.
7. **Survives deletion.** With every voice removed, the within-operator per-hour projection still back-tests perfectly.

## 6. The calibration corpus

* **Form.** The revision log: every service-difficulty report for the valve over three closed years with its supplements, each supplement
  carrying its original report number, and the working group's published removal counts for those years.
* **What it certifies.** The unit (removals reproduce the published counts exactly; rows overstate them by 22–26%) and the within-operator
  projection (each closed year projected from the year before within 3%, under either law).
* **What it is blind to.** Hours against cycles (above).
* **Twin pair.** Members M04 and M11 fly 42 aircraft of the same type and age, 118,000 hours a year, with the same reporting propensity. They
  removed 96 and 46 valves last year (2.09×): M04 flies 0.85-hour sectors and M11 1.8-hour ones. No per-hour rate reproduces both; the per-cycle
  rate reproduces each exactly.
* **Resemblance points at the decoy.** Next year's member mix resembles last year's on hours growth by operator, so every closed-year
  analogue nominates the per-hour projection.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The pool agreement: the pool is sized on the working group's figure for unscheduled removals across member fleets over the
  pool year. The reliability programme manual: one unscheduled removal is one event, however many reports describe it.
* **Empirical pins.** The per-cycle law, from the cross-section; next year's cycles, from the filed schedules.
* **Voices.** The working group chair: "Next year is this year with more aircraft." A member reliability engineer: "Strip out the big
  domestic carrier's over-reporting and the alert goes away."
* **Licensed wrong basis.** The pool agreement records that the OEM sizes the exchange pool on removals per thousand flight hours and will
  present its sizing on that basis.

## 8. Determinism by construction

* **Cycles.** One cycle per scheduled revenue flight; positioning and training flights are listed separately in the schedules and carry no
  valve removals in any closed year.
* **Window.** The pool year in the agreement; schedules cover it completely.
* **Rate.** Removals per thousand cycles is flat across operators to within 4%; pooled and by-operator per-cycle projections agree.
* **Supplements.** Every supplement names its original report; no chain crosses a year boundary.
* **Rounding.** The figure is filed to the nearest ten and sits mid-bin.

## 9. Prompt sketch and deliverables

> The OEM sizes the bleed-valve exchange pool off our figure for next pool year, and it goes into the contract on the 1st. Our chair thinks next
> year is just this year with more aircraft. Give me the number of unscheduled bleed-valve removals across the member fleets next pool year, to
> the nearest ten, as the figure we file. Send `valve_pool_case.xlsx` and a chart `removals_by_sector_length.png`.

* `valve_pool_case.xlsx` — the four constructions, the reporting-timeliness sheet (ask A), the AOG sheet (ask B) and the reproduction tables
  (ask C).
* `removals_by_sector_length.png` — the 14 operators' removals per thousand hours and per thousand cycles plotted against average sector
  length, with fitted lines, last year's and next year's member averages marked as vertical lines, and the committed figure labelled.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 14 members, the share of last year's reports filed within the 72-hour reporting
  window. *Device:* the submission stamp is in UTC and the event date in the operator's local time, as the reporting system's guide documents;
  comparing them naively misclassifies late-evening events at the three members furthest from UTC.
* **Ask B (device-carried).** For each ATA chapter, aircraft-on-ground events over the last twelve months. *Device:* a diversion logs the
  same event at the departure and the diversion station under one event id with a station sequence, as the AOG log's schema documents; counting
  rows double-counts 11% of events.
* **Ask C (validity).** The published removal counts for the three closed years against rows and removals; each operator's removals per hour
  and per cycle; and the figure under each of the four rung constructions.
* **Decoupling.** Clearing the per-cycle law changes no figure in asks A or B; neither touches a removal or an exposure figure.

## 11. Rubric arithmetic

14 members (ask A) + 46 chapters (ask B) + 3 years × 2 counts + 14 operators × 2 rates + 4 constructions (ask C) + the committed figure, next
year's cycles and the per-cycle rate + 5 named chart parts + 2 files ≈ 115 criteria.

## 12. World-building constraints

* Last year: 2.60M flight hours, 2.36M cycles, 1,350 removals, 1,690 report rows. Next year: 3.30M hours, 2.07M cycles.
* Per-cycle rate 0.572 per thousand for every operator within 4%; per-hour rates vary 2.6× with sector length (0.8 to 2.3 hours).
* Closed years: each operator's sector length constant within 2%, the members' pooled average between 1.08 and 1.12 hours.
* M04 and M11 identical on every alert-programme column.
* Timestamps and AOG station rows touch no removal, supplement or schedule.

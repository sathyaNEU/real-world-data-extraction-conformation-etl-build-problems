# RC05 — Which outage cause gets the distributor's one reliability programme, when the costliest cause leaves no fault record

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Supply Chain & Logistics · electricity distribution network operations |
| Mirrors | Reliability investment at networks that log incidents per component and judge them per customer (customer-impact minutes against incident duration at AWS, Azure and Google Cloud, maintenance windows run offline that never open an incident, planned outages on regional power networks), where work taken offline for want of crews leaves no incident record and the customers behind it carry the cost |
| Decision shape | Which of N root causes gets the fix: one reliability programme for the coming year |
| Committed call | The programme funded, and the customer minutes lost that its cause accounted for over the last twelve months, in millions to one decimal |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · E07 (two grains, both flawless: section outage minutes and customer minutes lost differ in shape, because a section minute weighs by the customers behind it and a planned interruption has no fault-log minute at all; the standard pins the customer grain, rebuilt from the smart meters' power-off and power-on messages), with E19 (a latent attribution marker: cause-unknown trips assigned through the recloser event-log chain) at rung 2 |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #2 counts file rows instead of the real unit · #11 beats the headline trap, misses the quiet one · #7 uses the ready-made measure |
| Calibration form | Counterparty acknowledgement file: the recloser manufacturer's accepted and rejected warranty outage claims for four closed quarters |
| Driving force | The operations report counts section outage minutes from the fault log, each coded by the crew; the reliability standard judges a programme on customer minutes lost, the minutes customers spent without supply. When no live-line crew is free, maintenance is done de-energised under a planned interruption, which never enters the fault log because nothing faulted. Every customer on the worked section loses supply, and where the network cannot back-feed, so does every customer beyond it. Rebuilt from the smart meters' power-off and power-on messages, with the planned-work log naming each interruption's reason, the crew shortage is the largest cause of customer minutes lost, ahead of the vegetation faults on the trunk feeders and the recloser trips the warranty chain recovers. |

## 1. Situation

A regional electricity distributor's outage minutes rose almost 90% on last year. The company launched a programme against animal contacts, its most
frequent fault code, and the chief operating officer points to two winter windstorms. The board will fund one reliability programme from a catalogue
of five: animal guarding (A), firmware and settings remediation on the new automated recloser fleet (B), vegetation management on the trunk feeders
(C), storm hardening of the overhead network (D) and live-line capacity, a programme to hire and train live-line crews (E). The reliability standard
sets how a programme is judged. The reclosers are under the manufacturer's warranty, which pays for outage minutes the manufacturer acknowledges as
its own. Since the spring, maintenance has been done de-energised most weeks for want of live-line crews.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: fault counts, coded section minutes, the operations report's table, the recloser event logs, switching and
  repair records, the planned-work log, the meter messages, the connectivity model and the acknowledgements. "Cause unknown" is an honest code,
  and a planned interruption honestly has no fault. No stakeholder's reading of their own numbers is overturned; the standard counts customers,
  and the fault log counts sections.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the animal programme, the operating officer's view and the licensed basis. The fault log still records no minute for a
  planned interruption, and the section-minute tables still name the reclosers once the cause-unknown trips are assigned.
* **Instrument repair.** Suspect file: the fault log's cause code, which records what the crew could see ("cause unknown" for 19,000 section
  minutes). Repaired so that every fault carries its true cause, rung 0's count still names A (recloser faults rise to 2,400 against 5,200), and
  rungs 1 and 2 both return B, the recloser trips the chain already recovers (17,700 section minutes against at most 16,900 for vegetation);
  none returns E. The planned-work log, the meter messages and the connectivity model are complete. The answer still needs customer minutes
  rebuilt from them, which no fault record, perfect or not, holds.
* **Lens swap.** The naive build counts section outage minutes; the answer counts customers' minutes without supply, including interruptions
  that never faulted: a different population (customers, and planned work with no fault) over the same year.

## 3. The driving force

A strong solver moves from counts to minutes, and on coded section minutes vegetation leads. The manufacturer's acknowledgement file then shows
that most cause-unknown trips are misoperations of the new reclosers: assigned through the recloser event-log, switching and repair-order chain the
acknowledgements follow, recloser trips lead at 17,700 section minutes. Every one of those is a section minute, and the standard judges a
programme on customer minutes lost. The operations report is the wrong unit for that in two ways. A section minute costs every customer behind
the section, and the reclosers sit at rural tie points with few customers beyond them, while vegetation trips the dense suburban trunk feeders.
And when no live-line crew is free, maintenance is done de-energised under a planned interruption, which never enters the fault log because
nothing faulted: every customer on the worked section loses supply, and where the network cannot back-feed, so does every customer beyond it.
Rebuilt from the smart meters' power-off and power-on messages, with the planned-work log naming each interruption's reason, the crew shortage
costs 9.29 million customer minutes, vegetation 7.74 million and the reclosers 5.68 million.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Faults by cause code, counted | A, animal contacts (5,200) | The company's own reading, and the code is by far the most frequent | The reliability standard judges a programme on minutes of lost supply, not on faults |
| 1 | Section outage minutes by cause code from the operations report's table, cause-unknown minutes left out | C, vegetation (12,500) | Minutes of lost supply from the published table, every coded minute accounted for | The acknowledgement file: the manufacturer accepted 61% of closed-quarter cause-unknown trips as recloser misoperations |
| 2 | Section minutes with the cause-unknown trips assigned through the recloser event-log, switching and repair-order chain the acknowledgements follow | B, recloser fleet (17,700 min) | Every minute assigned, every acknowledgement reproduced | The planned-work log: 2,400 planned interruptions for want of a live-line crew, none in the fault log, against the charter's customer minute |
| 3 | **Decisive:** customer minutes lost rebuilt from the meters' power-off and power-on messages, each planned interruption credited to its reason | **E, live-line capacity (9.29M)** (4th of 5 on rung 0) | — | — |

* **Position table.** E ranks 4th on rung 0 and 5th on rungs 1 and 2, and leads only rung 3. Rung leaders beat their runners-up by 5.78×, 1.30×,
  1.31× and 1.20× (9.29M against vegetation's 7.74M).
* **Discriminator dominance.** Recloser trips carry a 6.81× lead over the crew shortage into rung 3 (17,700 section minutes against 2,600).
  Customer minutes per section minute are 3,573 for E, its 2,400 planned interruptions included, and 321 for B, an edge of 11.1×, 1.36 times the
  required 1.2 × 6.81 = 8.17; the net margin is 1.64×.
* **Partial correction priced (L3).** Every half-rebuilt customer measure leaves another cause in front. Weighting section minutes by the
  network's average customers per section gives B 7.08M against C's 5.40M (1.31×), E 1.04M. Weighting each fault by its own section's customers,
  with no planned interruptions, gives C 7.02M against A's 4.61M (1.52×). Adding planned interruptions for the worked section's own customers,
  without the sections beyond it that the switching plan also de-energises, gives C 7.38M against B's 5.14M (1.44×), E 4.97M.
* **Grid.** Measure (counts, section minutes, section minutes at the average customers per section, section minutes at each section's own
  customers, customer minutes with planned work on the worked section only, full customer minutes) × cause unknown (dropped, chain) gives twelve
  feasible builds. Count builds name A; section-minute and average-weighted builds name C with the cause-unknown minutes dropped and B with them
  assigned; own-section and worked-section-only builds name C; only full customer minutes name E. The nearest wrong cell is the worked-section-
  only build, which needs the sections beyond the work added.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The customer charter defines a customer minute lost; the fault guide defines the codes, and the planned-work log its
   fields. No document converts faults or planned interruptions into customer minutes, or says a planned interruption's cost falls on customers
   beyond the worked section.
2. **Corpus blind for a computable reason.** *Every claim in the acknowledgement file concerns a recloser trip that faulted a section, so no
   closed quarter's acknowledged minutes include a planned interruption or a customer, and the file is arithmetically incapable of pricing one.*
   It pins rung 2's chain (1,860 of 1,860 acknowledgements reproduce) and cannot see the unit the standard counts.
3. **No arithmetic symptom.** Section minutes, faults, codes, planned interruptions and meter messages all reconcile; a planned interruption has
   no fault to reconcile.
4. **Not a row predicate.** A customer's minutes run from its meter's power-off message to its power-on message, credited to the event that
   de-energised its section, which takes the switching sequence and the connectivity model to tell.
5. **The enumeration is arithmetic.** No column holds a customer minute lost; 9.29 million are built from 2,400 planned interruptions, the
   sections each de-energised and the meters behind them.
6. **No cutover date.** Planned interruptions rose as live-line crews retired through the year; the dated events (the two windstorms, the
   animal programme's launch) are the decoys.
7. **Survives deletion.** With every voice gone, the section-minute tables still name the reclosers.

## 6. The calibration corpus

* **Form.** The manufacturer's acknowledgement file: 1,860 trips claimed in four closed quarters (coded recloser faults plus cause-unknown trips
  on sections behind new reclosers), each accepted or rejected, with the recloser event logs, switching and repair records for those quarters.
* **What it certifies.** The chain for cause-unknown trips (rung 2): it reproduces 1,860 of 1,860 acknowledgements, against 1,212 for the
  recloser code alone, 1,296 for the switching record's stated reason and 1,251 for the section's next repair order.
* **What it is blind to.** Customer minutes and planned interruptions (above).
* **Twin pair.** Tuesdays 9 and 16 April carried identical section minutes by code, faults, customers on the faulted sections and meter counts,
  and six planned interruptions each for want of a live-line crew. Customer minutes lost were 61,000 and 30,000 (2.03×): on the 9th the six jobs
  were on one radial trunk with no back-feed, so each de-energised the sections beyond it; on the 16th they fell on meshed suburban sections that
  were back-fed while the crews worked. Only the rebuilt customer measure separates the two days.
* **Resemblance points at the decoy.** This year's fault profile matches Q1, the quarter in which the manufacturer accepted the most recloser
  minutes, on codes, feeders and the share of sections behind new reclosers.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The reliability standard: a reliability programme is judged on the customer minutes lost its cause accounted for over the last
  twelve months, planned and unplanned interruptions alike. The customer charter: a customer minute lost is a minute a customer spends without
  supply. The programme catalogue lists the fault codes and planned-work reasons each covers.
* **Empirical pins.** The assignment chain, from the acknowledgement file; each customer's minutes, from the meter messages.
* **Voices.** The customer services director: "Animal contacts are most of our faults, so that's where the minutes go." The network engineer:
  "Those cause-unknown trips are the new reclosers misoperating. The manufacturer pays for most of them, and they're still our worst problem."
* **Licensed wrong basis.** The standard records that the board's finance committee reviews reliability programmes on the operations report's
  section outage minutes by cause group and will present that table.

## 8. Determinism by construction

* **Customer minutes.** A customer's minutes run from its meter's power-off message to its power-on message. Where a fault and a planned
  interruption overlap on one customer, the minutes go to the event that de-energised its section first; where a planned interruption's switching
  plan de-energises sections beyond the worked one, their customers' minutes go to the planned interruption's reason.
* **Meters.** Every customer has a smart meter whose power-off and power-on messages the head-end confirms, and every meter resolves to one
  section through the connectivity model.
* **Window.** Twelve complete months; the planned-work log is final.
* **Rounding.** Millions of customer minutes to one decimal; the committed figure sits mid-bin.

## 9. Prompt sketch and deliverables

> Outage minutes on the network are up almost 90% on last year and the board will fund one reliability programme. Our chief operating officer is
> sure it's the two windstorms. Tell me which programme we fund and how much lost supply its cause cost over the last twelve months, as the
> standard counts it, in millions to one decimal, in one sentence for the board pack. Send `outage_cause_case.xlsx`, a chart
> `outage_by_cause.png` and a short `reliability_memo.pdf`.

* `outage_cause_case.xlsx` — the five causes under each construction, the streetlight sheet (ask A), the pole-inspection sheet (ask B) and the
  acknowledgement reproduction (ask C).
* `outage_by_cause.png` — paired bars per cause of section minutes and customer minutes, the customer bar split into faults and planned
  interruptions, an inset of one planned interruption's de-energised sections on the feeder diagram, and the funded cause highlighted.
* `reliability_memo.pdf` — the funded programme, its figure, and why the other four are not it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the six depots and each of the last twelve months, streetlight faults reported and
  repaired. *Device:* a repeat report of a lamp already logged is written as a new row carrying a parent-report reference, as the streetlight
  service guide documents; counting rows overstates faults reported at two depots by about a quarter.
* **Ask B (device-carried).** For each of the six depots, wood poles inspected and poles condemned over the twelve months. *Device:* an
  inspection spanning two days is written as one row per day, later rows carrying a continuation flag, as the inspection guide documents;
  counting rows as inspections inflates the count at four depots.
* **Ask C (validity).** For each closed quarter, accepted minutes under each of the four assignment rules; and each cause's figure under each of
  the four rung constructions.
* **Decoupling.** Clearing the customer-minute rebuild changes no figure in asks A or B; neither touches a fault record, a planned interruption,
  a meter message or the connectivity model.

## 11. Rubric arithmetic

6 depots × 12 months × 2 figures (ask A) + 6 depots × 2 figures (ask B) + 4 quarters × 4 rules + 5 causes × 4 constructions (ask C) + the funded
programme, its figure and the runner-up's + 5 named chart parts + 3 files ≈ 205 criteria.

## 12. World-building constraints

* Fault counts A 5,200, D 900, C 800, E 650, B 600 (recloser faults with the cause-unknown trips assigned: 2,400). Coded section minutes C 12,500,
  A 9,600, D 6,800, B 3,100, E 2,600; of 19,000 cause-unknown section minutes the chain gives B 14,600 and C 1,000 and leaves 3,400 unassigned.
* Customer minutes per section minute: B 260, C 520, A 480, D 300, E 250. Planned interruptions: live-line crew unavailable 2,400, recloser
  replacement 300, vegetation work 200, storm repair 150; a planned interruption costs 3,600 customer minutes, half on the worked section and
  half on sections beyond it that cannot be back-fed. Customer minutes (millions): E 9.29, C 7.74, B 5.68, A 4.61, D 2.58.
* Acknowledgements: chain 1,860/1,860; recloser code 1,212; switching reason 1,296; next repair order 1,251.
* 9 and 16 April identical on every fault, section-minute, customers-per-section, meter-count and planned-interruption-count column.
* Streetlight parent reports and inspection continuation rows touch no fault record, planned interruption, meter message or section.

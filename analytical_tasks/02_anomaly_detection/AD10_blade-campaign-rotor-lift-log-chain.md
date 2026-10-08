# AD10 — Which turbine gets the summer's one leading-edge repair campaign, when the worst blades have been on two turbines this year

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Economics · wind-farm asset management |
| Mirrors | Repairing the component that carries a fault when components move between hosts (disk and network-card faults that follow a part across servers in hyperscale fleets, refurbished modules moving between devices in Apple and Google repair programmes, engines rotated between airframes in airline fleets) |
| Decision shape | Which of N gets one scarce thing: the rope-access team's single leading-edge repair campaign this summer |
| Committed call | The one turbine whose blades are repaired, and the energy the repair is expected to recover |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · an implicit multi-hop join (E20: turbine, position code, crane lift record, rotor serial), pinned by the pilot log, with a suppressed cell bounded at the lower rung (E25) |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #18 joins only on the visible key · #24 treats an unpublished figure as unknown · #4 never tests its reading against the control |
| Calibration form | Pilot log: nine blade-repair campaigns on the company's other farms last year, each with the deficit computed before repair and the energy recovered in the following year |
| Driving force | Leading-edge erosion travels with the rotor, and rotors move: when a main bearing is exchanged the crane lifts the rotor off and fits the spare from the laydown yard. The eroded rotor ran four months on G, sat in the yard, and has run six months on E, so each turbine-year shows half its deficit. Its whole deficit appears only when SCADA periods are linked through position codes and the crane's lift log to rotor serials, a chain the asset register's current-rotor field hides, and only that construction reproduces what the pilot campaigns recovered. |

## 1. Situation

A wind-farm owner's rope-access team can run one leading-edge repair campaign this summer, on one of the farm's ten turbines (A to J,
all the same model). The O&M policy judges a campaign by the energy the repair recovers over the following twelve months. The pack carries
twelve months of 10-minute SCADA by turbine ID, the status log, the met-mast record, the grid operator's curtailment report, the asset
register (each turbine's current rotor serial), the crane contractor's lift log (by position code), the site layout mapping position codes
to turbine IDs, the model's warranted power curve and the pilot log.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: production, wind, status codes, curtailment, the register's current rotors, every lift and every
  pilot outcome. Nothing reported is overturned and no stakeholder read is corrected; the difficulty is that the thing the repair acts on is
  a rotor, and rotors are not turbines.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices. A careful own-curve deficit per turbine-year, the industry's standard test, still names C, and
  joining the register's current rotors to it still credits E with only half of R-3's year.
* **Instrument repair.** Give every turbine perfect SCADA and the register perfect current fields; they are already right. A better
  instrument of turbines still splits a moving rotor's year across two turbines.
* **Lens swap.** The naive unit is the turbine-year; the answer's unit is the rotor over its months in operation, which spans two turbines and
  excludes months the turbine ran on another rotor: a different population of SCADA periods.

## 3. The driving force

A strong solver throws out year-on-year energy because the wind fell 6%, removes downtime and curtailment, bounds the curtailment cell the
grid operator suppressed, builds each turbine's power curve by the method of bins with density normalisation and the standard filters,
and compares it with the warranted curve. That names C at 6.1%, and the industry would sign it. But erosion lives on blades. When G's
main bearing was exchanged in January the crane lifted rotor R-3 off and fitted the yard spare; in April E's bearing was exchanged and E
received R-3. R-3 loses 8.0% wherever it runs, and the turbine-years show 2.8% at G and 4.0% at E. The asset register lists each turbine's
current rotor, which looks like the link and credits R-3 only with its months on E. The full history runs from turbine ID to position code
in the site layout, to the crane's dated lifts, to rotor serials, a chain that the O&M manual describes as practice ("the removed rotor is
held in the yard and fitted at the next exchange") and that no file joins. The pilot log's recoveries are reproduced only at rotor grain.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Year-on-year energy per turbine | A (−11.2%) | What the owners see on every report, and A had the worst year | The met mast: wind fell 6% across the farm, and A's own event log holds a 41-day gearbox outage |
| 1 | Shortfall against the farm mean after downtime and curtailment, the suppressed feeder's curtailment taken as unknown and set to zero | B (5.9%) | Wind and outages are out, and the operator's report is used as published | The curtailment report's farm total less its other feeders bounds the suppressed cell at 380–410 MWh, which covers all of B's shortfall |
| 2 | Own-curve deficit per turbine-year: method of bins, density-normalised, standard filters, against the warranted curve | C (6.1%) | The industry-standard performance test, every filter applied | The pilot log: turbine-year deficits reproduce the recovered energy of 5 of 9 campaigns, missing every one whose turbine changed rotor in the year |
| 3 | **Decisive:** SCADA periods linked through position codes and the crane's lift log to rotor serials; each installed rotor's deficit over its months in operation | **E, carrying rotor R-3 (8.0%)** (5th of 10 on rung 0) | — | — |

* **Position table.** E ranks 5th on rung 0 (−6.1%), 4th on rung 1 (3.9%) and 3rd on rung 2 (4.0%), and leads only rung 3, 1.31× C's rotor.
  Intermediate leaders hold margins of 1.24×, 1.23× and 1.24×.
* **Discriminator dominance.** C carries a 1.53× advantage over E into rung 3 (6.1% against 4.0%). Rotor grain doubles E's figure and leaves
  C's, whose rotor never moved, unchanged: an edge of 2.00 against the 1.2 × 1.53 = 1.83 required; net 1.31×.
* **Partial correction priced (L3).** A solver who joins the register's current rotor serials to the turbine-year deficits credits R-3 with
  E's 4.0% and names C again. A solver who follows the lift log but takes R-3's deficit over the calendar year, yard months as zero, gets
  6.7% and names E with an expected recovery 16% low.
* **Grid.** Curtailment cell (zero or bounded) × deficit basis (shortfall or own curve) × unit (turbine-year, current rotor, rotor history)
  gives twelve cells. Zero-cell shortfall cells name B; bounded shortfall cells and every turbine-year or current-rotor own-curve cell name
  C. Only rotor history names E, and the nearest wrong cell (C) needs the lift log left unjoined.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The O&M manual describes the yard practice for main-bearing exchanges; it says nothing about erosion, deficits or
   which rotor sits where now. The lift log is a crane contractor's record keyed by position code, which SCADA never uses.
2. **The corpus pins a construction, not a menu.** Rotor-grain deficits reproduce the recovered energy of 9 of 9 pilot campaigns within 0.3
   points; turbine-year deficits 5 of 9, over-predicting every miss, so they also over-state the pilot's total recovery by 22%. The
   reproducing unit is a construction: a rotor's operating months exist only after SCADA periods are chained through the layout and the
   lift log, and no column holds them.
3. **No arithmetic symptom.** SCADA ties to the export meter, the register's current rotors are correct today, and the lift log balances:
   every rotor is on a turbine or in the yard on every day.
4. **Not a row predicate.** It needs a two-hop join with dated intervals, an assignment of every 10-minute period to the rotor installed,
   and a power-curve fit per rotor across turbines.
5. **The enumeration is arithmetic.** Which rotor ran when is computed from lift dates; no SCADA column carries a rotor.
6. **No cutover date.** R-3's erosion is steady at 8.0% on both turbines; neither turbine's series steps at the lifts by more than its
   noise, because E's previous rotor was healthy and G's replacement is too.
7. **Survives deletion.** With every voice removed, the answer and the difficulty are unchanged.

## 6. The calibration corpus

* **Form.** The pilot log: nine leading-edge campaigns on the company's other farms last year, each with the turbine, the deficit the
  pilot computed before repair, and the energy recovered over the following year from the same SCADA, plus those farms' lift logs.
* **What it pins.** Recovered energy equals the repaired rotor's own deficit over its months in operation: 9 of 9 within 0.3 points. The
  turbine-year deficit reproduces 5 of 9; the current-rotor join 6 of 9.
* **Twin pair.** Campaigns P-3 and P-7 sit on identical turbines with identical turbine-year deficits (3.9%), site class, wind and age.
  P-3 recovered 3.8% and P-7 1.9% (2.0×): P-7's turbine had carried an eroded rotor for half the year before a lift moved it away, and the
  rotor repaired was the healthier one.
* **Every rule exercised.** One pilot rotor spent three months in a yard, so the operating-months basis is tested; one pilot farm's position
  codes run in a different order from its turbine IDs, so the layout hop is tested.
* **Resemblance points at the decoy.** E's turbine-year profile most resembles P-7's, the pilot's smallest recovery.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The O&M policy: a campaign is judged by the energy the repair recovers over the following twelve months, against the
  model's warranted power curve. The performance memo's bins, density normalisation and filters. The crane plan: no rotor lift is scheduled
  at any turbine in the next twelve months.
* **Empirical pins.** Rotor grain over operating months, from the pilot log.
* **Voices.** The owners' asset manager: "Year-on-year energy is what the owners see, and that's where I'd send the team." The contractor's
  performance engineer: "The own-curve test is the industry standard; I'd take whatever it puts first."
* **Licensed wrong basis.** The policy records that the owners' technical adviser ranks turbines on own-curve deficit per turbine-year and
  will review the campaign choice on that basis.

## 8. Determinism by construction

* **Lift dates.** Every lift is dated to the day and falls on a day the turbine was stopped, so no 10-minute period straddles two rotors.
* **Fit.** Bins of 0.5 and 1.0 m/s, and filters with or without the icing flag, keep R-3 first by at least 1.25×.
* **Curtailment bound.** Cells are rounded to 10 MWh, so the suppressed cell lies between 380 and 410 MWh; B's shortfall is 340 MWh, inside
  either end.
* **Forward.** With no lift planned, the repaired rotor stays on its turbine for the twelve months, so recovery is the rotor's deficit times
  its expected energy there.

## 9. Prompt sketch and deliverables

> The rope-access team can run one leading-edge repair campaign this summer, on one turbine. The owners' asset manager would go by last
> year's energy. Tell me the turbine and the energy the repair should recover over the next year, in a sentence for the work plan, with
> `campaign_choice.xlsx` holding the sheets below, the chart `rotor_deficits.png`, and a one-page `campaign_note.docx`.

* `campaign_choice.xlsx` — the turbine and rotor build, the yaw sheet (ask A), the reactive-power sheet (ask B) and the pilot back-test (ask C).
* `rotor_deficits.png` — a timeline of each turbine's rotor serials over the twelve months with the lifts marked, beside paired bars of
  turbine-year and rotor deficits, R-3's path from G through the yard to E highlighted.
* `campaign_note.docx` — the committed turbine, the expected recovery, and why C and the turbine-year ranking are not it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each turbine, yaw-misalignment events above 10° lasting more than 30 minutes in the last twelve
  months, and their total hours. *Device:* an event spanning a controller reboot is closed with a synthetic end record and reopened with a
  new start, as the OEM's event guide documents. Counting start records splits events at the four turbines with the most reboots. The
  power-curve build never reads the yaw log.
* **Ask B (device-carried).** For each month, the 10-minute periods in which the farm's power factor fell outside the grid code's band.
  *Device:* the grid code's annex exempts periods when export was below 5% of capacity, which the compliance file marks in a separate
  field. Counting every out-of-band period overstates breaches in the six calmest months.
* **Ask C (validity).** For each of the four rung constructions, the pilot campaigns whose recovered energy it reproduces within 0.3 points,
  out of 9.
* **Decoupling.** Clearing the rotor chain changes no figure in asks A or B.

## 11. Rubric arithmetic

10 turbines × 2 (ask A) + 12 months (ask B) + 4 constructions (ask C) + the committed turbine, R-3's deficit, the expected recovery and the
margin over C + 5 named chart parts + 3 files ≈ 48 criteria.

## 12. World-building constraints

* Rung leaders are A, B, C, E. E is 5th / 4th / 3rd / 1st; intermediate margins are at least 1.23×; E leads rung 3 by 1.31×.
* R-3 loses 8.0% on any turbine: four months on G, two in the yard, six on E. G's turbine-year reads 2.8% and E's 4.0%. C's rotor never moved.
* Lifts: G in January, E in April, both on stopped days; no lift is planned for the next twelve months.
* The curtailment report suppresses one two-turbine feeder; cells are rounded to 10 MWh.
* The pilot log holds nine campaigns; P-3 and P-7 are identical on every turbine-level column.
* Yaw reboots and power-factor exemptions never touch SCADA power, the lift log or the register.

# AD20 — Which tool unit comes down for the fab's one engineering hold, when four units read a 100% systematic share because the report counts lots, not wafers

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Supply Chain & Logistics · semiconductor fab operations |
| Mirrors | Breaking a 100% tie in a failure-attribution share by taking it down to the grain the work was done at (drive-failure attribution where a server batch is credited to every rack it touched, build-failure attribution in CI fleets where a job is credited to every runner in its pool, commonality analysis in contract manufacturing) |
| Decision shape | Which of N gets one scarce thing: this week's single engineering hold, one tool unit taken down for inspection |
| Committed call | The one tool unit held for inspection this week |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · a tie saturated by lot-grain crediting and broken at wafer grain by the standard's own rule (E21), pinned by the pilot log, with the deciding comparison at the lower rung (E22) |
| Gate G mechanism | method_or_model_selection, with signal_vs_noise_or_hold support |
| Measured traps engaged | #19 breaks a big tie instead of questioning it · #20 leaves the deciding comparison unstated · #7 uses the ready-made measure |
| Calibration form | Pilot log: last quarter's twelve pilot holds under the new hold standard, each with its unit, the unit report's share and the inspection finding |
| Driving force | The hold standard ranks units by systematic share, the share of a unit's processed wafers whose map shows a systematic pattern, and the yield system's unit report puts four units at 100%. The report works at lot grain: a lot is systematic when any wafer in it is, and a lot split across the etch tool's chambers is credited to every chamber in its set. The standard's own rule, the lowest value consistent with every file of record, takes the share down to wafer grain through the maps and the chamber log, where the deposition chamber and the implant source fall to 46%, the sibling etch chamber to 0%, and only etch chamber 3, which etched every patterned wafer, keeps 100%. |

## 1. Situation

A wafer fab can take one tool unit down for an engineering hold this week. Its hold standard gives the hold to the unit with the highest
systematic share over the last 14 days: of the wafers the unit processed, the share whose final-test map shows a systematic pattern
(join-count z of 3 or more with at least five failing dies). Every figure is the lowest value consistent with every file of record, and
ties go to the unit longest since its last preventive maintenance. The pack carries the yield system's unit report (each unit's share of
the lots it processed that were dispositioned systematic, as its header states), the 14 days' wafer maps, the MES lot history, the etch
tool's chamber log (every wafer by chamber), the fault-detection log, the fab's pattern-to-tool reference table, the maintenance log and
the pilot log.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: every map, lot record, chamber-log line, alarm and pilot finding. The four 100% readings are exactly
  what the unit report says it computes, a share of lots dispositioned systematic. Nothing reported is overturned and no stakeholder read
  is corrected; the difficulty is the grain at which the standard's share has to be computed.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the reference table. The unit report still puts four units at 100%, and the documented
  tie-break still picks the deposition chamber.
* **Instrument repair.** Map every wafer and log every lot perfectly; they already are. A better lot record still credits a split lot to
  both its chambers, and only the chamber log, read wafer by wafer, separates them.
* **Lens swap.** The naive share is over every wafer in the lots credited to a unit; the answer's is over the wafers the unit itself
  processed, a different population for each split-tool chamber: etch chamber 1 loses 529 credited wafers, etch chamber 3 loses 621.

## 3. The driving force

A strong solver turns away from alarm counts and pattern counts, because the standard asks for neither: it asks for the systematic share,
a unit's systematic wafers against all the wafers it processed. It takes that share from the yield system's unit report, finds four units
at 100%, and applies the documented tie-break, longest since preventive maintenance, which names the deposition chamber. Each step is
competent, and the deciding comparison was even stated. But the report works at lot grain: a lot is dispositioned systematic when any
wafer in it is, and the MES credits a lot split across the etch tool's chambers to every chamber in its set. Product K runs on etch
chambers 1 and 3, so every K lot holds wafers from chamber 3, every K lot is systematic, and every unit that runs only K reads 100%. The
standard's first rule says every figure is the lowest value consistent with every file of record. The maps show which wafers carry the
edge ring and the chamber log shows where each wafer was etched: 529 of the 1,150 K wafers, every one of them in chamber 3. At wafer
grain the deposition chamber and the K implant source fall to 46%, etch chamber 1 to 0%, and etch chamber 3 alone keeps 100%.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Fault-detection alarms per unit over 14 days | A, furnace tube 1 (47 alarms; 1.24× D) | The fab's own sensor screen, unit by unit | The fault-detection log's dispositions: 41 of A's 47 alarms were closed as thermocouple drift with no product impact |
| 1 | Patterned wafers per unit, credited to tool types by the fab's pattern-to-tool table and split by the lot history | B, stepper 1 (362 wafers; 1.75× H) | Systematic patterns, attributed the way the fab's engineers attribute them | The hold standard: the measure is a share, a unit's systematic wafers against all the wafers it processed, and stepper 1's 362 are a quarter of its 1,450 |
| 2 | The unit report's systematic share at lot grain; four units at 100%; ties to the unit longest since maintenance | C, deposition chamber (100%, 58 days since maintenance; 1.45× B, the first unit outside the tie) | The standard's own measure from the yield system, the documented tie-break applied, the comparison stated | The standard's rule: every figure is the lowest value consistent with every file of record, and the maps and the chamber log place each wafer's pattern and chamber one by one |
| 3 | **Decisive:** the share at wafer grain, each wafer's map flag joined to its chamber in the chamber log, patterned over processed wafers per unit | **E, etch chamber 3 (100%)** (5th of 9 on rung 0) | — | — |

* **Position table.** E ranks 5th on rung 0 (9 alarms), is credited with no patterned wafers on rung 1, sits last of rung 2's four tied
  units (16 days since maintenance), and leads only rung 3, 2.17× C and G (46%).
* **Discriminator dominance.** C reaches rung 3 level with E on the measure, both at 100%, carrying only the tie-break, which a broken tie no
  longer consults: a carried advantage of 1.0. Wafer grain multiplies E's share by 1.00 and C's by 0.46, an edge of 2.17 against the
  1.2 × 1.0 = 1.20 required, 1.81× headroom.
* **Partial correction priced (L3).** A solver who joins the maps but keeps the lot history's chamber sets credits every K wafer to both
  etch chambers, puts C, E, F and G level at 46%, and the tie-break names C again (the tied four 1.84× B, the next unit). A solver who joins
  the chamber log but keeps the lot dispositions leaves the same four at 100% and names C. Neither half lands on E.
* **Grid.** Measure (alarms, pattern count, systematic share) × wafer flags (lot disposition or map) × unit history (lot chamber sets or
  chamber log): alarms name A, pattern counts B, and every share cell without both the maps and the chamber log names C through the
  tie-break. Only maps with the chamber log name E, and the nearest wrong cell (C) needs either file left at lot grain.
* **The deciding comparison (#20).** Patterned against processed wafers per unit is the comparison the hold notice has to state; the
  pattern count alone names B, and the tie alone hands the hold to whichever unit is stalest.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The standard states its rule as a principle and names no file. Nothing says the unit report works at lot grain or
   that a split lot is credited to every chamber in its set; the chamber log is an equipment-engineering record the yield system never reads.
2. **The corpus pins a construction, not a menu.** Wafer grain reproduces all 12 pilot findings: every held unit at a wafer-grain 100% had a
   fault and every other had none. The unit report with its tie-break reproduces 5 of 12, and maps without the chamber log 7. The
   construction needs each wafer's map flag, each wafer's chamber from a second system, and a count per unit, and no column holds the
   wafer-grain share.
3. **No arithmetic symptom.** The unit report recomputes exactly from the lot history and the lot dispositions; maps tie to final test and
   the chamber log to the etch tool's wafer counters.
4. **Not a row predicate.** It needs every wafer's map flag joined to its chamber, patterned and processed wafers counted per unit, and a
   ratio.
5. **The enumeration is arithmetic.** Which units stay at 100% is computed per unit; no field marks a share at wafer grain.
6. **No cutover date.** Etch chamber 3 has patterned every wafer since its maintenance sixteen days ago, before the window opened; no series
   steps inside the window.
7. **Survives deletion.** With every voice and the reference table removed, the answer and the difficulty are unchanged.

## 6. The calibration corpus

* **Form.** The pilot log: twelve holds taken last quarter under the new standard, each with the unit held, the unit report's share, the tie
  it was chosen from, the inspection finding, and that period's maps and chamber log.
* **What it pins.** Faults were found at exactly the held units whose wafer-grain share is 100%; the unit report and its tie-break chose a
  faulty unit in 5 of 12 holds.
* **Twin pair.** Pilot holds H-04 and H-09 are identical on the unit report's share (100%), lots and wafers credited (300), unit type (etch
  chamber) and days since maintenance (12). At wafer grain they stand at 100% and 47% (2.13×): H-04's chamber etched every patterned
  wafer of its lots, while H-09's patterned wafers came from an upstream chamber. Inspection found a displaced focus ring at H-04 and
  nothing at H-09.
* **Every rule exercised.** One pilot fault sat on a whole-lot unit, which wafer grain leaves at 100%, so the grain does not merely demote
  split chambers; one pilot tie included three chambers of one tool, so the chamber grain is tested.
* **Resemblance points at the decoy.** By unit report and unit type, C most resembles the pilot's one confirmed fault at a deposition
  chamber.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The hold standard: the hold goes to the unit with the highest systematic share over the last 14 days; every figure is the
  lowest value consistent with every file of record; ties go to the unit longest since its last preventive maintenance. The yield
  manual's pattern flag.
* **Empirical pins.** Wafer grain, the maps joined to the chamber log, from the pilot log.
* **Voices.** The equipment manager: "The fault-detection system knows which tools are sick; take down the one that alarms most." The
  deposition module lead: "Edge rings come from deposition; every fab knows it."
* **Licensed wrong basis.** The standard records that the customer's quality team audits holds on the unit report's share and will review
  this week's on that basis.

## 8. Determinism by construction

* **Wafer identity.** Every wafer's scribed ID is read at every step, so the maps, the lot history and the chamber log join on wafer ID with
  no slot mapping.
* **Dispatch.** The etch tool sends each K wafer to chamber 1 or 3 as one frees, the chamber log records every assignment, and no wafer is
  etched twice.
* **Window.** The 14 days are filed; 10 or 21 days leave E alone at 100%.
* **Pattern flag.** No wafer sits within 0.2 of the join-count line or within one die of the five-die minimum.

## 9. Prompt sketch and deliverables

> The fab has one engineering hold this week: one tool unit comes down for inspection. Our equipment manager wants whichever unit the
> fault-detection system alarms on most. Name the unit in a line for the hold notice, with `hold_choice.xlsx` holding the sheets below,
> the chart `systematic_share.png`, and a short `hold_notice.pdf`.

* `hold_choice.xlsx` — every unit's alarms, pattern count and systematic share at lot and at wafer grain, the maintenance sheet (ask A), the
  starts sheet (ask B) and the pilot back-test (ask C).
* `systematic_share.png` — the nine units' systematic shares at lot grain and at wafer grain as paired bars, the 100% line, the four tied
  units marked, and the twin pilot holds shown as an inset.
* `hold_notice.pdf` — the committed unit, the deciding comparison, and why the tie-break's pick is not it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the nine units, maintenance hours in the last quarter and the mean time between
  maintenances. *Device:* a maintenance that runs across a shift change is logged as two records linked by a continuation ID, per the
  maintenance system's guide. Counting records doubles those maintenances and shortens the mean interval at four units. The hold build
  reads only each unit's last preventive maintenance date, which no continuation record moves.
* **Ask B (device-carried).** For each of the six products, wafer starts in the window and the share on priority lots. *Device:* a lot split
  into child lots keeps its parent's start date and gains a suffix, as the MES guide documents. Counting child lots as starts overcounts
  the two products split most.
* **Ask C (validity).** For each of the four rung constructions, the pilot findings it reproduces out of 12.
* **Decoupling.** Clearing the wafer-grain join changes no figure in asks A or B.

## 11. Rubric arithmetic

9 units × 2 (ask A) + 6 products × 2 (ask B) + 4 constructions (ask C) + the committed unit, its wafer-grain share and the margin over C + 5
named chart parts + 3 files ≈ 45 criteria.

## 12. World-building constraints

* Rung leaders are A, B, C, E. E is 5th / uncredited / last of four tied / 1st; rung margins 1.24×, 1.75× and the tie-break (1.45× over
  the first unit outside the tie); E leads rung 3 by 2.17×.
* Product K: 46 lots, 1,150 wafers, etched in chambers 1 (621 wafers) and 3 (529); every chamber-3 wafer carries the edge ring. Units
  running only K: the deposition chamber (C), etch chambers 3 (E) and 1 (F), implant source 2 (G).
* Days since preventive maintenance: C 58, G 44, F 30, E 16. Stepper 1 exposed 28 K lots and 30 others, 12 of them with focus-spot wafers.
* The pilot log holds twelve holds; H-04 and H-09 are identical on every lot-level column.
* Continuation maintenance records and child lots never touch the maps, the chamber log or the lot dispositions.

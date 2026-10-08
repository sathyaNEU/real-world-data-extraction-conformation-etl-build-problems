# AD20 — Which tool unit comes down for the fab's one engineering hold, when four units sit at a 100% systematic share and three of them owe it to wafers that never reached a map

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Supply Chain & Logistics · semiconductor fab operations |
| Mirrors | Breaking a 100% tie in a failure-attribution share by reconciling against units that never reached inspection (drive-failure attribution in hyperscale fleets where dead units never report, device-return analysis at Apple and Google where scrapped units carry no telemetry, commonality analysis in contract manufacturing) |
| Decision shape | Which of N gets one scarce thing: this week's single engineering hold, one tool unit taken down for inspection |
| Committed call | The one tool unit held for inspection this week |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · a saturated tie broken by the standard's own rule across files of record (E21), the reconciliation pinned by the pilot log, with the deciding comparison at the lower rung (E22) |
| Gate G mechanism | method_or_model_selection, with signal_vs_noise_or_hold support |
| Measured traps engaged | #19 breaks a big tie instead of questioning it · #20 leaves the deciding comparison unstated · #4 never tests its reading against the control |
| Calibration form | Pilot log: last quarter's twelve pilot holds under the new hold standard, each with its unit and the inspection finding |
| Driving force | The hold standard ranks units by their systematic share, the share of die loss on their wafers that sits on wafers with a systematic pattern, and four units read 100% on the wafer maps. The standard also says every figure is the lowest value consistent with every file of record. Wafers scrapped before final test have no map but are in the chamber log, and their dies are lost with no pattern shown; counted that way, three of the four fall to between 39% and 79%, and only the etch chamber that ran nineteen wafers, all mapped and all patterned, keeps 100%. |

## 1. Situation

A wafer fab can take one tool unit down for an engineering hold this week. Its hold standard gives the hold to the unit with the highest
systematic share over the last 14 days: of the die loss on wafers the unit processed, the share on wafers whose map shows a systematic
pattern (join-count z of 3 or more with at least five failing dies). Every figure is the lowest value consistent with every file of record,
and ties go to the unit that processed more wafers. The pack carries the 14 days' wafer maps from final test, the chamber log (every wafer
each unit processed, by wafer ID), the MES scrap records, the fab's pattern-to-tool reference table and the pilot log.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: every map, every chamber-log line, every scrap record and every pilot finding. The four 100% readings
  are exactly what the maps show. Nothing reported is overturned and no stakeholder read is corrected; the difficulty is that the maps cover
  only the wafers that reached final test.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the reference table. The maps still put four units at 100%, and the documented tie-break still
  picks the deposition chamber.
* **Instrument repair.** Map every wafer at final test perfectly; they already are. Scrapped wafers never reach final test, so a better
  final-test instrument still cannot show their patterns, and the standard's rule is what governs them.
* **Lens swap.** The naive share is over mapped wafers; the answer's is over processed wafers, a population that adds 81 scrapped wafers and
  changes which units are tied.

## 3. The driving force

A strong solver turns away from raw die loss and from pattern counts, because the standard asks for neither: it asks for the systematic
share, the comparison of patterned die loss with all die loss on a unit's wafers. It computes that share from the maps, finds four units
at 100%, and applies the documented tie-break, more wafers processed, which names the deposition chamber with 63 mapped wafers. Each step is
competent, and the deciding comparison was even stated. But a share of 100% on mapped wafers is a ceiling the maps make easy to reach, and
the standard's own first rule says every figure is the lowest value consistent with every file of record. The chamber log lists 92 wafers
through the deposition chamber in the window; 29 were scrapped at an earlier inspection and never mapped. Their dies are lost, and no file
shows them patterned, so the lowest consistent share falls to 68%. Reconciled the same way, the CMP head falls to 79% and
the implant source to 39%. Etch chamber C ran only nineteen wafers after its last maintenance, every one reached final test, and every one is
patterned: it alone keeps 100%.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Die loss per unit over 14 days | A, diffusion furnace (61,000 dies; 1.27× B) | Where the most dies are lost is where the money is | The hold standard: the hold goes on systematic share, and the furnace's losses are random particles, 58% unpatterned |
| 1 | Patterned wafers per unit, mapped to tools by the fab's pattern-to-tool table | B, stepper 1 (212 wafers; 1.26× D) | Systematic patterns, attributed the way the fab's engineers attribute them | The standard compares patterned loss with all loss on each unit's wafers; counted alone, the stepper's frequent focus spots lose three dies each |
| 2 | The systematic share from the wafer maps; four units at 100%; ties to more wafers processed | C, deposition chamber B (63 mapped; 1.54× D's 41) | The standard's own measure and its documented tie-break, the comparison stated | The standard's rule: figures are the lowest value consistent with every file of record, and the chamber log lists wafers no map covers |
| 3 | **Decisive:** the systematic share over every wafer in the chamber log, scrapped wafers counted as lost with no pattern shown | **E, etch chamber C (100%)** (5th of 9 on rung 0) | — | — |

* **Position table.** E ranks 5th on rung 0 (27,000 dies), 4th on rung 1 (96 wafers) and 3rd on rung 2 (tied at 100%, 19 wafers in the
  tie-break), and leads only rung 3, 1.27× D (79%) and 1.46× C (68%).
* **Discriminator dominance.** C reaches rung 3 level with E on the measure, both at 100%, carrying only the tie-break's 3.3× wafer count,
  which a broken tie no longer consults. On the reconciled share E's edge is 1.46× over C against the 1.2 × 1.0 required, and 1.27× over the
  runner-up.
* **Partial correction priced (L3).** A solver who reconciles against the MES wafer counts instead of the chamber log credits scrapped wafers
  to the tool, not the chamber, and lowers all four etch chambers alike; it names D, the CMP head, at 79%. A solver who imputes scrapped
  wafers at the unit's mapped share keeps the four-way tie and the tie-break's C.
* **Grid.** Measure (die loss, pattern count, systematic share) × wafer population (mapped or processed) × scrap handling (imputed or
  counted as unshown) gives the cells: die loss names A, pattern counts B, mapped shares C, imputed shares C, MES-grain reconciliation D.
  Only the chamber-log reconciliation names E, and the nearest wrong cell (D) needs the scrap credited to the tool instead of the chamber.
* **The deciding comparison (#20).** Patterned against all die loss per unit is the comparison the hold notice has to state; die loss alone
  and pattern counts alone each name a different unit.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The standard states its rule as a principle and names no file. Nothing says final-test maps miss scrapped wafers,
   and the scrap records sit in the MES, which the maps never reference.
2. **The corpus pins a construction, not a menu.** The chamber-log reconciliation reproduces all 12 pilot findings: every unit inspected at a
   reconciled 100% had a fault and every other inspected unit had none. Map-only shares with the tie-break reproduce 5 of 12, and the MES
   grain 8. The reconciliation is a construction: processed wafers per unit from one log, mapped wafers from another, scrapped wafers from
   a third, and no column holds the reconciled share.
3. **No arithmetic symptom.** Maps tie to final-test records and the chamber log ties to wafer starts; the 100% shares are exact for what
   they cover.
4. **Not a row predicate.** It needs, per unit, a count of processed wafers from the chamber log, a count of mapped wafers, the dies lost on
   the unmapped ones, and a recomputed share.
5. **The enumeration is arithmetic.** Which units stay at 100% is computed per unit; no field marks a share as settled.
6. **No cutover date.** Scrap is spread across the window, and etch chamber C has run steadily patterned since its maintenance three weeks
   ago; no series steps inside the window.
7. **Survives deletion.** With every voice and the reference table removed, the answer and the difficulty are unchanged.

## 6. The calibration corpus

* **Form.** The pilot log: twelve holds taken last quarter under the new standard, each with the unit held, its systematic share as the
  pilot computed it from maps, the tie it was chosen from, and what inspection found.
* **What it pins.** Faults were found at exactly the units whose share stays at 100% after the chamber-log reconciliation; the map-only
  share would have held the same unit in 5 of 12 cases.
* **Twin pair.** Pilot holds H-04 and H-09 are identical on map-only share (100%), mapped wafers (38), die loss, unit type and maintenance
  age. H-04 found a cracked focus ring and H-09 found nothing: H-09 had 29 scrapped wafers in the chamber log, a reconciled share of 57%.
* **Every rule exercised.** One pilot unit's scrapped wafers were scrapped for a reason unrelated to the pattern, so scrap is counted
  whatever its cause; one pilot tie involved chambers of one tool, so the chamber grain is tested.
* **Resemblance points at the decoy.** By map profile C most resembles H-04, a confirmed fault.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The hold standard: the hold goes to the unit with the highest systematic share over the last 14 days; every figure is the
  lowest value consistent with every file of record; ties go to the unit that processed more wafers. The yield manual's pattern flag.
* **Empirical pins.** Scrapped wafers counted as lost with no pattern shown, at chamber grain, from the pilot log.
* **Voices.** The yield manager: "Send the engineers wherever the most dies are being lost." The deposition module lead: "Edge rings come
  from deposition; every fab knows it."
* **Licensed wrong basis.** The standard records that the customer's quality team audits holds on map-only systematic shares and will review
  this week's on that basis.

## 8. Determinism by construction

* **Wafer identity.** Every wafer's scribed ID is read at every step, so the chamber log, the maps and the scrap records join on wafer ID with
  no slot mapping.
* **Window.** The 14 days are filed; 10 or 21 days leave E alone at 100%.
* **Pattern flag.** No wafer sits within 0.2 of the join-count line or within one die of the five-die minimum.
* **Die loss on scrap.** A scrapped wafer loses all its dies, a convention the yield manual states.

## 9. Prompt sketch and deliverables

> The fab has one engineering hold this week: one tool unit comes down for inspection. Our yield manager wants it wherever the most dies are
> being lost. Name the unit in a line for the hold notice, with `hold_choice.xlsx` holding the sheets below, the chart
> `systematic_share.png`, and a short `hold_notice.pdf`.

* `hold_choice.xlsx` — every unit's die loss, pattern count and systematic share on mapped and on processed wafers, the maintenance sheet
  (ask A), the starts sheet (ask B) and the pilot back-test (ask C).
* `systematic_share.png` — the nine units' systematic shares on mapped wafers and on processed wafers as paired bars, the 100% line, scrapped
  wafers stacked on each bar, and the twin pilot holds shown as an inset.
* `hold_notice.pdf` — the committed unit, the deciding comparison, and why the tie-break's pick is not it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the nine units, maintenance hours in the last quarter and the mean time between
  maintenances. *Device:* a maintenance that runs across a shift change is logged as two records linked by a continuation ID, per the
  maintenance system's guide. Counting records doubles those maintenances and shortens the mean interval at four units. The hold build
  never reads the maintenance log.
* **Ask B (device-carried).** For each of the six products, wafer starts in the window and the share on priority lots. *Device:* a lot split
  into child lots keeps its parent's start date and gains a split suffix, as the MES guide documents. Counting child lots as starts
  overcounts the two products split most.
* **Ask C (validity).** For each of the four rung constructions, the pilot findings it reproduces out of 12.
* **Decoupling.** Clearing the chamber-log reconciliation changes no figure in asks A or B.

## 11. Rubric arithmetic

9 units × 2 (ask A) + 6 products × 2 (ask B) + 4 constructions (ask C) + the committed unit, its reconciled share and the margin over D + 5
named chart parts + 3 files ≈ 45 criteria.

## 12. World-building constraints

* Rung leaders are A, B, C, E. E is 5th / 4th / 3rd (tied) / 1st; rung margins 1.27×, 1.26×, the tie-break's 1.54×; E leads rung 3 by 1.27×.
* Mapped-only 100%: C (63 wafers), D (41), E (19), F (12). Processed: C 92, D 52, E 19, F 31; reconciled 68%, 79%, 100%, 39%.
* The pilot log holds twelve holds; H-04 and H-09 are identical on every map-level column.
* Continuation maintenance records and split lots never touch the maps, the chamber log or the scrap records.

# DA46 — Which maternity hospital gets the region's next small-baby unit, when only growth-restricted small babies ever need it

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Policy & Education · health-system commissioning |
| Mirrors | Sizing a service on a flagged population when need splits on a marker held in another system (fraud reviews needed only for flagged accounts with a device signal, support escalations needed only for tickets with a failed payment, returns inspections needed only where a sensor fired), so the flagged count overstates where the marker is rare |
| Decision shape | Which of N gets one scarce thing: an eight-cot small-baby unit for one of six maternity hospitals |
| Committed call | The hospital that gets the unit, and the small-for-gestational-age babies a year the unit would care for there |
| Gap · Pattern | Gap 2 (population) over Gap 3 (objective) · Pattern E (conditioned yield: need splits on a scan reading reached through a join), with a binding transfer limit applied in the count at rung 2 (measured #10) |
| Gate G mechanism | method_or_model_selection, with binding_constraint support |
| Measured traps engaged | #13 validates on one population, applies to another · #10 notes a binding limit as a risk · #7 uses the ready-made measure |
| Calibration form | Settled-transaction ledger: the top-ups settled for the region's eight existing small-baby units over twelve closed quarters, each unit-quarter the number of SGA babies the unit cared for 48 hours or more |
| Driving force | A baby small for its gestation needs special care only if it is growth-restricted, and the mother's last-trimester Doppler reading says which: the existing units' 96 settled unit-quarters return exactly when 88% of kept small babies with an abnormal reading are admitted and none with a normal one. The reading sits in the scan file, joined through the mother, not on the birth record. Calderbrook's small babies are mostly constitutionally small, born to a population of smaller mothers; Elmhurst's are growth-restricted. |

## 1. Situation

A regional health authority's commissioning board will fund one more eight-cot small-baby unit. Eight of the region's fourteen maternity
hospitals run one, each caring only for babies born in its own hospital; the other six keep small babies in their general neonatal cots,
which draw no top-up. The framework sends the new unit to whichever of those six has the most small-for-gestational-age babies it would
care for. Babies are classed against the region's reference table of birthweight percentiles by completed week. The pack holds three years
of birth records for all fourteen hospitals with mothers' identifiers, the scan file from the maternity dashboard's scan audit, the
reference table with its plausibility bounds, the network transfer protocol, the top-up ledger for the eight units, and the framework.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: each birth record, each scan reading, each reference percentile, each settled unit-quarter.
  Nobody ranks the hospitals on the framework's basis and nothing reported is overturned. The difficulty is which small babies need the
  unit.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the neonatal lead's view and the network's basis. Small babies counted on the reference table, cleaned and net
  of transfers, still name Calderbrook.
* **Instrument repair.** Suspect: the birth records' implausible weight-for-week entries. Corrected, rung 0 returns rung 1's Brookside,
  and rungs 1 and 2 stay Brookside and Calderbrook. Every mother's last scan is in the scan file, and the ledger records what it claims,
  each existing unit's settled top-ups each quarter; the six candidates have no unit to settle. The babies the new unit would care for
  are a forward count, built from each hospital's small babies and a need conditioned on a reading joined through the mother, so the
  answer stays Elmhurst and the conditioning is still needed.
* **Lens swap.** The naive count takes every kept small baby as needing the unit; the answer takes the growth-restricted ones, a
  different population that is a third of Calderbrook's and nearly all of Elmhurst's.

## 3. The driving force

A strong solver classes each baby against the reference table, drops the implausible weight-for-week records the table's bounds mark, and
counts only the babies the unit would keep, since the network protocol sends babies under 1,500 g to the tertiary centre. Calderbrook
leads with 250 a year. It then checks the ledger: the existing units' pooled admission rate, 52%, returns only 9 of their 96 settled
unit-quarters, and no visible column explains the misses. The mother's last-trimester scan does. Small babies whose umbilical Doppler
reading was abnormal, the growth-restricted, were admitted at 88% in every unit-quarter; those with a normal reading, constitutionally
small, never. Calderbrook serves a population of smaller mothers whose babies are small and well, and Elmhurst's small babies are
growth-restricted. Conditioned on the reading, the new unit would care for 167 Elmhurst babies a year and 66 from Calderbrook.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Babies below the 10th percentile for recorded week | A, Ashgate (410 a year, 1.24× Brookside) | The clinical record against the regional table | The table's plausibility bounds: 14% of Ashgate's small babies are impossible weights for their recorded week |
| 1 | Hygiene: implausible weight-for-week records excluded | B, Brookside (320, 1.23× Calderbrook) | Clean, bounded, reconciled to the register | The network transfer protocol: babies under 1,500 g transfer to the tertiary centre |
| 2 | Babies the unit would keep: under 1,500 g removed as the protocol requires (binding limit applied) | C, Calderbrook (250, 1.22× Brookside) | The framework's count, with the limit applied in the figure | The ledger: any rate applied to every kept small baby returns at most 9 of 96 settled unit-quarters |
| 3 | **Decisive:** kept small babies × need conditioned on the mother's last Doppler reading (0.88 abnormal, none normal), joined through the scan file | **E, Elmhurst (167, 1.40× Dunford)** (5th of 6 on rung 0) | — | — |

* **Position table.** Elmhurst ranks 5th on rung 0 (240), 4th on rung 1 (232) and 3rd on rung 2 (200), and leads only rung 3.
* **Discriminator dominance.** Calderbrook carries 1.25× into rung 3 (250 against 200). Conditioning keeps 0.84 of Elmhurst's count and
  0.26 of Calderbrook's, an edge of 3.16×, against the 1.2 × 1.25 = 1.50 needed (2.1× headroom). The product, 3.16 / 1.25 = 2.53, is
  Elmhurst's lead over Calderbrook on rung 3; Dunford is runner-up at 119.
* **Partial correction priced (L3).** A solver who applies the ledger's pooled rate keeps Calderbrook, 1.25× Elmhurst. One who marks need
  by birthweight below the 3rd percentile, the visible proxy, counts Calderbrook's constitutionally small babies and names it at 1.28×
  Elmhurst (125 against 98). One who uses the booking risk flag names Dunford at 1.23× Elmhurst (128 against 104). No half lands on
  Elmhurst.
* **Grid.** On rung 2's base, need (every kept baby, pooled rate, below the 3rd percentile, booking risk, Doppler reading) = 5 cells; four
  name Calderbrook or Dunford. Doppler conditioning names Elmhurst on every base, with or without hygiene and the limit.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The framework counts the small babies the unit would care for. The ledger settles each existing unit's top-ups; the
   scan file ships for the dashboard's scan audit. No document links a reading to special care.
2. **Pattern E, pinned at zero tolerance.** Doppler-conditioned need returns all 96 settled unit-quarters exactly. The pooled rate,
   fitted to the ledger's three-year total, returns 9, the 3rd-percentile marker 23 and booking risk 14. The conditioning is a
   construction: each baby joined to its mother's last scan, then counted by reading, unit by unit and quarter by quarter.
3. **No arithmetic symptom.** Births tie to the register and scans to mothers, and the pooled rate returns the ledger's three-year total
   exactly.
4. **Not a row predicate.** A hospital's figure needs each baby's mother's last scan, joined across files, and a yield recovered from
   other hospitals' settled totals; no row of the birth file carries it.
5. **The enumeration is arithmetic.** No column marks a baby as growth-restricted or as needing the unit.
6. **No cutover date.** The scan protocol and the protocol limit are the same in all three years, and nothing steps.
7. **Survives deletion.** With every voice removed, the protocol-net count still names Calderbrook.

## 6. The calibration corpus

* **Form.** The top-up ledger: the eight existing units' settled small-baby top-ups for twelve closed quarters, 96 unit-quarters, each
  the number of SGA babies the unit cared for 48 hours or more.
* **What it certifies.** The three-year total, which any rate fitted to it returns.
* **What pins the conditioning.** The unit-quarter totals, which only Doppler-conditioned need returns.
* **Twin pair.** The Netherby unit's 2023 Q2 and the Westmere unit's 2024 Q1 match on kept small babies (54), birthweight distribution,
  gestation and booking risk. Their settled top-ups are 44 and 22 (2.0×): 50 of Netherby's 54 small babies had an abnormal reading, and
  25 of Westmere's.
* **Resemblance points at the decoy.** On every birth-record column, Calderbrook's small babies resemble those of the units with the
  most settled top-ups.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The framework: the new unit goes to the hospital without one whose small-for-gestational-age babies it would care for most each year,
  classed by the region's reference table on completed gestational weeks. The network protocol: babies under 1,500 g transfer to the
  tertiary centre.
* **Empirical pins.** The need and its marker, from the ledger.
* **Voices.** Calderbrook's neonatal lead: "We see more small babies than anyone; the numbers speak for themselves." The commissioning
  analyst: "A small baby is a small baby; the chart decides."
* **Licensed wrong basis.** The framework records that the regional maternity network ranks hospitals on all small-for-gestational-age
  births, transfers included, and will present that ranking at the board.

## 8. Determinism by construction

* **Scans.** Every small baby's mother had a last-trimester scan with a Doppler reading, and no reading lies within 5% of the cut-off.
* **Need.** In every unit-quarter, top-ups equal 0.88 of the kept small babies with an abnormal reading, to the nearest whole baby, and
  no product lies within 0.1 of a half; babies with a normal reading are never admitted.
* **Weights.** Birthweights are heaped at 50 g, and no heaped value equals a reference percentile.
* **Year.** Each hospital's yearly count is the three-year mean, and no year departs from it by more than 6%.

## 9. Prompt sketch and deliverables

> The board commissions the small-baby unit on the 19th, and Calderbrook's neonatal lead says the numbers make the case. Tell me which
> hospital gets the unit and how many small-for-gestational-age babies a year it would care for there, in one line for the board paper.
> Send `unit_siting.xlsx`, a chart `need_by_reading.png`, and a one-page `siting_note.pdf`.

* `unit_siting.xlsx` — the count for all six hospitals under each rung, the stay sheet (ask A), the residence sheet (ask B) and the
  ledger table (ask C).
* `need_by_reading.png` — each hospital's kept small babies as bars split by Doppler reading, the babies the unit would care for
  labelled, the ledger's 96 unit-quarters inset against each construction, the 1,500 g limit noted, and the chosen hospital marked.
* `siting_note.pdf` — the committed hospital, its count, and why the others fall away.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each hospital, the median postnatal stay in days. *Device:* ward moves split one stay into
  two episodes, which the patient administration system links by spell number; counting episodes halves the median at three hospitals.
* **Ask B (device-carried).** For each hospital, the share of births to mothers living outside the region. *Device:* the postcode-to-region
  lookup carries boundary changes with effective dates; using the current boundaries misassigns 7% of births.
* **Ask C (validity).** Each hospital's count under each of the four rungs, and the settled unit-quarters returned by each need construction.
* **Decoupling.** Clearing the Doppler conditioning changes no figure in asks A or B.

## 11. Rubric arithmetic

6 hospitals (ask A) + 6 hospitals (ask B) + 6 × 4 rung counts and 4 reproduction counts (ask C) + the committed hospital, its count and
its margin + 5 named chart parts + 3 files ≈ 51 criteria.

## 12. World-building constraints

* Counts a year: rung 0 A 410, B 330, C 300, D 270, E 240, F 190; rung 1 B 320, C 260, A 250, E 232, D 215, F 180; rung 2 C 250, B 205, E 200,
  A 190, D 180, F 150; rung 3 E 167, D 119, B 99, A 84, F 79, C 66.
* Abnormal readings among kept small babies: Elmhurst 95%, Dunford 75%, Fairholme 60%, Brookside 55%, Ashgate 50%, Calderbrook 30%; the
  existing units' pooled admission rate 52%.
* Partial cells (kept small babies a year): below the 3rd percentile C 125, E 98, D 97, A 86, B 82, F 68; with the booking risk flag
  D 128, E 104, C 100, A 95, B 92, F 81.
* Ledger: 8 units × 12 quarters; returned 96 / 23 / 14 / 9 by Doppler, 3rd percentile, booking risk and the pooled rate. Netherby
  2023 Q2 and Westmere 2024 Q1 match on every birth-record column.
* Spell numbers and postcode boundaries never touch a scan, a weight or a payment.

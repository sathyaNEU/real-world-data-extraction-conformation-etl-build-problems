# DA46 — Which maternity hospital gets the region's one small-baby unit, when recorded gestation carries an offset set by a scanner rota

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Policy & Education · health-system commissioning |
| Mirrors | Classifying units against a reference by a recorded attribute whose offset is set upstream in batches (delivery dates stamped by depot run, device ages from activation batches, order cohorts from weekly processing cycles), as large retailers and device makers meet when the stamp is not the event |
| Decision shape | Which of N gets one scarce thing: an eight-cot small-baby unit for one of six maternity hospitals |
| Committed call | The hospital that gets the unit, and the small-for-gestational-age babies a year the unit would care for there |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · S4 (a mixture, not a constant, recovered at zero tolerance), with a binding transfer limit applied in the count at rung 2 (measured #10) |
| Gate G mechanism | method_or_model_selection, with binding_constraint support |
| Measured traps engaged | #10 notes a binding limit as a risk · #4 never tests its reading against the control · #3 stops at a close but inexact match |
| Calibration form | Settled-transaction ledger: three closed years of small-baby top-up payments, each settled after the regional audit confirmed the baby small for its audited gestation |
| Driving force | A baby's recorded gestation is its true gestation when its mother booked in a week the shared scanner was at her clinic, and seven days more when she was dated from her last period. The scanner rotates across four booking clinics on a three-week cycle that no file records. Every settled payment agrees with exactly one set of rota phases, and those phases decide which hospitals' "small" babies are a week younger than their charts say. |

## 1. Situation

A regional health authority's commissioning board will fund one eight-cot small-baby unit, and its framework sends the unit to the
hospital whose small-for-gestational-age babies the unit would care for most. Babies are classed against the region's reference table of
birthweight percentiles by completed week. Six maternity hospitals are eligible. The pack holds three years of birth records with booking
clinic and booking date, the reference table with its plausibility bounds, the network transfer protocol, the top-up ledger, and the
framework.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: each birth record, each reference percentile, each settled payment. Nobody ranks the hospitals on
  the framework's basis and nothing reported is overturned. The difficulty is which gestational week a recorded week is.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the neonatal lead's view and the network's basis. Classing babies on recorded gestation, cleaned and net of
  transfers, still names Calderbrook.
* **Instrument repair.** Scan every mother at booking from now on: the three years of records already made stay a mixture, and the unit
  is commissioned on them. Which records carry the offset is recoverable only from the ledger.
* **Lens swap.** The naive count classes babies at their recorded week; the answer re-dates a third of them a week earlier, so different
  babies fall below the line.

## 3. The driving force

A strong solver classes each baby against the reference table, drops the implausible weight-for-week combinations the table's bounds mark,
and, because the network protocol sends babies under 1,500 g to the tertiary centre, counts only the babies the unit would keep.
Calderbrook leads. The settled ledger disagrees with every one of those counts. The audit behind each payment re-dated pregnancies, and
the pattern is sharp: babies of mothers dated from their last period sit exactly seven days later on the record than their audited
gestation. Which mothers were dated that way depends on whether the scanner was at their booking clinic in their booking week. The rota
covers four clinics on a three-week cycle, and one set of phases makes all 18 hospital-year settled counts return exactly. Calderbrook's
mothers mostly booked in scanner-less weeks. Re-dated, half its small babies are simply a week younger, and Elmhurst leads with 196 a
year.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Babies below the 10th percentile for recorded week | A, Ashgate (410 a year, 1.24× Brookside) | The clinical record against the regional table | The table's plausibility bounds: 14% of Ashgate's small babies are impossible weights for their recorded week |
| 1 | Hygiene: implausible weight-for-week records excluded | B, Brookside (320, 1.23× Calderbrook) | Clean, bounded, reconciled to the register | The network transfer protocol: babies under 1,500 g transfer to the tertiary centre |
| 2 | Babies the unit would keep: under 1,500 g removed as the protocol requires (binding limit applied) | C, Calderbrook (250, 1.22× Brookside) | The framework's count, with the limit applied in the figure | The ledger: these counts return 4 of 18 settled hospital-years |
| 3 | **Decisive:** gestation re-dated by booking-week dating method, scanner rota phases recovered from the ledger | **E, Elmhurst (196, 1.23× Dunford)** (5th of 6 on rung 0) | — | — |

* **Position table.** Elmhurst ranks 5th on rung 0 (240), 4th on rung 1 (232) and 3rd on rung 2 (200), and leads only rung 3.
* **Discriminator dominance.** Calderbrook carries 1.25× into rung 3. Re-dating keeps 0.98 of Elmhurst's count and 0.50 of
  Calderbrook's, an edge of 1.96×, against the 1.2 × 1.25 = 1.50 needed (1.31× headroom). The product, 1.96 / 1.25 = 1.57, is Elmhurst's
  lead over Calderbrook on rung 3; Dunford is runner-up at 160.
* **Partial correction priced (L3).** A solver who subtracts the regional average offset (3.5 days) from every record, a per-line
  constant, still names Calderbrook at 190, 1.12× Elmhurst's 170. One who treats each clinic as all-scan or all-period by its majority
  method names Dunford at 1.10× Elmhurst. Neither half lands on Elmhurst.
* **Grid.** Hygiene (off or on) × transfer limit (off or on) × dating (recorded, constant offset, clinic majority, rota phases) = 16
  cells. Fifteen name Ashgate, Brookside, Calderbrook or Dunford.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The birth record carries one gestation field. The booking guidance says mothers are "dated by scan where
   available". No document records the rota or the seven-day offset.
2. **Pattern B, a mixture fixed at zero tolerance.** One set of rota phases (one of 81) returns all 18 settled hospital-year counts
   exactly. Recorded gestation returns 4, the constant offset 2 and clinic majority 9, and no other phase set returns more than 11. The
   phases are a construction: each birth's booking week tested against a clinic's cycle, then the offset applied birth by birth.
3. **No arithmetic symptom.** Recorded gestations are all plausible after hygiene, births tie to the register, and every count reconciles
   under every dating.
4. **Not a row predicate.** Whether a record carries the offset depends on a clinic-level phase recovered across thousands of other births.
5. **The enumeration is arithmetic.** No column marks a birth as scan-dated.
6. **No cutover date.** The rota repeats every three weeks for three years, with nothing stepping.
7. **Survives deletion.** With every voice removed, the protocol-net count still names Calderbrook.

## 6. The calibration corpus

* **Form.** The top-up ledger: every small-baby payment settled for the six hospitals over three closed years, each after audit, with
  hospital and year.
* **What it certifies.** That the framework's count is net of transfers and implausible records, which a back-tester confirms at rung 2's
  totals for four hospital-years.
* **What pins the mixture.** The 14 hospital-years only the rota phases return.
* **Twin pair.** Brookside 2023 and Dunford 2022 match on births, booking-clinic mix, recorded gestation distribution and birthweights.
  Their settled payments are 160 and 80 (2.0×): Dunford's booking clinic had the scanner in the weeks most of its mothers booked.
* **Resemblance points at the decoy.** On every record column, Calderbrook resembles the hospital-years with the most settled payments.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The framework: the unit goes to the hospital whose small-for-gestational-age babies it would care for most each year,
  classed by the region's reference table on completed gestational weeks. The network protocol: babies under 1,500 g transfer to the
  tertiary centre.
* **Empirical pins.** The rota phases and the offset, from the ledger.
* **Voices.** Calderbrook's neonatal lead: "We see more small babies than anyone; the numbers speak for themselves." The commissioning
  analyst: "Recorded gestation is the clinical record, and we shouldn't second-guess it."
* **Licensed wrong basis.** The framework records that the regional maternity network ranks hospitals on all small-for-gestational-age
  births, transfers included, and will present that ranking at the board.

## 8. Determinism by construction

* **Offset.** Every audited period-dated pregnancy sits exactly seven days later on the record; scan-dated ones sit at zero.
* **Rota.** One clinic holds the scanner each week, on a fixed three-week cycle per clinic, unchanged across the three years.
* **Weights.** Birthweights are heaped at 50 g, and no heaped value equals a reference percentile.
* **Year.** Each hospital's yearly count is the three-year mean, and no year departs from it by more than 6%.

## 9. Prompt sketch and deliverables

> The board commissions the small-baby unit on the 19th, and Calderbrook's neonatal lead says the numbers make the case. Tell me which
> hospital gets the unit and how many small-for-gestational-age babies a year it would care for there, in one line for the board paper.
> Send `unit_siting.xlsx`, a chart `redated_counts.png`, and a one-page `siting_note.pdf`.

* `unit_siting.xlsx` — the count for all six hospitals under each rung, the stay sheet (ask A), the residence sheet (ask B) and the
  ledger table (ask C).
* `redated_counts.png` — each hospital's count on recorded and on re-dated gestation as paired bars, with the share of period-dated
  births labelled on each hospital, the 1,500 g limit noted, and the chosen hospital marked.
* `siting_note.pdf` — the committed hospital, its count, and why the others fall away.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each hospital, the median postnatal stay in days. *Device:* ward moves split one stay into
  two episodes, which the patient administration system links by spell number; counting episodes halves the median at three hospitals.
* **Ask B (device-carried).** For each hospital, the share of births to mothers living outside the region. *Device:* the postcode-to-region
  lookup carries boundary changes with effective dates; using the current boundaries misassigns 7% of births.
* **Ask C (validity).** Each hospital's count under each of the four rungs, and settled hospital-years returned by each dating
  construction.
* **Decoupling.** Clearing the rota re-dating changes no figure in asks A or B.

## 11. Rubric arithmetic

6 hospitals (ask A) + 6 hospitals (ask B) + 6 × 4 rung counts and 4 dating reproduction counts (ask C) + the committed hospital, its count
and its margin + 5 named chart parts + 3 files ≈ 51 criteria.

## 12. World-building constraints

* Counts a year: rung 0 A 410, B 330, C 300, D 270, E 240, F 190; rung 1 B 320, C 260, A 250, E 232, D 215; rung 2 C 250, B 205, E 200,
  A 190, D 180; rung 3 E 196, D 160, B 150, A 140, C 125.
* Period-dated births: Calderbrook 64%, Elmhurst 4%; rota phases unique among 81.
* Ledger: 18 hospital-years; returned 18 / 9 / 4 / 2 by rota phases, clinic majority, recorded and constant offset.
* Spell numbers and postcode boundaries never touch a gestation, a weight or a payment.

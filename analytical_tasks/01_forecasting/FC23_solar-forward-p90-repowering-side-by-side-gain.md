# FC23 — How much of next year's solar output to sell forward at P90, when the repowering's gain was measured side by side, not promised

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Economics · corporate energy procurement and hedging |
| Mirrors | Committing forward volumes after an upgrade whose gain must be measured side by side rather than taken from the vendor (data-centre cooling retrofits measured on paired halls at Google and Meta, Amazon fulfilment automation rollouts measured on paired shifts, telecom network upgrades measured against control cells) |
| Decision shape | One figure committed at a date: the volume of 2027 output sold forward in the desk's annual hedge |
| Committed call | 2027 energy sold forward at the one-year P90, in MWh rounded down to the nearest 1,000 |
| Gap · Pattern | Gap 1 (time) over Gap 3 (objective) · change-log natural experiments: the repowering's gain measured where both halves of a plant ran under the same sky, against an assumed gain or a before-and-after reading; with a latent attribution marker in the meter history below it |
| Gate G mechanism | forecasting, with method_or_model_selection |
| Measured traps engaged | #25 assumes an effect the log could measure · #26 picks a window across a documented confounder · #17 guesses an attribution the data can settle |
| Calibration form | Parallel-run overlap: the eight-week side-by-side periods of the operator's five earlier repowerings, when the repowered and original halves of each plant ran together |
| Driving force | The plant's modules are replaced on the existing racking and inverters before 2027. The vendor's yield report promises 35% more energy, and before-and-after comparisons at the operator's five earlier repowerings average 33%, because each was done in spring and its "after" months were sunnier. Each of those repowerings also ran a new half beside an old half for eight weeks under the same sky, and in every one the new half produced 22% more, within half a point, because the old inverters clip what the new modules add. The side-by-side periods sit in the commissioning records of the change log, not in the production history. |

## 1. Situation

A corporate buyer owns a 40 MW solar plant and hedges its output a year ahead. The energy desk's memo sets the 2027 forward sale at the
one-year P90: 25 weather years of plane-of-array irradiance, turned into energy by a performance ratio calibrated on the last five years'
metered output, with the sample standard deviation of the annual energies. The plant's original modules are being replaced, on the same
racking and inverters, and the work finishes in December. The operator has repowered five similar plants since 2019.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the irradiance record, the revenue-meter history, the plant and neighbour SCADA, the vendor's
  yield report, the change log and its commissioning records. No one's claim about their own numbers is overturned. The difficulty is
  the size of an effect that has happened five times and was promised once.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the lender's basis. The memo's P90 with the vendor's yield report still sells 132,000 MWh.
* **Instrument repair.** Suspect: the revenue-meter history, whose rows do not say which arrays they covered, and for 18 months of the
  calibration window the meter also carried the neighbouring community array. Assign those months: rung 0 then returns rung 1's 137,000
  MWh and rung 2 still 132,000 MWh. The irradiance record, SCADA and change log are complete, and the side-by-side gain is still needed
  for 119,000.
* **Lens swap.** The naive read and the answer differ in moment: a gain read from months before and after each repowering, against the
  gain both halves of a plant showed in the same weeks.

## 3. The driving force

A strong solver calibrates the performance ratio on metered output, notices that for 18 months the meter also carried a neighbouring
array, and removes it. For the repowering it reads the vendor's yield report, which models this plant's inverters and promises 35%. It
may then check the promise against the operator's five earlier repowerings: before and after, they gained 33% on average. Every one of
those was done in March or April, so its "after" months had longer days and its comparison is a season, not a repowering. The change
log's commissioning records hold the clean measurement. At each plant the contractor repowered one half first and ran it beside the
untouched half for eight weeks. Under the same sun the new half produced 21.6% to 22.4% more, flat across irradiance levels, because the
original inverters clip the new modules' extra midday power. Applied to every weather year, that gain sets the 2027 one-year P90 at
119,503 MWh.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The memo's one-year P90 with the ratio calibrated on the revenue meter, the new modules at their nameplate ratio to the old (+40%) | 149,000 MWh, +25% | The filed method on the plant's own settled output, the new modules as rated | **E19 (a latent attribution marker):** for 18 months the meter reading exceeds plant SCADA by exactly the neighbour array's SCADA, and the utility settled those months by that split |
| 1 | The same with the neighbour's energy removed from those months | 137,000 MWh, +15% | Clean calibration, every month tied to settlement | The vendor's yield report: modelled on this plant's inverters, the gain is 35% |
| 2 | The vendor's modelled gain (+35%) | 132,000 MWh, +11% | A plant-specific engineering estimate, and the earlier repowerings' before-and-after average (+33%) roughly agrees | The change log's commissioning records: each earlier repowering ran a new half beside an old half for eight weeks, and the new half produced 22% more every time |
| 3 | **Decisive:** the side-by-side gain (+22.0%) applied to every weather year's energy, then the one-year P90 | **119,503 → 119,000 MWh** | — | — |

* **Figure shape.** Every correction lowers the volume (+25%, +15%, +11%), and the answer is the smallest cell of the grid, so every
  partial application over-sells.
* **Partial correction priced (L3).** Measuring the gain from the earlier repowerings but before and after, as an event study does,
  gives +33% and 130,000 MWh (+9%). Taking the side-by-side gain on the uncorrected meter calibration also gives 130,000 MWh (+9%).
* **Grid.** Calibration (meter as recorded, neighbour removed) × gain (nameplate, vendor model, before and after, side by side) gives 8
  cells, from 130,000 to 149,000 MWh outside the answer. The nearest wrong cells sit 9% away, each one step from it.
* **Licensed basis, priced.** The lender's ten-year P90 on the vendor's gain gives 143,000 MWh, +20%.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The vendor's report gives its gain and the memo its method. No document says the earlier repowerings ran side by
   side or that spring timing biases a before-and-after reading; the commissioning records ship as acceptance paperwork.
2. **The reproduction numbers.** The side-by-side gain reproduces all five commissioning periods within half a point; the vendor's 35%
   and the event-study 33% miss all five high. The measurement is a construction: each period's paired halves joined to its own
   irradiance, not a parameter on the production history.
3. **No arithmetic symptom.** Every year's output ties to settlement, the irradiance record to the station, and the P90 to the sample
   standard deviation the memo names, under every rung.
4. **Not a row predicate.** The gain is a ratio between two halves of a plant over the same weeks, built from SCADA by block and the
   commissioning records' split, then applied to 25 synthetic weather years.
5. **The enumeration is arithmetic.** Which months and blocks form each side-by-side period comes from the commissioning records'
   dates and block lists. No column marks them.
6. **No cutover date carries the answer.** Each repowering is dated, and aligning on those dates is the event study, which is the decoy;
   the answer needs the weeks when old and new ran together.
7. **Survives deletion.** No wrong number exists to delete. Without the voices, rung 2 is where a careful build stops.

## 6. The calibration corpus

* **Form.** The five earlier repowerings' side-by-side periods: eight weeks each, block-level SCADA for the repowered and original
  halves, the irradiance at each plant, and the commissioning record naming which blocks were done first.
* **What it certifies.** The gain on existing inverters: 21.6% to 22.4% across the five, flat across irradiance bins within 0.5%, so it
  scales every weather year's energy alike.
* **What it pins against.** The event study on the same five plants: +18% to +45%, averaging 33%, because each "after" window sits in a
  sunnier season than its "before".
* **Twin pair.** Repowerings R-2 and R-4 are identical on every change-log column: plant size, module and inverter models, latitude and
  completion month. Their before-and-after gains were 44% and 22% (2.0×), because R-2's following spring was the sunniest in a decade.
  Side by side, both gained 22%.
* **Resemblance points at the decoy.** This plant matches R-2 on every change-log column, the repowering whose before-and-after gain was
  largest.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The desk memo: the forward volume is the one-year P90 of next year's energy, from 25 weather years, a performance
  ratio calibrated on the last five years of metered output and the sample standard deviation, rounded down to 1,000 MWh. The asset plan:
  modules replaced on the existing racking and inverters, finished in December. The interconnection agreement: the neighbour's array may
  export through the plant's meter while its own is out of service.
* **Empirical pins.** The neighbour's share of the bypass months, from the two SCADA feeds. The gain, from the side-by-side periods.
* **Voices.** The asset manager: "New modules are rated 40% higher; the plant will make 40% more." The trading head: "The vendor
  guarantees thirty-five. That's the number we hedge."
* **Licensed wrong basis.** The memo records that the plant's lender sizes its covenant on a ten-year P90 and will present that figure in
  its annual review.

## 8. Determinism by construction

* **Gain.** Every value in the five periods' 21.6–22.4% range gives a P90 between 119,111 and 119,894 MWh, so the rounded volume is
  119,000 under any averaging of the five.
* **Form.** The side-by-side ratio is flat across irradiance bins, so the gain multiplies each weather year and the P90 scales with it.
* **Bypass months.** Meter less plant SCADA equals the neighbour's SCADA to the kilowatt-hour in each of the 18 months and is zero in
  every other month, so the assignment is exact.
* **Degradation.** The new modules' first-year degradation is inside the side-by-side gain, since each period compared new modules with
  aged ones, as here.
* **Maturity.** The repowering finishes before the delivery year, so all of 2027 runs on the new modules.

## 9. Prompt sketch and deliverables

> We sell next year's output forward this month and I need the volume we are 90% sure the plant will deliver, rounded down to the nearest
> thousand megawatt-hours. Our trading head wants to hedge on the vendor's guarantee. Send `forward_volume.xlsx`, a chart
> `repowering_gain.png`, and a one-page `hedge_note.pdf` that commits to the volume.

* `forward_volume.xlsx` — the P90 build under each construction, the availability sheet (ask A) and the curtailment sheet (ask B).
* `repowering_gain.png` — the five earlier repowerings' gains as paired bars (before-and-after against side-by-side), the vendor's 35% as
  a line, an inset of one side-by-side period's daily ratio, and the 25 weather years' 2027 energy as a histogram with P50 and P90 marked.
* `hedge_note.pdf` — the committed volume, the gain behind it, and the lender's basis.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each month of last year, the plant's availability: the share of block-hours producing
  while irradiance exceeded 50 W/m². *Device:* a block restarted after a trip posts a second "available" event under the same event ID
  with a restart flag, and the O&M contract runs an outage from the first fault to the final restart. Reading the first event as the
  restart understates outages in four months.
* **Ask B (device-carried).** For each quarter of the last two years, the curtailment the grid operator ordered and the energy it cost.
  *Device:* an order revised mid-event posts as a new row carrying the original order number and a revision flag, and settlement counts
  the event once at its revised cap. Summing rows double-counts revised events in three quarters.
* **Ask C (validity).** The volume under each of the four rung constructions, with each one's reproduction of the five side-by-side
  periods.
* **Decoupling.** Replacing the side-by-side gain with the vendor's changes no figure in asks A or B.

## 11. Rubric arithmetic

12 months × 2 (ask A) + 8 quarters × 2 (ask B) + 4 constructions × 2 (ask C) + the committed volume, the gain and the bypass correction
+ 5 named chart parts + 3 files ≈ 59 criteria.

## 12. World-building constraints

* Present plant: P50 110,000 MWh and σ 9,400 across 25 weather years; one-year P90 97,953 MWh. The bypass months raise the calibrated
  ratio by 9%.
* Gains: nameplate 40%, vendor model 35%, before-and-after average 33% (18–45%), side by side 22.0% (21.6–22.4%).
* Volumes: 149,000 / 137,000 / 132,000 / 119,000 MWh; partial cells 130,000 and 130,000; lender's basis 143,000.
* R-2 and R-4 are identical on every change-log column; this plant matches R-2.
* Restart events and revised curtailment orders never touch the meter history, SCADA energy or the commissioning records.

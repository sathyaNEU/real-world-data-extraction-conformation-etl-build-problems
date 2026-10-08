# FC09 — The district's water order for next season, when canal losses are paid per refill and not per acre-foot delivered

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Economics · agricultural water management |
| Mirrors | Ordering gross supply when the overhead is paid per dispatch and shared by every line the dispatch serves (pipeline line-fill in fuel distribution, empty repositioning on Amazon milk runs, warm-up energy per batch in data-centre cooling plants) |
| Decision shape | One figure committed at a date: the headgate order placed with the water project |
| Committed call | Next season's headgate order in acre-feet, rounded up to the next 100 AF, placed by 1 February |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · Pattern B, the loss law recovered from closed water balances as a mixture (fill per refill plus seepage per wetted day), with a unit the acreage file does not store |
| Gate G mechanism | method_or_model_selection, with forecasting support |
| Measured traps engaged | #2 counts file rows instead of the real unit · #3 stops at a close but inexact match · #4 never tests its reading against the control |
| Calibration form | Prior-period close-out: thirty audited seasonal water balances by lateral (diversion, turnout deliveries, losses), 270 cells |
| Driving force | A lateral that sits dry for more than four days must be refilled before its next delivery, and the refill water is lost. So a season's loss is a fixed fill per refill plus seepage per wetted day, and a loss rate per acre-foot is a mixture that depends on how deliveries cluster. Refills appear in no column; they come from grouping each lateral's deliveries at the one dry-out gap that reproduces all 270 closed balances exactly. The order is set by a dry season, when laterals stay wet and the loss share falls to 8%, against a 20% average. |

## 1. Situation

An irrigation district places its headgate order with the state water project by 1 February. The operations memo sets the order at the
80th percentile of the seasonal headgate requirement across thirty replayed weather seasons, rounded up to the next 100 AF, and it
specifies the daily soil-water model for each crop. Nine laterals carry water from the headgate to 412 farm turnouts. Every season's water
balance is closed and audited by lateral.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the weather, the crop reports, the parcel file, the delivery ledger and the audited close-outs. No
  one's claim about their own numbers is overturned. The difficulty is the unit of crop demand and the form of a loss that every closed
  balance reports correctly.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the project's check basis. The replay on split crop-acres with the latest audited loss rate
  is still the careful build, and it still orders 19% too much.
* **Instrument repair.** Suspect: the parcel file, which records one crop per parcel where 10,850 acres carry two. Record every crop
  season. Rung 0 then returns rung 1's 50,600 AF and rung 2 still 52,600 AF; no constant loss rate reproduces the close-outs, so the
  refill mixture is still needed for 44,100.
* **Lens swap.** The naive read and the answer differ in moment: last season's wet-year loss rate against a dry season in which laterals
  never dry out.

## 3. The driving force

A strong solver replays thirty seasons day by day, finds that the parcel file lists one crop per parcel while 10,850 acres carry winter
wheat and then summer corn, and grosses the farm requirement up for canal losses. The close-outs give a loss rate: 20% on average and
23% last season, rising as drip orchards spread. Every figure is right and the rate is the wrong object. A lateral that sits dry for more
than four days soaks up about 51 AF before it carries water again, and while wet it seeps steadily. Loss per acre-foot therefore depends
on how often deliveries let laterals dry out. Wet seasons with scattered orders refill often; dry seasons with continuous orders refill
almost never. The 80th-percentile season is dry, and its loss share is 8%. Refills are nowhere in the ledger. They are runs of deliveries
on a lateral split wherever the gap exceeds four days, and only that gap makes all 270 close-outs balance to the acre-foot.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The memo's daily replay on the parcel file (one crop per parcel row), P80, grossed up at the 30-season average loss rate | 37,500 AF, −15% | The specified model, the district's own acreage, the district's own loss history | **E02 (the unit not stored):** growers' crop reports put two crops on 10,850 acres, and the county crop report's harvested acres match only crop-acres, not parcels |
| 1 | The same on crop-acres (double-cropped parcels split into two crop seasons) | 50,600 AF, +15% | Every acre's every crop is now demanded, and acreage ties to the county report | The close-outs: the loss rate has climbed from 17% to 23% over five seasons |
| 2 | The same at the latest audited loss rate (23%) | 52,600 AF, +19% | The most recent audited balance on a complete replay | The close-outs by lateral and season: no constant rate per lateral reproduces any season exactly, and losses track the number of times a lateral was refilled |
| 3 | **Decisive:** each lateral's loss as fill × refills + seepage × wetted days (refills found by a four-day dry-out gap), computed on every replayed season's daily deliveries, then P80 of headgate totals | **44,022 AF → 44,100** | — | — |

* **Figure shape.** Rung 0's two errors pull opposite ways and leave it 15% low. The next two corrections walk the figure up (+15%,
  +19%), and the decisive rung reverses them, because the season that sets the 80th percentile is the one with almost no refills.
* **Partial correction priced (L3).** A solver who adopts the fill-plus-seepage law but applies the close-outs' average refill count,
  instead of counting refills in each replayed season, gets an 18% loss share and 49,400 AF (+12%). The same law on parcel rows lands at
  32,600 AF (−26%).
* **Grid.** Acreage (parcel rows, crop-acres) × loss (average rate, latest rate, mixture with average refills, mixture with replayed
  refills) gives 8 cells. The nearest wrong cell is parcel rows at the latest rate (−11.5%), which needs two errors pulling opposite ways.
  Every single-error cell is at least 12% away.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The memo defines the soil-water model and the percentile. The close-outs report losses. No document says what a
   loss is made of, or that laterals must be refilled.
2. **The reproduction numbers.** With a four-day gap, fill plus seepage fitted per lateral reproduces 270 of 270 close-out cells to the
   acre-foot. A three-day gap reproduces 188, a five-day gap 201, and the best constant rate per lateral none. The constant rate errs low
   in every season with frequent refills and high in every season with few, so it fits the 30-season total and no season. The rule is a
   construction: runs built by grouping and ordering deliveries per lateral. The gap is not a stand-alone parameter, because it only means
   something inside that grouping.
3. **No arithmetic symptom.** Every close-out balances, deliveries tie to turnout meters, and crop-acres tie to the county report under
   every rung.
4. **Not a row predicate.** Refills are a property of a lateral's delivery sequence: deliveries mapped to laterals through the parcel map,
   ordered in time and split at gaps, then priced per run.
5. **The enumeration is arithmetic.** How many refills each replayed season needs is computed from its simulated daily deliveries. No
   column holds it.
6. **No cutover date.** Loss shares move with weather and ordering patterns, season by season, and no series steps.
7. **Survives deletion.** No wrong number exists to delete. Without the voices, rung 2 is where a careful build stops.

## 6. The calibration corpus

* **Form.** Thirty audited close-outs by lateral: each season's diversion into each lateral, deliveries at its turnouts and the loss
  between, with the delivery ledger beneath them.
* **What it pins (Pattern B).** The loss law and its per-lateral constants (fill 38–64 AF per refill, seepage 0.9–2.2 AF per wetted day).
  Its total certifies a 20% average, which is why rungs 0–1 feel confirmed.
* **Twin pair.** Lateral 5's 2009 and 2016 seasons are identical on every column a lookup can see: 3,410 AF delivered, the same crop mix,
  ETo, rain and wetted days. Their losses were 1,020 and 510 AF (2.0×), because 2009's deliveries let the lateral dry out sixteen times
  and 2016's six. No rate reproduces both; fill plus seepage does.
* **Resemblance points at the decoy.** By crop mix the coming season most resembles the last two close-outs, the highest-loss seasons in
  the file.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The operations memo: the order is the 80th percentile of seasonal headgate requirement across thirty replayed seasons,
  rounded up to 100 AF, with the daily soil-water model and crop coefficients it lists. The crop reports: each grower's crops by parcel and
  season. The parcel map: each parcel's lateral.
* **Empirical pins.** The four-day gap and each lateral's fill and seepage constants, from the close-outs. Crop-acres, through the county
  report's harvested acres.
* **Voices.** The district engineer: "Twenty per cent losses is what this system has always run." The board chair: "Drip orchards are
  only going to push our losses up."
* **Licensed wrong basis.** The memo records that the project's contracts office checks every district order against the district's
  five-year average loss rate and will present that check at the order review.

## 8. Determinism by construction

* **Gap convergence forward.** In the 80th-percentile replay season every gap between deliveries on a lateral is at most two days or at
  least nine, so any gap from three to eight days counts the same refills. The corpus needs four, but the order would not move under any
  gap in that range.
* **Percentile.** Thirty seasons with inclusive interpolation, as the memo states. The 80th-percentile headgate total falls between two
  dry seasons whose refill counts are both zero or one per lateral.
* **Double crops.** Each double-cropped parcel's two crop seasons do not overlap, so the split is exact.
* **Turnout mapping.** Every parcel maps to one lateral, and no turnout serves two laterals.
* **Maturity.** All thirty close-outs are audited and final, and the delivery ledger is complete for each.

## 9. Prompt sketch and deliverables

> I place our water order with the project by 1 February, and I'll put in whatever you give me, rounded up to the next hundred acre-feet.
> Our district engineer says we should keep grossing up at the losses this system has always had. Send me `water_order.xlsx` with the
> build, a chart `lateral_losses_refills.png`, and a one-page `order_note.pdf` that commits to the figure.

* `water_order.xlsx` — the replay and order build, the meter sheet (ask A) and the order-change sheet (ask B).
* `lateral_losses_refills.png` — closed-season losses against refills for each lateral (one panel per lateral), the fitted fill-plus-
  seepage lines, the 80th-percentile replay season marked, and the twin seasons annotated.
* `order_note.pdf` — the committed order, the season that sets it, and the bases the project's contracts office will raise.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each lateral, the number of turnout meters outside ±5% at last winter's calibration and the
  median deviation. *Device:* a replaced meter gets a new meter ID, and the asset register links old and new IDs to the same turnout.
  Keying on meter ID double-counts 31 turnouts and splits their deviations across two rows.
* **Ask B (device-carried).** For each lateral, delivery orders cancelled within 24 hours of their start last season, and the share of
  orders affected. *Device:* the scheduling system records a changed start time as a cancel-and-rebook pair sharing a chain ID, as its
  dictionary documents. Counting cancellations overstates true cancellations threefold on two laterals.
* **Ask C (validity).** The order under each of the four rung constructions, with each construction's hits on the 270 close-out cells.
* **Decoupling.** Replacing the fill-plus-seepage law with a constant rate changes no figure in asks A or B.

## 11. Rubric arithmetic

9 laterals × 2 (ask A) + 9 laterals × 2 (ask B) + 4 constructions × 2 (ask C) + the committed order, the season that sets it and its
loss share + 5 named chart parts + 3 files ≈ 55 criteria.

## 12. World-building constraints

* 31,000 parcel acres carry 41,850 crop-acres (10,850 acres double-cropped). The farm requirement at P80 is 30,000 AF on parcel rows and
  40,500 AF on crop-acres.
* Loss share: 20% over thirty seasons, 23% last season, 8% in the 80th-percentile replay season.
* Rung figures 37,500 / 50,600 / 52,600 / 44,022 AF. Partial cells 49,400 and 32,600 AF. No single-error cell is within 12%.
* Each lateral's fill (38–64 AF) and seepage (0.9–2.2 AF per wetted day) reproduce all 30 seasons at a four-day gap only.
* Meter replacements and rebooked orders never touch deliveries, crop reports or close-outs.

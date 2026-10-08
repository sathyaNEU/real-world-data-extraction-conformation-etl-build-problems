# DS35 — Which twelve business clients get the retailer's peak-shaving batteries, when a billing period's peak is set by every day in it

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Economics · business electricity services |
| Mirrors | Placing scarce buffers to shave a capped peak where the biggest overage is the least shaveable (data-centre batteries against demand charges at hyperscalers, burst credits on cloud instances, safety stock that only covers short spikes in fulfilment networks) |
| Decision shape | An allocation under a cap: twelve batteries among twenty clients, one per client |
| Committed call | The twelve clients who get a battery, and the excess-demand penalties the placement avoids next year, in € thousands |
| Gap · Pattern | Gap 3 (objective) over Gap 2 (population) · S5, a cap that does not commute (a billing period's maximum is a maximum over days, so a shave applied to the peak day does not shave the period), with the billing-period unit (E02) at rung 1 |
| Gate G mechanism | binding_constraint, with decomposition_attribution |
| Measured traps engaged | #13 validates on one population, applies to another · #2 counts file rows instead of the real unit · #20 leaves the deciding comparison unstated |
| Calibration form | Settled-transaction ledger: two years of the twenty clients' settled network bills, one line per client per billing period, with contracted power, recorded maximum and penalty |
| Driving force | A battery holds one demand threshold for the billing period, and the period's penalty is set by its highest 15 minutes on any day. The threshold therefore has to hold on every day, each within the battery's 200 kWh, and the clients paying the biggest penalties have plateaus that recur day after day. A 100 kW battery takes 100 kW off a single spike and barely 18 kW off a plateau. |

## 1. Situation

An electricity retailer is launching a peak-shaving service: it owns twelve batteries (100 kW, 200 kWh usable each) and will place them at
twelve of the twenty business clients on its advisory book, one per client, in January. Each client pays the network operator an
excess-demand penalty of €19.50 per kW by which its highest 15-minute demand in a billing period exceeds its contracted power, and the
contracts for next year are already signed. The account team believes the clients paying the largest penalties will save the most. The
launch figure is the penalties the placement avoids.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the 15-minute loads, the billing register, the settled bills, the battery datasheet and the
  controller's specification. No stakeholder read is overturned: the account team's clients really do pay the largest penalties. The
  difficulty is how much of a penalty a battery can actually remove.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the account team's view and the board's basis. Ranking clients by the penalty a 100 kW battery would remove
  still names the plateau clients first.
* **Instrument repair.** Meter every client at one-second resolution. The plateaus are still plateaus and still recur on many days; a finer
  instrument changes no client's shaveable share.
* **Lens swap.** The naive read and the answer differ in population and moment: the peak 15 minutes that set last year's penalty, against
  every day of next year's billing periods, each of which can set the shaved maximum.

## 3. The driving force

A strong solver cleans the load data, rebuilds each billing period from the read dates, reproduces the settled penalties, and values a
battery as the penalty it removes. The obvious valuation takes 100 kW off each period's maximum, up to the excess. A careful one adds the
battery's energy: on the peak day, the deepest threshold the 200 kWh can hold. Both rank clients by their penalties, and both are wrong in
the same way. The controller holds one threshold for the billing period and discharges whenever demand exceeds it, recharging overnight.
Shaving the peak day only exposes the next-highest day, so the period's maximum after shaving is the lowest threshold every day of the
period can hold within 200 kWh. For a cold store whose compressors plateau for three hours on twenty days a month, that threshold sits 18
kW below the old maximum. For a press shop whose peaks are single 15-minute spikes, it sits 100 kW below. The largest penalties belong to
the plateau clients.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Raw loads by calendar month; each battery removes up to 100 kW of each month's excess; top twelve by penalty removed | €221k (+87%), led by the cold stores | The tariff's own arithmetic on the largest penalty payers | The settled bills: a raw calendar-month rebuild misses 85 of 480 settled lines |
| 1 | Hygiene and unit: loads cleaned of the clock-change artefacts (zeros in the March hour, the doubled October hour), penalties rebuilt per billing period from the read dates; power-limited value | €196k (+66%) | Every settled line reproduced exactly, so the valuation rests on the real penalty | The battery datasheet: 200 kWh usable, so a 100 kW discharge lasts two hours |
| 2 | Energy-limited value: on each period's peak day, the deepest threshold 200 kWh can hold | €163k (+38%) | A proper battery model, energy and power both respected | The controller specification: one threshold for the billing period, discharging whenever demand exceeds it, recharging overnight |
| 3 | **Decisive:** each period's lowest threshold that every day can hold within 100 kW and 200 kWh; value is the penalty above that threshold removed; top twelve | **€118k, twelve clients led by three press shops** | — | — |

* **Figure shape.** Every correction walks the figure down, and the answer is the minimum cell of the grid.
* **Position table.** The five clients who enter only at rung 3 rank 13th to 19th by penalty on rung 0. The press shop that leads the
  answer is 17th on rung 0, 15th on rung 1 and 9th on rung 2. The three cold stores that lead rungs 0 to 2 fall to 14th, 16th and 18th.
* **Discriminator dominance.** The largest cold store carries a 2.6× penalty advantage over the leading press shop into rung 3. Its
  shaveable share is 0.18 against the press shop's 0.91, an edge of 5.1×, more than 1.2 × 2.6 = 3.1.
* **The deciding comparison (#20).** The cold store's €2.9k of avoidable penalty against the press shop's €5.6k is what the launch note
  has to state; neither client's penalty bill shows it.
* **Partial correction priced (L3).** Holding the threshold on the top two days of each period files €141k (+19.5%). Holding it every day
  but ignoring the 100 kW power limit lets the spiky clients shave their whole spikes and files €151k (+28.0%). Half the construction
  stays well above the answer.
* **Grid.** Data (raw, cleaned) × period (calendar month, billing period) × battery model (power, peak-day energy, every-day threshold) = 12
  cells. Only cleaned data, billing periods and the every-day threshold give €118k; the nearest other cell is cleaned calendar months with
  the every-day threshold at €131k (+11.0%).

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The datasheet gives power and energy, the controller specification gives the threshold rule, and the tariff gives
   the penalty. No document says the period's shaved maximum is set by the worst day, or which clients are plateaus.
2. **Corpus blind for a computable reason.** *No client had a battery in any settled period, so every settled line records an unshaved
   maximum, and the ledger is the same under every battery model.* It certifies the penalty, the billing period and the cleaning exactly.
3. **No arithmetic symptom.** Loads reconcile to the settled maxima, penalties to the ledger, and every battery model returns a feasible,
   positive saving.
4. **Not a row predicate.** The threshold is a search per client and billing period over every day's load curve, with each day's energy
   above the threshold summed and tested against 200 kWh.
5. **The enumeration is arithmetic.** Which clients are plateaus is computed from the shape of their days; no column records a load shape.
6. **No cutover date.** No series steps; the batteries act on next year's periods.
7. **Survives deletion.** No wrong number exists to delete. Without any voice, ranking by penalties still names the cold stores.

## 6. The calibration corpus

* **Form.** Two years of settled network bills: per client and billing period, the contracted power, the recorded 15-minute maximum and the
  excess penalty, 480 lines.
* **What it certifies.** Rung 1: cleaned loads rebuilt on billing periods reproduce 480 of 480 lines to the cent. Calendar months miss 61
  lines, and uncleaned October data a further 24, every miss overstating the penalty, so both rivals also miss the ledger total, by 6.1%.
* **What it is blind to.** Shaving (above).
* **Twin pair.** Clients 07 and 14 are identical on every ledger column: 400 kW contracted, the same 24 recorded maxima and the same
  penalties, €14.6k a year. With a battery, client 14 avoids €11.2k and client 07 €5.6k (2.0×): client 14's maximum came from one day in
  each period, client 07's recurred within 15 kW on six to nine days. Only the every-day threshold separates them.
* **Resemblance points at the decoy.** By sector and contracted power, the largest cold store most resembles the client whose demand
  response saved most last year.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The network tariff: excess penalty of €19.50 per kW of the billing period's highest 15-minute demand above contracted
  power. The billing register: each client's read dates. The battery datasheet: 100 kW, 200 kWh usable. The controller specification: one
  demand threshold per billing period, discharge whenever demand exceeds it, full recharge overnight. The service charter: batteries go
  where they avoid the most penalty, one per client.
* **Empirical pins.** The billing-period unit and the clock-change cleaning, both fixed by reproducing every settled line.
* **Voices.** The account director: "The clients paying the biggest penalties will save the most." The battery product manager: "A 100 kW
  unit takes 100 kW off the peak; that's what it's for." The energy-services analyst: "Cold stores are our best demand-response sites."
* **Licensed wrong basis.** The charter records that the board's investment committee reviews the launch on each client's penalties paid
  last year and will see that table.

## 8. Determinism by construction

* **Threshold search.** Thresholds are searched to the kilowatt; every client's binding day leaves at least 6 kWh of slack against
  200 kWh at the chosen threshold and exceeds it one kilowatt lower.
* **Recharge.** Overnight demand at every client stays at least 60 kW below its contracted power, so recharging at 50 kW never sets a new
  maximum.
* **Clock changes.** The March gap is interpolated and the October hour split, per the dataset notes; neither day holds a binding peak for
  any client.
* **Placement.** Clients are independent, so the top twelve by value is the optimum; the 12th and 13th clients differ by €0.9k.

## 9. Prompt sketch and deliverables

> Our twelve peak-shaving batteries go out to clients in January, and the account team has twenty on the list. They believe the clients
> paying the biggest excess penalties will save the most. Tell me which twelve get a battery and the penalties the placement avoids next
> year, in € thousands, as the figure for the launch. Send `battery_placement.csv`, a chart `peak_shaving_days.png`, and a one-slide
> `launch_note.pptx`.

* `battery_placement.csv` — the twenty clients with penalties paid and avoidable penalty under each battery model (ask C), plus the
  reactive-energy rows (ask A) and the band rows (ask B).
* `peak_shaving_days.png` — for the twin clients and the largest cold store, each billing period's daily peaks as dots, with the old
  maximum, the peak-day threshold and the every-day threshold drawn as labelled lines, and each client's avoidable penalty annotated.
* `launch_note.pptx` — the twelve clients, the €118k figure, and why the biggest payers are not first.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the twenty clients, last year's reactive-energy charge. *Device:* the meter export
  carries inductive and capacitive registers, and the tariff charges only inductive reactive energy above a tan φ of 0.3 per billing
  period. Charging both registers, or charging without the allowance, overstates every client with capacitor banks.
* **Ask B (device-carried).** For each of the twelve billing periods, the portfolio's energy by tariff band (peak, shoulder, off-peak).
  *Device:* the tariff's calendar annex bills public holidays as off-peak all day. A weekday rule misbands eleven holidays.
* **Ask C (validity).** For each of the twenty clients, the avoidable penalty under the power-limited and every-day-threshold models.
* **Decoupling.** Clearing the every-day threshold changes no figure in asks A or B. Reactive registers and the holiday calendar touch no
  demand maximum or battery record.

## 11. Rubric arithmetic

20 clients (ask A) + 12 periods × 3 bands (ask B) + 20 clients × 2 models (ask C) + the twelve clients, the €118k figure and the margin at
the twelfth place + 5 named chart parts + 3 files ≈ 118 criteria.

## 12. World-building constraints

* Rung figures €221k / €196k / €163k / €118k. Partial cells €141k and €151k; the nearest grid cell €131k.
* Three cold stores and two food processors plateau for at least two hours on at least 15 days a period; three press shops and two
  bakeries spike for one or two intervals on one or two days. The plateau clients pay the five largest penalties.
* Clients 07 and 14 match on all 24 settled lines.
* No battery operated at any client in the settled years. Reactive registers and holidays are independent of every main-call record.

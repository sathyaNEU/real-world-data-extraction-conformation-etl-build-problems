# FC01 — The contracted demand for a garage's new charging service, when the faster pedestals meet cars that cannot use them

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Supply Chain & Logistics · EV charging infrastructure and power procurement |
| Mirrors | Committing a power reservation for hardware whose draw is set by the device plugged in, not by the socket (data-centre rack power commitments when servers draw below the PDU rating, GPU cluster power envelopes, depot charging for electric delivery-van fleets at Amazon-scale logistics operators) |
| Decision shape | One figure committed at a date: the contracted on-peak demand filed with the utility for the new service |
| Committed call | The contracted demand, in kW rounded to the nearest 5 kW, for the Civic Center decks' new charging service, filed by 1 March |
| Gap · Pattern | Gap 1 (time) over Gap 2 (population) · S4, the forward window generated under a regime the closed window never reached, with L1 (the corpus certifies the shallow rungs and is blind to the decisive one) |
| Gate G mechanism | forecasting, with method_or_model_selection |
| Measured traps engaged | #13 validates on one population, applies to another · #14 coarsens the segment it was asked about · #7 uses the ready-made measure |
| Calibration form | Settled-transaction ledger: 36 months of settled charging sessions at the eight municipal garages, each with its 15-minute interval energy readings |
| Driving force | In every closed session a car drew exactly the pedestal's 6.6 kW, so "a session draws the port rating" reproduces every closed month. The new pedestals are rated 11.5 kW, and what a session draws on them is the smaller of the rating and the car's onboard limit, a property of the vehicle three joins away. Most permit holders' cars stop at 7.2–7.7 kW, so their charging runs past noon into the billed window instead of finishing before it. |

## 1. Situation

The city's parking division runs Level 2 charging in eight garages. The two permit-only decks at Civic Center (32 pedestals at 6.6 kW)
reach end of life this winter and will be replaced by 32 pedestals rated 11.5 kW on a new dedicated utility service. The utility needs a
contracted demand for that service by 1 March. A month whose billed demand exceeds the contract is ratcheted for a year, and every
contracted kilowatt carries a fixed monthly charge, so the division signs the figure it forecasts for the year's maximum billed demand.

## 2. Gate G: why this is legal

* **Litmus.** Every number in the pack is correct: the settled sessions, their interval readings, the operator's peak report, the permit
  registry and the state's vehicle list. No one's claim about their own figures is overturned. The difficulty is that a session's draw on
  equipment that does not exist yet is not the draw the closed record shows.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the operator's peak report and both voices. The interval ledger still certifies "draw = port rating" in every
  closed month, and a replay at 11.5 kW is still the natural sophisticated build.
* **Instrument repair.** Make every meter and every settlement perfect; they already are. No better instrument of the past observes how a
  7.2 kW car behaves on an 11.5 kW pedestal that has never been installed.
* **Lens swap.** The naive read and the answer differ in moment and regime: the permit base's sessions on 6.6 kW pedestals last year
  against the same base's sessions on 11.5 kW pedestals next year.

## 3. The driving force

A strong solver distrusts the dashboard, reads the tariff, rebuilds the on-peak maximum from interval data and then does the careful
thing: it replays each closed session on the new pedestals. The ledger certifies how a session behaves (full rating until its energy is
delivered, then nothing) in all 36 closed months, so the replay feels proven. At 11.5 kW commuters arriving before 09:30 finish before
11:30, and the billed window, which opens at noon, looks nearly empty. But the rating was never the binding limit; it only looked that way
because every closed pedestal was slower than every car. On the new pedestals the binding limit is the car's onboard charger, and 78% of
the decks' permit vehicles stop at 7.2 or 7.7 kW. Their sessions run about three hours, past noon, and stack into the first billed hour.
The limit is not a column on any session. It sits behind session → permit → registered model → the state list's charger rating.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The operator's monthly peak-kW report for the two decks, highest month, × the filed growth factor 1.12 × the rating ratio 11.5/6.6 | 373 kW, +148% | The division's standing peak report, scaled for growth and for the faster pedestals | The tariff's billing-demand clause counts only on-peak intervals (weekdays 12:00–20:00, listed holidays excluded) |
| 1 | **E18 (the segment coarsened):** the on-peak maximum rebuilt from the ledger's interval readings, × 1.12 × the rating ratio | 244 kW, +62% | The billed window, at the grain the tariff names, from meter-grade data | The interval readings show every session draws its full rating only until its energy is delivered, so faster pedestals end sessions sooner and empty the billed window |
| 2 | Session replay: each closed session redrawn at 11.5 kW until its delivered energy is reached, on-peak maximum × 1.12 | 116 kW, −23% | A session-level model the ledger reproduces to the kWh in all 36 closed months | The permit registry's vehicle models, read against the state list, cap 78% of the decks' cars at 7.2–7.7 kW |
| 3 | **Decisive:** replay at the smaller of 11.5 kW and each car's onboard limit, joined session → permit → model → limit, on-peak maximum × 1.12 | **150.4 kW → 150** | — | — |

* **Figure shape.** The three corrections walk the figure down (+148%, +62%, −23%) and the decisive rung turns it back up by 30%. A solver
  who stops anywhere short is wrong in a known direction.
* **Partial correction priced (L3).** A solver who learns that cars limit the draw but applies the fleet-average limit (8.2 kW) to every
  session lands at 110 kW (−27%), further away than rung 2. The maximum is driven by the slow cars that spill past noon, and an average
  hides them. Scaling the rung 1 peak by the average limit instead of replaying lands at 174 kW (+16%).
* **Grid.** Window (all hours, on-peak) × five draw constructions (rating-ratio scaling, average-limit scaling, replay at rating, replay at
  the fleet-average limit, replay at each car's limit) gives 10 cells: 373 / 266 / 283 / 239 / 238 all-hours and 244 / 174 / 116 / 110 /
  150.4 on-peak. The nearest wrong cell is average-limit scaling at +16%, which needs the vehicle insight without the replay; next are
  replay at rating (−23%) and the fleet-average replay (−27%). Each is one omission away, and none is within 16%.
* **Licensed basis, priced.** The utility's nameplate sizing (32 × 11.5 kW × its 0.6 diversity factor) gives 221 kW, +47%.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The pedestal specification gives 11.5 kW. No document says a session's draw is set by the car, and the state list
   ships because the permit office prices permits by vehicle class.
2. **Corpus blind for a computable reason.** *In every closed session at the decks the car's onboard limit was not binding, because every
   closed pedestal was rated 6.6 kW and every registered vehicle accepts at least 7.2 kW.* "Draw = rating" reproduces 36 of 36 closed
   on-peak maxima to the kWh.
3. **No arithmetic symptom.** Interval readings sum to session energy, sessions to the settled ledger, and the ledger to the deck meters,
   under every rung.
4. **Not a row predicate.** The figure is a maximum over on-peak intervals of a sum over concurrently charging sessions, each re-timed by
   its own car's limit through a three-hop join.
5. **The enumeration is arithmetic.** Which sessions are still charging at 12:30 is computed by re-timing. No column says so.
6. **No cutover date.** The pedestal swap is in the future, and no closed series steps.
7. **Survives deletion.** No wrong number exists to delete. Remove the report and the voices, and rung 1 becomes the natural start.

## 6. The calibration corpus

* **Form.** The settled ledger: every session at the eight garages over 36 months, with permit ID, plug-in and plug-out times, delivered
  energy and 15-minute interval readings.
* **What it certifies.** The session model behind rung 2: full rating until the delivered energy, then zero, in every closed session. The
  replay reproduces all 36 monthly on-peak maxima at both decks to the kWh.
* **What it cannot show.** Vehicle limits at the decks (above).
* **Free training instance (O3).** The Library garage has had one 11.5 kW pedestal for three years, used only by the enforcement unit's
  vans, whose chargers stop at 11.0 kW. Its sessions draw 11.0, not 11.5. The pattern is visible there and harmless, because the Library
  service is far below its contract. It is also the case that exercises the composition (the smaller of rating and limit).
* **Twin pair.** The North and South decks are identical on every ledger-visible column: 16 pedestals each, session counts, arrival,
  dwell and energy distributions, and closed on-peak maxima within 1 kW. Replayed on the new pedestals their on-peak maxima are 99.6 and
  50.8 kW (1.96×), because 92% of North's permits are an agency fleet of 7.2 kW cars and 64% of South's cars accept 11 kW.
* **Resemblance points at the decoy.** Next year's permit base resembles last year's within 2% on every count, and last year is the year
  the rating replay reproduces exactly.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The tariff: billing demand is the highest 15-minute demand in on-peak hours (weekdays 12:00–20:00, listed holidays
  excluded). The planning standard: forecast loads are the latest twelve closed months scaled by the county's EV registration growth
  factor, filed at 1.12. The service agreement: the new service feeds the two decks and nothing else. The permit rules: both decks are
  permit-only.
* **Empirical pins.** The session model, from the ledger. Each car's limit, from the permit registry and the state list. The composition
  of rating and limit, from the Library pedestal.
* **Voices.** The facilities engineer: "With the new pedestals everyone is topped up before lunch." The network operator's account
  manager: "Our peak report is what every city in the region sizes a service on."
* **Licensed wrong basis.** The utility's new-service guide records that its planners size EV services on connected nameplate times the
  utility's diversity factor and will present that sizing at the service review.

## 8. Determinism by construction

* **Interval labels.** The ledger labels intervals by their start, as its dictionary says. Every rung's on-peak maximum sits at least 30
  minutes inside the window, so either labelling convention returns the same maxima.
* **Departure.** Every closed session's plug-out falls at least two hours after its energy would be delivered at 7.2 kW, so no replayed
  session is cut short by departure, and delivered energy is unchanged by the draw.
* **Vehicle mapping.** Every deck permit maps to one registered vehicle, and no permit changed vehicle in the replay year. Roaming records,
  where they exist, give the same limits as the state list.
* **Coincidence.** Both decks' replayed maxima fall in the same 12:30 interval, so the coincident maximum equals the sum of the decks'.
* **Maturity.** Sessions settle within ten days of month-end, and the extract postdates the last month's settlement.
* **Rounding.** The unrounded answer is 150.4 kW, two kilowatts inside its 5 kW bin.

## 9. Prompt sketch and deliverables

> The utility needs our contracted demand for the Civic Center charging service by 1 March, and I will sign the figure you give me,
> rounded to the nearest 5 kW. Our facilities engineer is sure the new pedestals will have everyone charged before lunch. Send me
> `civic_service_demand.xlsx`, a chart `deck_load_day.png`, and a one-page `contract_demand_note.pdf` that commits to the number.

* `civic_service_demand.xlsx` — the demand build, the garage availability sheet (ask A) and the bill reconciliation (ask B).
* `deck_load_day.png` — the replay year's highest on-peak day at 15-minute grain, with three series (last year's actual load, the replay
  at rating, the replay at each car's limit), the on-peak window shaded, the contracted figure as a labelled line and the noon spill
  annotated.
* `contract_demand_note.pdf` — the committed figure, the deck split and the alternatives the utility will raise.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the eight garages, pedestal availability in the weekday 07:00–19:00 window over the
  last twelve months and the count of unplanned outages longer than two hours, worst first. *Device:* the status log posts planned
  firmware windows as offline events with a maintenance flag, which the operator's service agreement excludes from availability, and an
  outage spanning midnight posts as two rows. Counting every offline row understates availability at three garages and doubles outages at
  two.
* **Ask B (device-carried).** For each garage, ledger energy against utility-billed energy over the last four billing cycles, with the gap
  as a percentage. *Device:* bills run on meter-read cycles of 27 to 34 days with the read dates printed on each bill. Calendar-month
  matching shows phantom gaps of up to 18% at four garages; the true gaps are all under 3%.
* **Ask C (validity).** The contracted figure under each of the four rung constructions, with each construction's hits out of 36 closed
  on-peak maxima.
* **Decoupling.** Setting every draw back to the pedestal rating changes no figure in asks A or B.

## 11. Rubric arithmetic

8 garages × 2 (ask A) + 8 garages × 3 (ask B) + 4 constructions × 2 (ask C) + the committed figure, the deck split and the margin to the
nameplate sizing + 5 named chart parts + 3 files ≈ 59 criteria.

## 12. World-building constraints

* Every registered vehicle's onboard limit is 7.2, 7.7 or 11.0 kW, all above 6.6. 78% of deck vehicles are at 7.2–7.7 kW. North's base is
  92% an agency's 7.2 kW fleet; South's is 64% 11 kW-capable.
* Every closed session draws 6.6 kW until its delivered energy and then zero. The Library pedestal's sessions draw 11.0 kW.
* Rung figures are 373 / 244 / 116 / 150.4 kW. The fleet-average cell is 110 and the average-scaled cell 174. Every non-answer cell of the
  10-cell grid sits at least 16% from the answer.
* North and South are identical on every ledger-visible column; their replayed maxima are 99.6 and 50.8 kW in the same interval.
* Maintenance flags, midnight-split outages and bill read dates never touch deck sessions or permits.

# RC47 — How much of this winter's rise in home electricity is heating, when the heat pumps sit on supply points the hubs never see

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Product Analytics · smart-home energy service |
| Mirrors | Per-customer metrics at platforms where one customer's activity spans several accounts or devices and the second one is new this period (a household's second device or profile at Netflix and YouTube, a seller's second storefront on Amazon, a smart-home customer's second hub at Google Nest), so the like-for-like comparison drops the new one as a new customer and the change per household disappears |
| Decision shape | One figure committed at a date (a component): the weather-normalised rise in winter space-heating electricity per dwelling, given to the network partner for its reinforcement plan |
| Committed call | Heating added 330 kWh per dwelling this winter after weather, 280 of it from the 14,400 homes whose new heat pumps run on their own supply points |
| Gap · Pattern | Gap 2 (population) at the decisive rung, Gap 1 (time) at rung 1 · the unit the decision funds is not stored (measured #2): the partner plans per dwelling, the files hold supply points, and a dwelling with a heat pump has two, linked only by the installer's commissioning certificate; with the population a flag suggests (measured #5) at rung 1 |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection support |
| Measured traps engaged | #2 counts file rows instead of the real unit · #5 takes the population a flag or filter suggests · #13 validates on one population, applies to another |
| Calibration form | Gold-standard verification subsample: the service's engineer audit of 400 homes last spring, each home's circuits traced and its winter heating verified with clamp meters |
| Driving force | Space heating sits in each hub's unmetered remainder, and once movers are dropped and the colder winter is normalised the remainder rose by only 17 kWh per home. The engineer audit confirms that construction home by home. But the partner's heat-pump tariff runs every heat pump on its own supply point, registered at the meter cabinet's location code, with no hub on it. The like-for-like comparison drops those supply points as new connections, and the homes' main supply points show their old electric heating falling. Only the installer's commissioning certificate names the main supply point each heat pump serves. Built as dwellings, the 14,400 heat-pump homes added 2,300 kWh each, and heating rose 330 kWh per dwelling. |

## 1. Situation

A smart-home energy service has hubs on the main supply points of 120,000 homes. Each hub meters four fixed circuits and reports the
whole-home reading, so space heating, lighting and plug loads sit in the unmetered remainder. The network partner is planning reinforcement
for winter peaks and asks for one figure: how much winter space-heating electricity rose per dwelling, after weather. The service's
dashboard points at water heaters. Over the year the service's heat-pump partner installed heat pumps in 14,400 of the homes, each on its
own supply point under the partner's tariff, read by the partner and shared with the service.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct: the hubs' readings, the settlement reads on every supply point, the supply-point register,
  the weather record, the commissioning certificates and the audit. The dashboard's circuit figures are right, and the remainder really did
  rise little after weather. No one's reading of their own figures is overturned. The question is what a dwelling is.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the dashboard's advice and every voice. The audit still certifies the remainder construction, the like-for-like
  comparison still returns 17 kWh, and nothing in the hub data points at a second supply point.
* **Instrument repair.** Suspect: the hubs miss 1.8% of half-hours. Repair at every depth: every half-hour recorded, then a heating sub-meter
  on every hub, so heating is metered rather than read from the remainder. With the gaps filled, rung 0 returns 399, rung 1 199 and rung 2
  19. With heating metered, rungs 0 and 1 move by under 5 kWh and rung 2 reads 17, because the heat pumps sit on supply points no hub
  meters. None reaches 329. The continuing flag
  records an account's continuity and the location code records where a meter is; both are correct fields recording other attributes. A
  dwelling with two supply points is a unit no row records, so building it through the certificates is still needed.
* **Lens swap.** The naive unit is the supply point a hub sits on. The answer's is the dwelling, which for 12% of homes is two supply points,
  one of them new this year. These are different populations of load.

## 3. The driving force

A strong solver knows the dashboard's circuits leave out the heating, which sits in the remainder. It compares continuing accounts, then
drops the 7,500 that moved home between winters, because the supply-point register's dates show a different home behind the same account.
It normalises the colder winter with each home's degree-day model, which the engineer audit confirms within 3% in all 400 audited homes.
Heating rose 17 kWh per home. But the network partner plans per dwelling, and since the spring the heat-pump partner's tariff has put
every new heat pump on its own supply point. Those supply points are registered at the meter cabinet's location code, carry no hub and
have no previous winter, so the like-for-like comparison drops them as new connections. In the same homes the main supply points show the
old electric secondary heating falling by 300 kWh. The only record joining the two is the installer's commissioning certificate, which names
the main supply point each heat pump serves. Built as dwellings, the 14,400 heat-pump homes added 2,300 kWh each after weather, and heating
rose 330 kWh per dwelling.

## 4. The ladder

| Rung | Construction | Lands on (heating rise, kWh per dwelling) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Remainder change per continuing account, winter on winter | 397 (+21%) | The heating is in the remainder, and the continuing flag is the service's own like-for-like rule | The supply-point register's dates: 7,500 continuing accounts moved home between the winters |
| 1 | Remainder change per supply point connected through both winters, by the register's dates | 197 (−40%) | The same homes in both winters, by the register's own dates | The weather record: this winter had 21% more heating degree-days |
| 2 | Each home's degree-day model fitted on last winter, the change normalised to last winter's weather | 17 (−95%) | Like for like and weather-normalised, and the audit confirms the construction in 400 of 400 homes | The commissioning certificates: 14,400 homes had a heat pump commissioned on its own supply point between the winters |
| 3 | **Decisive:** dwellings built by joining each heat-pump supply point to the main supply point its certificate names, each normalised, the dwelling's change averaged | **329** | — | — |

* **Figure shape.** The corrections walk the figure down from 397 to 17, and the decisive move reverses them to 329. Offsets from the answer
  are +68, −132 and −312.
* **Partial correction priced (L3).** A solver who finds the heat-pump supply points but counts them as new homes, rather than joining them,
  divides the same load across 134,400 units and lands at 294 (−11%). One who joins them but leaves the heat pumps' readings at this
  winter's weather lands at 365 (+11%). Neither half lands within 10% of the answer.
* **Grid.** Population (continuing flag, register dates) × weather (raw, normalised) × unit (supply point, heat pumps as new homes,
  dwelling) gives 12 cells. The nearest wrong cells are the two partials, each 11% away. Every other cell is at least 21% away.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The partner's planning standard defines a dwelling as a self-contained home. The tariff terms put a heat pump on its
   own supply point. No document says a dwelling can hold two supply points, or that the certificates join them.
2. **Corpus blind for a computable reason.** *In every audited home all of the heating ran through the main supply point, because the audit
   visited homes last spring, before the heat-pump tariff took its first customer, so a home and its main supply point were the same thing.*
   The audit certifies rung 2's construction in 400 of 400 homes.
3. **No arithmetic symptom.** Each hub's whole-home reading reconciles to its main supply point's settlement reads, and each heat-pump supply
   point reconciles to the partner's settlement. Nothing spans the two.
4. **Not a row predicate.** A dwelling is its main supply point plus the heat-pump supply point a certificate names, each normalised with
   its own degree-day model, then differenced across the winters.
5. **The enumeration is arithmetic.** No field marks a supply point as part of a dwelling. The 14,400 dwellings with two are counted from the
   certificates.
6. **No cutover date.** Heat pumps were commissioned week by week from the spring, so there is no step to align on.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The service's engineer audit of 400 homes last spring. In each home an engineer traced the circuits, recorded the heating type
  and verified last winter's heating with clamp meters.
* **What it certifies.** The remainder construction: a home's degree-day model on the remainder, fitted on its own days, reproduces its
  verified heating within 3% in 400 of 400 homes. The raw remainder misses by more than 10% in 122, because of lighting and plug loads.
* **What it is blind to.** Second supply points (property 2).
* **Twin pair.** The Ashby Vale and Kerrow Fields districts are identical on every main-supply-point column: 2,600 homes each, both winters'
  hub readings, the circuit splits and the like-for-like normalised change (17 kWh). Heat-pump homes are 16% of Ashby Vale and 8% of Kerrow
  Fields, so heating rose 433 and 225 kWh per dwelling (1.92×). Only the certificates separate them.
* **Resemblance points at the decoy.** The remainder's rise tracks degree-days as closely as it did in the audited homes with electric
  storage heating, so it reads as weather.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The partner's planning standard: "Winter load is planned per dwelling, a dwelling being a self-contained home." The
  tariff terms: "The heat pump is supplied through a dedicated supply point." The service's metrics guide: "A like-for-like home is a
  supply point connected throughout both winters."
* **Empirical pins.** Each home's degree-day model comes from its own days, certified by the audit. Heating degree-days use the 15.5°C base
  of the audit.
* **Voices.** Product manager: "The dashboard is clear: water heaters drove the winter." Data scientist: "It's the cold. Normalise the
  winter and nothing is left." Heat-pump partner's account manager: "Our customers' heat pumps are on our meters; they have nothing to do
  with the hub data." Network planner: "Every new connection on our feeders is a new home."
* **Licensed wrong basis.** The metrics guide records that the service's quarterly report states usage per like-for-like supply point and
  that the partner has seen past figures on that basis.

## 8. Determinism by construction

* **Weather.** Each home's model is daily heating on degree-days, fitted on last winter's days. Any base from 14°C to 17°C moves the figure
  by under 5 kWh. A heat pump, with no previous winter, is fitted on this winter's days and evaluated at last winter's degree-days.
* **Gaps.** Days with more than 10% of half-hours missing are dropped, and shorter gaps are interpolated. Any rule from 5% to 20% moves the
  figure by under 2 kWh.
* **Join.** Every heat-pump supply point has exactly one certificate, and each certificate names one main supply point. No main supply point
  has two heat pumps.
* **Movers.** A supply point is like for like if connected before the first winter began and after the second ended, by the register's dates.
* **Maturity.** Every supply point's winter reads are final settlement reads, and the extract follows the final run.

## 9. Prompt sketch and deliverables

> The network partner needs one number for its reinforcement plan by Friday: how much this winter's rise in home electricity came from space
> heating once the weather is taken out, in kWh per home, to the nearest 10. Our dashboard says the water heaters drove it. Give me the figure
> in a sentence the partner can put in its plan. Send `heating_load.xlsx`, a chart `heating_bridge.png`, and a one-page `partner_note.pdf`.

* `heating_load.xlsx` — the figure on every construction, the solar-export sheet (ask A), the charger sheet (ask B) and the audit back-test
  (ask C).
* `heating_bridge.png` — a bridge from last winter's heating per dwelling to this winter's with bars for weather, movers, main supply points
  and heat pumps, an inset of daily heating against degree-days for heat-pump and other homes, and a title stating the figure.
* `partner_note.pdf` — the figure, the dwelling it is measured on and the heat-pump share.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each month of both winters, the solar export of the homes with panels. *Device:* the export
  register is cumulative and rolls over at 99,999 kWh, as the meter specification states. Differencing across a rollover gives a large
  negative month for about 300 older meters. Export never enters heating.
* **Ask B (device-carried).** For each month of both winters, the energy delivered by the service's managed car chargers. *Device:* the
  charger log splits a session that crosses midnight into two rows under one session ID, and the second row repeats the session's opening
  meter value. Summing rows overstates delivered energy by about an eighth. The main call reads the hubs' circuits, never the charger log.
* **Ask C (validity).** For each of the audit's eight strata (home type by heating type), the verified heating beside the figure your
  construction gives for the audited homes.
* **Decoupling.** Clearing the dwelling join changes no figure in asks A or B. Ask C holds no heat pump, by property 2.

## 11. Rubric arithmetic

12 months (ask A) + 12 months (ask B) + 8 strata (ask C) + the committed figure, the heat-pump dwellings' count and change, the other homes'
change and the weather term + 5 named chart parts + 3 files ≈ 45 criteria.

## 12. World-building constraints

* 120,000 like-for-like homes, 127,500 continuing accounts of which 7,500 moved home. This winter has 21% more degree-days.
* Normalised heating change: other homes +60 kWh, heat-pump homes' main supply points −300 and their heat pumps +2,600 (2,900 at this
  winter's weather). 14,400 heat-pump homes (12%).
* The figure is 397 / 197 / 17 / 329 by rung. Partials sit at 294 and 365. Every other grid cell is at least 21% from 329.
* The audit holds 400 homes, none with a heat pump. Ashby Vale and Kerrow Fields are identical on every main-supply-point column, with
  heat-pump shares of 16% and 8%.
* Export registers and charger rows never touch hub readings, supply-point reads or certificates.

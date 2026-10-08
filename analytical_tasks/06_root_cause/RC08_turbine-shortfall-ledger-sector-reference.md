# RC08 — Which fault on the underperforming wind turbine gets the one crew visit, when the instrument that measures the shortfall is part of it

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Supply Chain & Logistics · field service and asset maintenance |
| Mirrors | Field-service dispatch for fleets of connected equipment (data-centre cooling units at Google and Meta, fulfilment robots at Amazon, Cisco network hardware under service contracts), where the telemetry that measures underperformance is itself bent by the fault |
| Decision shape | Which of N root causes gets the fix: one crew visit to one turbine this spring |
| Committed call | The fault the crew is sent to fix, and the energy it cost the turbine over the winter, in MWh |
| Gap · Pattern | Gap 4 (rule) · Pattern B (the settled warranty ledger pins the lost-energy method, whose decisive component is a sector reference recovered from a healthy year), with E33 (the population a flag suggests) at rung 1 |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution |
| Measured traps engaged | #1 reports a failed back-test, ships anyway · #5 takes the population a flag or filter suggests · #3 stops at a close but inexact match |
| Calibration form | Settled-transaction ledger: 24 settled warranty lost-energy claims on the farm's turbines, each to the MWh |
| Driving force | Every lost-energy figure needs a reference wind speed. The turbine's own anemometer under-reads when the rotor is yawed off the wind or iced, so it hides the very faults in question; the met mast does not, but it stands 600 m away and sees the westerlies differently from the turbine's ridge. Only a mast reference corrected by direction-sector factors recovered from the turbine's healthy commissioning year reproduces the OEM's settled claims, and under it yaw misalignment, not ice, is the largest loss. |

## 1. Situation

One turbine (T07) on a 12-turbine hill farm produced about 6% less than its neighbours over the winter. The OEM's service team wants to replace its pitch
bearing; the farm's performance engineer is sure it was ice. The owner has one crew visit this spring and the asset policy sends it to the fault with
the largest winter lost energy. Five faults have signatures in the 10-minute data: pitch offset (A), yaw misalignment (B), blade icing (C), nacelle
anemometer drift (D) and leading-edge erosion (E). The turbines are under the OEM's warranty, which compensates lost energy, and its settled claims sit
in the ledger.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the 10-minute SCADA data, the mast record, the curtailment instructions, the warranted and site power
  curves and the 24 settled claims. The service team and the performance engineer each read a true signature. No reported figure is overturned;
  the question is which way of measuring loss the settled record certifies, and what it says about T07.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the licensed basis. The natural SCADA analysis still reads loss against the turbine's own
  anemometer and the warranted curve, and still names the pitch.
* **Instrument repair.** Replace the nacelle anemometer with a perfect one and the yaw and icing losses still need a free-stream reference;
  replace the mast with a perfect one and it still stands in different terrain from T07. The sector correction is a property of the site, not a
  flaw of either instrument.
* **Lens swap.** The naive build measures T07 against what its own sensor saw; the answer measures it against what the wind at T07 was, a
  different reference population of 10-minute periods.

## 3. The driving force

A strong solver conditions residuals on each fault's signature, the textbook diagnosis, and it does so against the turbine's own anemometer and
the warranted curve, which is what the SCADA system offers. When it checks that build against the ledger, as the asset policy requires, it
reproduces 15 of 24 settled claims. Moving to the mast reference (the obvious repair, since a yawed or iced rotor bends its own anemometer's
reading) reaches 19, and ice becomes the largest loss. The remaining misses are months when the wind came from the west. The mast sits in a
saddle, T07 on a ridge, and in westerlies T07 sees 6% more wind than the mast; in the cold easterlies that bring ice it sees 8% less. The OEM's
assessments correct the mast by 30° direction sector, with factors fitted on the commissioning year when T07 was healthy. No document says so.
The factors exist only once a solver fits them from the concurrent mast and turbine data of that year. With them, every claim reproduces to the
MWh, the easterly ice loss shrinks, the westerly yaw loss grows, and yaw misalignment leads.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Signature-conditioned residuals against the nacelle anemometer and warranted curve, over periods the SCADA state flag marks "operating" | A, pitch offset (340 MWh) | The SCADA system's own reference and states, with the textbook diagnosis on top | The grid operator's curtailment instructions: 150 MWh of "pitch" loss falls in setpoint periods the state flag still calls operating |
| 1 | The same, with curtailed periods removed through the instruction log | E, leading-edge erosion (260) | The population is now the turbine's own unconstrained operation | The ledger: the nacelle reference reproduces 15 of 24 settled claims, understating every claim from a yawed or iced month |
| 2 | Free-stream reference from the met mast, density-corrected, warranted curve | C, icing (360) | The fault-bent anemometer is gone, and 19 of 24 claims now reproduce | The ledger's five misses are westerly-dominated months; the mast and T07 disagree by direction |
| 3 | **Decisive:** mast wind corrected by 30° sector factors fitted on the commissioning year's concurrent data, against the site power curve | **B, yaw misalignment (400 MWh)** (4th of 5 on rung 0) | — | — |

* **Position table.** B ranks 4th on rungs 0 and 1 and 3rd on rung 2, and leads only rung 3. Rung leaders beat their runners-up by 1.31×,
  1.37×, 1.33× and 1.38×.
* **Discriminator dominance.** Ice carries a 1.50× lead into rung 3 (360 against 240 MWh). The sector reference multiplies yaw's loss by 1.67
  (westerly hours) and ice's by 0.81 (easterly hours), an edge of 2.07×, above the required 1.2 × 1.50 = 1.80; the net margin is 1.38×.
* **Partial correction priced (L3).** Adopting the site curve without sector factors removes the curve gap that inflated erosion but leaves ice
  at 360 against yaw's 240, naming C as rung 2 does. Sector factors fitted on last year (when the yaw fault had begun) reproduce 16 of 24 and
  name C; factors at 10° or 45° reproduce 20 and 18. Sector factors with the warranted curve name B but put its loss at 452 MWh, 13% high, and
  reproduce 21 of 24.
* **Grid.** Population (state flag, instruction log) × reference (nacelle, mast, mast by sector) × curve (warranted, site) gives twelve builds.
  Every flag-based build names A, every nacelle build E or A, every unsectored mast build C, and only the sector reference names B; with the
  site curve it alone reproduces the ledger.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The warranty says lost energy is "assessed by the agreed methodology as applied in prior settlements". The site
   calibration description gives the mast's position and height; no document gives sector factors or says the claims use them.
2. **The ledger pins a construction, not a menu.** The full method reproduces 24 of 24 claims to the MWh; the best rival (sectors with the
   warranted curve) 21, the mast without sectors 19, the nacelle reference 15. Each rival's misses run one way (the nacelle reference understates,
   the warranted curve overstates), so none reconciles to the ledger's total either. The factors are fitted, twelve of them, on a reference year
   chosen by the turbine's health, so there is no parameter to scan.
3. **No arithmetic symptom.** Energy, availability and curtailment hours reconcile under every reference; the mast and the anemometer both
   record cleanly.
4. **Not a row predicate.** The factors are ratios fitted within direction sectors over a different year, then applied by joining each
   10-minute period's mast direction to its sector.
5. **The enumeration is arithmetic.** Which hours carry how much yaw loss follows from a reference built in three steps; no column records it.
6. **No cutover date.** The vane offset crept in over the autumn; the dated event (the pitch controller software update in November) is the
   service team's decoy.
7. **Survives deletion.** With every voice and the licensed basis gone, the mast reference still names ice.

## 6. The calibration corpus

* **Form.** The warranty ledger: 24 settled lost-energy claims (turbine-months across the farm over three years), each with the settled MWh,
  and the 10-minute SCADA and mast data for those months.
* **What it pins.** The reference method (above), including the reference year for the factors and the 30° sectors.
* **Twin pair.** Claims T03-2023-01 and T09-2024-02 are identical on turbine model, mean mast wind speed, density, availability, fault hours and
  curtailment hours. They settled at 58 and 121 MWh (2.09×), because one month's wind came mostly from the 240–270° sector (factor 1.06) and the
  other from 90–120° (0.92). Only the sector reference reproduces both.
* **Every rule exercised.** One claim month had curtailment (testing the population rule), one had icing on the nacelle anemometer (testing
  the reference), one had an easterly-only wind rose (testing the factors).
* **Resemblance points at the decoy.** This winter's worst weeks resemble claim T07-2023-12, an icing month, on temperature, humidity and loss.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The asset policy: the crew is sent to the fault with the largest lost energy over December to February, lost energy being
  assessed only on a method that reproduces every settled warranty claim to the MWh. The diagnostic guide's condition windows for each fault.
* **Empirical pins.** The sector factors and their reference year, from the ledger.
* **Voices.** The OEM's site lead: "The blades aren't reaching fine pitch at rated; the bearing is going." The farm's performance engineer:
  "It's ice. Every bad week was a cold week."
* **Licensed wrong basis.** The service agreement records that the OEM's service team assesses underperformance against the warranted curve
  on the nacelle anemometer and will present that at the dispatch meeting.

## 8. Determinism by construction

* **Fault windows.** The diagnostic guide's windows (icing by temperature and humidity, pitch at or above rated, yaw by misalignment band) are
  applied in its stated order, so every period belongs to one fault or none.
* **Curtailment.** Instructions carry start and end times to the second; no instruction edge falls inside a 10-minute period.
* **Factors.** The commissioning year has at least 400 valid hours in every sector; the factor is the ratio of mean wind speeds.
* **Density.** The guide's correction is applied to every reference; no build differs on it.
* **Rounding.** Losses to the nearest MWh; the committed figure sits mid-bin.

## 9. Prompt sketch and deliverables

> We get one crew visit to T07 this spring, and the OEM's people want to replace the pitch bearing. Tell me which fault the crew goes to fix and
> how many MWh it cost us over the winter, as the sentence that goes on the work order. Send `t07_diagnosis.xlsx` and a chart
> `loss_by_fault.png`.

* `t07_diagnosis.xlsx` — the five faults under each construction, the fleet availability sheet (ask A), the components sheet (ask B) and the
  ledger reproduction (ask C).
* `loss_by_fault.png` — a wind rose of T07's winter loss by 30° sector split by fault, beside a bar chart of each fault's loss under the nacelle,
  mast and sector references, with the sector factors printed on the rose and the dispatched fault highlighted.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 12 turbines and each winter month, contractual availability. *Device:* the
  state log stops the availability clock for environmental stops (low wind, high wind, ice detection) under the O&M agreement's definition,
  and these share the "stopped" state with faults, separated by a category code; counting every stop as unavailability understates availability
  for the seven turbines on the exposed ridge.
* **Ask B (device-carried).** For each of the eight major components, failures and mean time to repair over three years. *Device:* a component
  exchange is logged as two work orders (removal and installation) under one job number, as the maintenance system's guide documents; counting
  work orders doubles failures and halves repair times.
* **Ask C (validity).** For each of the 24 settled claims, the settled MWh and the MWh under each of the four constructions.
* **Decoupling.** Clearing the sector reference changes no figure in asks A or B.

## 11. Rubric arithmetic

12 turbines × 3 months (ask A) + 8 components × 2 figures (ask B) + 24 claims × 4 constructions (ask C) + the fault dispatched, its MWh and the
runner-up's + 5 named chart parts + 2 files ≈ 160 criteria.

## 12. World-building constraints

* T07 winter losses by rung (A / B / C / D / E, MWh): 340 / 90 / 140 / 60 / 260; 190 / 90 / 140 / 60 / 260; 190 / 240 / 360 / 60 / 270;
  190 / 400 / 290 / 60 / 110.
* Sector factors from the commissioning year: 1.06 in the westerly sectors, 0.92 in the easterly ones, near 1 elsewhere; the yaw fault's hours
  are 70% westerly and the icing hours 85% easterly.
* Ledger: full method 24/24, sectors with warranted curve 21, mast 19, nacelle 15; last-year factors 16, 10° sectors 20, 45° sectors 18.
* The twin claims are identical on every claim-summary column.
* Environmental stop codes and component work orders touch no T07 winter period or ledger claim.

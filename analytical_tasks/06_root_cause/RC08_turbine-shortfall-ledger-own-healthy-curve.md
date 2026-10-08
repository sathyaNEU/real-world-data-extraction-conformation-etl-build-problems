# RC08 — Which fault on the underperforming wind turbine gets the one crew visit, when only the turbine's own healthy year says what it should have made

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Supply Chain & Logistics · field service and asset maintenance |
| Mirrors | Field-service dispatch for fleets of connected equipment (data-centre cooling units at Google and Meta, fulfilment robots at Amazon, Cisco network hardware under service contracts), where underperformance is judged against a nameplate rating and only each unit's own healthy history says what it should have delivered |
| Decision shape | Which of N root causes gets the fix: one crew visit to one turbine this spring |
| Committed call | The fault the crew is sent to fix, and the energy it cost the turbine over the winter, in MWh |
| Gap · Pattern | Gap 4 (rule) · Pattern B (the settled warranty ledger pins the lost-energy method, whose decisive component is the expected-output baseline: T07's own power curve fitted on its healthy commissioning year against its sector-corrected wind), with E33 (the population a flag suggests) at rung 0 |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution |
| Measured traps engaged | #1 reports a failed back-test, ships anyway · #5 takes the population a flag or filter suggests · #3 stops at a close but inexact match |
| Calibration form | Settled-transaction ledger: 24 settled warranty lost-energy claims on the farm's turbines, each to the MWh |
| Driving force | Lost energy is the gap between what the turbine made and what it should have made. Read against the warranted curve, which runs 7% above what T07 made even when new between 9 m/s and rated, the clean westerly hours show a gap that the diagnostic guide assigns to erosion, its residual fault. The OEM's settled claims read what each turbine should have made from its own power curve over its healthy commissioning year, at the wind the met mast records corrected by direction sector. Against T07's own curve the erosion residual collapses, and yaw misalignment, concentrated in the westerlies, is the largest loss. |

## 1. Situation

One turbine (T07) on a 12-turbine hill farm produced about 14% less than its neighbours over the winter. The OEM's service team wants to replace its pitch
bearing; the farm's performance engineer is sure it was ice. The owner has one crew visit this spring and the asset policy sends it to the fault with
the largest winter lost energy. Five faults have signatures in the 10-minute data: pitch offset (A), yaw misalignment (B), blade icing (C), nacelle
anemometer drift (D) and leading-edge erosion (E). The turbines are under the OEM's warranty, which compensates lost energy, and its settled claims sit
in the ledger.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the 10-minute SCADA data, the mast record, the curtailment instructions, the warranted curve, the
  commissioning-year records and the 24 settled claims. The service team and the performance engineer each read a true signature. No reported
  figure is overturned; the question is which expected output the settled record certifies, and what it says about T07.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the licensed basis. The natural analysis still reads loss against the warranted curve, and still
  names the pitch on the state flag's population and erosion on the corrected wind.
* **Instrument repair.** Suspect files: the SCADA state flag, which calls curtailed periods operating, and the met mast, which records the wind
  at the saddle, not at T07. Repaired so that the flag marks every setpoint period and a perfect free-stream instrument records the wind at
  T07's hub, rung 0 and rung 1 both return E (570 MWh against yaw's 470), as rung 2 already does, and none returns B. The answer still needs
  T07's healthy-year curve: against the warranted curve the clean westerly hours' gap lands on erosion, and no wind instrument, however good,
  records what T07 should have made.
* **Lens swap.** The naive build measures T07 against what a turbine of its model is warranted to make; the answer measures it against what
  T07 itself made when healthy, at the wind it actually saw: a reference built from a different year's periods.

## 3. The driving force

A strong solver knows a yawed or iced rotor bends its own anemometer, so it reads T07's wind from the met mast, conditions residuals on each
fault's signature against the warranted curve, and removes the grid operator's curtailment periods, which the SCADA state flag still calls
operating. Ice then leads, and the build reproduces 19 of the ledger's 24 settled claims. The misses are westerly months: the mast sits in a
saddle and T07 on a ridge, so in westerlies T07 sees 6% more wind than the mast and in the cold easterlies that bring ice 8% less. Correcting
the mast by 30° direction sector, with factors fitted on the commissioning year, reproduces 21 claims, shrinks ice and grows yaw, but erosion
jumps to the top: between 9 m/s and rated the warranted curve runs 7% above what the ridge turbines made even when new, and the diagnostic guide
assigns every unexplained below-rated shortfall to erosion. The OEM's assessments measure loss against each turbine's own commissioning-year
curve. No document says so, and the curve exists only once a solver fits it from T07's healthy year against the corrected wind. With it, every
claim reproduces to the MWh, the erosion residual collapses to 110 MWh, and yaw misalignment leads at 430.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Signature-conditioned residuals against the met mast and the warranted curve, over periods the SCADA state flag marks "operating" | A, pitch offset (440 MWh) | The free-stream reference a yawed or iced rotor cannot bend, the SCADA system's own states, and the textbook diagnosis on top | The grid operator's curtailment instructions: 250 MWh of "pitch" loss falls in setpoint periods the state flag still calls operating |
| 1 | The same, with curtailed periods removed through the instruction log | C, icing (360) | The population is now the turbine's own unconstrained operation, and 19 of 24 settled claims reproduce | The ledger's five misses are westerly-dominated months; the mast and T07 disagree by direction |
| 2 | Mast wind corrected by 30° sector factors fitted on the commissioning year's concurrent data, warranted curve | E, leading-edge erosion (570) | The reference is now the wind at T07, and 21 of 24 claims reproduce | The ledger's three misses are high-wind months on ridge turbines, each settled below its warranted-curve figure |
| 3 | **Decisive:** the sector-corrected wind against T07's own power curve, fitted on its healthy commissioning year | **B, yaw misalignment (430 MWh)** (4th of 5 on rung 0) | — | — |

* **Position table.** B ranks 4th on rung 0, 3rd on rung 1 and 2nd on rung 2 (1.21× behind erosion), and leads only rung 3. Rung leaders beat
  their runners-up by 1.22×, 1.33×, 1.21× and 1.59× (430 against ice's 270).
* **Discriminator dominance.** Erosion carries a 1.21× lead into rung 3 (570 against 470 MWh). T07's own curve multiplies yaw's loss by 0.91
  and erosion's by 0.19, an edge of 4.74×, 3.26 times the required 1.2 × 1.21 = 1.46; the net margin over erosion is 3.91×.
* **Partial correction priced (L3).** Each half of the method names a wrong fault. T07's own curve on the unsectored mast removes the erosion
  residual but leaves the easterly ice loss inflated and the westerly yaw loss understated: ice 360 against yaw's 228, naming C, rung 1's
  answer (1.58×), with 20 of 24 claims. Factors and curve fitted on last winter, when the vane offset had begun, fold part of the yaw loss into
  the reference: ice 310 against yaw's 255, naming C (1.22×), with 16 of 24.
* **Grid.** Population (state flag, instruction log) × reference (nacelle, mast, mast by sector) × curve (warranted, T07's own) gives twelve
  builds. Every flag-based build names A (curtailed "pitch" loss grows from 150 MWh on the nacelle reference to 250 on the mast and 320 on the
  sector reference, so even the flag-based sector-and-own-curve build gives A 510 against B's 430, 1.19×). With the log, every nacelle build
  names A or E, every unsectored mast build C, the sector reference with the warranted curve E, and only the sector reference with T07's own
  curve names B; it alone reproduces the ledger.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The warranty says lost energy is "assessed by the agreed methodology as applied in prior settlements". The site
   calibration description gives the mast's position and height; no document gives sector factors or a turbine's own curve, or says the
   claims use them.
2. **The ledger pins a construction, not a menu.** The full method reproduces 24 of 24 claims to the MWh; the best rival (sectors with the
   warranted curve) 21, T07's own curve on the unsectored mast 20, the mast 19, the nacelle reference 15. Each rival's misses run one way (the
   warranted curve overstates, the unsectored mast misreads by direction), so none reconciles to the ledger's total either. The curve and the
   factors are fitted on a reference year chosen by the turbine's health, so there is no parameter to scan.
3. **No arithmetic symptom.** Energy, availability and curtailment hours reconcile under every reference and curve; the mast, the anemometer
   and the commissioning-year records all record cleanly.
4. **Not a row predicate.** The curve is T07's own output binned by corrected wind over a different year, then joined to each winter period by
   its corrected wind speed.
5. **The enumeration is arithmetic.** Which hours carry how much yaw loss follows from a reference and a curve built in three steps; no column
   records it.
6. **No cutover date.** The vane offset crept in over the autumn; the dated event (the pitch controller software update in November) is the
   service team's decoy.
7. **Survives deletion.** With every voice and the licensed basis gone, the sector reference with the warranted curve still names erosion.

## 6. The calibration corpus

* **Form.** The warranty ledger: 24 settled lost-energy claims (turbine-months across the farm over three years), each with the settled MWh,
  and the 10-minute SCADA and mast data for those months and for each turbine's commissioning year.
* **What it pins.** The method (above): the 30° sector factors, the expected output read from each turbine's own commissioning-year curve, and
  the reference year for both.
* **Twin pair.** Claims T03-2023-01 and T09-2024-02 are identical on turbine model, mean mast wind speed, wind rose, density, production,
  availability, fault hours and curtailment hours. They settled at 58 and 121 MWh (2.09×): T03 stands on the ridge and its commissioning-year
  curve runs 7% below the warranted curve between 9 m/s and rated, while T09's in the saddle matches it. Only the turbine's own curve
  reproduces both.
* **Every rule exercised.** One claim month had curtailment (testing the population rule), one an easterly-only wind rose (testing the
  factors), and one ran mostly between 9 m/s and rated on a ridge turbine (testing the curve).
* **Resemblance points at the decoy.** This winter's worst weeks resemble claim T07-2023-12, an icing month, on temperature, humidity and loss.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The asset policy: the crew is sent to the fault with the largest lost energy over December to February, lost energy being
  assessed only on a method that reproduces every settled warranty claim to the MWh. The diagnostic guide's condition windows for each fault.
* **Empirical pins.** The sector factors, T07's own curve and their reference year, from the ledger.
* **Voices.** The OEM's site lead: "The blades aren't reaching fine pitch at rated; the bearing is going." The farm's performance engineer:
  "It's ice. Every bad week was a cold week."
* **Licensed wrong basis.** The service agreement records that the OEM's service team assesses underperformance against the warranted curve
  on the nacelle anemometer and will present that at the dispatch meeting.

## 8. Determinism by construction

* **Fault windows.** The diagnostic guide's windows (icing by temperature and humidity, pitch at or above rated, yaw by misalignment band) are
  applied in its stated order, and erosion takes the below-rated shortfall left outside every other window, so every period belongs to one
  fault or none.
* **Curves.** T07's own curve is its commissioning-year output against the sector-corrected mast, in 0.5 m/s bins of at least 30 periods;
  between 9 m/s and rated the warranted curve runs 7% above it, and both reach rated power at rated.
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
* `loss_by_fault.png` — a wind rose of T07's winter loss by 30° sector split by fault, beside a bar chart of each fault's loss under the mast,
  sector and own-curve builds, with T07's own and the warranted curve overlaid in an inset and the dispatched fault highlighted.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 12 turbines and each winter month, contractual availability. *Device:* the
  state log stops the availability clock for environmental stops (low wind, high wind, ice detection) under the O&M agreement's definition,
  and these share the "stopped" state with faults, separated by a category code; counting every stop as unavailability understates availability
  for the seven turbines on the exposed ridge.
* **Ask B (device-carried).** For each of the eight major components, failures and mean time to repair over three years. *Device:* a component
  exchange is logged as two work orders (removal and installation) under one job number, as the maintenance system's guide documents; counting
  work orders doubles failures and halves repair times.
* **Ask C (validity).** For each of the 24 settled claims, the settled MWh and the MWh under each of the four constructions.
* **Decoupling.** Clearing T07's own curve changes no figure in asks A or B.

## 11. Rubric arithmetic

12 turbines × 3 months (ask A) + 8 components × 2 figures (ask B) + 24 claims × 4 constructions (ask C) + the fault dispatched, its MWh and the
runner-up's + 5 named chart parts + 2 files ≈ 160 criteria.

## 12. World-building constraints

* T07 winter losses by rung (A / B / C / D / E, MWh): 440 / 240 / 360 / 60 / 270; 190 / 240 / 360 / 60 / 270; 190 / 470 / 270 / 60 / 570;
  190 / 430 / 270 / 60 / 110.
* Partial builds (same order): own curve on the unsectored mast 190 / 228 / 360 / 60 / 100; last winter's factors and curve 190 / 255 / 310 /
  60 / 105; nacelle reference with the log and the warranted curve 190 / 90 / 140 / 60 / 260. Curtailed "pitch" loss: 150 MWh on the nacelle
  reference, 250 on the mast, 320 on the sector reference.
* Sector factors from the commissioning year: 1.06 in the westerly sectors, 0.92 in the easterly ones, near 1 elsewhere; the yaw fault's hours
  are 70% westerly and the icing hours 85% easterly, nearly all below 9 m/s. Between 9 m/s and rated the warranted curve runs 7% above T07's own
  curve, and 1,900 clean westerly hours fall there.
* Ledger: full method 24/24, sectors with the warranted curve 21, own curve on the unsectored mast 20, mast 19, nacelle 15; last-year factors and
  curve 16, 10° sectors 20, 45° sectors 18.
* The twin claims are identical on every claim-summary column.
* Environmental stop codes and component work orders touch no T07 winter period or ledger claim.

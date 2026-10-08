# FC35 — How 400 proactive transformer replacements split across twelve districts, when the pilot's filed determinations reproduce only with each home's own charging start

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Supply Chain & Logistics · electric distribution asset replacement |
| Mirrors | Allocating capacity upgrades by where load lands in time rather than how much of it there is (data-centre power upgrades by rack load profiles, delivery-station dock upgrades, fleet depot charging, utility EV readiness programmes) |
| Decision shape | An allocation under a cap: 400 replacements in 2027, split across twelve districts in proportion to forecast at-risk transformers |
| Committed call | Each district's replacements, summing to 400, with the Foothill district's figure stated on its own |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · Pattern B (the at-risk method recovered from a pilot's filed determinations under a reproduction clause), with the unit not stored (S1) at rung 1 |
| Gate G mechanism | method_or_model_selection, with forecasting support |
| Measured traps engaged | #1 reports a failed back-test, ships anyway · #3 stops at a close but inexact match · #2 counts file rows instead of the real unit |
| Calibration form | Pilot log: the 2025–26 proactive-replacement pilot in three districts, 1,240 transformers each with its inputs and its filed at-risk determination |
| Driving force | A transformer is at risk when its forecast 4–9 pm peak exceeds 1.2 times nameplate, and an electric vehicle adds to that peak only if its home starts charging before 9 pm. The pilot's filed determinations reproduce only when each home's charging start is read from its own interval-meter data: the flat 0.30 coincidence reproduces 1,190 of 1,240 and the EV-rate proxy 1,221. Coastal early adopters charge on timers after midnight whatever their rate; inland newer owners charge on arrival home whatever theirs. Built that way, the inland districts' share of at-risk transformers roughly doubles. |

## 1. Situation

A California utility has approval for 400 proactive service-transformer replacements in 2027. The regulator's decision allocates them
across its twelve districts in proportion to each district's forecast count of transformers at risk of summer overload, defined as a
forecast 4–9 pm peak above 1.2 times nameplate, and requires the allocation method to reproduce every determination the utility filed in
its 2025–26 pilot. The pilot covered three districts. The pack holds vehicle registrations by address, the premise and transformer
connectivity model, nameplate and base-peak data, fifteen-minute interval-meter data for every premise, rate schedules, the district
sales-share forecasts and the pilot log. The compliance filing is due on the 30th.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: registrations, connectivity, nameplates, interval data, rates, forecasts and the pilot's filed
  determinations. No stakeholder's reading of their own numbers is overturned; the coastal districts really did adopt first. The
  difficulty is recovering the method behind the determinations, which no document spells out.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete every voice. The flat-coincidence build still reproduces 96% of the pilot and still puts the coastal
  districts first.
* **Instrument repair.** Clean-data test. No file the ladder reads is incomplete, stale or narrower than it claims: vehicle registrations,
  premises links, the interval data and the pilot log are complete, and the EV-rate flag records a tariff, a different attribute from when
  a home charges, so using it is an ordinary wrong rung. With nothing to repair, rung 0 returns 18, rung 1 22 and rung 2 31, and the
  decisive build is still needed for the 2027 additions, whose charging depends on their district's recent-adopter mix rather than on any
  record of the past.
* **Lens swap.** The naive read and the answer count different populations: vehicles on a transformer, against vehicles whose homes start
  charging inside the peak window, which differ most in exactly the districts that adopted first.

## 3. The driving force

A strong solver links each registered vehicle through its address to a premise and a transformer, adds forecast 2027 vehicles, applies
the industry coincidence of 0.30 at 7.2 kW to each transformer's base peak, and tests the result against the pilot as the decision
requires: 1,190 of 1,240 determinations reproduce. The 50 misses are all transformers the pilot filed as not at risk, all serving homes on
the EV rate, so the solver takes EV-rate homes out of the peak and reaches 1,221. The last 19 misses are the rule. The pilot read each
home's charging start from its own interval data, the hour its evening load steps up by a charger's draw, and counted a vehicle only if
that step comes before 9 pm. Coastal early adopters set timers for after midnight whether or not they are on the EV rate; inland owners who
bought in the last two years plug in on arrival home, rate or no rate. Rebuilt per home, Foothill's at-risk count rises and the coastal
districts' falls.

## 4. The ladder

| Rung | Construction | Lands on (Foothill replacements) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Districts weighted by forecast 2027 vehicle growth from the sales-share curves | 18 (−50%) | The adoption forecast every EV plan starts from, and Foothill's growth really is slower | The regulator's decision: the split follows forecast at-risk transformers, not vehicles |
| 1 | Vehicles linked by address to premises and transformers, flat 0.30 coincidence, at-risk test per transformer | 22 (−39%) | The right unit, the industry coincidence, and 96% of the pilot reproduced | The pilot log: all 50 misses are transformers filed as not at risk whose homes are on the EV rate |
| 2 | EV-rate homes taken out of the peak | 31 (−13.9%) | 1,221 of 1,240 reproduced, and the remaining misses look like noise | The pilot log's last 19 misses: EV-rate homes that charge at six and default-rate homes on timers, each visible in its interval data |
| 3 | **Decisive:** each home's charging start recovered from its interval data, vehicles counted only where it falls before 9 pm, 2027 additions given their district's recent-adopter mix | **36** | — | — |

* **Figure shape.** Every correction walks Foothill's figure up and the decisive rung lands highest, so the answer is the maximum cell and
  every partial build under-allocates the inland districts. Rungs 0–2 sit 50%, 39% and 13.9% below it.
* **Partial correction priced (L3).** A solver who recovers charging starts but gives 2027's added vehicles the windows of the district's
  existing fleet, early adopters included, lands at 32 (−11.1%). One who reads starts from the rate plan's tariff hours lands on rung 2.
* **Grid.** Unit (district vehicles, ZIP counts spread evenly, address-linked transformers) × peak contribution (flat, EV-rate proxy,
  interval-data start) × additions (existing-fleet mix, recent-adopter mix) = 18 cells. Every wrong cell sits at least 11% from 36. The
  nearest is the full build with additions given the existing-fleet mix (32), which the pilot's own 2026 forecasts, filed with recent-adopter
  mixes, refute in 23 transformers.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The decision names the overload criterion and the reproduction condition. No document says how a vehicle enters
   the peak, mentions charging starts, or links interval data to the determination.
2. **Reproduction (Pattern B).** The interval-data construction reproduces 1,240 of 1,240 filed determinations; the best rival (the EV-rate
   proxy) 1,221; the flat coincidence 1,190. The flat coincidence's 50 misses are all over-flags, 5.3% on the pilot's at-risk total; the EV-rate
   proxy's 19 run both ways and leave its total within 0.4%, a false clean only the row count exposes. The rule is a construction, not a menu: a charging start is a step recovered from each home's fifteen-minute load curve, two
   joins away from the transformer, and the tempting attribute (the rate plan) is a near miss.
3. **No arithmetic symptom.** Registrations link to premises and transformers without orphans, interval data sums to billed energy, and
   the at-risk totals tie to their own transformer counts on every rung.
4. **Not a row predicate.** A vehicle's contribution needs its home's load curve fitted for a step, then summing over every home on the
   transformer against its nameplate.
5. **The enumeration is arithmetic.** No column says when a home charges; the at-risk set is computed transformer by transformer.
6. **No cutover date.** Charging habits are standing properties of homes; nothing steps.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The pilot log: 1,240 transformers in three pilot districts, each with nameplate, base peak, linked vehicles, the 2026 forecast
  additions and the filed at-risk determination for summer 2026.
* **What it certifies.** The address-to-transformer link (the pilot's filed vehicle counts per transformer reproduce exactly), the 1.2
  overload factor and the 7.2 kW draw.
* **What it pins.** The peak-contribution rule (above), and that additions take their district's recent-adopter mix.
* **Twin pair.** Transformers T-48817 and T-51203 are identical on nameplate (50 kVA), base peak, six linked vehicles and the rate plans of
  every home they serve. One was filed at risk with a forecast peak of 1.31 times nameplate, the other not at risk at 0.96, because five of
  T-48817's homes start charging between 5:45 and 6:30 pm and five of T-51203's after 11:30 pm. No function of the visible columns
  reproduces both.
* **Resemblance points at the decoy.** The 2027 fleet's district mix most resembles the pilot districts' 2025 fleet, on which the flat
  coincidence reproduced 96%.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The regulator's decision: the 400 replacements are allocated across districts in proportion to forecast transformers at
  risk of summer overload (forecast 4–9 pm peak above 1.2 times nameplate), by a method that reproduces every pilot determination, with
  largest-remainder rounding. The district sales-share forecasts are the utility's adopted adoption forecast.
* **Empirical pins.** Each home's charging start, from its interval data. The recent-adopter window mix per district, from homes whose
  first charging step appears in the last twelve months.
* **Voices.** The planning engineer: "A coincidence of 0.3 is the industry standard and it has served us for a decade." The coastal
  district manager: "Our customers bought first; our transformers are the ones at risk." The rates manager: "Anyone on the EV rate charges
  overnight. That's what the rate is for."
* **Licensed wrong basis.** The decision records that the ratepayer advocate will propose splitting replacements by district vehicle
  growth and will present it at the compliance workshop.

## 8. Determinism by construction

* **Charging starts.** Every charging home's evening step falls before 8:30 pm or after 9:30 pm, so the 9 pm cut is unambiguous, and the
  step is at least 6 kW in every case, so step-detection settings converge.
* **Additions.** The decision's convention places 2027 additions on transformers in proportion to their current vehicles; the recent-adopter
  mix is stable across 9-, 12- and 15-month windows.
* **Overload test.** No transformer's forecast peak sits within 3% of 1.2 times nameplate under the decisive construction.
* **Maturity.** Summer 2026 interval data is complete and validated; no premise's data is estimated in June to September.
* **Rounding.** Foothill's share of at-risk transformers (8.99%) gives 35.96, which rounds to 36 under largest remainder.

## 9. Prompt sketch and deliverables

> We have 400 proactive transformer replacements for 2027, and the compliance filing that splits them across our twelve districts is due
> on the 30th. The coastal managers are sure their early adopters put their transformers first in line. Give me each district's
> allocation, with Foothill's in a sentence for the filing's cover letter, and send `replacement_allocation.xlsx` with the build and the
> sheets below, a chart `charging_windows.png`, and a two-page `allocation_filing.pdf`.

* `replacement_allocation.xlsx` — the transformer-level at-risk build, the district allocation, the asset-history sheet (ask A) and the
  reliability sheet (ask B).
* `charging_windows.png` — for each district, a histogram of charging start times for homes with vehicles, with the 4–9 pm window shaded,
  coastal and inland districts in separate panels, and each district's at-risk count and allocation annotated.
* `allocation_filing.pdf` — the committed allocation and the reproduction record the decision requires.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the twelve districts, service transformers installed and retired in 2025–26 by
  nameplate class (25, 37.5, 50, 75 kVA). *Device:* a transformer replaced in place keeps its location ID under a new asset ID, filed as one
  retirement and one installation, as the asset register guide documents; counting location IDs hides every pilot replacement. The 2027
  build uses the current asset at each location either way.
* **Ask B (device-carried).** For each district, 2026 customer minutes of interruption caused by transformer failures per customer served.
  *Device:* the reliability standard excludes momentary interruptions under five minutes, which the outage log records alongside sustained
  ones, as the reliability report documents; including them overstates the figure in every district.
* **Ask C (validity).** For each of the four rung constructions, the pilot determinations it reproduces and Foothill's allocation.
* **Decoupling.** Clearing the charging-start rule changes no figure in asks A or B.

## 11. Rubric arithmetic

12 districts × 4 nameplate classes (ask A) + 12 districts (ask B) + 4 constructions × 2 (ask C) + 12 district allocations and Foothill's
committed figure + 5 named chart parts + 3 files ≈ 89 criteria.

## 12. World-building constraints

* Network forecast at-risk transformers under the decisive build: about 1,900, of which Foothill 171 (8.99%). Foothill's allocation by
  rung: 18 / 22 / 31 / 36; existing-fleet mix for additions 32.
* Pilot: 1,240 transformers; reproduction 1,240 / 1,221 / 1,190. Charging before 9 pm: 22% of coastal homes with vehicles, 81% of inland
  homes with vehicles; EV-rate share 58% coastal, 21% inland.
* The twin transformers are identical on nameplate, base peak, linked vehicles and every served home's rate plan.
* Asset replacements in place and momentary interruptions touch no transformer, vehicle or interval reading in the build.

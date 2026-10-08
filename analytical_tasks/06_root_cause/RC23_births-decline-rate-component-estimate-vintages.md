# RC23 — How many of the region's lost births falling fertility rates account for, filed before the maternity network decides on a unit closure

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Demographic & Social Science · fertility and maternity service planning |
| Mirrors | Volume declines split into per-capita behaviour and base size (orders = customers × order rate at Amazon, impressions = users × sessions at Meta), where the base is a published estimate that is revised after the fact and the two ends of the comparison quietly come from different vintages |
| Decision shape | One figure committed at a date (a component): the rate component of the five-year births decline, filed at the capacity review on the 3rd |
| Committed call | Births lost to falling age-specific fertility rates over five years, to resident mothers, to the nearest ten |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · E15 (the quiet second trap: denominators from two vintages of the population estimates), with E14 (a binding limit applied in the figure: the units' registered capacity) at rung 1 |
| Gate G mechanism | decomposition_attribution, with confirm_surface_read support |
| Measured traps engaged | #11 beats the headline trap, misses the quiet one · #10 notes a binding limit as a risk · #4 never tests its reading against the control |
| Calibration form | Revision log: every published vintage of the female population estimates by age and area, and the provisional and final birth registrations |
| Driving force | The base year's female population comes from the estimates as first published, before the census rebased them. The census found more women in their early thirties than the old estimates carried, so a decomposition that sets the base year's old figures against this year's rebased ones books part of a real fall in that age group as a fall in rates. Only the revision log's latest vintage, used at both ends, reproduces the network's previous published review. |

## 1. Situation

Births to mothers living in a region fell 11% over five years, from 21,800 to 19,400. The maternity network's finance director calls it a permanent fall
in fertility and wants to close one of six units; the network's planning guidance closes a unit only if falling fertility rates account for at least
half of the five-year decline in births to resident mothers. The units' own delivery counts fell further than residents' births, because one unit hit
its registered capacity this year and diverted mothers to neighbouring networks. Population estimates for the base year were revised after the
census.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: registrations by residence, delivery counts by unit, the capacity register, the exchange file of births
  across network boundaries, and every vintage of the population estimates. The total fertility rate did fall. Nothing is overturned; the
  component is measured whole, with both ends on one basis.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the finance director's view, the planner's and the licensed basis. The shipped base-year estimate file is still
  the one the network's plan used, and a correct three-factor decomposition on it still puts the rate component above half.
* **Instrument repair.** A perfect population estimate is exactly what the latest vintage is; the error lies in pairing it with an older one,
  which no better instrument prevents.
* **Lens swap.** The naive decomposition sets one population against a differently estimated one; the answer compares the same population
  estimated the same way at both dates.

## 3. The driving force

A strong solver discards the "fertility crisis" reading at once: a total fertility rate is standardised for age and cannot explain a count of
births. It uses births to resident mothers, as the guidance says, rather than the units' deliveries, which fell further because one unit's
registered capacity bound for five months and 240 resident mothers delivered elsewhere. It runs the three-factor decomposition (population size,
age structure, age-specific rates) on births and women by age. Rates come out at 1,620 of the 2,400 lost births, two-thirds, and the closure
proceeds. The women behind the base year came from the estimate file the network's original plan used, published before the census. The census
rebased the base year's women aged 30–34 up by 6%; the current year's estimates, published since, are rebased already. Mixing the two vintages
leaves the base year's rates too high and its peak-age population too small, so the fall in rates looks larger than it was and part of the
fall in women of peak childbearing age is booked to rates. With the latest vintage at both ends, as the network's previous review was computed, rates account for 1,020 births, 42.5%.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The units' delivery counts, the whole fall read as falling fertility, as the total fertility rate suggests | 2,640 births (+159%) | It is the network's own count, read the way the national commentary reads it | The capacity register: one unit's registered cap bound for five months and diverted 240 resident mothers out of the network |
| 1 | Births to resident mothers, the cap's diversions restored, still read as falling fertility | 2,400 (+135%) | The guidance's own population, every birth to a resident counted | A rate standardised for age cannot explain a count: size and age structure have to be separated from rates |
| 2 | Three-factor decomposition (size, age structure, age-specific rates) on resident births, women by age from the shipped estimate files | 1,620 (+59%) | The headline trap beaten: the textbook symmetric decomposition, closing exactly | The revision log: the base-year file is a vintage the census has since rebased, and the current-year file is not from that vintage |
| 3 | **Decisive:** the same decomposition with both years' women from the latest vintage | **1,020 births** | — | — |

* **Figure shape.** Every correction walks the figure down (−9%, −33%, −37% per step), and the answer is the minimum cell, so every partial
  application closes a unit the guidance keeps open.
* **Partial correction priced (L3).** A solver who sees that the vintages differ and makes them consistent on the old basis (the base year's
  first estimate and the current year's pre-census projection, both in the log) removes the mismatch but keeps the pre-census age structure at
  both ends, and lands at 1,700 (+67%), further than rung 2.
* **Grid.** Births (deliveries, residents) × method (all to rates, three-factor) × vintage (as shipped, original for both, latest for both)
  gives eight feasible cells. The nearest wrong cell is 1,260 (+24%), the latest vintage applied to delivery counts with the capacity cap
  ignored, and it still sits above half of the deliveries' fall.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The guidance names the method and the population. The estimate files carry their publication dates; nothing says the
   base year was rebased or that the two files differ in vintage.
2. **The corpus pins a construction, not a menu.** The network's previous review published its three components to the birth; the latest
   vintage then available, used at both ends, reproduces all three exactly, and the as-published pairing misses the rate component by 31%. Every
   pairing that mixes vintages misses in the same direction, inflating rates. The rule is a join of every area-age cell to the latest vintage of
   its year, not a setting.
3. **No arithmetic symptom.** Each estimate file ties to its own published totals; the decomposition closes exactly on either pairing.
4. **Not a row predicate.** The rebasing differs by area and age, so each cell of the base year has to be replaced from the log before the
   decomposition is rebuilt.
5. **The enumeration is arithmetic.** No column flags the base year as superseded; the 600 births moved from rates to structure come out of the
   rebuilt decomposition.
6. **No cutover date.** The census rebasing is a revision to a past year, not an event in the series; the dated event (the capacity cap this
   year) is the rung-1 trap.
7. **Survives deletion.** With every voice gone, the shipped files still give two-thirds to rates.

## 6. The calibration corpus

* **Form.** The revision log: every vintage of the female population estimates by area and five-year age group for each of the last eight
  years, with publication dates, and provisional and final birth registrations by residence.
* **What it pins.** The consistent-vintage rule (above), and that final registrations differ from provisional ones by under 0.3% for the years
  used, so registration timing is not a fork.
* **Twin pair.** Areas L-07 and L-11 had identical births, women aged 15–44 and age structures in the base-year file as shipped. Their rate
  components were 210 and 100 births (2.1×), because the census rebased L-07's women aged 30–34 up by 9% and L-11's by 1%. Only the latest
  vintage separates them.
* **Resemblance points at the decoy.** The region's age-specific rates fell like the national rates, and the national commentary attributes
  the national decline mostly to rates.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The planning guidance: a unit closes only if falling age-specific rates account for at least half of the five-year decline
  in births to resident mothers, by the three-factor symmetric decomposition. The capacity register.
* **Empirical pins.** The consistent-vintage rule, from the previous review's published components.
* **Voices.** The finance director: "The birth rate is falling and it isn't coming back." The network planner: "Our delivery counts tell the
  whole story; we don't need anyone else's figures."
* **Licensed wrong basis.** The guidance records that the national statistics office's commentary attributes regional changes to the total
  fertility rate and will be presented at the review.

## 8. Determinism by construction

* **Ages.** Births under 20 assigned to 15–19 and 40 and over to 40–44, as the guidance specifies; no other mapping is available.
* **Residence.** Births to resident mothers from registrations; the diverted births are in them already, and the exchange file reconciles
  deliveries to registrations exactly.
* **Vintage.** The latest vintage in the log for every year; no later vintage is due before the review.
* **Decomposition.** Symmetric three-factor weights (1/3, 1/6) close exactly to the 2,400 decline.
* **Rounding.** To the nearest ten; the answer is 180 births, 15%, below the half-way line.

## 9. Prompt sketch and deliverables

> Births in the region are down 11% in five years and the capacity review on the 3rd decides whether we close a maternity unit. Our chair is
> convinced the birth rate has fallen for good. Tell me how many of the lost births falling fertility rates account for, to the nearest ten, as
> the figure for the review paper. Send `births_decomposition.xlsx` and a chart `births_bridge.png`.

* `births_decomposition.xlsx` — the four constructions, the units sheet (ask A), the registered-women sheet (ask B) and the review
  reproduction (ask C).
* `births_bridge.png` — a waterfall from 21,800 to 19,400 births by size, age structure and rates, shown twice (shipped vintages and latest
  vintage), with the half-of-decline line marked on the rate bar and the 30–34 age group's revision annotated.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the six units, last year's caesarean rate. *Device:* a twin or triplet delivery is one
  maternity with two or three births, and the rate is per maternity, as the maternity data set documents; counting births inflates the rate at
  the two units with fetal-medicine services.
* **Ask B (device-carried).** For each area, women aged 15–44 registered with a family doctor. *Device:* patients who leave the area stay on
  practice lists until list cleaning, which the register marks with a last-validated date, as the list-maintenance guidance documents; counting
  all registrations overstates the three areas with student populations.
* **Ask C (validity).** The previous review's three published components and what each vintage pairing returns for them; and the figure under
  each of the four rung constructions.
* **Decoupling.** Clearing the vintage rule changes no figure in asks A or B.

## 11. Rubric arithmetic

6 units (ask A) + 14 areas (ask B) + 3 components × 3 pairings + 4 constructions (ask C) + the committed figure, the structure and size
components, and the closure decision + 5 named chart parts + 2 files ≈ 50 criteria.

## 12. World-building constraints

* Resident births 21,800 to 19,400; deliveries fell by 2,640, 240 more, all from five capped months at one unit.
* Rate component: 1,620 with shipped vintages, 1,700 with the original vintage at both ends, 1,020 with the latest at both ends.
* The census rebased base-year women aged 30–34 up 6% region-wide (9% in L-07, 1% in L-11).
* L-07 and L-11 identical on every shipped base-year column.
* Multiple-birth maternities and list-cleaning dates touch no registration or population-estimate cell.

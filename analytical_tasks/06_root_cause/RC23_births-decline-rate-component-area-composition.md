# RC23 — How many of the region's lost births falling fertility rates account for, filed before the maternity network decides on a unit closure

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Demographic & Social Science · fertility and maternity service planning |
| Mirrors | Volume declines split into per-capita behaviour and base size (orders = customers × order rate at Amazon, impressions = users × sessions at Meta), where users move between segments with different rates and the platform-wide rate falls with no segment's behaviour changing |
| Decision shape | One figure committed at a date (a component): the rate component of the five-year births decline, filed at the capacity review on the 3rd |
| Committed call | Births lost to falling age-specific fertility rates over five years, to resident mothers, to the nearest ten |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · E15 (the quiet second trap: past the loud fertility-rate reading and the capacity cap, the region's age-specific rates fall partly because women of peak childbearing age moved into the low-fertility city, a shift the area grain books to structure), with E14 (a binding limit applied in the figure: the units' registered capacity) at rung 1 |
| Gate G mechanism | decomposition_attribution, with confirm_surface_read support |
| Measured traps engaged | #11 beats the headline trap, misses the quiet one · #10 notes a binding limit as a risk · #14 coarsens the segment it was asked about |
| Calibration form | Revision log: every published vintage of the female population estimates by age and area, the provisional and final birth registrations, and the network's two previous reviews |
| Driving force | The symmetric decomposition on the region's births and women by age puts 1,320 of the 2,400 lost births on falling age-specific rates, over half. Over the five years women aged 25–34 moved from the rural east, where rates are high, into the city, where they are a third lower, so the region's rate at each age fell though within each area it barely moved. Read within the 14 areas, with the move between areas booked to structure, rates account for 960 births, and the unit stays open. |

## 1. Situation

Births to mothers living in a region fell 11% over five years, from 21,800 to 19,400. The maternity network's finance director calls it a permanent fall
in fertility and wants to close one of six units; the network's planning guidance closes a unit only if falling fertility rates account for at least
half of the five-year decline in births to resident mothers. The units' own delivery counts fell further than residents' births, because one unit hit
its registered capacity this year and diverted mothers to neighbouring networks. The city's university and service jobs grew over the period while
the rural east lost its two largest employers.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: registrations by residence, delivery counts by unit, the capacity register, the exchange file of births
  across network boundaries, and the estimates of women by area and age. The region's age-specific rates did fall. Nothing is overturned; the
  component is measured where the rates live.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the finance director's view, the planner's and the licensed basis. The textbook decomposition on the region's women
  still puts rates above half, and nothing in the pack reads rates within areas.
* **Instrument repair.** None suspect. The estimates ship as one vintage, the latest, census-rebased for both years; the registrations are
  final; the capacity register and the exchange file are complete. Every rung reads complete, current files, so rung 0 stays at 2,640, rung 1
  at 2,400 and rung 2 at 1,320; none returns 960. The decisive construction reads the same files at a finer grain: no repair of any record moves
  a woman back to the area she left.
* **Lens swap.** The naive decomposition reads rates across the region; the answer reads them within each area and books the move between areas
  to structure: different rates for a population that moved.

## 3. The driving force

A strong solver discards the "fertility crisis" reading at once: a total fertility rate is standardised for age and cannot explain a count of
births. It uses births to resident mothers, as the guidance says, rather than the units' deliveries, which fell further because one unit's
registered capacity bound for five months and 240 resident mothers delivered elsewhere. It runs the symmetric three-factor decomposition
(population size, age structure, age-specific rates) on the region's births and women by age, and it reproduces both of the network's previous
reviews to the birth. Rates come out at 1,320 of the 2,400 lost births, 55%, and the closure proceeds. Over these five years women aged 25–34
moved from the rural east, as its employers closed, into the city, where women of every age have a third fewer births. The region's rate at each
age fell because more of its women now live in the city, while within each area rates fell 4–6%. Read within the 14 areas, with the change in
where each age group lives booked to structure, rates account for 960 births, 40%, and 360 births move to the population's redistribution.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The units' delivery counts, the whole fall read as falling fertility, as the total fertility rate suggests | 2,640 births (+175%) | It is the network's own count, read the way the national commentary reads it | The capacity register: one unit's registered cap bound for five months and diverted 240 resident mothers out of the network |
| 1 | Births to resident mothers, the cap's diversions restored, still read as falling fertility | 2,400 (+150%) | The guidance's own population, every birth to a resident counted | A rate standardised for age cannot explain a count: size and age structure have to be separated from rates |
| 2 | Three-factor symmetric decomposition (size, age structure, age-specific rates) on the region's births and women by age | 1,320 (+38%) | The headline trap beaten: the textbook decomposition, closing exactly and reproducing both previous reviews | The estimates by area: women aged 25–34 rose 15% in the city and fell 18% in the rural east, where age-specific rates are half as high again |
| 3 | **Decisive:** the decomposition at the grain of area and age, the change in where each age group lives booked to structure and rates read within areas | **960 births** | — | — |

* **Figure shape.** Every correction walks the figure down (−9%, −45%, −27% per step), and the answer is the minimum cell; every rung but the
  last puts rates over half and closes a unit the answer keeps open.
* **Partial correction priced (L3).** A solver who suspects the move but decomposes at the area grain with crude birth rates, births per woman
  aged 15–44, lets the city's younger age profile pass for higher fertility and lands at 1,380 (+44%). One who books the shift between areas
  over all women aged 15–44 rather than within each age group moves part of the age-structure effect into it and lands at 560 (−42%). Both are
  further from the answer than rung 2.
* **Grid.** Births (deliveries, residents) × method (all to rates, regional decomposition, area decomposition) gives six cells: 2,640, 2,400,
  1,450, 1,320, 1,230 and 960. The nearest wrong cell is 1,230 (+28%), the area decomposition on deliveries, which still puts rates over half of
  the residents' decline.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The guidance names the population and a symmetric decomposition, and the estimates carry each area's women by age. No
   document says women moved between areas of different fertility or that rates are read within areas.
2. **Corpus blind for a computable reason.** *In both previous review periods the region's women in every age group were spread across the 14
   areas in the same shares within half a point, so the regional and the area decompositions return the same rate component, to the birth, on
   every vintage of both reviews.* The log certifies the regional decomposition and the latest vintage, and cannot see the move.
3. **No arithmetic symptom.** Both decompositions close exactly to the 2,400 decline; areas sum to the region in every vintage.
4. **Not a row predicate.** The redistribution component sets each age group's women against their areas at both dates and each area's rates at
   both dates, a symmetric decomposition over 14 areas × 6 age groups.
5. **The enumeration is arithmetic.** No column carries births lost to the move; 360 come out of the rebuilt decomposition.
6. **No cutover date.** Women moved to the city year by year as jobs moved; the dated event (the capacity cap this year) is the rung-0 trap.
7. **Survives deletion.** With every voice gone, the regional decomposition still gives 55% to rates.

## 6. The calibration corpus

* **Form.** The revision log: every vintage of the female population estimates by area and five-year age group for the last eight years, with
  publication dates; provisional and final registrations by residence; and the network's two previous five-year reviews with their published
  components.
* **What it certifies.** The symmetric decomposition (both reviews' components reproduced to the birth on the vintages then current), the latest
  vintage as the census-rebased basis for both years, and final registrations within 0.3% of provisional ones.
* **What it is blind to.** The move between areas (above).
* **Twin pair.** Women aged 25–29 and 30–34 had identical regional births, women and changes in regional age-specific rates over the five years.
  Their rate components at the area grain were 240 and 115 births (2.09×): the 25–29s moved to the city, the 30–34s mostly stayed where they
  were. Only the area decomposition separates them.
* **Resemblance points at the decoy.** The region's age-specific rates fell like the national rates, and the national commentary attributes
  the national decline mostly to rates.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The planning guidance: a unit closes only if falling fertility rates account for at least half of the five-year decline in
  births to resident mothers, by symmetric decomposition. The capacity register.
* **Empirical pins.** The latest vintage at both ends and the symmetric weights, from the previous reviews.
* **Voices.** The finance director: "The birth rate is falling and it isn't coming back." The network planner: "Our delivery counts tell the
  whole story; we don't need anyone else's figures."
* **Licensed wrong basis.** The guidance records that the national statistics office's commentary attributes regional changes to the total
  fertility rate and will be presented at the review.

## 8. Determinism by construction

* **Ages.** Births under 20 assigned to 15–19 and 40 and over to 40–44, as the guidance specifies; no other mapping is available.
* **Residence.** Births to resident mothers from registrations; the diverted births are in them already, and the exchange file reconciles
  deliveries to registrations exactly.
* **Areas.** The 14 areas of the latest vintage, with boundaries unchanged over the five years; every area-age cell has at least 400 women.
* **Decomposition.** Symmetric weights; at the area grain the four factors (size, age structure, distribution across areas within age, rates)
  close exactly to the 2,400 decline.
* **Rounding.** To the nearest ten; the answer is 240 births, 10 points, below the half-way line.

## 9. Prompt sketch and deliverables

> Births in the region are down 11% in five years and the capacity review on the 3rd decides whether we close a maternity unit. Our chair is
> convinced the birth rate has fallen for good. Tell me how many of the lost births falling fertility rates account for, to the nearest ten, as
> the figure for the review paper. Send `births_decomposition.xlsx` and a chart `births_bridge.png`.

* `births_decomposition.xlsx` — the four constructions, the units sheet (ask A), the registered-women sheet (ask B) and the review
  reproduction (ask C).
* `births_bridge.png` — a waterfall from 21,800 to 19,400 births by size, age structure, redistribution across areas and rates, with the
  half-of-decline line on the rate bar and an inset map of the change in women aged 25–34 by area.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the six units, last year's caesarean rate. *Device:* a twin or triplet delivery is one
  maternity with two or three births, and the rate is per maternity, as the maternity data set documents; counting births inflates the rate at
  the two units with fetal-medicine services.
* **Ask B (device-carried).** For each area, women aged 15–44 registered with a family doctor. *Device:* patients who leave the area stay on
  practice lists until list cleaning, which the register marks with a last-validated date, as the list-maintenance guidance documents; counting
  all registrations overstates the three areas with student populations.
* **Ask C (validity).** The two previous reviews' published components and what the regional and the area decompositions return for them; and
  the figure under each of the four rung constructions.
* **Decoupling.** Clearing the area decomposition changes no figure in asks A or B.

## 11. Rubric arithmetic

6 units (ask A) + 14 areas (ask B) + 2 reviews × 3 components × 2 decompositions + 4 constructions (ask C) + the committed figure, the
structure, redistribution and size components, and the closure decision + 5 named chart parts + 2 files ≈ 50 criteria.

## 12. World-building constraints

* Resident births 21,800 to 19,400; deliveries fell by 2,640, 240 more, all from five capped months at one unit.
* Rate component: 1,320 at the regional grain, 960 at the area grain, 360 moved to redistribution. Partials: crude rates by area 1,380;
  redistribution over all women 15–44 560; grid cells 1,450 (deliveries, regional) and 1,230 (deliveries, area).
* Women aged 25–34: city +15%, rural east −18%; the rural east's age-specific rates half as high again as the city's; within-area rates fell
  4–6%.
* Previous review periods: every age group's area shares stable within half a point.
* The 25–29 and 30–34 groups identical on regional births, women and rate change.
* Multiple-birth maternities and list-cleaning dates touch no registration or estimate cell.

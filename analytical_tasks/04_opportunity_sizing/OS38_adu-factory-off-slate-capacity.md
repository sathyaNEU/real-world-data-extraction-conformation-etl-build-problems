# OS38 — What capacity the backyard-home factory commits to, when every size the investors priced fails the fund's own tests

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Supply Chain & Logistics · manufacturing capacity planning for prefabricated housing |
| Mirrors | Sizing a capacity commitment when every option the stakeholders priced fails policy and the right size is off the menu (data-centre build-outs where the vendor's standard pod sizes all miss utilisation targets, fulfilment-centre sizing between catalogue designs, cloud reservations between offered tiers) |
| Decision shape | Which of N gets one scarce thing, with the sizing graded: one factory capacity is committed this round |
| Committed call | The factory capacity in units a year, and the year-3 prefab orders it runs on |
| Gap · Pattern | Gap 3 (objective) · E13 (the admissible capacity is off the investors' slate), with E20 below it (combined-project permits reach their parcel only through the project file) |
| Gate G mechanism | binding_constraint, with forecasting |
| Measured traps engaged | #9 picks from the offered options when none passes · #18 joins only on the visible key · #15 follows the requester's hunch over the rule |
| Calibration form | Gold-standard verification subsample: the city's completion verification sample, 900 ADU permits from 2017–2024 drawn at random, field-verified and linked to their parcels |
| Driving force | Once the forecast is right (1,300 prefab orders in year 3, 2,180 in year 5), none of the three capacities the investors priced passes the fund's tests: 1,000 drowns in backlog, and 2,000 and 4,000 run under 70% in year 3. The investment policy admits any multiple of 250 units, and exactly one, 1,750, passes both. The forecast itself needs the ADU permits filed under combined projects, which reach their parcel only through the project file. |

## 1. Situation

A prefab manufacturer of backyard homes (ADUs) is building a factory to serve one city, and its board commits a capacity this round
because the land option expires. The investors' term sheet prices three sizes: 1,000, 2,000 and 4,000 units a year. The fund's investment
policy requires year-3 utilisation of at least 70% and year-5 orders no more than 130% of capacity, and admits any capacity in multiples
of 250 units up to the site's 5,000. The city's permit file, the assessor roll and a field-verification sample are in the pack. The lead
investor prefers 2,000.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the permits, the parcel roll, the project file, the verification sample and the term sheet's
  prices. The investor's preference is a belief and the slate is a menu, and neither is a wrong number. The difficulty is that the right
  answer is not on the menu.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the investor's preference and every voice. The term sheet still lists three capacities, and testing each
  against the policy still leaves none standing.
* **Instrument repair.** Perfect permit data makes the forecast exact, which is what makes every slate option fail. A better instrument
  sharpens the trap.
* **Lens swap.** The answer is a different object, a capacity outside the priced set, and no change of lens on the slate reaches it.

## 3. The driving force

A strong solver discards a citywide permit rate for hazards by lot-size and value band on each band's remaining parcels. It joins permits
to parcels through the project file, so ADUs filed under combined projects are counted, and converts permits to completed units at the
verification sample's rate. The forecast it reaches is right: 1,300 prefab orders in year 3 and 2,180 in year 5. Then it tests the slate.
1,000 units carries a year-5 backlog of 218%. 2,000 runs at 65% in year 3 and 4,000 at 33%. Faced with three failures, the solver files
the least-bad option, 2,000, as an exception, or reports that no option qualifies. The policy's general section admits any multiple of 250
units. The admissible band is 1,677 ≤ capacity ≤ 1,857, and exactly one multiple of 250 lies in it.

## 4. The ladder

| Rung | Construction | Names (capacity) and year-3 orders | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Last three years' citywide ADU permits per eligible parcel × all eligible parcels × the term sheet's 15% prefab share; test the slate | A, 4,000 (77.5% in year 3); 3,100, +138% | The standard market-sizing build and the investors' own share assumption | Parcels that already have an ADU cannot add one, and hazards run from 0.4% to 2.6% a year across lot-size and value bands |
| 1 | Band hazards on each band's remaining parcels, permits joined to parcels on the APN column | B, 1,000 (76.0% in year 3); 760, −41.5% | Segment hazards on a shrinking risk set, the right forecasting method | The permit data guide: ADUs filed under combined projects carry only a project number, and 31% of 2022–2024 ADU permits reach a parcel only through the project file |
| 2 | Hygiene: permits linked through the project file and converted to completed units at the sample's rate; no slate option passes, so the least-bad one is filed | C, 2,000 (65.0%, an exception); 1,300 | The forecast is now exact, and the exception is flagged honestly | The investment policy admits any capacity in multiples of 250 units |
| 3 | **Decisive:** test every admissible capacity; only 1,750 meets both tests | **E, 1,750 (74.3% in year 3; year-5 orders 125% of capacity); 1,300** | — | — |

* **The answer.** 1,750 units a year, running on 1,300 prefab orders in year 3.
* **Position table.** 1,750 is on no slate, so no slate-bound rung can name it. Each rung names a different capacity: 4,000, 1,000, 2,000,
  1,750.
* **Margins.** At 1,750, year-3 utilisation clears 70% by 4.3 points, and year-5 orders sit 5.4 points under 130%. The nearest admissible
  rivals fail by wide margins: 1,500 carries 145% of year-5 orders and 2,000 runs at 65%.
* **Partial correction priced (L3).** Every half-opened search lands on a wrong capacity. Searching off the slate only in the term
  sheet's 500-unit steps tests 1,500 (year-5 orders at 145% of capacity) and 2,500 (52% in year 3), finds neither passes, and files 2,000
  as the exception, 14.3% above the answer and 5 points under the utilisation test. Solving year-3 utilisation for exactly 70% gives
  1,857, 6.1% above the answer and not a multiple of 250, so it is not admissible.
* **Grid.** Forecast (rung 0, rung 1, exact) × choice set (slate, admissible) = 6 cells. Every non-answer cell names a wrong capacity:
  rung 0's forecast with the full set passes everything from 3,000 to 4,250, and the policy's "largest passing" rule then picks 4,250.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere as a choice.** The admissibility clause sits in the policy's general section. The term sheet prices three sizes and
   nothing else, and no document puts the clause next to the slate.
2. **No corpus nominates it.** The verification sample certifies the forecast. The off-slate capacity is a property of the policy and the
   forecast together, and no closed case contains it.
3. **No arithmetic symptom.** The forecast reconciles to permits, parcels and the sample. Every slate test is computed correctly and fails
   honestly.
4. **Not a row predicate.** The answer is an interval, 2,180 ÷ 1.30 ≤ capacity ≤ 1,300 ÷ 0.70, intersected with a lattice the policy
   defines.
5. **The enumeration is arithmetic.** Which capacities pass is computed from two forecasts and two thresholds, and no file lists 1,750.
6. **No cutover date.** The land-option deadline forces the decision but no outcome steps.
7. **Survives deletion.** Removing the investor's preference leaves the slate and the policy exactly as they were.

## 6. The calibration corpus

* **Form.** 900 ADU permits from 2017–2024, drawn at random and field-verified as built and occupied, built and vacant, or abandoned, each
  linked to its parcel through the project file.
* **What it certifies.** The completed-unit rate (82% of permits become units) and the project-file link: every sampled combined-project
  permit maps to exactly one parcel. A solver who back-tests rung 2's forecast against the sample is confirmed.
* **What it cannot show.** Anything about which capacity is admissible (above).
* **Twin pair.** Bands L2-V3 and L3-V2 are identical on every assessor-roll column a lookup reaches: parcel counts, lot sizes, values and
  ADUs on record by APN. Their 2022–2024 hazards differ 2.0× (1.1% against 2.2%) once combined-project permits are linked, because L3-V2's
  owners build ADUs alongside remodels. The APN join cannot separate them.
* **Resemblance points at the decoy.** By the investors' own comparables, the city resembles the region where the company's last factory
  runs at 2,000 units.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The policy sets the two tests, admits capacity in multiples of 250 up to 5,000, selects the largest capacity that passes
  both, and rules out deferral this round. The term sheet sets the prefab share at 15%. Forecasts use the last three complete years.
* **Empirical pins.** The completed-unit rate and the project-file link come from the verification sample.
* **Voices.** The lead investor: "2,000 is the right scale for a city this size." The company's founder: "Backyard homes are taking off
  everywhere; build big."
* **Licensed wrong basis.** The term sheet records that the co-investor's adviser evaluates only the three priced sizes and will present
  them at the board.

## 8. Determinism by construction

* **Hazard window.** The policy pins the last three complete years, and band hazards are stable across them to within 0.1 points.
* **Risk set.** Parcels leave the risk set in the year their ADU completes, which the verification sample dates.
* **Thresholds.** The answer clears both tests by more than 4 points, so no rounding of utilisation moves it.
* **Unique pass.** Under the exact forecast no other multiple of 250 passes, so the "largest passing" rule is inert at the answer.
* **Maturity.** 2024 permits are issued and final, and the project file is complete through 31 December.

## 9. Prompt sketch and deliverables

> The land option on the factory site expires this month, so the board commits a capacity this round, and our lead investor favours 2,000
> units a year. Tell me the capacity we commit to, in units a year, and how many prefab orders it will run on in year three, in a sentence
> for the board resolution. Send `factory_capacity.xlsx`, a chart `capacity_tests.png`, and a one-page `board_resolution_note.pdf`.

* `factory_capacity.xlsx`: the forecast build by band under the three forecast rungs, every admissible capacity tested, the plan-check
  sheet (ask A) and the reassessment sheet (ask B).
* `capacity_tests.png`: year-3 utilisation and year-5 order ratio against capacity from 500 to 5,000 as two curves, with the 70% and 130%
  lines drawn, the admissible band shaded, the three slate options marked as points and the committed capacity labelled.
* `board_resolution_note.pdf`: the committed capacity, the year-3 orders and why each priced option fails.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the nine lot-size × value bands, the median number of plan-check correction cycles
  per 2024 ADU application, and the share needing three or more. *Device:* each discipline's review (structural, fire, planning) is a
  separate row, and one cycle is one round across all disciplines, per the plan-check guide. Counting rows as cycles triples them.
* **Ask B (device-carried).** For each band, the median change in assessed value in the year an ADU completes. *Device:* new construction
  posts to a supplemental roll row, not to the base value, per the assessor's guide. Reading only the base roll shows no change for 70% of
  completions.
* **Ask C (validity).** Year-3 and year-5 orders under each of the three forecast rungs, and each slate option's two test results under
  the exact forecast.
* **Decoupling.** Clearing the admissible-set search changes no figure in asks A or B, and neither touches the forecast's parcels or permits.

## 11. Rubric arithmetic

9 bands × 2 (ask A) + 9 (ask B) + 3 forecasts × 2 + 3 slate options × 2 tests (ask C) + the committed capacity, year-3 orders, year-3
utilisation and the year-5 ratio + 5 named chart parts + 3 files ≈ 51 criteria.

## 12. World-building constraints

* Exact forecast: 1,300 prefab orders in year 3 and 2,180 in year 5. Rung 0 gives 3,100 and 3,600, and rung 1 gives 760 and 1,250.
* Band hazards 0.4% to 2.6% a year. 31% of 2022–2024 ADU permits carry only a project number. 82% of permits become units.
* Under the exact forecast the admissible band is 1,677 to 1,857 and contains only 1,750. The slate fails as stated: 1,000 at 218% of
  year-5 orders, 2,000 at 65% and 4,000 at 33% in year 3.
* Bands L2-V3 and L3-V2 are identical on every assessor-roll column.
* Plan-check rows and supplemental rolls never touch permits, the project file or the base roll used for bands.

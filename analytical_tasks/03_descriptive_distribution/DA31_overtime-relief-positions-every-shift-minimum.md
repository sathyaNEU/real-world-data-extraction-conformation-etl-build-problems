# DA31 — Where 60 overtime-relief positions go, when a unit's double-time regime lifts only once every shift slot is covered

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Policy & Education · public-sector workforce and payroll |
| Mirrors | Capacity allocation where a premium regime lifts only at full coverage (on-call premiums for SRE rotations, minimum-crew rules in warehouses and airline reserve), so spreading headcount by spend buys no relief anywhere |
| Decision shape | An allocation under a cap: 60 funded positions placed across eight 24/7 units |
| Committed call | Positions per unit, and the overtime cost the allocation avoids next fiscal year, to $0.1 million |
| Gap · Pattern | Gap 4 (rule) over Gap 3 (objective) · S5 (a premium that lifts only when every sub-unit clears) with Pattern B (the revision log pins the minimum law), and the segment kept at the staffing standard's grain at rung 1 |
| Gate G mechanism | binding_constraint, with method_or_model_selection |
| Measured traps engaged | #14 coarsens the segment it was asked about · #4 never tests its reading against the control · #1 reports a failed back-test, ships anyway |
| Calibration form | Retry or revision log: the payroll revision log for 26 closed pay periods, recording each unit-period whose overtime was re-rated from time-and-a-half to double time |
| Driving force | A unit's overtime is re-rated to double time in any pay period where one shift slot fell below its minimum on any day. Staffing totals and averages do not decide it; the worst day of the worst slot does. That law is a minimum over sub-units, recoverable only from the revision log. Relief therefore comes in whole units: a position avoids the premium only as part of the block that brings every slot of one unit to minimum. |

## 1. Situation

The City Council funded 60 overtime-relief positions for next fiscal year. The resolution places them in units and scores the allocation
on overtime cost avoided. Eight 24/7 units across four titles are eligible: three detention centres, two dispatch floors, an EMS station
group and two sanitation garages. The pack holds a year of payroll records, the shift rosters, the staffing standard with each unit's minimum
per shift slot, the union contract, the payroll revision log, and the budget office's title-level overtime table.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: pay records, rosters, minimums, the revision log and the title table. Nobody proposes an allocation
  and nothing is overturned. The difficulty is what a position has to accomplish before it relieves the double-time premium.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the title table and both voices. Greedy placement by overtime displaced, built from payroll and rosters,
  still clears no unit.
* **Instrument repair.** No file is suspect: payroll, rosters, minimums and the revision log are complete for the 26 closed periods, and
  the title table is a correct summary at a coarser grain. Recording every shift to the minute moves no rung: rung 0 still avoids $8.7M,
  rung 1 $9.2M and rung 2 $8.6M, none clearing a unit. The re-rating law, a minimum over slots and days, is recovered by reproduction
  from complete records, and the allocation is next year's.
* **Lens swap.** The naive allocation buys hours of overtime wherever they are dearest. The answer buys complete coverage in three units,
  a different set of units relieved in a different way.

## 3. The driving force

A strong solver moves from titles to units, prices the overtime each position displaces, notices that some unit-periods pay double time,
and models the premium. The natural model says a unit is critical when its rostered hours fall short of its required hours, and the
solver packs positions to close those aggregate gaps. The revision log refuses that law in 61 of 208 unit-periods. Re-rating follows the
worst day of the worst slot: a dispatch floor with one weekend overnight slot two dispatchers short on a single day pays double time on the
whole period's overtime. Closing a unit takes as many positions as its slots' worst-day shortfalls add up to, often twice its aggregate
gap. With 60 positions, only North Detention, Borough East Dispatch and Riverside Dispatch can be cleared together. Clearing them avoids
$6.2 million of premium that no spreading rule touches.

## 4. The ladder

| Rung | Construction | Allocates | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Pro rata to each title's overtime spend from the budget office's table, spread by headcount | 27 / 13 / 12 / 8 across the four titles; clears none; $8.7M | The Council's own spend measure | The staffing standard sets minimums by unit and slot, not by title |
| 1 | Unit grain: positions placed greedily on overtime displaced per position, within each unit's overtime | West 28, North 16, South 16; clears none; $9.2M | Priced in dollars at the grain positions are deployed | Payroll: 31% of unit-periods paid overtime at double time |
| 2 | Premium modelled with a unit critical when rostered hours fall short of required hours; positions packed to close aggregate gaps | North 16, Harbour 20, West 15, Ridge 9; claims $17.0M, clears none, avoids $8.6M | Every dollar has a model, and the knapsack is exact | The revision log: the aggregate law misses 61 of 208 unit-periods |
| 3 | **Decisive:** critical whenever any slot falls below minimum on any day; positions packed to clear every slot | **North 18, Borough East 24, Riverside 15, West 3; avoids $14.6M** | — | — |

* **Allocation shape.** No intermediate rung clears a unit or names the answer's set. The true avoided cost runs $8.7M, $9.2M and $8.6M
  against $14.6M, so the nearest rung sits 37% below.
* **Partial correction priced (L3).** A solver who adopts the slot law but measures each slot's shortfall on its average day understates
  Borough East (14 against 24) and Riverside (9 against 15). It packs North, Borough East, West and Riverside on needs that do not clear
  them, clears none, and avoids $8.9M, inside the band where every allocation that clears nothing lands.
* **Grid.** Grain (title or unit) × status law (none, aggregate, slot average day, slot worst day) = 8 cells. Seven clear no unit and land
  between $8.6M and $9.2M. Only unit grain with the worst-day slot law clears three units.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The union contract says double time applies "in a period of critical staffing as the Department determines". The
   staffing standard lists minimums without linking them to pay.
2. **Pattern B, a law with a flat-loss field of rivals.** The worst-day slot law reproduces 208 of 208 re-ratings at zero tolerance. The
   aggregate law reproduces 147, the average slot ratio 155, and a share-of-short-slots rule peaks at 171 at every cut from 2% to 9%, a
   flat loss curve. Every rival misses toward too few critical periods, so none reconciles in total either.
3. **No arithmetic symptom.** Rosters tie to scheduled hours, overtime lines tie to payroll, and the revision log ties to the pay-rate
   column.
4. **Not a row predicate.** It needs each slot's worst day per period, a minimum against the slot's standard, a unit-level any-short test,
   and clearing needs summed across slots.
5. **The enumeration is arithmetic.** Which units clear at which headcount is computed; no column states a clearing requirement.
6. **No cutover date.** Status turns on and off period by period with nothing stepping.
7. **Survives deletion.** With every voice removed, the aggregate model still packs the wrong units.

## 6. The calibration corpus

* **Form.** The payroll revision log: 208 unit-periods (8 units × 26 closed pay periods), each marked re-rated or not, with the re-rated
  amount.
* **What it certifies.** That double time exists and how large it is, which takes a solver to rung 2.
* **What pins the law.** Only the worst-day slot minimum returns every re-rating. In all 61 unit-periods the aggregate law misses, the
  aggregate hours were met and the period was still re-rated, each time because one slot fell short on one day.
* **Twin pair.** West Detention and South Detention match on headcount (412), scheduled hours, overtime hours, average slot staffing
  (0.96) and wage. West was re-rated in 14 periods and South in 7 (2.0×): West's shortages fall in one overnight slot and South's are
  spread thinly across slots.
* **Resemblance points at the decoy.** By aggregate gap, Harbour EMS looks like the units the log re-rates most often.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The Council resolution: 60 positions, placed in units, scored on overtime cost avoided next fiscal year on this year's
  overtime base. The staffing standard: the eight units and each slot's minimum. The union contract: double time in critical periods.
* **Empirical pins.** The status law, from the revision log.
* **Voices.** The budget director: "Put the positions where the overtime dollars are; that is what the Council funds." The union liaison:
  "Every title is short. Spreading them is the only fair way."
* **Licensed wrong basis.** The budget memo records that the Council's finance committee allocates relief positions pro rata to each
  title's overtime spend and will review the allocation on that basis.

## 8. Determinism by construction

* **Slots.** Each unit has 21 weekly slots (3 shifts × 7 days), and one full-time position covers five slot-shifts a week.
* **Worst day.** Rosters are complete for every day, so each slot's worst-day staffing is a single number.
* **Optimum.** The best clearing set leads the next ({North, Harbour}, $5.5M) by $0.7M of premium, and the three leftover positions go to
  West, whose displacement value per position ($155k) is highest.
* **Base.** The resolution scores next year on this year's overtime hours, so no forecast convention enters.

## 9. Prompt sketch and deliverables

> Council funded sixty relief positions and the budget director wants them where the overtime dollars are. I need the allocation by unit
> and the overtime cost it avoids next year, to the nearest $0.1 million, as the table and sentence that go in the budget memo. Send
> `relief_allocation.xlsx`, a chart `unit_clearing.png`, and a one-page `allocation_memo.pdf`.

* `relief_allocation.xlsx` — the allocation build, the pay-distribution sheet (ask A), the headcount sheet (ask B) and the law table
  (ask C).
* `unit_clearing.png` — for each unit, positions needed to clear every slot against premium at stake, with the 60-position budget line, the
  three cleared units highlighted and the twin detention centres annotated.
* `allocation_memo.pdf` — the committed allocation, its avoided cost, and why each rival allocation buys less.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the four titles, the 10th, 50th and 90th percentiles of annualised base pay. *Device:*
  pay basis varies (per annum, per hour, per day) and partial-year records must be annualised as the payroll dictionary specifies; gross
  pay drags the 10th percentile down in the two high-turnover titles.
* **Ask B (device-carried).** Distinct employees per title over the year. *Device:* inter-agency transfers appear as two payroll records,
  and the HR transfer register links old and new employee numbers; counting records double counts 214 people.
* **Ask C (validity).** Re-ratings reproduced by each of the four status laws, and the true avoided cost of each rung's allocation.
* **Decoupling.** Clearing the slot law changes no figure in asks A or B.

## 11. Rubric arithmetic

4 titles × 3 percentiles (ask A) + 4 counts (ask B) + 4 laws and 4 allocations (ask C) + 8 unit allocations, the avoided cost and the
cleared set + 5 named chart parts + 3 files ≈ 42 criteria.

## 12. World-building constraints

* Clearing needs (positions) and premiums ($M): North 18/2.9, Borough East 24/2.2, West 31/2.0, Central 12/0.3, Harbour 40/2.6, Ridge 22/0.9,
  Riverside 15/1.1, South 31/1.6. Aggregate-law needs are 6 to 26 and always smaller.
* Displacement value per position ($k): West 155, North 152, South 150, dispatch 140, Harbour 135, garages 130, within each unit's
  overtime capacity (North 16, West 28, South 28).
* Revision log: 208 unit-periods, 64 re-rated; laws reproduce 208 / 171 / 155 / 147. West and South match on every visible column.
* Pay basis and transfers never touch a roster, a slot or a re-rating.

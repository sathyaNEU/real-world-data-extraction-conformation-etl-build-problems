# OS41 — Which basin gets the first reclaimed-water plant, when native effluent is reusable only on days nobody below the outfall is calling

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Economics · water markets and utilities |
| Mirrors | Sizing a supply that belongs to the seller only when no senior claimant downstream needs it (water-replenishment programmes at large cloud and data-centre operators that count return flows owed to the river, curtailable grid capacity sold without checking when the senior offtaker calls, marketplace inventory that a priority channel can claim on some days) |
| Decision shape | Which of N gets one scarce thing, with the sizing graded: the firm's first reclaimed-water plant goes to one of six basins |
| Committed call | The basin that gets the plant, and the effluent there that can lawfully be reused, in acre-feet a year to the nearest 1,000 |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · E01 (a reproduction-gated control set: the state's parallel-run determinations reproduce only when each outfall-day of native effluent is credited unless a call is active at a headgate below the outfall, a join from the call record through the rights register to the permit's river mile), with E29 below it (municipal effluent split by source water through each discharger's supplier and its decree) |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution |
| Measured traps engaged | #1 reports a failed back-test, ships anyway · #3 stops at a close but inexact match · #6 treats a mixed segment all one way |
| Calibration form | Parallel-run overlap: the state engineer's two-year parallel run of the old and new reuse accounting, publishing both determinations for 14 existing reuse projects |
| Driving force | Native-derived effluent may be reused only on days when no senior right below the outfall is calling for water. The firm's policy admits only a method that reproduces all 14 of the parallel run's new-method determinations. The old basin factor reproduces 10, an outfall's annual call share 12 and a basin's daily calls 12. Only crediting each outfall-day unless an active call's headgate lies downstream reproduces 14, and that needs the call record joined through the rights register to each permit's river mile. Shale Creek's city discharges below its calling ditches and its sugar factory only in winter, so 94% of its effluent is reusable, against 40% at its basin factor. |

## 1. Situation

A water-reuse company will build its first reclaimed-water plant next year in one of six river basins of a prior-appropriation state. It
buys treated effluent from dischargers and sells reclaimed water to industrial users, whose demand exceeds the available effluent in every
basin. The plant goes where the most effluent can lawfully be reused. For two years the state engineer ran the old and new reuse
accounting in parallel and published both determinations for the 14 existing reuse projects; from next year only the new accounting
applies. The firm's investment policy admits a sizing method only if it reproduces every new-method determination in that report. The
founder is sure Cinder River, the state's power-plant river, is the biggest water market.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the discharge reports, the supply decrees, the daily call record, the rights register and both sets
  of determinations. The founder is right that Cinder River moves the most water. Nothing reported is overturned. The difficulty is which
  effluent is owed downstream on which days.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the founder's view and every voice. The published basin factors still rank Sage River first and still
  reproduce every old-method determination.
* **Instrument repair.** No file is suspect. Discharge reports, supply decrees, the call record, the rights register and both sets of
  determinations are complete and current, and the basin factors are exactly what the old accounting used. Rungs 0, 1 and 2 still name
  Cinder River, Tunnel Creek and Sage River. Which outfall-days are owed depends on where another party's headgate sits on each day, which
  no file records and the reproduction recovers.
* **Lens swap.** The answer counts effluent-days that no right below the outfall needs, a different population from the effluent volume or
  its source.

## 3. The driving force

A strong solver refuses to count cooling returns and splits effluent by source through each discharger's supplier, because the statute lets
transbasin and nontributary effluent be reused to extinction. It then credits native-derived effluent the way the state's published basin
factors do, which reproduces every old-method determination and names Sage River. From next year the state uses its new daily accounting,
and the parallel run's new-method figures depart from the basin factor in four projects, all upward. Native effluent is owed to the river
only on days when a senior right below the outfall is calling. An outfall below every calling headgate owes nothing, and a discharger that
runs only in winter, when no right calls, owes nothing either. The rule needs each day's active calls from the call record, each calling
right's headgate river mile from the rights register, and each outfall's river mile from its permit. Shale Creek's city plant sits below
its basin's senior ditches and its sugar factory discharges from November to March. Its credit rises from 40% to 94% of its effluent.

## 4. The ladder

| Rung | Construction (acre-feet a year that can be reused) | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | All reported discharges, cooling returns included | A, Cinder River, 366,900 (2.37× Sage River) | The state's discharge reports, read as the market | The reuse statute: only effluent from transbasin or nontributary water may be reused to extinction; native effluent and once-through cooling returns belong to the stream |
| 1 | Effluent of dischargers whose supplier holds transbasin or nontributary decrees (permit → supplier → decree) | B, Tunnel Creek, 38,100 (2.34× Granite Fork) | The statute applied through the right join | The state engineer's determinations credit native effluent too, at one minus the basin's published call factor |
| 2 | Imported effluent plus native effluent × (1 − basin call factor) | C, Sage River, 58,132 (1.21× Tunnel Creek) | The state's own factors, reproducing every old-method determination | The parallel run: the basin factor reproduces 10 of the 14 new-method determinations, and all four misses under-credit |
| 3 | **Decisive:** native effluent credited day by day unless an active call's headgate lies below the outfall | **E, Shale Creek, 94,000 (1.17× Granite Fork)** (4th of 6 on rung 0) | — | — |

* **The answer.** Shale Creek, where 94,000 acre-feet a year of effluent can lawfully be reused.
* **Position table.** Shale Creek ranks 4th on rung 0, 6th on rung 1 and 4th on rung 2, and leads only rung 3. It is never 2nd. Rung
  leaders beat their runners-up by 2.37×, 2.34×, 1.21× and 1.17×.
* **Discriminator dominance.** Sage River carries a 1.45× lead into rung 3 (58,132 against 40,000). Its outfalls sit above every calling
  headgate and discharge evenly, so it keeps 1.00 of its value, while Shale Creek's rises 2.35×. The edge of 2.35× is 1.35 times the
  required 1.2 × 1.45 = 1.74.
* **Partial correction priced (L3).** Every half-built rule names a wrong basin. Crediting by the outfall's annual share of downstream-call
  days, location without timing, names Granite Fork, 80,200 against Shale Creek's 67,000 (1.20×). Crediting by the basin's daily calls,
  timing without location, names Cottonwood Wash, 79,100 against 67,000 (1.18×). Each half reproduces 12 of the 14 determinations.
* **Grid.** Cooling returns (counted, excluded) × native credit (full, none, basin factor, outfall annual share, basin daily calls,
  downstream-call days) = 12 cells. Every non-answer cell names Cinder River, Tunnel Creek, Sage River, Granite Fork or Cottonwood Wash.
  The nearest is full native credit without cooling returns, Sage River at 114,500 against Shale Creek's 100,000 (1.15×), reached by
  ignoring both the statute and the determinations.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The statute says native effluent belongs to the stream. The state engineer publishes determinations, not the
   accounting behind them, and no document says which days or which calls matter.
2. **The corpus pins the rule by reproduction (Pattern B).** Downstream-call days reproduce 14 of 14 new-method determinations to the
   acre-foot. The basin factor reproduces 10, the outfall's annual call share 12 and the basin's daily calls 12, and every miss
   under-credits, so each rival also fails the 14-project total. The reproducing rule is a construction: active calls by day, joined to
   their headgates' river miles through the rights register, compared with each outfall's river mile and weighted by its daily discharge.
3. **No arithmetic symptom.** Discharges tie to the permits, effluent splits sum to each plant's total, and the old determinations
   reproduce exactly under the basin factor.
4. **Not a row predicate.** Whether an outfall-day is owed depends on another party's call that day and on where that party's headgate sits,
   which no row of the discharge or call file holds.
5. **The enumeration is arithmetic.** No column says "owed downstream". Each basin's credit is summed over outfalls and days.
6. **No cutover date.** The new accounting's start is the dated decoy. The decisive fact is where outfalls and calls sit on each day, which
   the old accounting also faced and averaged away.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The state engineer's parallel-run report: 14 existing reuse projects, each with its old- and new-method determination for the
  same two water years, plus the daily discharge reports, the call record and the rights register those years cover.
* **What it certifies.** The source split (every project's imported effluent is credited in full under both methods) and the basin factors,
  which reproduce all 14 old-method determinations. A solver who back-tests rungs 1 and 2 against the old method is confirmed.
* **What it pins.** The new method, by reproduction (above). Ten projects discharge evenly above every calling headgate, where all four
  rules agree. Millrace discharges below its basin's callers, Kettle Bend between two calling ditches, Redwing Sugar only in winter, and
  Pinecrest mostly in May and June.
* **Twin pair.** Larkspur and Millrace, both in Sage River, are identical on every column a lookup reaches: effluent (6,200 acre-feet a
  year), native source, permit class, even daily discharge and old-method determination (2,976). Their new-method determinations are 2,976
  and 6,200, 2.08× apart, because Millrace enters the river below the senior ditch that calls and Larkspur above it.
* **Resemblance points at the decoy.** Sage River resembles the parallel run's largest projects on city size, source mix and basin factor,
  so a solver transferring their determinations by resemblance lands on Sage River.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The statute lets effluent from transbasin and nontributary water be reused to extinction and returns native effluent to
  the stream. Effluent takes its source from the discharger's supplier. Determinations use the last complete water year's daily records.
  The investment policy admits a sizing method only if it reproduces every new-method determination in the parallel-run report.
* **Empirical pins.** The new accounting's credit rule, from the parallel run; each basin's call days and outfall positions, from the call
  record, the rights register and the permits.
* **Voices.** The founder: "Cinder River moves more water than the rest of the state together." The company's water counsel: "Native return
  flows belong to the river, so count imported effluent and nothing else."
* **Licensed wrong basis.** The investment policy records that the project lender's engineer sizes supply on the published basin factors and
  will present that basis to the credit committee.

## 8. Determinism by construction

* **River positions.** No outfall lies within a mile of a calling headgate, so river-mile and reach ordering agree everywhere.
* **Overlapping calls.** A day is owed if any active call's headgate lies below the outfall; several calls on one day count once.
* **Source water.** Every supplier in the six basins draws on one source class, so no discharger's effluent needs a pro rata split.
* **Season.** Every call in the record falls between 1 April and 31 October, and Shale Creek's sugar factory discharges only from November
  to March.
* **Existing projects.** Effluent already committed to the 14 projects is excluded from every basin's volumes.
* **Rounding.** 94,000 acre-feet sits 500 from the nearest rounding boundary, and the water year is closed with final records.

## 9. Prompt sketch and deliverables

> Our first reclaimed-water plant goes into one of six basins next year, and our founder is convinced Cinder River is the biggest water
> market we have. Tell me which basin gets the plant and how many acre-feet a year of effluent we could lawfully reuse there, to the nearest
> thousand, in a sentence for the investment committee. Send `basin_reuse_case.xlsx`, a chart `reusable_effluent.png`, and a one-page
> `committee_memo.pdf`.

* `basin_reuse_case.xlsx`: the six basins under the four rung bases, the 14 reproductions under each rule, the water-court sheet (ask A)
  and the storage sheet (ask B).
* `reusable_effluent.png`: for each basin, effluent stacked as imported, native credited and native owed downstream, as paired horizontal
  bars under the basin factor and the downstream-call rule, the chosen basin highlighted and each basin's share of native effluent
  discharged on downstream-call days printed.
* `committee_memo.pdf`: the committed basin, its reusable effluent and why Sage River is not it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each basin, the water-right change applications filed in the last water year and the median
  days from filing to decree. *Device:* an amended application keeps its case number and adds a filing row, and one case is one
  application, per the water-court docket guide. Counting rows overstates applications by 30% in the two basins with contested changes.
* **Ask B (device-carried).** For each basin, reservoir storage on 1 April as a share of active capacity in each of the last five years.
  *Device:* the storage report gives total contents including dead pool, while the reservoir register lists active capacity, and usable
  storage is contents less dead pool, per the reservoir operations guide. Dividing total contents by active capacity overstates the share,
  above 100% at three reservoirs.
* **Ask C (validity).** Each basin's reusable effluent under each of the four rung bases, and the parallel-run reproduction counts for the
  basin factor, the outfall's annual call share, the basin's daily calls and the downstream-call rule (10, 12, 12 and 14 of 14).
* **Decoupling.** Clearing the downstream-call construction changes no figure in asks A or B.

## 11. Rubric arithmetic

6 basins × 2 (ask A) + 6 × 5 years (ask B) + 6 × 4 bases + 4 reproduction counts (ask C) + the committed basin, its reusable effluent and its
margin + 5 named chart parts + 3 files ≈ 81 criteria.

## 12. World-building constraints

* Acre-feet a year (cooling returns / imported effluent / native effluent / basin call factor): Cinder River 301,400 / 5,200 / 60,300 /
  0.50, Tunnel Creek 0 / 38,100 / 24,800 / 0.60, Sage River 40,200 / 6,100 / 108,400 / 0.52, Granite Fork 29,700 / 16,300 / 63,900 / 0.55,
  Shale Creek 0 / 0 / 100,000 / 0.60, Cottonwood Wash 19,800 / 3,900 / 75,200 / 0.58.
* Native effluent by outfall class: Cinder River, Tunnel Creek and Sage River discharge evenly above every calling headgate; Granite Fork
  evenly below them; Cottonwood Wash only in winter, above them; Shale Creek 10% evenly above, 45% evenly below and 45% in winter above.
* Rung leaders Cinder River, Tunnel Creek, Sage River and Shale Creek, with margins of 2.37×, 2.34×, 1.21× and 1.17×. Half-built rules
  name Granite Fork (1.20×) and Cottonwood Wash (1.18×), and all twelve grid cells name as stated.
* Parallel run: 14 projects; the four rules reproduce 10, 12, 12 and 14. Larkspur and Millrace are identical on every lookup column.
* Docket amendments and reservoir dead pool never touch discharges, decrees, calls or determinations.

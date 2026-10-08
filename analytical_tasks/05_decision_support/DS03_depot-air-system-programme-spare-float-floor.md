# DS03 — Which depot gets the truck air-system monitoring programme, when a prevented breakdown only saves a trip on days the spare float is gone

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Supply Chain & Logistics · fleet maintenance and distribution operations |
| Mirrors | Deciding where predictive maintenance pays when the cost of a failure depends on whether spare capacity absorbs it (Amazon delivery-station van fleets, airline spare-aircraft cover at outstations, cloud spare-host pools, rail rolling-stock spares) |
| Decision shape | Which of N gets one scarce thing: the vendor's single rollout crew and this year's 250 retrofit kits |
| Committed call | The depot that gets the rollout, and the net annual value it should bring, in € thousands to the nearest ten |
| Gap · Pattern | Gap 2 (population) over Gap 3 (objective) · S5, a floor that does not commute (a lost trip is a depot-day's excess of stood-down trucks over its spare float), with a binding kit allocation (#10) at rung 1 and a transported prevention rate (#13) at rung 2 |
| Gate G mechanism | binding_constraint, with decomposition_attribution |
| Measured traps engaged | #10 notes a binding limit as a risk · #13 validates on one population, applies to another · #7 uses the ready-made measure · #20 leaves the deciding comparison unstated |
| Calibration form | Prior-period close-out: last year's depot operations close-out (six depots × twelve months of air-system stand-downs, lost trips, tows and spare floats) with the daily stand-down log it was built from |
| Driving force | A trip is lost only on a day when more trucks are stood down than the depot holds in spare float, so a prevented stand-down is worth a trip only if it would have fallen on such a day. The close-out's lost-trip share per stand-down is correct, but it is an average over days the programme does not touch evenly. Highmoor's lost trips all fall on frost mornings, when air dryers freeze without warning and the model has no lead time. Fenwick, with one spare truck, saves a trip for almost every stand-down the model prevents. Only a day-by-day replay of the closed year, with exactly the stand-downs the alert back-test flagged in time removed, prices that. |

## 1. Situation

A national grocery distributor can put a vendor's air-system monitoring programme into one depot this year. The vendor runs one rollout
crew, and the supplier allocation register lists 250 retrofit kits. The model flags a truck for inspection before its air system fails.
The charter values the rollout on net annual value: avoided tow-and-roadside cost, plus avoided lost trips, less kit and inspection cost.
Six depots compete. Last year's close-out reports stand-downs, lost trips, tows and floats by depot and month. The vendor's back-test of
last year's telematics shows, for each stand-down, whether an alert fired at least three days before it. The vendor quotes 45% of
stand-downs prevented across its reference fleets. The fleet director wants the programme where the failures are.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct and no stakeholder read is overturned. That covers the close-out's stand-downs, lost trips
  and shares, the vendor's 45% (true of its reference fleets), the kit allocation and the alert back-test. The difficulty is that a
  prevented stand-down is worth a trip only on some days, and no depot-level average carries which.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the vendor's 45% and the director's view. Stand-downs priced at the close-out's own lost-trip share still name
  Kingsbridge, then Highmoor once the kits bind, and nothing fails a check.
* **Instrument repair.** No file the ladder uses is suspect: the close-out, the daily stand-down log, the alert back-test and the float
  register are complete and exact, and no field records which stand-downs cost a trip. Perfect telematics and records leave rung 0 at
  Kingsbridge, rung 1 at Ravensdale and rung 2 at Highmoor, Highmoor's frost failures still come without warning, and the day-by-day replay
  is still needed for Fenwick.
* **Lens swap.** The naive read prices every stand-down at the depot's average. The answer prices only the stand-downs the model removes,
  each on the day it would have fallen: a different population, valued at the depot-day grain.

## 3. The driving force

A strong solver prices prevented stand-downs at tow cost plus the close-out's lost-trip share, applies the 250-kit limit and replaces the
vendor's pooled rate with each depot's own alert-flagged share. Each step is competent, and Highmoor wins on its 33.5% lost-trip share.
But a lost trip is the day's excess of stood-down trucks over the float. Highmoor holds three spare trucks. 144 of its 146 lost trips fell on 24 frost mornings, each with nine frozen dryers, and no alert precedes a frozen dryer. The gradual leaks the model does catch fall on Highmoor's ordinary days, when the float covers them. Replayed day by day, its prevented stand-downs save 2 trips, not the 59 the share implies. Fenwick holds one spare truck and its stand-downs are almost all gradual leaks. The replay saves 49 of its 50 lost trips, more than its share credits. The value is a sum of per-day floors and does not commute with the depot totals.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Vendor's 45% × stand-downs × (tow and roadside cost + close-out lost-trip share × trip cost), kits on every truck | A, Kingsbridge hub (€1,030k) | The vendor's rate and the depot's own record, a complete-looking value | The supplier allocation register: 250 kits, so 250 of Kingsbridge's 600 trucks |
| 1 | The 250 kits applied in the figure (#10) | B, Ravensdale (€803k) | The binding limit is respected and the cost is per equipped truck | The alert back-test: 7% of Ravensdale's stand-downs had an alert three days ahead (debris ruptures on quarry routes) |
| 2 | Each depot's alert-flagged share in place of the vendor's 45% (#13), lost trips still at the close-out share | C, Highmoor (€564k) | Prevention is now measured on the depot's own failures, not on the vendor's fleets | The daily stand-down log: Highmoor's lost trips fall on its 24 frost mornings, none of them alert-preceded |
| 3 | **Decisive:** replay the closed year day by day, remove the flagged stand-downs of equipped trucks and recompute each day's lost trips as the excess over float | **E, Fenwick (€494k)** (4th of 6 on rung 0) | — | — |

* **Position table.** Fenwick is 4th on rung 0 (€250k, behind 1,030, 803 and 639), 4th on rung 1, and 2nd on rung 2 (1.29× behind
  Highmoor). It leads only rung 3, by 1.70× over Highmoor (€291k). Rung margins: 1.28, 1.26, 1.29, 1.70.
* **Discriminator dominance.** Highmoor carries a 1.29× advantage into rung 3 (564 against 439). On the decisive axis, lost trips saved per
  prevented stand-down, Fenwick sits at 0.34 and Highmoor at 0.01. The replay raises Fenwick by 12.6% and cuts Highmoor by 48.4%, a relative
  swing of 2.18. Product: 0.78 × 2.18 = 1.70. The swing is 1.41× the 1.54 it needs (1.2 × the carried 1.29).
* **Partial correction priced (L3).** Replaying day by day but thinning every stand-down at the vendor's 45%, frost and debris failures
  included, names Ravensdale (€1,056k, 1.32× over Highmoor's €800k). That is rung 1's decoy again, because it saves trips on days no
  alert could reach. Doing both halves and forgetting the kit limit names Kingsbridge (€681k, 1.38× over Fenwick's €494k).
* **Grid.** Kits (ignored, applied) × prevention (vendor 45%, alert-flagged) × lost trips (close-out share, day replay) gives 8 cells, naming
  A, B, A, A, B, B, C and E. The nearest wrong cell is alert-flagged prevention with day replay and no kit limit (Kingsbridge, 1.38× clear),
  and it costs one omission.
* **The deciding comparison (#20).** Trips saved per prevented stand-down at Fenwick against Highmoor (0.34 against 0.01) is what the note has
  to state. No depot-level figure in the close-out shows it.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The operations manual defines a lost trip as no serviceable truck at dispatch. Nothing says a prevented stand-down's
   worth depends on its day, or that frozen dryers give no alert.
2. **No sweepable corpus nominates it.** *In every closed month no stand-down was prevented, because the programme has never run at any
   depot.* So the share valuation and the day replay return the same 72 lost-trip cells. The close-out certifies the floor and cannot price
   a removed stand-down.
3. **No arithmetic symptom.** Stand-downs, tows and lost trips reconcile to the close-out under every rung, and the share is the close-out's
   own ratio.
4. **Not a row predicate.** It needs stood-down trucks counted per depot-day at dispatch, a join of each stand-down to the alert back-test
   by truck and date, a pro-rata removal for equipped trucks, and the excess over float taken day by day and summed.
5. **The enumeration is arithmetic.** Which lost trips the programme saves is computed by replay. No column marks a stand-down as having cost
   a trip.
6. **No cutover date.** Frost mornings recur every winter and the floats are unchanged, so no series steps.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The close-out: six depots × twelve months of stand-downs, lost trips, tows and floats, with the daily stand-down log behind it.
* **What it certifies.** Lost trips are the day's excess of trucks stood down at dispatch over the float. That reproduces all 72 monthly
  cells. A monthly rule (stand-downs less float × operating days, floored at zero) reproduces 19 of 72, and its total is 31% short. The
  share valuation reproduces the totals trivially, which is why a solver who back-tests is confirmed at rung 2.
* **What it is blind to.** Any prevented stand-down (above).
* **Twin pair.** Ravensdale in March and Highmoor in February are identical on every close-out input column: 220 trucks, float 3, 46
  stand-downs, 31 tows. Their lost trips are 6 and 12, 2× apart. Highmoor's month held two frost mornings. Only the day-grain floor
  reproduces both, and any monthly rate gives them the same count.
* **Every rule exercised.** Thornbury's float rose from 2 to 3 in June when a hired truck joined, with the date effective in the fleet
  register, so the floor is tested at two values. Eleven Fenwick repairs ran across two dispatches, so "stood down at dispatch" is tested
  against "failed that day".
* **Resemblance points at the decoy.** Highmoor's profile matches the vendor's published case-study depot. On stand-downs per truck and tows,
  Fenwick looks like Ashworth and Thornbury, the two depots worth least.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The charter: the rollout goes where it adds the most net annual value (tow and roadside cost avoided, plus lost trips
  avoided, less kit and inspection cost). The operations manual: a trip is lost when no serviceable truck is available at dispatch. The
  allocation register: 250 kits this year. The vendor's service terms: an inspection follows within 72 hours of an alert. One sentence each.
* **Empirical pins.** The day-grain floor, from the close-out. Each depot's preventable stand-downs, from the back-test.
* **Voices.** The fleet director: "The programme belongs where the failures are." The vendor's account manager: "Forty-five per cent, on
  every fleet we've worked with." The Highmoor depot manager: "Every winter we run out of trucks; nobody needs it more."
* **Licensed wrong basis.** The charter records that the group finance committee prices depot investments at the close-out's lost-trip share
  per stand-down and will see that basis.

## 8. Determinism by construction

* **Dispatch count.** Dispatch is 05:00, and no stand-down opens or closes within 30 minutes of it, so "open at dispatch" has one reading.
* **Alert lead.** No alert falls between 2.5 and 3.5 days before its stand-down, so the 72-hour inspection term selects one set under any
  lead convention.
* **Equipping.** Fenwick's 100 trucks are all equipped. At capped depots stand-downs are spread evenly across trucks, so the pro-rata
  removal is exact in expectation, and Fenwick's figure does not depend on it.
* **Costs.** Tow and roadside €2.1k per stand-down, €4.8k per lost trip, €0.4k per equipped truck-year, all filed in the charter's schedule.
* **Maturity.** The close-out year and the back-test cover the same closed twelve months.

## 9. Prompt sketch and deliverables

> I can give the vendor's air-system programme to one depot this year, and our fleet director wants it where the failures are. Tell me
> which depot gets it and the net value a year it should bring us, in thousands of euros to the nearest ten, as a line I can put to the
> board. Send `depot_case.xlsx`, a chart `value_by_depot.png`, and a one-page `rollout_note.pdf`.

* `depot_case.xlsx` — the six depots' build, the tyre sheet (ask A), the fuel sheet (ask B) and the basis sheet (ask C).
* `value_by_depot.png` — two panels: the six depots' value under the four rung bases as grouped bars with the chosen depot highlighted, and
  Highmoor's and Fenwick's daily stood-down trucks for the closed year with each float as a labelled reference line and the frost mornings
  shaded.
* `rollout_note.pdf` — the committed depot and its value, with the deciding comparison.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each depot, the mean days between drive-axle tyre replacements last year. *Device:* a retread is
  logged as a new fitment, with the casing's original serial in a separate field, as the tyre register documents. Counting fitments halves
  the interval at the three depots that run retread programmes.
* **Ask B (device-carried).** For each depot and quarter, diesel litres per 100 km. *Device:* the fuel-card system also dispenses AdBlue
  under a product code. Summing litres across products inflates four depots' figures by 4–6%, and bulk tank deliveries carry a supplier
  flag that must not be read as dispensing.
* **Ask C (validity).** Each depot's value under each of the four rung bases.
* **Decoupling.** Clearing the day replay and the alert join changes no figure in asks A or B. Tyre and fuel records never enter the
  stand-down log or the close-out.

## 11. Rubric arithmetic

6 depots (ask A) + 6 × 4 quarters (ask B) + 6 × 4 bases (ask C) + the committed depot, its value, the runner-up and the deciding comparison +
6 named chart parts + 3 files ≈ 67 criteria.

## 12. World-building constraints

* Fleets and floats: Kingsbridge 600 / 18, Ravensdale 220 / 3, Highmoor 220 / 3, Ashworth 180 / 3, Fenwick 100 / 1, Thornbury 200 / 2
  (3 from June). Stand-downs: 1,344 / 707 / 436 / 210 / 193 / 149. Lost trips: 0 / 103 / 146 / 2 / 50 / 4.
* Alert-flagged shares: 33% / 7% / 40% / 69% / 74% / 48%. Highmoor's 24 frost mornings carry nine frozen-dryer stand-downs each and no
  gradual leak, and 144 of its 146 lost trips. The replay saves 2.0 trips at Highmoor and 48.6 at Fenwick.
* Rung values (€k): 1,030 / 803 / 564 / 494 for the four leaders. Fenwick 250 / 250 / 439 / 494, Highmoor 639 / 639 / 564 / 291.
* The twin months are identical on every close-out input column. No closed month holds a prevented stand-down.
* Tyre fitments and fuel transactions never touch stand-downs, alerts or floats.

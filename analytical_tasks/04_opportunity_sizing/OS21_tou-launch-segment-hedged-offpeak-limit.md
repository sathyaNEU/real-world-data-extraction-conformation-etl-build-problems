# OS21 — Which customer segment gets the time-of-use launch, when the biggest savers would move more demand into the night than the hedge can carry

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Product Analytics · energy tariff launches |
| Mirrors | Launching a usage-based price plan to the segment with most to gain, when a supply-side limit caps how much behaviour change the business can absorb (utility time-of-use and EV tariffs limited by hedged off-peak volume, Uber commuter passes limited by driver supply, AWS savings plans limited by spare capacity, airline fare products limited by seat inventory) |
| Decision shape | Which of N gets one scarce thing, with the sizing kept as the graded figure: the launch campaign goes to one of five customer segments |
| Committed call | The segment the time-of-use tariff launches to, and the customer savings a year it delivers, to the nearest £0.1M |
| Gap · Pattern | Gap 3 (objective) over Gap 2 (population) · a binding limit applied in the figure (#10), the risk register's cap on added off-peak demand, with the eligible population set by tariff history on the launch date rather than the CRM's field (#5) below it |
| Gate G mechanism | binding_constraint, with method_or_model_selection |
| Measured traps engaged | #10 notes a binding limit as a risk · #5 takes the population a flag suggests · #6 treats a mixed segment all one way |
| Calibration form | Parallel-run overlap: twelve months in which 8,000 pilot-region homes were billed on their flat tariff and shadow-billed on the time-of-use tariff, with the switch offer at month six and each switcher's metered shift afterwards |
| Driving force | A time-of-use launch can take on only as much new night-time demand as the supplier has hedged, and the risk register caps new sales at 25 GWh a year until the overnight hedge is extended. Heat-pump switchers each move 1,800 kWh into the night, so the segment with the biggest savings can enrol 13,900 of its 32,400 switchers and keeps 43% of its savings; solar-and-battery switchers move 350 kWh and keep all of theirs. The limit becomes a number of customers only through each segment's metered shift from the parallel run, and the run never came near it. |

## 1. Situation

An energy supplier launches its time-of-use tariff on 1 March to one customer segment first: standard smart homes, EV owners, heat-pump
homes, storage-heater homes, or solar-and-battery homes. The launch paper must name the segment and the customer savings a year it will
deliver. The offer is open to customers on the single-rate tariff on the launch date. The pricing team's model applies the tariff to each
segment's average half-hourly profile. The CRM carries each customer's segment and tariff type, the billing system each account's tariff
history, and the risk register the supplier's trading limits. Last year's parallel run shadow-billed 8,000 pilot homes. The commercial
director says heat-pump homes are where the savings are.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the profiles, the CRM, the tariff history, the parallel run's bills and shifts, and the risk
  register. Heat-pump switchers really do save £160 a year. No stakeholder read is overturned. The difficulty is that the launch can enrol
  only as many switchers as the hedge can carry, and that number is derived, segment by segment.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the director's view and the pricing model. Per-home savings on the eligible population, certified by the
  parallel run, still name heat-pump homes by 1.26×.
* **Instrument repair.** Two files are suspect: the CRM's tariff field, set at acquisition and now stale, and the parallel run, one region's
  8,000 homes. Replace the field with each account's tariff on 1 March and shadow-bill every home (segment rates are the same in every
  region): rung 0 still returns storage-heater homes, rung 1 collapses onto rung 2 and both return heat-pump homes, and the limit is still
  needed.
* **Lens swap.** The naive read is customers who would gain. The answer is customers the launch can take on under the hedge, a different
  population counted in a different register.

## 3. The driving force

A strong solver drops the average-profile model, because the parallel run shows the average home is nobody's profile: savings come from
each home's own half-hourly data, and homes saving £25 or more switch. On the CRM's segments EV owners lead by 2×. Joining the billing
history, it finds 65% of those EV owners already on the old EV tariff and 60% of storage-heater homes on two-rate meters, neither on the
single-rate tariff the offer requires, and heat-pump homes lead. The risk register says new time-of-use sales may add no more than 25
GWh a year of night-time demand until the overnight hedge is extended. Heat-pump switchers each move 1,800 kWh into the night, so 32,400
switchers would add 58 GWh; the launch can take 13,900 of them, £2.2M of savings. Solar-and-battery switchers move 350 kWh, all 29,700
fit under the limit, and they deliver £3.8M.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Each segment's average profile billed on both tariffs × homes in the CRM segment | D, storage-heater homes (£4.5M, 3.75× over standard homes) | The pricing team's own model on the customer base | The parallel run: average-profile savings reproduce none of the switchers' actual bills, and savings come from each home's own profile |
| 1 | Each home's own savings, homes saving £25 or more as switchers, on the CRM's segments | B, EV owners (£11.8M, 2.04× over heat-pump homes) | Certified by the parallel run's bills and switch decisions | The billing tariff history: 65% of the CRM's EV owners and 60% of its storage-heater homes are not on the single-rate tariff on the launch date |
| 2 | The same on homes on the single-rate tariff on 1 March, from the tariff history | C, heat-pump homes (£5.18M, 1.26× over EV owners) | The right population, every input certified | The risk register: new sales may add 25 GWh a year of night-time demand, and heat-pump switchers would add 58 GWh |
| 3 | **Decisive:** switchers enrolled up to the limit (25 GWh ÷ each segment's metered shift per switcher) × savings per switcher | **E, solar-and-battery homes** (5th of 5 on rung 0), **£3.8M a year** | — | — |

* **Position table.** Solar-and-battery homes rank 5th on rung 0, 4th on rung 1 and 3rd on rung 2, and lead only rung 3 (1.52× over EV
  owners).
* **Discriminator dominance.** Heat-pump homes carry a 1.36× advantage into rung 3 (£5.18M against £3.80M). The limit keeps 1.00 of the
  solar-and-battery savings and 0.43 of the heat-pump savings, an edge of 2.33×, 1.43 times the 1.64× floor. Product: 2.33 / 1.36 = 1.71.
* **Partial correction priced (L3).** Every half-applied construction names a wrong segment. A solver who applies the limit on the CRM's
  segments names storage-heater homes (£5.25M against £4.22M, 1.24×), because their two-rate homes stay in. One who converts the limit
  with each segment's average-home shift (700 kWh for heat pumps) finds heat-pump enrolment under it and stays on heat-pump homes
  (£5.18M against £4.12M, 1.26×). One who notes the limit as a launch risk and sizes unconstrained stays on heat-pump homes (1.26×).
* **Grid.** Savings (average profile, own profile) × population (CRM field, tariff history) × limit (ignored, applied) gives 8 cells.
  Average-profile cells all name storage-heater homes (1.58× to 7.2×); own-profile cells name EV owners (2.04×), storage-heater homes
  (1.24×), heat-pump homes (1.26×) and the answer. Only the answer cell names solar-and-battery homes.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The risk register states the 25 GWh limit on new night-time demand. No document converts it into customers, or
   says the launch sizing must apply it.
2. **Corpus blind for a computable reason.** *In the parallel run the switchers' added night-time demand was 1.9 GWh a year, under a
   tenth of the limit, because the run enrolled 2,900 switchers in one region, so no enrolment was ever held back.* Per-home savings
   reproduce every switcher's bill, and the limit never shows.
3. **No arithmetic symptom.** Segment savings sum to the campaign total, metered shifts reconcile to the run's half-hourly data, and the
   limit sits in a register no sizing file touches.
4. **Not a row predicate.** The cap is a quantity: 25 GWh divided by each segment's shift per switcher, compared with its eligible
   switchers, and savings recomputed on the smaller.
5. **The enumeration is arithmetic.** No column marks a customer as beyond the limit; the number exists only after the division.
6. **No cutover date.** The limit holds for the whole campaign year, and no hedge renewal falls inside it.
7. **Survives deletion.** Removing the pricing model and every voice leaves the parallel run certifying rung 2.

## 6. The calibration corpus

* **Form.** The parallel run: twelve months of flat bills and time-of-use shadow bills for 8,000 pilot homes, the switch decisions at
  month six, and six months of metered half-hourly data after each switch.
* **What it certifies.** Per-home savings, which reproduce all 2,900 switchers' actual bills within 1%; the switch rule (every home
  shadowed at £25 or more switched, and none below); and each segment's shift per switcher (250, 2,400, 1,800, 400 and 350 kWh).
  Average-profile savings reproduce none of the bills.
* **What it is blind to.** The limit (above).
* **Twin pair.** Pilot streets Ashby Road and Kiln Lane each have 120 heat-pump homes on the single-rate tariff, 60% switched, and their
  switchers save £160 a year. Ashby's switchers moved 900 kWh into the night and Kiln's 1,800, so each GWh of the limit carries £178,000 of
  savings on Ashby's pattern and £89,000 on Kiln's, 2.0× apart. Only the metered shift against the limit separates them.
* **Resemblance points at the decoy.** Heat-pump homes most resemble the run's biggest savers, the switchers it was built to showcase.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The launch brief: the tariff launches to one segment first and is sized on customer savings a year. The offer terms:
  open to customers on the single-rate tariff on 1 March. The switch rule: a customer switches when the tariff saves £25 a year or more on
  their own profile. The risk register: until the overnight hedge is extended, new time-of-use sales may add no more than 25 GWh a year of
  night-time demand.
* **Empirical pins.** Savings and shifts per switcher, from the parallel run. Eligibility, from the tariff history.
* **Voices.** The commercial director: "Heat pumps are where the savings are. Lead with them." The trading manager: "The hedge is a
  trading question, not a marketing one."
* **Licensed wrong basis.** The launch brief records that the board's pricing committee compares segments on the average-profile model's
  savings per home and will present that comparison.

## 8. Determinism by construction

* **Enrolment.** The campaign enrols in response order, and in the run neither savings nor shift varied with response day, so capped
  switchers carry their segment's averages.
* **Shift.** Each segment's shift per switcher is the same in every post-switch month of the run within 3%, and the limit never falls
  within 10% of any segment's eligible demand.
* **Eligibility.** The tariff history is complete to the launch date, and no tariff change straddles it.
* **Switching.** No home's shadow saving lies within £2 of the £25 threshold.
* **Regions.** Each segment's savings and shift per switcher in the pilot region match the half-hourly data of every other region within 2%.
* **Rounding.** 29,700 switchers × £128 is £3.80M, mid-bin at £0.1M.

## 9. Prompt sketch and deliverables

> We launch the time-of-use tariff to one customer segment first, on 1 March, and the board wants the segment and the customer savings a
> year it will deliver, to the nearest £0.1M. Our commercial director's view is that heat-pump homes are where the savings are. Give me the
> call as one sentence for the launch paper, with `segment_case.xlsx`, a chart `savings_under_limit.svg`, and a one-slide
> `launch_paper.pptx`.

* `segment_case.xlsx` — the five segments on four bases, the eligibility and limit builds, the meter sheet (ask A) and the
  estimated-bills sheet (ask B).
* `savings_under_limit.svg` — a script-rendered bar chart per segment: savings of all eligible switchers, savings of the switchers the
  limit admits drawn inside them, each bar's night-time demand in GWh printed against the 25 GWh line, and the committed segment
  highlighted.
* `launch_paper.pptx` — the committed segment, its savings, and why heat-pump homes fall away.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each segment, the share of smart meters that missed their daily read on more than ten days
  last quarter. *Device:* a meter whose communications hub was replaced reports under a new device ID carrying `replaces_device`, and the
  metering guide counts by meter. Counting device IDs double-counts the failures of the two segments with most hub replacements.
* **Ask B (device-carried).** For each segment, the share of last quarter's bills issued on an estimated read. *Device:* when an actual read
  arrives after an estimated bill, the billing system keeps the estimate and posts the actual as a new read flagged `replaces_estimate`, and
  the billing guide classes each bill by the read it finally rests on. Counting every estimated read as an estimated bill overstates the
  share in the two segments whose meters report latest.
* **Ask C (validity).** Each segment's savings under each of the four rung bases, eligible homes under the CRM field and the tariff
  history, and switchers' bills reproduced (of 2,900) by own-profile and average-profile savings.
* **Decoupling.** Ignoring the limit changes no figure in asks A or B. Meter communications and billing reads touch neither the tariff
  history, the parallel run nor the risk register.

## 11. Rubric arithmetic

5 segments × 2 (ask A) + 5 segments (ask B) + 5 segments × 4 bases, 5 × 2 eligibility counts and 2 reproduction counts (ask C) + the
committed segment, its savings, the runner-up and the margin + 5 named chart parts + 3 files ≈ 59 criteria.

## 12. World-building constraints

* Segments (standard, EV, heat pump, storage heater, solar and battery): CRM homes 600,000 / 70,000 / 60,000 / 150,000 / 55,000;
  single-rate share on 1 March 95% / 35% / 90% / 40% / 90%; average-profile saving £2 / £8 / £10 / £30 / £5 a home; switch share 8% / 70% /
  60% / 35% / 60%; saving per switcher £40 / £240 / £160 / £100 / £128; shift per switcher 250 / 2,400 / 1,800 / 400 / 350 kWh.
* Limit 25 GWh a year: EV owners capped at 10,400 switchers (£2.5M), heat-pump homes at 13,900 (£2.2M); others uncapped.
* Rung leaders D, B, C, E at 3.75×, 2.04×, 1.26×, 1.52×; solar-and-battery homes 5th, 4th, 3rd, 1st.
* Ashby Road and Kiln Lane match on every CRM and billing column.
* Meter communications and billing reads never touch tariffs, the parallel run's half-hourly data or the risk register.

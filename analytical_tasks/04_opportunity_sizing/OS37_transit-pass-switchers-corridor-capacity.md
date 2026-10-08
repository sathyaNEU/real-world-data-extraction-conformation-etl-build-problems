# OS37 — How many car commuters a transit-pass programme takes off the road, when the trains they would ride are already full

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Demographic & Social Science · commuting and travel behaviour |
| Mirrors | Two-sided eligibility sized against a shared resource that is already full (ride-hail incentives in zones where drivers are saturated, marketplace promotions into fulfilment lanes at capacity, enterprise seat expansions into a support queue at its service limit) |
| Decision shape | One figure committed at a date: car commuters removed next year, written into the travel-plan agreement signed on the 15th |
| Committed call | The number of car commuters the coalition's transit-pass programme takes off the road next year |
| Gap · Pattern | Gap 3 (objective) · E14 (a binding limit applied in the figure: switchers ride corridors whose spare peak capacity caps them), with E22 below it (eligibility as the combination of both commute ends, which either end read alone overstates) |
| Gate G mechanism | binding_constraint, with forecasting |
| Measured traps engaged | #10 notes a binding limit as a risk · #20 leaves the deciding comparison unstated · #13 validates on one population, applies to another |
| Calibration form | Prior-period close-out: the coalition's signed close-out of last year's pass pilot at one employment centre (eligible car commuters, activations and switchers by journey-time band and corridor) |
| Driving force | Switchers have to fit on the trains. Northline and Harbour Rail already run at 96% and 97% of registered peak capacity, with 500 spare places between them, yet 3,100 of the programme's 5,813 likely switchers would ride them. The pilot's corridors had just doubled frequency, so its close-out never met a full train. The cap is a sum over corridors of the smaller of switchers and spare places, built by routing every commute onto a corridor. |

## 1. Situation

An employer coalition at four employment centres is extending last year's subsidised transit-pass pilot to all 62,000 employees. Its
travel-plan agreement with the city, signed on the 15th, must state how many car commuters the programme removes next year, and the
city's parking-levy rebate is paid on that number. The coalition holds employees' home and work addresses. The transit agency publishes
each corridor's registered peak capacity and peak-hour loads for service planning. The sustainability chair is sure most of the workforce
works near a station.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the address file, the frequent-stop list, the commute survey, the pilot close-out and the agency's
  capacity and load data. The chair is right that most people work near a station. Nothing is overturned. The difficulty is a physical
  limit that the pilot never reached.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the chair's view and every voice. Both-ends eligibility at the pilot's banded switching rates still gives
  5,813, and no document says switchers are limited by space.
* **Instrument repair.** No file is suspect. Addresses, the frequent-stop list, the survey, the close-out and the agency's capacity and load
  file are complete and current. Rungs 0, 1 and 2 still return 8,525, 4,675 and 5,813. The pilot's trains had room, so no better instrument
  of the pilot shows a cap, and the corridor routing is still needed for 3,213.
* **Lens swap.** The answer counts commuters whose trips land on corridors with room, a different population from the commuters who would
  switch.

## 3. The driving force

A strong solver refuses to count workplaces near transit and builds eligibility from both ends of each commute. It then refuses the pilot's
pooled switching rate, because the close-out shows switching splits by journey-time ratio, and transports the banded rates to the forward
mix. The result is 5,813 switchers. But every switcher is a peak-hour rider on a particular corridor, and the agency's planning file shows
Northline and Harbour Rail at 96% and 97% of their registered peak capacity. Together they have 500 spare places, while routing each
eligible commute through the network puts 3,100 of the likely switchers on those two lines. The pilot centre's two corridors had their
frequency doubled the year the pilot began and never passed 72% loading, so its close-out reproduces perfectly with or without a cap.
Removed commuters are Σ over corridors min(switchers, spare places).

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Car commuters whose workplace is within 0.5 miles of a frequent stop × the pilot's 25% switching rate | 8,525, +165% | The coalition's lever is the workplace, and the rate is its own pilot's | Home addresses: 45% of those commuters live nowhere near a frequent stop |
| 1 | Both ends within 0.5 miles (the commute pair, not either end) × 25% | 4,675, +45.5% | The two-sided condition, built from each commute | The close-out: switching was 41.0% for commutes whose transit time is at most 1.3× the drive and 5.6% above it |
| 2 | Banded rates applied to the forward mix (72% of eligible commutes within 1.3×) | 5,813, +80.9% | Causal rates from the coalition's own pilot, transported correctly | The agency's planning file: Northline and Harbour Rail have 500 spare peak places and would carry 3,100 switchers |
| 3 | **Decisive:** each commute routed to its corridor; removed = Σ over corridors min(switchers, spare peak places) | **3,213** | — | — |

* **Figure shape.** The corrections walk down, up and down (−45.2%, +24.3%, −44.7%), and the answer is the minimum of every cell on the
  ladder. Each rung sits at least 45% from it.
* **The deciding comparison (#20).** Northline and Harbour Rail: 3,100 likely switchers against 500 places. The other four corridors:
  2,713 against 4,900 places, which do not bind. The note has to set these side by side.
* **Partial correction priced (L3).** A solver who sees the crowding but caps at the system-wide spare capacity (5,400 places) lands at
  5,400 (+68%). A solver who removes the two full corridors' commuters entirely lands at 2,713 (−15.6%), on the far side of the
  answer.
* **Grid.** Eligibility (workplace end, both ends) × rate (pooled, banded) × corridor cap (off, on) = 8 cells. The nearest wrong cell is
  both ends at the pooled rate with the cap, 2,683 (−16.5%), reached by skipping the close-out's bands. Every other cell is further away.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The agency's file lists capacities and loads for its own planners. The pass agreement says passes are valid on all
   services. No document says switchers need room.
2. **Corpus blind for a computable reason.** *In every corridor serving the pilot centre, peak loads stayed under 72% of registered
   capacity, because the agency doubled frequency on both lines the year the pilot began.* The banded rates reproduce the pilot's 775
   switchers capped or uncapped alike.
3. **No arithmetic symptom.** Employees, eligible commutes, survey shares and the pilot's activations reconcile on every rung.
4. **Not a row predicate.** Each commute is routed through the network to a corridor, switchers are summed by corridor, and each sum is
   capped by that corridor's spare places.
5. **The enumeration is arithmetic.** No column assigns an employee to a corridor or says a corridor is full.
6. **No cutover date.** The frequency doubling is a dated pilot-centre fact and the decoy. The forward cap is a standing load.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The signed close-out of last year's pilot: 3,100 eligible car commuters at the pilot centre, activations and switchers by
  journey-time band and corridor, and weekly peak loads on its two corridors.
* **What it certifies.** Both-ends eligibility (every switcher lived within 0.5 miles of a frequent stop) and the banded rates: 697 of
  1,700 (41.0%) within 1.3× and 78 of 1,400 (5.6%) above. A solver who back-tests rung 2 is confirmed to the commuter.
* **What it is blind to.** Capacity (above).
* **Twin pair.** Forward centres Quayside and Mill Lane are identical on every column a lookup reaches: employees, both-ends eligible car
  commuters (2,600 each), journey-time mix and survey shares. Quayside's commutes route mainly onto Northline and Mill Lane's onto
  uncrowded lines, so they remove 404 and 808 commuters, 2.0× apart.
* **Resemblance points at the decoy.** By eligible share and journey-time mix, the forward centres most resemble the pilot centre, so a
  solver transferring its uptake by resemblance files rung 2.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The travel-plan agreement counts car commuters removed as employees who drove to work and ride transit at the peak with a
  coalition pass. The frequent network is stops with peak headways of 15 minutes or less. The agency's crowding standard sets registered
  capacity at 85% of crush load.
* **Empirical pins.** The banded switching rates come from the close-out, corridor routing from the agency's network, and spare places from
  registered capacity minus current peak-hour load.
* **Voices.** The sustainability chair: "Most of our people work right by a station; uptake will be huge." The pilot coordinator: "The
  pilot hit every number we set." That is true.
* **Licensed wrong basis.** The agreement records that the city's transport committee scores travel plans on eligible employees × the
  pilot's uptake and will see that basis.

## 8. Determinism by construction

* **Radius and headway.** No home or work block lies within 0.05 miles of the 0.5-mile radius, and no stop's peak headway falls between 12
  and 18 minutes, so neighbouring definitions return the same commutes.
* **Corridor routing.** The network is radial, and no commute has a second corridor within five minutes of its fastest, so assignment is
  unique.
* **Journey-time band.** No commute's ratio lies within 0.05 of 1.3.
* **Peak timing.** 96% of the pilot's switchers rode in the 07:00–09:00 peak, which is the window the registered capacity describes.
* **Shared places.** On a full corridor, places are shared pro rata to switchers. That affects only the per-centre split, never the
  committed total.
* **Maturity.** The pilot year is closed and its close-out is signed.

## 9. Prompt sketch and deliverables

> Our coalition signs its travel-plan agreement with the city on the 15th, and it has to state how many car commuters our pass programme
> takes off the road next year, as a whole number. Our sustainability chair is confident that most of our people work near a station. Send
> `pass_programme_case.xlsx`, a chart `corridor_absorption.png`, and a one-page `agreement_note.pdf`.

* `pass_programme_case.xlsx`: the build under the four rung bases, switchers and spare places by corridor, the parking sheet (ask A) and
  the expenses sheet (ask B).
* `corridor_absorption.png`: for each of the six corridors, likely switchers against spare peak places as paired bars, the binding
  corridors highlighted, current loading printed as a percentage of capacity, and the committed total in the title.
* `agreement_note.pdf`: the committed figure, the corridor comparison and the basis the city's committee will bring.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the four centres, parking spaces leased by coalition employers and the average monthly
  cost per space last year. *Device:* a renewed lease is a new row with a new number that references the lease it replaces, and the
  overlap month is billed once, per the property guide. Counting rows doubles spaces at the two centres that renewed mid-year.
* **Ask B (device-carried).** For each centre, the average monthly transit-fare spend reimbursed per employee, and the share of employees
  claiming. *Device:* a resubmitted claim posts as a reversal of the original and a new claim, both carrying the original claim number.
  Summing claims overstates spend by 9% at the centre with a mid-year system change.
* **Ask C (validity).** The figure under each of the four rung bases, and the close-out reproduction under the pooled rate (the total only)
  and the banded rates (both bands and the total).
* **Decoupling.** Clearing the corridor cap changes no figure in asks A or B.

## 11. Rubric arithmetic

4 centres × 2 (ask A) + 4 × 2 (ask B) + 4 bases + 3 reproduction figures (ask C) + the committed figure, switchers and places for the six
corridors and removed commuters per centre + 5 named chart parts + 3 files ≈ 48 criteria.

## 12. World-building constraints

* 62,000 employees; 34,100 car commuters with a workplace near a frequent stop; 18,700 with both ends near; 72% of those within 1.3× the
  drive time.
* Pilot: 3,100 eligible car commuters, 775 switchers (697 of 1,700 within 1.3×, 78 of 1,400 above), peak loads under 72% throughout.
* Forward switchers by corridor: Northline and Harbour Rail 3,100 against 300 and 200 spare places; four other corridors 2,713 against
  4,900.
* Rung figures 8,525 / 4,675 / 5,813 / 3,213, and the nearest other cell is 2,683 (−16.5%). Quayside and Mill Lane are identical on every
  centre-level column.
* Lease renewals and resubmitted claims never touch addresses, survey shares, the close-out or corridor loads.

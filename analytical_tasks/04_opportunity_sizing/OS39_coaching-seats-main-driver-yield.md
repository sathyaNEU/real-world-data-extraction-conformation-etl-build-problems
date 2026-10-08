# OS39 — How an insurer splits 24,000 driver-coaching seats, when coaching only works on the person who actually drives the car

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Product Analytics · telematics coaching and insurance claims |
| Mirrors | Targeting an intervention delivered to an account holder when the behaviour belongs to whoever uses the account (engagement nudges on shared streaming or gaming accounts, family cloud plans where the payer is not the user, B2B seats bought by an admin for others) |
| Decision shape | An allocation under a cap: 24,000 coaching seats from the vendor contract, across six customer segments |
| Committed call | Seats per segment, and the annual claims cost the split avoids |
| Gap · Pattern | Gap 2 (population) over Gap 3 (objective) · Pattern E (conditioned yield: coaching cuts claims only where the coached policyholder actually drives the car), with E02 below it (a claim's net cost is built from payment rows and a separate recoveries file) |
| Gate G mechanism | binding_constraint, with decomposition_attribution |
| Measured traps engaged | #13 validates on one population, applies to another · #2 counts file rows instead of the real unit · #7 uses the ready-made measure |
| Calibration form | Settled-transaction ledger: the closed claims ledger of last year's randomised coaching pilot (8,000 invited vehicles, half coached), with payments, stopped payments and recoveries, and both arms' trip logs |
| Driving force | Coaching goes to the policyholder's phone and changes the driving of whoever holds it. In the pilot, coached vehicles with at least 90% of trips driven with the policyholder's phone paired cut behavioural claim costs by 31%, and vehicles under 50% by nothing, with no vehicle in between. The pooled 19% fits no segment. Main-driver share comes from the trip log's phone pairings, not the policy's declared main driver: 0.97 among retirees, 0.35 in two-car families. |

## 1. Situation

A motor insurer's coaching vendor will run 24,000 coaching seats next year: a phone app that scores each trip and coaches the policyholder.
The pricing committee wants the seats where they avoid the most claims cost. Last year's pilot invited 8,000 vehicles, coached half of
them at random, and the claims ledger for the pilot year is closed. Every pilot vehicle carried a trip-logging device that records the
paired phone. The telematics lead is sure the two-car-family segment is where coaching pays.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the claims ledger, the recoveries file, the trip logs and the pilot's 19% headline. Families really
  do have the most behavioural claims per vehicle. Nothing is overturned. The difficulty is which yield applies to each segment's
  vehicles.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the telematics lead's view and every voice. The pilot's randomised 19% on behavioural claims still ranks
  two-car families first, and no document mentions who drives.
* **Instrument repair.** Make the randomisation larger and every claim settled to the penny. The 19% is still a correct average over a mix
  that no forward segment shares.
* **Lens swap.** The answer applies to each segment's own vehicles split by who drives them, a different population from the pilot's
  pooled cohort.

## 3. The driving force

A strong solver builds each claim's net cost by grouping payment rows and netting the separate recoveries file. It keeps the claims
coaching can touch, at-fault collisions, and applies the randomised pilot's 19%. That is causal, correctly costed and correctly scoped,
and it puts the seats in two-car families. But coaching is delivered to the policyholder's phone. The pilot's trip logs record which phone
was paired on each trip, and the yield splits absolutely on the share of a vehicle's trips driven with the policyholder's phone: 31% at
90% and above, 0% below 50%, and no vehicle in between. In two-car families the policyholder drives the car under coaching on 35% of
vehicles. Among retirees it is 97%. The policy file's "declared main driver" field says 95% for both. The real share is a statistic over
trips through the pairing join, rolled up by segment.

## 4. The ladder

| Rung | Construction ($ claims avoided per seat; fill 24,000 by value) | Names (ranked first) and annual saving | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Claims cost per vehicle from summed payment rows × the pilot's 19% | A, added teens, 334 (1.17× rideshare); $7.27M, +42.8% | The insurer's own ledger and its own randomised effect | The ledger guide: a reissued payment leaves the stopped original as a row, and recoveries sit in a separate file by claim number |
| 1 | Hygiene: net cost per claim (stopped payments out, recoveries netted) × 19% | B, shared-car pairs, 270 (1.18× rideshare); $5.83M, +14.6% | The real unit, a settled claim's net cost | The pilot report: arms differ only on at-fault collision claims, and theft, glass and weather claims are identical |
| 2 | Net behavioural claims × 19% | C, two-car families, 186 (1.15× shared-car pairs); $4.13M, −18.9% | Causal, correctly costed and correctly scoped | The trip logs: the pilot's yield is 31% at a main-driver share of 0.90 and above and 0% below 0.50 |
| 3 | **Decisive:** net behavioural claims × 31% × each segment's share of vehicles driven at least 90% with the policyholder's phone | **E, retirees, 253 (1.26× trade vans); $5.09M** (5th of 6 on rung 0) | — | — |

* **The answer.** Retirees 8,000 seats, trade vans 6,000, rideshare 7,000 and shared-car pairs 3,000, avoiding $5,088,740 a year,
  committed as $5,090,000.
* **Position table.** Retirees rank 5th on rung 0, 3rd on rung 1 and 4th on rung 2, and lead only rung 3. They are never 2nd on the
  ladder.
* **Discriminator dominance.** Two-car families carry a 1.16× lead into rung 3. Conditioning multiplies retirees' yield by 1.58 and
  families' by 0.57, an edge of 2.8×, above 1.2 × 1.16 = 1.40.
* **Partial correction priced (L3).** Every half-applied conditioning puts a wrong segment first. Conditioning the yield on the policy's
  declared main driver keeps two-car families first, 289 against shared-car pairs' 261 (1.11×), because families declare the policyholder
  as main driver on 95% of vehicles. Conditioning on the trip-based share without netting recoveries names trade vans, 348 against
  retirees' 291 (1.19×). Conditioning without restricting to behavioural claims names rideshare, 353 against retirees' 317 (1.12×).
* **Grid.** Cost (payment rows, net claims) × scope (all claims, behavioural) × yield (pooled, main-driver conditioned) = 8 cells. Every
  non-answer cell names added teens, shared-car pairs, two-car families, rideshare or trade vans. The nearest figure is rung 1 at +14.6%.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The pilot report gives one effect, and the policy file's declared main driver looks like the answer. No document
   ties the effect to who holds the phone.
2. **The corpus pins the conditioning only through a join.** The ledger carries claims by vehicle and arm. Who drove sits in the trip log,
   reached through phone pairings, so every group-by on the ledger shows a 19% effect with mild variation by segment and never the
   31-against-0 split.
3. **No arithmetic symptom.** Payments, stopped payments, recoveries and claim counts reconcile, and the pilot's arms balance on every
   policy column.
4. **Not a row predicate.** Main-driver share is a statistic over each vehicle's trips (paired phone against the policyholder's), and
   then a share of vehicles per segment.
5. **The enumeration is arithmetic.** No column holds the trip-based share, and the declared field disagrees with it on 41% of vehicles.
6. **No cutover date.** The pilot is one closed year, and nothing steps.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The pilot year's claims ledger (payments, stopped payments and recoveries by claim number) for 8,000 randomised vehicles, and
  both arms' trip logs with the paired phone per trip.
* **What it certifies.** Net claim cost as the unit, behavioural claims as the scope, and the pooled 19% (coached against holdout on net
  behavioural claims). A solver who back-tests rung 2 is confirmed.
* **The absolute split (O2).** Main-driver share 0.90 or above: coached vehicles' behavioural claims 31% below holdout. Below 0.50: no
  difference. No pilot vehicle had a share between 0.50 and 0.90. The pilot's mix was 61% high-share, so 0.61 × 31% = 19%.
* **Twin pair.** Pilot clusters Kenwood and Wye Valley are identical on every policy column: age bands, vehicle types, declared main
  driver, prior claims and arm sizes. Coaching cut behavioural claims by 27% and 13%, 2.1× apart, because their trip-based main-driver
  shares are 0.87 and 0.42.
* **Resemblance points at the decoy.** Two-car families resemble the coached cohort on declared main driver, vehicles per policy and prior
  claims.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The vendor contract provides 24,000 seats, one policyholder on one vehicle each. The committee scores coaching on annual
  claims cost avoided. The claims manual's cause codes define behavioural claims.
* **Empirical pins.** The 31% and 0% yields and the 0.90 threshold come from the pilot through the trip log. Segment main-driver shares
  come from the last six months of trips.
* **Voices.** The telematics lead: "Families have the worst claims, so coaching belongs there." The pilot analyst: "The randomised effect
  was 19%, as clean as it gets." That is true of the pilot.
* **Licensed wrong basis.** The contract records that the reinsurer's actuary prices coaching at the pilot's pooled effect and will see
  that basis.

## 8. Determinism by construction

* **Trip window.** Vehicle shares sit at 0.90 or above or at 0.50 or below in every segment too, so 3-, 6- and 12-month windows classify
  identically.
* **Unpaired trips.** Under 1% of trips have no paired phone, and counting them either way moves no vehicle across a threshold.
* **Ledger closure.** Every pilot-year claim is settled, so there are no reserves to choose.
* **Fill boundary.** The last seats fall between rideshare ($194) and shared-car pairs ($164), $30 apart, and the order among fully
  filled segments never changes the total.
* **Rounding.** The answer, $5,088,740, sits $3,740 from the nearest $10,000 rounding boundary.

## 9. Prompt sketch and deliverables

> Our coaching vendor gives us 24,000 seats next year, and I have to tell the pricing committee which customers get them and what they
> save us in claims. Our telematics lead is sure the two-car families are where coaching pays. Give me the split of seats across our six
> segments and the annual claims cost avoided, to the nearest $10,000, in a form the committee can minute. Send `coaching_allocation.xlsx`,
> a chart `seat_value.png`, and a one-page `committee_memo.pdf`.

* `coaching_allocation.xlsx`: the six segments under the four rung bases, the vehicle-level main-driver shares, the premium sheet (ask A)
  and the message sheet (ask B).
* `seat_value.png`: value per seat by segment under the pooled and conditioned yields as paired bars, with the 24,000-seat fill drawn as a
  cumulative line, each segment's trip-based and declared main-driver shares printed, and the chosen segments marked.
* `committee_memo.pdf`: the committed split, the saving and the families comparison.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each segment, written premium per vehicle last year and the share of policies paying monthly.
  *Device:* mid-term adjustments post as separate positive or negative premium rows carrying the original policy number, per the premium
  guide. Taking only the original row misstates premium at the three segments with frequent vehicle changes.
* **Ask B (device-carried).** For each of the app's three coaching modules (speed, phone use, braking), the weekly open rate over the
  pilot's last four weeks. *Device:* a message re-sent after a delivery failure carries the same message number with a retry counter.
  Counting sends as messages halves the phone-use module's open rate.
* **Ask C (validity).** The split and saving under each of the four rung bases, and the pilot reproduction: the conditioned yield matches
  both main-driver groups in both arms, while the pooled yield matches only the total.
* **Decoupling.** Clearing the main-driver conditioning changes no figure in asks A or B.

## 11. Rubric arithmetic

6 segments × 2 (ask A) + 3 modules × 4 weeks (ask B) + 4 bases × 2 + 2 reproduction results (ask C) + 6 seat counts, the saving, its margin
and the families comparison + 5 named chart parts + 3 files ≈ 51 criteria.

## 12. World-building constraints

* Per vehicle (payment-row cost / net cost / behavioural share / trip-based main-driver share): added teens $1,760 / $1,000 / 0.85 / 0.15,
  shared-car pairs $1,450 / $1,420 / 0.60 / 0.62, two-car families $1,180 / $1,032 / 0.95 / 0.35, rideshare $1,500 / $1,200 / 0.55 / 0.95,
  retirees $1,211 / $1,053 / 0.80 / 0.97, trade vans $1,500 / $870 / 0.85 / 0.88. Eligible vehicles 9,000 / 12,000 / 10,000 / 7,000 /
  8,000 / 6,000.
* Pilot: 61% of vehicles at a share of 0.90 or above, yields 31% and 0%, none between 0.50 and 0.90.
* Rung figures $7.27M / $5.83M / $4.13M / $5.09M. The off-ladder cells are +82.7%, +46.7%, +30.1% and +16.5%.
* Kenwood and Wye Valley are identical on every policy column.
* Premium adjustments and message retries never touch claims, recoveries or trip logs.

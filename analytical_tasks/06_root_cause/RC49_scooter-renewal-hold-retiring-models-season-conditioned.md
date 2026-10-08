# RC49 — Whether the council refuses any scooter operator's renewal, when this year's worst rates ride on models the renewal will not license

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Policy & Education · micromobility permitting |
| Mirrors | Partner safety reviews at platforms where a partner is judged on a fleet or catalogue it is already retiring (vehicle-age rules for Uber and Lyft drivers, marketplace sellers delisting a recalled model on Amazon, app-store reviews of developers on a deprecated SDK), so last year's rate on everything that ran overstates the rate of what will run next term |
| Decision shape | Hold, forced by a blocking quantity: no operator's injury rate on the fleet the renewal will license reaches the permit's refusal threshold |
| Committed call | Renew all four permits and refuse none, because the highest injury rate on a renewal fleet is Glide's 9.0 per 100,000 trips against the threshold of 10 |
| Gap · Pattern | Gap 1 (time) at the decisive rung, Gap 4 (rule) at rung 2 · the population a flag suggests (measured #5): the active flag says which devices ran this year, the permit register's dates say which the renewal licenses, and the renewal fleet's rate is built from the approved models' winter months conditioned on season; with the binding minimum fleet of measured #10 at rung 2, and the hold of Part 6.4 |
| Gate G mechanism | signal_vs_noise_or_hold, with binding_constraint support |
| Measured traps engaged | #5 takes the population a flag or filter suggests · #10 notes a binding limit as a risk · #13 validates on one population, applies to another |
| Calibration form | Existing-book actuals: nine past permit renewals in the city and two peer cities, each with the rate assessed at renewal and the rate realised over the following term |
| Driving force | Injuries on shared scooters tripled, but trips grew faster, and on this year's fleet Zippa's rate of 14.2 per 100,000 trips is over the threshold of 10. Refusing Zippa would breach the mobility plan's minimum licensed fleet, so the framework would refuse Volt, at 11.5, instead. Both rates are right for this year's fleet. But the permit renews for next term's, and the new approval scheme ends the registrations of Zippa's and Volt's old models when this term closes. The register's dates, not the active flag, say which devices run next term. The approved models arrived in October and have ridden only through winter, the riskiest months. Conditioned on season, Zippa's renewal fleet carries 8.6 and Volt's 8.1, the highest is Glide's 9.0, and no permit is refused. |

## 1. Situation

A city licenses four shared e-scooter operators. Injuries on shared scooters tripled over three years, and a council motion would refuse
every renewal. The permit framework renews an operator unless its injury rate per 100,000 trips on the fleet licensed for the renewal term
exceeds 10. The mobility plan requires at least 3,000 licensed devices across the city in every term. This year the city brought in a
device-approval scheme, under which an unapproved model's registration ends when the current term closes. Zippa and Volt began replacing
their old models with approved ones in October.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct: the operators' incident reports, the trip logs, the active-device flags, the permit
  register, the mobility plan's minimum and the book. Injuries really did triple, and Zippa's and Volt's rates really are over 10 on this
  year's fleet. No one's reading of their own figures is overturned. The question is which fleet the renewal judges.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the motion and every voice. The book still certifies judging a renewal on this year's active fleet, and that
  construction still refuses Zippa, or Volt once the minimum fleet binds.
* **Instrument repair.** No file is suspect. The incident reports are audited each quarter against the city's trauma registry and are
  complete, the trip logs and the register are complete, and the active flag correctly records which devices are in service now, a
  different attribute from which devices the renewal licenses. With nothing to repair, rung 0 still refuses every operator, rung 1 Zippa
  and rung 2 Volt. No instrument records next term's rate, which has not happened. Building it from the register's dates and the approved
  models' winter months, conditioned on season, is a forward population no row records, so the decisive rung is still needed.
* **Lens swap.** The naive population is this year's active fleet. The answer's is the fleet the register licenses for next term, and its
  rate is a full year's, not a winter's. These differ in population and in moment.

## 3. The driving force

A strong solver does not count injuries. Trips grew 3.6× while injuries tripled, so it computes each operator's rate per 100,000 trips, as
the permit does, and the book confirms that a renewal's rate on the active fleet predicted the next term's within 6% in all nine past
renewals. Zippa is at 14.2. It then applies the mobility plan: refusing Zippa leaves at most 2,600 licensed devices against the required
3,000, so the framework passes to the next operator over the threshold and refuses Volt, at 11.5. But the permit judges the fleet licensed
for the renewal term, and the register ends the registrations of Zippa's and Volt's old models when this term closes. The active flag
still marks them in service. On the approved models alone the raw rates are 11.0 and 10.4, which still look like refusals. Those models
arrived in October and have ridden only from October to March, when rates per trip run 1.28 times the full-year level on every model that
ran all year. Conditioned on season, Zippa's renewal fleet carries 8.6 and Volt's 8.1. Glide's single model sits at 9.0 and Hop's at 7.5.
No operator reaches 10.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Shared-scooter injuries from the incident reports, three years apart | Refuse all four (injuries ×3.0) | The motion's own figure, and every injury is reported | The trip logs: trips grew 3.6× over the same three years |
| 1 | Injuries per 100,000 trips by operator on this year's active fleet | Refuse Zippa (14.2, 1.23× Volt's 11.5) | The permit's own measure, and the book confirms it 9 of 9 | The mobility plan: refusing Zippa leaves at most 2,600 licensed devices against the required 3,000 |
| 2 | The same rates with the minimum fleet applied: operators over 10 refused in order of rate while 3,000 devices stay licensed | Refuse Volt (11.5; refusing Zippa breaches the minimum by 400) | The permit's measure and the plan's limit, both applied exactly | The permit register: the registrations of 45% of Zippa's and 35% of Volt's active devices end when this term closes |
| 3 | **Decisive:** each renewal fleet from the register's dates, its rate built from the approved models' trips and conditioned on season to a full year's mix | **Hold: refuse none.** Highest renewal fleet Glide at 9.0 | — | — |

* **Every candidate fails, and why.** Zippa (8.6) and Volt (8.1) are retiring the models that carried their rates. Glide (9.0) and Hop (7.5)
  never reached 10. Refusing all four fails because the rate per trip fell as trips grew.
* **The blocking quantity.** The highest renewal-fleet rate, Glide's 9.0, sits 10% under the threshold. It would become a refusal if
  Glide's rate were 12% higher, or if Zippa kept a quarter of its old model's trips into the new term.
* **Partial correction priced (L3).** A solver who takes the renewal fleet but reads the approved models' raw winter rates finds Zippa at 11.0
  and refuses it, or Volt at 10.4 once the minimum binds. One who conditions on season but keeps the active fleet finds Zippa at 13.6 and
  Volt at 11.0 and refuses one of them. Neither half reaches the hold.
* **Grid.** Population (active, renewal) × season (raw, conditioned) × minimum fleet (ignored, applied) gives 8 cells. Only the two renewal,
  conditioned cells hold, with or without the limit, since no operator is over. Every other cell refuses Zippa or Volt.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The framework names the fleet licensed for the renewal term, and the approval scheme ends unapproved registrations at
   term close. No document says the approved models' rates are winter-only, or that the active flag includes retiring devices.
2. **Corpus blind for a computable reason.** *In every past renewal the fleet licensed for the new term was the fleet assessed, because no
   approval scheme retired a model at renewal before this year, so this year's rate and the renewal fleet's were the same.* The book
   certifies judging the active fleet in 9 of 9 renewals.
3. **No arithmetic symptom.** Incident reports reconcile to the trauma registry, trips to the operators' billing, and the register to the
   permits issued.
4. **Not a row predicate.** The renewal fleet comes from each device's registration dates, and its rate needs the approved models' monthly
   trips and injuries reweighted to a full year's months by the seasonal profile of models that ran all year.
5. **The enumeration is arithmetic.** No field gives a renewal-fleet rate. It is computed from months and models.
6. **No cutover date.** The approved models arrived over five months from October, and each device's registration carries its own dates.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** Nine past permit renewals in the city and two peer cities. Each holds the operator's rate on the active fleet at renewal and the
  rate realised over the following term.
* **What it certifies.** Rates per trip on the active fleet, and that the term-to-term rate is stable: the assessed and realised rates agree
  within 6% in 9 of 9. Injury counts alone miss all nine.
* **What it is blind to.** Retiring fleets (property 2).
* **Twin pair.** Zippa's Riverside zone and Hop's Old Town zone are identical on active devices (300), trips (640,000), injuries (83) and rate
  (13.0). Riverside's fleet is 80% old model, all retiring. Old Town's single model is renewed whole. On their renewal fleets the
  conditioned rates are 6.5 and 13.0 (2.0×). Only the register's dates and the seasonal conditioning separate them.
* **Resemblance points at the decoy.** Zippa's profile most resembles the book's 2021 renewal of a peer city's operator, refused at 13.8,
  whose rate over the next term came out at 13.5.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The permit framework: "A permit is renewed unless the operator's injury rate per 100,000 trips on the fleet licensed for
  the renewal term exceeds 10." The mobility plan: "At least 3,000 shared devices are licensed across the city in every term." The approval
  scheme: "An unapproved model's registration ends when the current term closes." The permit register lists each operator's device cap.
* **Empirical pins.** The seasonal profile comes from three years of every model that ran all year. Rates come from the incident reports
  and trip logs.
* **Voices.** Council member: "Three times the injuries is three times too many." Transport officer: "Per trip, Zippa is plainly the worst,
  and the numbers say so." Volt's policy lead: "Our rate is near the city's average; look at Zippa." Trauma consultant: "Most of the scooter
  patients we see were not on shared scooters at all."
* **Licensed wrong basis.** The framework records that the council's transport committee reads operator safety from the annual incident
  league table on the active fleet and will see the renewals on that basis.

## 8. Determinism by construction

* **Season.** The winter factor of 1.28 comes from every model that ran all year in all three years. Any factor from 1.20 to 1.36 keeps
  Zippa's renewal fleet between 8.1 and 9.2, under 10.
* **Renewal fleet.** Every unapproved device's registration ends at term close, no approved device's does, and approved devices registered
  but not yet delivered carry their model's rate.
* **Trips.** A trip is a log entry from unlock to lock. Every operator's app logs trips the same way, so no chaining rule applies.
* **Minimum fleet.** Caps are Zippa 2,000, Volt 1,000, Glide 900 and Hop 700, all at their caps.
* **Maturity.** Incident reports for the term closed 30 days after its last trip, and the extract follows the final quarterly audit.

## 9. Prompt sketch and deliverables

> The council votes on the scooter renewals next month, and one member's motion would refuse all four because injuries tripled. Tell me which
> operators we refuse, if any, in a sentence the council can vote on, with each operator's injury rate per 100,000 trips as you count it, to
> one decimal. Send `renewal_case.xlsx`, a chart `operator_rates.png`, and a one-page `council_paper.pdf`.

* `renewal_case.xlsx` — the four operators on every construction, the parking sheet (ask A), the curb-fee sheet (ask B) and the book
  back-test (ask C).
* `operator_rates.png` — each operator's rate on this year's fleet beside its renewal fleet's, with the threshold as a labelled line, an inset
  of monthly rates per trip for models that ran all year, and a title stating the decision.
* `council_paper.pdf` — the hold, the blocking quantity and what would turn it into a refusal.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each operator and quarter, the share of trips that ended in a designated parking corral.
  *Device:* the parking rule counts a trip ending within 10 metres of a corral's polygon, as the permit's parking schedule states. Testing
  the end point against the bare polygon undercounts compliant trips by about a fifth. Parking never enters injury rates.
* **Ask B (device-carried).** For each operator and quarter, the curb-use fees owed. *Device:* fees accrue per licensed device-day, and
  devices on maintenance hold accrue nothing on held days, recorded in a separate hold table. Ignoring the holds overstates fees by about
  8%. The main call never reads the hold table.
* **Ask C (validity).** For each of the nine past renewals, the realised rate beside the rate your construction gives at renewal.
* **Decoupling.** Clearing the renewal-fleet construction or the minimum fleet changes no figure in asks A or B. Ask C holds no retiring
  fleet, by property 2.

## 11. Rubric arithmetic

4 operators × 4 quarters (ask A) + 4 operators × 4 quarters (ask B) + 9 renewals (ask C) + the hold, the blocking quantity and each operator's
renewal-fleet rate + 5 named chart parts + 3 files ≈ 55 criteria.

## 12. World-building constraints

* Injuries ×3.0 and trips ×3.6 over three years. Active-fleet rates are Zippa 14.2, Volt 11.5, Glide 9.0 and Hop 7.5.
* Zippa's old model carries 75% of its trips at 15.3 and Volt's 80% at 11.8. Their approved models ran October to March at raw rates of
  11.0 and 10.4, which the 1.28 winter factor turns into 8.6 and 8.1.
* Caps total 4,600, so refusing Zippa leaves 2,600, and refusing Volt leaves 3,600.
* The book holds nine renewals, none with a retiring model. Riverside and Old Town are identical on every active-fleet column.
* Every non-hold cell refuses Zippa or Volt, and the hold's blocking quantity sits 10% under the threshold.
* Corral polygons and maintenance holds never touch incidents, trips or registrations.

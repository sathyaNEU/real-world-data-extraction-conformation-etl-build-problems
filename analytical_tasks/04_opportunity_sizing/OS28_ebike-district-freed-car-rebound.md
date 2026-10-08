# OS28 — Which district gets the city's 1,500 leased e-bikes, when the car a rider leaves at home is driven by someone else

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Policy & Education · urban transport programmes |
| Mirrors | Substitution sizing that counts the user who switches but not the shared asset they free (ride-hail and car-share substitution where another household member drives the freed car, a released cloud reservation absorbed by another team's workloads, a family subscription that keeps streaming after one member leaves) |
| Decision shape | Which of N gets one scarce thing, with the sizing graded: the e-bike leasing scheme goes to one of six districts |
| Committed call | The district that gets the scheme, and the car-kilometres a year it removes there |
| Gap · Pattern | Gap 2 (population) · S2 (the decisive population is a residual between two correct records: trips by other household drivers in the car the rider frees), with E29 below it (short car trips split by the home-to-home tour each sits in) |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #6 treats a mixed segment all one way · #5 takes the population a flag or filter suggests · #20 leaves the deciding comparison unstated |
| Calibration form | Gold-standard verification subsample: last year's pilot households, logged by the rider's phone and a logger on every household car, one week before delivery and one week six months after |
| Driving force | A rider's car does not stop moving. In a household with fewer cars than licensed drivers, where another adult takes the bus because the car goes to work, that adult takes the freed car. The household car's logger records those trips and nobody's survey row does: they are an exact residual between the car logger and the rider's own driving. They appear only in "contested-car" households, a property of the household roster and of each other member's travel. |

## 1. Situation

A metropolitan transport fund has 1,500 subsidised e-bikes on two-year leases and will place the whole scheme in one of six districts next
year. The fund scores schemes on the annual reduction in kilometres driven by the district's household cars. Last year a pilot leased 400
e-bikes in two other districts, and the city's travel-survey team verified 380 of the riders' households with GPS loggers. The programme
officer wants the scheme in Old Town, the inner district with the most short car trips in the city.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the travel survey, the riders' switched kilometres, the car loggers and the household rosters.
  Riders really do stop driving those kilometres, and the officer's count of short trips is right. Nothing is overturned; the difficulty is
  that the scored quantity belongs to the household's cars, and some cars keep moving.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the officer's view and every voice. Tour-level substitution with the verified switched shares still names
  Northgate, and nothing in the pack mentions anyone but the rider.
* **Instrument repair.** Give every rider a perfect diary and every car a perfect logger. Both already are perfect. The rebound is
  produced by other people's real trips, and no better instrument of the rider removes it.
* **Lens swap.** The rider's own driving and the trips other household members make in the freed car are different populations. The
  answer needs the second one, which is in no survey row.

## 3. The driving force

A strong solver counts short car trips, then keeps only those in home-to-home tours that can be ridden end to end, then prices each tour
type at the GPS-verified switched shares. That is the textbook substitution build, verified against a gold standard, and it names
Northgate. But the fund scores kilometres driven by household cars, and in 166 of the 380 verified households the car logger fell by only
12% of what the rider stopped driving. In those households the car had been the reason another adult took the bus, and once the rider
switched, that adult drove. The rebound shows only as the car logger's vehicle-kilometres minus the rider's follow-up driving. It occurs
exactly where the household has fewer cars than licensed drivers and another driver used a non-car mode on the rider's commute days. That
is a household-level construction across members' diaries. Northgate is a district of one-car, two-commuter households; Ashby Vale's
second adults mostly work from home.

## 4. The ladder

| Rung | Construction (per eligible resident, km a week) | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Short car-driver trips (3 miles or less) × the pilot's switched share of all short kilometres (0.36) | A, Old Town, 11.52 (1.23× Riverside) | The official definition of a bikeable trip and the pilot's own switching rate | The fund's guidance counts a car journey as replaceable only when its whole home-to-home tour can be ridden |
| 1 | Short kilometres inside all-short tours only (a join from trip to person-day tour) × the pilot's pooled in-tour share (0.48) | B, Riverside, 9.98 (1.19× Northgate) | Tour-level feasibility, which is the planners' own objection to trip counting, executed correctly | The verified riders switched 0.72 of kilometres in single-stop tours and 0.31 in multi-stop ones |
| 2 | Tour-type switched shares applied to each district's single-stop and multi-stop mix | C, Northgate, 12.24 (1.22× Ashby Vale) | Gold-standard switching rates by tour type, reproduced by every verified rider | Car loggers fell by only 12% of switched kilometres in 166 of 380 verified households |
| 3 | **Decisive:** net of rebound: × (1 − 0.88 × the district's contested-car share), the share built from the household roster and each other driver's travel | **E, Ashby Vale, 9.61 (1.29× Riverside)** (5th of 6 at rung 0) | — | — |

* **The answer.** Ashby Vale: 9.61 km per rider-week, so 1,500 riders over 52 weeks remove 749,300 car-kilometres a year, committed as
  750,000.
* **Position table.** Ashby Vale ranks 5th on rung 0, 3rd on rung 1 and 2nd on rung 2 (1.22× behind Northgate), and leads only rung 3.
  Rung leaders beat their runners-up by 1.23×, 1.19×, 1.22× and 1.29×.
* **Discriminator dominance.** Northgate carries a 1.22× lead into rung 3. Ashby Vale keeps 0.956 of its switched kilometres (contested
  share 0.05) against Northgate's 0.490 (0.58), an edge of 1.95×, which is 1.34 times the required 1.2 × 1.22 = 1.46.
* **The deciding comparison (#20).** For Northgate, the memo must set 12.24 km switched against 6.25 km rebound. For Ashby Vale it is 10.05
  against 0.44. Switched kilometres alone never decide.
* **Partial correction priced (L3).** Every half-applied netting names a wrong district. Netting rebound at the pilot's pooled 0.39 keeps
  Northgate, 7.47 against Ashby Vale's 6.13 (1.22×). Charging rebound to every household with fewer cars than drivers also keeps
  Northgate, 5.56 against 4.92 (1.13×), because Ashby Vale has many such households whose second adult never needed the car. Finding the
  contested rebound but skipping the tour-type rates names Riverside, 9.11 against Ashby Vale's 7.23 (1.26×).
* **Grid.** Trip or tour grain × pooled or typed in-tour shares × rebound (none, pooled, every short-of-cars household, contested) = 12
  feasible cells. Every non-answer cell names Old Town, Riverside, Northgate or Westmoor.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The guidance defines replaceable journeys and the scored quantity. No document mentions other household members, the
   freed car, or rebound.
2. **Corpus pins it only as a residual.** *In every pilot household's before week, car-logger kilometres equal the sum of all members' diary
   driving exactly, because every member was surveyed.* In the after week only the rider is followed, so the rebound exists as the
   difference between two of the subsample's files and in no row of either. The rider files alone confirm rung 2 for all 380 households.
3. **No arithmetic symptom.** Trips, tours, riders, loggers and survey weights reconcile on every rung, and the rider-level switched
   kilometres tie to the logger kilometres in non-contested households to the metre.
4. **Not a row predicate.** Contested status needs a household group-by: cars against licensed drivers, then each other driver's mode on the
   rider's commute days from their own diary rows.
5. **The enumeration is arithmetic.** No column says "contested". The district shares are computed over 6,200 surveyed households.
6. **No cutover date.** Rebound starts household by household as bikes are delivered, and no aggregate series steps.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** 380 pilot households with rider phone logs, car loggers on every household vehicle, the before-week diaries of every member and
  the rider's after-week diary.
* **What it certifies.** Tour feasibility (every switched trip sat in an all-short tour) and the switched shares by tour type (0.72 and 0.31),
  which reproduce every rider's switched kilometres within 3%. A solver who back-tests rungs 1 and 2 is confirmed.
* **The absolute split (O2).** In 214 non-contested households the car logger fell by exactly the rider's switched kilometres. In 166
  contested households it fell by 0.12 of them (0.09 to 0.15), with no household in between.
* **Twin pair.** Pilot neighbourhoods Larchfield and Mill Row are identical on riders' tour mix, household size, cars, licences and switched
  kilometres. Their car-kilometre reductions differ 2.13×, at contested shares of 0.10 and 0.65. No rider-level rate reproduces both.
* **Resemblance points at the decoy.** Northgate's riders match the pilot's best-switching riders on tour mix, commute length and age.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The fund's guidance scores a scheme on the annual reduction in kilometres driven by the district's household cars, counts a
  journey as replaceable only when its whole home-to-home tour can be ridden, and annualises a survey week at 52. The scheme's eligibility
  is adult residents who drive to work on at least three days a week.
* **Empirical pins.** Switched shares by tour type and the 0.88 rebound in contested households come from the verification subsample, and
  contested shares by district come from the survey rosters and diaries.
* **Voices.** The programme officer: "Old Town has more short car trips than anywhere; that's where e-bikes pay." The cycling campaign's
  chair: "Every e-bike is a car off the road."
* **Licensed wrong basis.** The guidance records that the regional assembly's transport committee compares schemes on riders' own driving
  kilometres and will see that basis.

## 8. Determinism by construction

* **Contested threshold.** Other drivers used a non-car mode on 0–1 or 4–5 of the rider's commute days, never 2–3, so 2-, 3- and 4-day
  definitions return the same households.
* **Tour construction.** Every person-day starts and ends at home, and no trip lacks a purpose code, so tour building has no convention to
  choose.
* **Annualisation.** Pinned at 52 survey weeks by the guidance. The answer (749,300) sits 4,300 from the nearest rounding boundary.
* **Weights.** The survey's household weights are filed and reproduce district populations, so weighted and unweighted shares order the
  districts identically.
* **Maturity.** Every pilot after-week fell six months after delivery, no bike was returned, and no household changed cars between weeks.

## 9. Prompt sketch and deliverables

> The fund will put its 1,500 leased e-bikes into one district next year, and our programme officer thinks Old Town is the obvious home.
> Tell me which district gets the scheme and how many car-kilometres a year it saves, to the nearest 10,000, in a sentence for the fund
> board. Send `ebike_district_case.xlsx`, a chart `district_net_km.png`, and a one-page `board_note.pdf`.

* `ebike_district_case.xlsx`: the six districts under the four rung bases, the bus sheet (ask A) and the parking sheet (ask B).
* `district_net_km.png`: for each district, switched kilometres and rebound kilometres as a diverging bar per rider-week, net marked as a
  dot, districts sorted by net, the chosen district highlighted and the contested share printed on each bar.
* `board_note.pdf`: the committed district, its annual figure and the deciding comparison.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the six districts, average weekday bus boardings at the district's stops last year and
  the share that were transfers. *Device:* a tap within 60 minutes of a previous tap is a free transfer with a zero fare and a transfer
  flag, as the smartcard guide documents. Counting taps as boardings overstates boardings by 18% in the three districts on trunk routes.
* **Ask B (device-carried).** For each district, secure cycle-parking spaces at its ten busiest destinations and their weekday occupancy.
  *Device:* the parking register counts stands, and a stand holds two bicycles while a locker holds one, per the register guide. Reading
  stands as spaces halves capacity and doubles occupancy at stand-heavy sites.
* **Ask C (validity).** Each district's per-rider value under each of the four rung bases. Also the subsample's aggregate car-kilometre fall
  as predicted by riders' switched kilometres against the logged figure. Switched kilometres exceed the logged fall by 64% (the rebound is
  0.39 of switched kilometres), and the contested netting reproduces every household to within 3%.
* **Decoupling.** Clearing the rebound construction changes no figure in asks A or B.

## 11. Rubric arithmetic

6 districts × 2 (ask A) + 6 × 2 (ask B) + 6 × 4 bases + 1 reproduction figure (ask C) + the committed district, its annual figure, its margin
and the two deciding comparisons + 5 named chart parts + 3 files ≈ 62 criteria.

## 12. World-building constraints

* District values (km per eligible resident-week): short car-driver km Old Town 32, Riverside 26, Northgate 25, Westmoor 22, Ashby Vale 21,
  Crossfield 17. All-short-tour shares 0.45 / 0.80 / 0.70 / 0.55 / 0.75 / 0.65. Single-stop shares 0.80 / 0.20 / 0.95 / 0.40 / 0.80 /
  0.55. Contested shares 0.70 / 0.10 / 0.58 / 0.05 / 0.05 / 0.20. Shares of households with fewer cars than drivers 0.85 / 0.55 / 0.62 /
  0.30 / 0.58 / 0.35.
* Pilot: 380 verified households, 214 non-contested (rebound 0) and 166 contested (rebound 0.88 ± 0.03). Pilot all-short-tour share 0.75
  and single-stop share 0.415, so 0.48 × 0.75 = 0.36.
* Rung leaders are Old Town, Riverside, Northgate and Ashby Vale with margins of at least 1.19×, and all twelve grid cells name as stated.
* Larchfield and Mill Row are identical on every rider- and household-level column except other drivers' modes.
* Transfer taps and parking stands never touch the travel survey, the riders' logs or the car loggers.

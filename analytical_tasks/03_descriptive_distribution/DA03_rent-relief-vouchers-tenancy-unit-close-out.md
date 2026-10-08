# DA03 — How a city splits 3,000 anti-displacement vouchers across nine neighbourhoods, when last year's close-out counted tenancies and the survey counts dwellings

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Policy & Education · housing policy and programme allocation |
| Mirrors | Allocating a capped benefit across markets from panel estimates built on households when the benefit attaches to each paying contract (relief offers on shared streaming and telecom plans whose members pay separately, host-relief funds per listing against per property on lodging marketplaces, seat-based licence credits across shared workspaces) |
| Decision shape | An allocation under a cap: 3,000 vouchers split pro rata to severely rent-burdened renter households, no neighbourhood above its enrolled landlord units |
| Committed call | The allocation table in whole vouchers summing to 3,000, headed by Harlow Flats' allocation |
| Gap · Pattern | Gap 4 (rule) over Gap 3 (objective) · Pattern B (the certified close-out reproduces only on tenancies), with E14 (the landlord-registry limit applied in the figure) below it |
| Gate G mechanism | method_or_model_selection, with binding_constraint |
| Measured traps engaged | #1 reports a failed back-test, ships anyway · #3 stops at a close but inexact match · #10 notes a binding limit as a risk · #2 counts file rows instead of the real unit |
| Calibration form | Prior-period close-out: the 2025 programme close-out, which certified each neighbourhood's count and margin of error from the 2025 survey wave (18 cells) under a basis no document spells out |
| Driving force | The close-out certified severely burdened tenancies, and no file stores a tenancy. A tenancy is everyone whose rent reaches the landlord through the same payer, read from the person roster's rent-payer pointer, with burden on the tenancy's pooled income. Rooming houses in Harlow Flats and Delph Row hold three to five tenancies per dwelling, while Corran Hill's flat-shares are one joint lease paid through a lead tenant. The survey household pools the roomers' incomes and hides the first; splitting unrelated adults, the textbook repair, invents the second. |

## 1. Situation

A city's anti-displacement programme has 3,000 rent-relief vouchers for 2027 and must split them across nine neighbourhoods in proportion
to each one's severely rent-burdened renter households (rent above half of income). A voucher can only be used in a unit whose landlord
is enrolled in the programme's landlord registry. The estimate comes from the city's Housing Conditions Survey, a stratified sample of
rental dwellings with design weights, 80 successive-difference replicate weights, a dwelling file and a person roster. The pack holds
the 2026 and 2025 survey waves, the landlord registry, and the 2025 close-out with its certified estimates and the allocation it made.
Council approves the split on 9 February.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the survey's weights and records, the registry's enrolments and the close-out's certified cells.
  The survey's dwelling-level burden is a true statement about dwellings, and nobody's reading of their own numbers is overturned. The
  difficulty is the unit the certified basis counts, and where a capped share then goes.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Remove the housing director's view, the coalition's view and the finance committee's licensed basis. The dwelling
  file still offers one weighted row per household with rent and income on it, and pro-rata shares off it still look complete.
* **Instrument repair.** A perfect dwelling interview already records every occupant, income and rent share, and this one does. A
  tenancy is an arrangement between occupants and a landlord that the dwelling record carries only through the roster's pointer, so no
  better dwelling instrument removes the construction.
* **Lens swap.** The reads count different units: 61,400 weighted renter dwellings against 78,900 tenancies, 11,910 of them severely
  burdened against 10,040 burdened dwellings.

## 3. The driving force

A strong solver weights the dwelling file, counts dwellings whose rent exceeds half the household's income, applies the registry limit
and checks itself against the close-out, as the programme rules require. It reproduces Eastgate, Corran Hill and Quarry Bank and misses
the other six, every miss low. The textbook repair splits unrelated adults into their own units. That reproduces 14 of 18 certified cells,
and the four misses (Corran Hill and Quarry Bank, too high) look like a student quirk. The certified basis is the tenancy. In a rooming
house each roomer pays the landlord under their own agreement, and a third of a dwelling's pooled income hides a roomer paying two-thirds
of their own income. In a flat-share on a joint lease, the occupants pay through a lead tenant and are burdened as one. Only the roster's
rent-payer pointer separates the two. Grouped by payer, with burden on each tenancy's pooled income, the 2025 wave reproduces all 18
cells, and the shares move toward the rooming-house neighbourhoods.

## 4. The ladder

| Rung | Construction | Lands on (Harlow Flats) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Weighted burdened dwellings, vouchers pro rata | 323 (−46.8%) | The survey's own unit and weights, cleanly applied | The programme rules' registry clause: Eastgate's pro-rata 986 against 450 enrolled units |
| 1 | Same counts, Eastgate held to its 450 enrolled units, the excess shared pro rata | 409 (−32.7%) | The binding limit applied in the figure rather than noted as a risk | The close-out: dwellings reproduce 6 of 18 certified cells, every miss low (−15.7% on the total) |
| 2 | Unrelated adults split into their own units (families and unrelated individuals), limit applied | 532 (−12.4%) | The textbook repair for shared housing, reproducing 14 of 18 cells | The roster's rent-payer pointer: Corran Hill and Quarry Bank flat-shares pay through a lead tenant on one lease |
| 3 | **Decisive:** tenancies grouped by rent payer, burden on each tenancy's pooled income, limit applied | **607** | — | — |

* **Figure shape.** Harlow Flats' allocation is the maximum cell of the grid; every partial basis under-funds the rooming-house
  neighbourhoods. The full answer is Eastgate 450, Harlow Flats 607, Corran Hill 225, Millbrook 350, Stanwick 281, Delph Row 450,
  Ingleby 255, Quarry Bank 225, Whitlow 157.
* **Partial correction priced (L3).** A solver who groups by the payer but divides a joint lease's rent by the lead tenant's income alone
  over-counts the flat-shares and lands at 529 (−12.9%), beside rung 2. Tenancies built without the registry limit land at 516 (−15.0%).
* **Grid.** Unit (dwelling, individual, tenancy) × registry limit (ignored or applied) gives 6 cells. The nearest non-answer cell is
  rung 2 at −12.4%. Reaching 607 takes the tenancy and the limit together.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The rules allocate "in proportion to severely rent-burdened renter households, on the basis certified in the most
   recent close-out". The roster codebook glosses the pointer as "line number of the person who pays this person's rent". No sentence
   mentions a tenancy or a lease.
2. **Reproduction, and why it is a construction.** Tenancies reproduce 18 of 18 certified cells (9 counts, 9 margins of error).
   Individuals reproduce 14 and dwellings 6. Each rival misses one way (dwellings low by 15.7% on the total, individuals high by 10.2%), so
   neither nets out. The reproducing unit is built from the person roster by a pointer, then burdened on pooled income. It has no
   parameter a sweep can reach, and no flat add-on or split rule matches both twins.
3. **No arithmetic symptom.** Dwelling weights sum to the frame. All three units partition the same weighted persons, so person and
   income totals tie under every rung, and replicate estimates reconcile.
4. **Not a row predicate.** Burden belongs to a group of roster persons formed by the pointer, with that group's income and rent. Neither
   a dwelling row nor a person row carries it.
5. **The enumeration is arithmetic.** No column says "tenancy". 78,900 weighted tenancies are assembled from 152,000 roster lines.
6. **No cutover date.** Rooming houses and joint leases are standing features of each neighbourhood's stock, and nothing steps.
7. **Survives deletion.** No wrong number exists to delete. Without any voice, the dwelling file still invites itself as the unit.

## 6. The calibration corpus

* **Form.** The 2025 close-out: for each neighbourhood, the certified count of severely burdened renter units and its 90% margin of error
  from the 2025 wave, plus the allocation made. The 2025 wave's dwelling file and roster ship with it.
* **What it pins.** The tenancy (above). It also pins the variance method: the certified margins reproduce only under the 80-replicate
  successive-difference formula (factor 4/80, 1.645 for 90%), which a binomial or design-effect shortcut misses in all nine.
* **Twin pair.** Corran Hill and Delph Row are identical on every dwelling and person column: dwellings, occupants per dwelling,
  relationships (all unrelated adults), incomes, rents and weights. Only the pointer differs. Corran's occupants pay through a lead
  tenant, and Delph's each pay the landlord. Their certified counts are 760 and 1,520 (2.0×). Dwellings give both 760 and individuals
  give both 1,520; only tenancies give both right.
* **Resemblance points at the decoy.** Harlow Flats' dwelling profile (older converted houses, three to five unrelated adults) most
  resembles Corran Hill's, whose certified count equals its dwelling count.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The programme rules: "Vouchers are allocated in proportion to each neighbourhood's severely rent-burdened renter
  households, rent above half of income, on the basis certified in the most recent close-out; a basis may be used only if it reproduces
  every certified estimate and margin of error in that close-out." The programme rules: "No neighbourhood receives more vouchers than
  the units enrolled in the landlord registry there on 1 January; any excess is shared pro rata among the rest, in whole vouchers by
  largest remainder."
* **Empirical pins.** The tenancy, and the replicate variance formula, both from the close-out.
* **Voices.** The housing director: "The survey's household weights were built for exactly this; use them as delivered." The tenant
  coalition's organiser: "Every adult in a shared flat is fighting the rent on their own; count each one."
* **Licensed wrong basis.** The rules record that the council's finance committee checks allocations against the survey's published
  household estimates and will table its own split.

## 8. Determinism by construction

* **Threshold.** Burden is rent strictly above half of income. No tenancy, dwelling or individual sits within 0.5 points of 50%, and none
  has zero income.
* **Weights.** A dwelling's weight carries to every tenancy in it, and each replicate weight likewise, so tenancy margins need no new
  weighting convention.
* **Registry date.** Enrolments are counted on 1 January 2027 from the registry's effective dates, and none starts or ends within a week
  of it.
* **Rounding.** Largest-remainder rounding fixes the whole vouchers, and the world has no tied remainders. Only Eastgate binds, under every
  unit.

## 9. Prompt sketch and deliverables

> Council approves the 3,000 anti-displacement vouchers on 9 February, and I have to table how they split across our nine
> neighbourhoods. The housing director would use the survey's household weights as delivered. Give me each neighbourhood's allocation in
> whole vouchers, summing to 3,000, as the table I put to council, and send `voucher_allocation.xlsx` with the build and the sheets below,
> plus `allocation_shift.png`.

* `voucher_allocation.xlsx` — the 2025 reproduction and the 2026 allocation, the four constructions' allocations and hit counts (ask C),
  the inspection sheet (ask A) and the eviction sheet (ask B).
* `allocation_shift.png` — grouped bars of each neighbourhood's allocation under the four rung constructions, Eastgate's 450-unit limit
  as a marker, Corran Hill and Delph Row annotated as the twin pair, and each construction's certified-cell hit count in the legend.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each neighbourhood, the share of 2026 code-enforcement inspections of rental units that found
  a hazard in each of three categories (heating, damp and mould, fire safety). *Device:* a re-inspection of an open violation posts as a
  new inspection record with follow-up type F, as the inspection manual documents. Counting follow-ups as inspections inflates the
  denominator and understates every share by 3 to 11 points.
* **Ask B (device-carried).** Distinct residential eviction cases filed in each half of 2026, per neighbourhood. *Device:* adding a
  respondent to a filing creates a new docket entry with an "-A" suffix that the court's filing guide treats as the same case. Counting
  entries overstates cases by 14% overall and by 31% in Delph Row.
* **Ask C (validity).** Harlow Flats' allocation and the certified-cell hit count (of 18) under each of the four rung constructions.
* **Decoupling.** The inspection log and the court file share no row with the survey. Clearing the tenancy construction changes no figure
  in asks A or B.

## 11. Rubric arithmetic

9 neighbourhoods × 3 hazard shares (ask A) + 9 × 2 half-years (ask B) + 4 constructions × 2 (ask C) + the nine committed allocations and
Eastgate's reallocated excess + 4 named chart parts + 2 files ≈ 69 criteria.

## 12. World-building constraints

* Burdened counts by unit (Eastgate, Harlow Flats, Corran Hill, Millbrook, Stanwick, Delph Row, Ingleby, Quarry Bank, Whitlow):
  dwellings 3,300 / 1,080 / 760 / 1,100 / 920 / 760 / 840 / 760 / 520; individuals 3,300 / 2,050 / 1,520 / 1,180 / 950 / 1,520 / 860 /
  1,220 / 530; tenancies 3,300 / 2,050 / 760 / 1,180 / 950 / 1,520 / 860 / 760 / 530.
* Enrolled units: Eastgate 450, Harlow Flats 690, and every other neighbourhood above its share under every unit, so only Eastgate binds.
* Harlow Flats lands at 323 / 409 / 532 / 607 by rung, and the other grid cells are 468 and 516.
* In the 2025 wave, tenancies reproduce 18 of 18 certified cells, individuals 14 and dwellings 6. Dwellings miss the certified total by
  −15.7% and individuals by +10.2%.
* Corran Hill and Delph Row differ only in the rent-payer pointer. No tenancy straddles two dwellings.
* The inspection log and the court file touch no survey row.

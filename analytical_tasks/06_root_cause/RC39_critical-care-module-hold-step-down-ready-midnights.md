# RC39 — Whether the board's critical-care module goes anywhere, when the fullest unit's winter nights are patients waiting for a ward bed

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Economics · health-system finance and capital planning |
| Mirrors | Critical-care expansion cases at large hospital operators (HCA Healthcare, Kaiser Permanente, NHS critical-care networks), and the same shape in capacity cases at cloud platforms and fulfilment networks, where occupied capacity includes units held only because the next stage has no room (GPU nodes held by jobs waiting on storage, dock doors held by trailers waiting for yard space) |
| Decision shape | Hold, forced by a blocking quantity: no unit's projected peak of critical-care need reaches the 85% trigger |
| Committed call | Place the 12-bed critical-care module nowhere this round, because the highest projected peak of critical-care need is Brackenfield's 80.8% against the 85% trigger |
| Gap · Pattern | Gap 3 (objective) at rung 1, Gap 2 (population) at the decisive rung · Pattern D (spending against occupied midnights) beneath the quiet second trap of measured #11 (step-down-ready midnights inside the critical-care census, with their own control in the units' readiness record), and the hold of Part 6.4 |
| Gate G mechanism | signal_vs_noise_or_hold, with decomposition_attribution |
| Measured traps engaged | #11 beats the headline trap, misses the quiet one · #13 validates on one population, applies to another · #7 uses the ready-made measure |
| Calibration form | Existing-book actuals: the regional capital programme's seven closed critical-care projections at hospitals in two neighbouring regions, each with its basis year and the peak occupancy realised three years on |
| Driving force | Every number is correct: the deck's spending, the critical-care census, the stays, the bed bureau's log and the book. Once the deck's price-driven "intensity" is set aside and age is weighted by each group's critical-care use (the projection the book reproduces 7 of 7), Brackenfield projects to 98.6% and takes the module. But 18% of Brackenfield's winter-peak midnights belong to patients the intensivist had already recorded as ready to step down to a ward, who stay only because the medical wards are full. The capital rule counts patients who need critical care. On that basis no unit reaches 85%, and Brackenfield peaks at 80.8%. |

## 1. Situation

Northvale Health runs five adult critical-care units with 136 commissioned beds. Critical-care spending rose 48% in five years. The
strategy director's deck deflates spending per resident by consumer prices, calls the result an intensity boom and asks for more
critical-care beds. The deck reports spending by service line and never projects occupancy or ranks units. The board has one 12-bed
critical-care module in this capital round. The capital rule approves it for a unit whose projected peak occupancy exceeds 85% within
three years, and where several qualify the largest shortfall takes it. The CFO wants the growth taken apart before the board commits. The
board may also place the module nowhere this round.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct: the deck's spending series, the critical-care census, the stays, the readiness record, the
  bed bureau's log, the population projections and the book. No one's reading of their own figures is overturned, and Brackenfield's unit
  really is full every winter night. The difficulty is which of those midnights the trigger counts.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the deck and every voice. The census projection on age-sex weights, which the book certifies 7 of 7, still names
  Brackenfield at 98.6%, and only the readiness record turns it into a hold.
* **Instrument repair.** Record every admission, readiness decision and ward transfer to the minute. Step-down-ready patients still hold 18%
  of Brackenfield's peak beds, and the trigger still counts only patients who need critical care.
* **Lens swap.** The naive read is spending per resident over the whole year. The answer is January midnights of patients before their
  step-down point, a different population and a different moment.

## 3. The driving force

A strong solver sets the deck aside, because its intensity is ECMO consumables, devices and drug prices, and none of those holds a bed. It
rebuilds growth from occupied midnights at the census. It weights age by each group's critical-care use rather than by the 65+ share,
because residents over 85 use less critical care than those aged 70 to 79. The book reproduces that projection at all seven closed
hospitals. Brackenfield, where retirees aged 65 to 79 are moving in, projects to 98.6% and takes the module. The quiet trap sits inside the
census. Once the intensivist records a patient as ready for a ward bed, the patient stays in critical care until the medical wards free one,
and Brackenfield's medical wards run fullest in January. The readiness record dates each step-down point. The bed bureau's log looks like
the same evidence, but direct transfers within medicine never pass through the bureau. Counted from the readiness record, 18% of
Brackenfield's peak midnights are patients who no longer need critical care. Its need projects to 80.8%, and no unit reaches 85%.

## 4. The ladder

| Rung | Construction | Names (projected peak, % of beds; beds short) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The deck's CPI-deflated critical-care spending per resident, carried onto each unit's base-year peak | Thornleigh (100.0%, 8.5 short, 2.18× Greyford's 3.9) | The board's own intensity series, already per resident | The census: Thornleigh's occupied midnights per resident grew 0.5% a year while its real spending per resident grew 6.5%, the gap being ECMO, device and drug prices |
| 1 | Occupied midnights per resident, ageing adjusted by the 65+ share, five-year trend carried forward | Ostley (103.7%, 4.4 short, 1.88× Brackenfield's 2.3) | The decision's own grain and the standard ageing correction | The regional age-sex rates: residents over 85 use 40% fewer critical-care midnights per head than those aged 70 to 79, and Ostley's growth is almost all over 85 |
| 2 | Midnights per age-sex-weighted resident, the projection the book reproduces 7 of 7 within 1.5 points | Brackenfield (98.6%, 3.8 short, 3.83× Ostley's 1.0) | Certified on every closed projection, and Brackenfield resembles Tarnside General | The readiness record: 18% of Brackenfield's peak midnights fall after the intensivist recorded the patient as ready for a ward bed |
| 3 | **Decisive:** midnights before each patient's step-down point, rebuilt night by night, peaked over the 28 busiest nights and projected on age-sex weights | **Hold.** Highest unit Brackenfield at 80.8%, 4.2 points under the trigger | — | — |

* **Every candidate fails, and why.** Thornleigh (77.8%) and Greyford (77.5%) grew in price, not in midnights. Ostley (79.4%) is ageing past
  the years of heaviest critical-care use. Pennard (79.2%) never approached the trigger. Brackenfield (80.8%) grows fastest, but 18% of its
  peak is patients waiting for a ward bed.
* **The blocking quantity.** The highest projected peak of critical-care need, Brackenfield's 80.8%, sits 4.9% (4.2 points) under the 85%
  trigger, and every unit has beds spare. It would become a build if Brackenfield's step-down-ready share of peak midnights were 13.8% or
  less, or if its need grew 5.2% more over the three years than the age-sex projection gives.
* **Partial correction priced (L3).** A solver who finds the waits in the bed bureau's log, which misses direct transfers within medicine,
  removes 8% of Brackenfield's peak and builds there at 90.7%, 1.6 beds short and 6.7% over the trigger, the only unit over it. One who
  removes the readiness record's midnights but weights age by the 65+ share builds at Ostley, 92.3% and 1.7 beds short, 8.6% over the
  trigger and again the only unit over it. Neither half holds.
* **Grid.** Basis (deck spending, 65+ share, age-sex weights) × step-down treatment (none, bureau log, readiness record) gives 9 cells. Only
  age-sex weights with the readiness record hold. The deck's three cells name Thornleigh, the 65+ share's three name Ostley and the other two
  age-sex cells name Brackenfield. The nearest wrong cell is age-sex weights with the bureau log, Brackenfield at 90.7%, 9.9 points above the
  hold's 80.8%.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The capital rule says "critical-care occupancy". The regional glossary defines it through patients who need critical
   care, and the readiness record's dictionary defines its own field. No document says the census counts patients after their step-down
   point, how many there are, or that they gather in January.
2. **Corpus blind for a computable reason.** *In every closed projection in the book, step-down-ready patients held under 2% of peak
   midnights, because each of those hospitals ran its medical wards under 85% at the winter peak, so a ready patient reached a ward bed
   within hours and critical-care occupancy equalled critical-care need.* The book certifies the age-sex projection 7 of 7.
3. **No arithmetic symptom.** Census, stays, readiness record and bureau log reconcile on every rung, and no unit's base-year occupancy
   exceeds its beds.
4. **Not a row predicate.** The step-down point comes from a different file than the census. It splits stays rather than selecting them, and
   it matters only through nightly counts at the peak, so need is rebuilt for 365 nights per unit before the 28-night peak is taken and
   projected.
5. **The enumeration is arithmetic.** No field marks a midnight as unneeded. The count comes from intervals joined across two files.
6. **No cutover date.** Brackenfield's step-down-ready share of peak midnights has sat between 16% and 20% in each of the five winters.
   Nothing stepped on a date.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The regional capital programme's book of seven closed critical-care projections at hospitals in two neighbouring regions. Each
  carries its basis year's census, stays, readiness record and populations, and the peak occupancy realised three years on.
* **What it certifies.** The projection. Midnights per age-sex-weighted resident with the five-year trend reproduce the realised peak at 7 of
  7 hospitals within 1.5 points. The 65+ share reproduces 3 of 7 and overstates the four with the oldest catchments by 5 to 11 points. The
  deck's spending method reproduces none.
* **What it is blind to.** Step-down-ready midnights (property 2).
* **Twin pair.** Brackenfield's pod B and Ostley's pod A are 10-bed pods identical on winter admissions (205 each), case-mix score, age-sex
  mix, mean stay, total midnights in the peak window (262) and every count in the bed bureau's log. The readiness record gives them 58 and 28
  step-down-ready midnights (2.07×), because Brackenfield's medical wards take a day longer to free a bed for patients moved directly within
  medicine.
* **Resemblance points at the decoy.** Brackenfield most resembles Tarnside General in the book: 24 beds, a mixed medical-surgical unit and
  a catchment of retirees aged 65 to 79. Tarnside's projection came true within a point, and it took the region's last module.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The capital rule: "A critical-care module is approved for a unit whose projected peak critical-care occupancy exceeds 85%
  within three years; where several qualify, the largest shortfall in beds takes it." The regional planning glossary, among forty entries:
  "Critical-care occupancy: midnights of patients who need critical care, as a share of commissioned critical-care beds." The readiness
  record's dictionary: "step_down_ready_at: when the consultant intensivist recorded that the patient no longer needs critical care." The
  census guidance: "Peak occupancy is the mean of the year's 28 busiest consecutive midnights." The first three form a chain, and each says
  nothing about the decision alone.
* **Empirical pins.** The projection (age-sex weights, five-year trend) comes from the book's 7 of 7. Populations are the county's
  projections of record.
* **Voices.** Strategy director: "Patients reach us sicker every year; you can see it in what each of them costs." Brackenfield's clinical
  director for critical care: "From December to March we are full every single night." Ostley's chief nurse: "Our catchment is the oldest in
  the county and ageing fastest." CFO: "Capacity should follow patients, not prices."
* **Licensed wrong basis.** The capital rule records that the board's finance committee reads critical-care cases through the deck's real
  spending per resident and will see this one on that basis.

## 8. Determinism by construction

* **Peak window.** Every unit's 28 busiest midnights fall in the first four weeks of January, on the total count and the need count alike.
* **Step-down point.** Every readiness time lies between 08:00 and 20:00, so the first midnight not counted is unambiguous. Readiness
  reversals (0.6% of stays) all fall outside the peak windows.
* **Alternative peaks.** The busiest single midnight, the 95th-percentile midnight and the busiest calendar month keep Brackenfield's need
  between 78.9% and 82.6% and its total between 96% and 101%.
* **Projection.** Base-year weights taken from the book's rates or recomputed from Northvale's own stays agree within 0.3 points at every
  unit, and a five-year compound trend and a fitted trend agree within 0.4 points.
* **Beds and maturity.** Commissioned beds were unchanged over the five years, and no surge beds opened in any peak window. Every stay holding
  a peak-window midnight closed before the extract.

## 9. Prompt sketch and deliverables

> I have to give the board one line on our 12-bed critical-care module this round: which of our five units gets it, or that none does this
> time. Our strategy director reads the last five years as an intensity boom. Give me that line, with each unit's projected peak as a
> percentage of its beds to one decimal place and the beds it would be short or spare, also to one decimal. Send `module_case.xlsx`, a
> chart `unit_peaks.png`, and a two-page `board_line.pdf`.

* `module_case.xlsx` — the five units on every construction, the cancellations sheet (ask A), the outreach sheet (ask B) and the book
  back-test (ask C).
* `unit_peaks.png` — for each unit, a stacked bar of the projected third-year peak split into critical-care need and step-down-ready
  midnights, a marker at the base-year peak, the 85% trigger as a labelled line, and a title that states the call.
* `board_line.pdf` — the call, the blocking quantity and what would turn the hold into a build.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each unit and each month from December to March, elective operations cancelled on the day for
  want of a critical-care bed. *Device:* the theatre system logs one cancellation row per procedure code, while the national
  cancelled-operations return counts one per patient per list, as its guidance states. Counting rows overstates Thornleigh by about a
  quarter, because its cardiac lists carry two codes per patient. Cancellations never enter the census.
* **Ask B (device-carried).** For each hospital and quarter, critical-care outreach call-outs to the wards. *Device:* the outreach log records
  every visit, and the outreach standard counts a call-out as the first visit to a patient within 24 hours, with follow-up visits inside
  it. Counting visits overstates call-outs by about 60% at the two hospitals whose teams make scheduled follow-ups.
* **Ask C (validity).** For each of the seven closed projections, the realised peak beside what your construction gives from its basis year.
* **Decoupling.** Clearing the step-down construction or the age-sex weights changes no figure in asks A or B. Ask C cannot separate need
  from occupancy, by property 2.

## 11. Rubric arithmetic

5 units × 4 months (ask A) + 5 hospitals × 4 quarters (ask B) + 7 closed projections (ask C) + the hold, the blocking quantity and each
unit's projected peak and beds short or spare + 5 named chart parts + 3 files ≈ 67 criteria.

## 12. World-building constraints

* Commissioned beds are 48 / 28 / 24 / 20 / 16 for Thornleigh, Greyford, Brackenfield, Ostley and Pennard. Base-year peaks on all midnights
  are 82 / 80 / 88 / 85 / 81%.
* Three-year factors are 1.22 / 1.21 / 1.05 / 1.03 / 1.10 on the deck's spending, 1.03 / 1.04 / 1.06 / 1.22 / 1.06 on the 65+ share and
  1.02 / 1.03 / 1.12 / 1.05 / 1.04 on age-sex weights.
* Step-down-ready shares of peak midnights are 7 / 6 / 18 / 11 / 6% in the readiness record and 4 / 3 / 8 / 6 / 3% in the bureau's log, each
  within two points of these in all five winters.
* Midnights per age-sex-weighted resident moved by under 1% a year at every unit. The deck's CPI-deflated spending per resident grew 3% to
  7% a year.
* The book holds 7 closed projections, each with step-down-ready midnights under 2% of its peak and medical wards under 85% at the peak.
* The twin pods are identical on every census, stay and bureau column, with 58 against 28 step-down-ready midnights.
* Every non-hold grid cell names a build at least 6.7% over the trigger, and the hold sits 4.9% under it.
* Cancellation codes and outreach visits never touch the census, the stays or the readiness record.

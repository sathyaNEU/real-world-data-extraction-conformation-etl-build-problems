# RC39 — Whether the board's critical-care module goes anywhere, when the fastest-growing unit's growth is an elective programme that already fills its theatres

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Economics · health-system finance and capital planning |
| Mirrors | Capacity cases at large hospital operators (HCA Healthcare, Kaiser Permanente, NHS critical-care networks) and at cloud platforms, where a unit's growth trend is fed by an upstream programme already running at its own ceiling (post-operative beds fed by full theatres, a storage tier fed by an ingest pipeline at its quota), so the trend cannot continue |
| Decision shape | Hold, forced by a blocking quantity: no unit's projected peak occupancy reaches the 85% trigger |
| Committed call | Place the 12-bed critical-care module nowhere this round, because the highest projected peak is Brackenfield's 79.9% against the 85% trigger |
| Gap · Pattern | Gap 3 (objective) at rung 1, Gap 1 (time) at the decisive rung · Pattern D (spending against occupied midnights) beneath the quiet second trap of measured #11 (post-operative midnights inside the five-year trend, with their own control in the theatre session log), and the hold of Part 6.4 |
| Gate G mechanism | signal_vs_noise_or_hold, with forecasting |
| Measured traps engaged | #11 beats the headline trap, misses the quiet one · #13 validates on one population, applies to another · #10 notes a binding limit as a risk |
| Calibration form | Existing-book actuals: the regional capital programme's seven closed critical-care projections at hospitals in two neighbouring regions, each with its basis year and the peak occupancy realised three years on |
| Driving force | Every number is correct: the deck's spending, the critical-care census, the admissions, the theatre session log and the book. Set the deck's price-driven "intensity" aside and weight age by each group's critical-care use, and the projection the book reproduces 7 of 7 carries Brackenfield's five-year trend forward to 97.3%. But 40% of Brackenfield's peak midnights follow elective lists, and the whole trend is its elective programme filling four theatres. Every session has been used since last spring, so post-operative midnights cannot keep growing. Held at the theatres' capacity, with the rest projected on age-sex weights, Brackenfield peaks at 79.9%, and no unit reaches 85%. |

## 1. Situation

Northvale Health runs five adult critical-care units with 136 commissioned beds. Critical-care spending rose 48% in five years. The
strategy director's deck deflates spending per resident by consumer prices, calls the result an intensity boom and asks for more
critical-care beds. The deck reports spending by service line and never projects occupancy or ranks units. The board has one 12-bed
critical-care module in this capital round. The capital rule approves it for a unit whose projected peak occupancy exceeds 85% within
three years, and where several qualify the largest shortfall takes it. No unit is over 85% today. The CFO wants the growth taken apart
before the board commits, and the board may place the module nowhere this round.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct: the deck's spending series, the critical-care census, the admissions, the theatre session
  log, the theatre register, the population projections and the book. No one's reading of their own figures is overturned, and
  Brackenfield's unit really did grow fastest. The difficulty is whether that growth can continue.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the deck and every voice. The age-sex projection the book certifies 7 of 7 still puts Brackenfield at 97.3%, and
  only the theatre session log turns it into a hold.
* **Instrument repair.** No file is suspect. The census counts every occupied midnight, and the admissions, theatre session log, theatre
  register, populations and book are complete and current. Repair them anyway at every depth, down to an admission-type field on every
  critical-care stay. Rung 0 still names Thornleigh (95.2%), rung 1 Ostley (90.0%) and rung 2 Brackenfield (97.3%), because the trend
  carries the elective growth whatever the stay record says. Holding post-operative midnights at the theatres' capacity, a binding limit
  that no row records, is still needed to reach the hold.
* **Lens swap.** The naive read is spending per resident over a year. The answer projects January midnights by what drives them, demography
  for most and a full theatre programme for the rest, over the next three winters rather than the last five years: a different population
  and a different moment.

## 3. The driving force

A strong solver sets the deck aside, because its intensity is ECMO consumables, devices and drug prices, and none of those holds a bed. It
rebuilds growth from occupied midnights at the census. It weights age by each group's critical-care use rather than by the 65+ share,
because residents over 85 use less critical care than those aged 70 to 79. It carries each unit's five-year trend in midnights per
weighted resident forward, which is the projection the book reproduces at all seven closed hospitals. Brackenfield, the fastest-growing
unit, projects to 97.3% and takes the module. The quiet trap is in the trend. Linked through the theatre session log, 40% of Brackenfield's
peak midnights belong to patients admitted from an elective list, and its whole five-year trend is the elective programme growing until it
filled its four theatres. Every session has run since last spring, and the register shows no fifth theatre, so post-operative midnights
are at their ceiling. Projected on demography alone, the rest of the unit grows 4% in three years. Brackenfield peaks at 79.9%.

## 4. The ladder

| Rung | Construction | Names (projected peak, % of beds; beds short) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The deck's CPI-deflated critical-care spending per resident, carried onto each unit's base-year peak | Thornleigh (95.2%, 5.7 short, 2.13× Greyford's 2.7) | The board's own intensity series, already per resident | The census: Thornleigh's occupied midnights per resident grew 0.5% a year while its real spending per resident grew 6.5%, the gap being ECMO, device and drug prices |
| 1 | Occupied midnights per resident, ageing adjusted by the 65+ share, five-year trend carried forward | Ostley (90.0%, 1.2 short, the only unit over) | The decision's own grain and the standard ageing correction | The regional age-sex rates: residents over 85 use 40% fewer critical-care midnights per head than those aged 70 to 79, and Ostley's growth is almost all over 85 |
| 2 | Midnights per age-sex-weighted resident with the five-year trend, the projection the book reproduces 7 of 7 within 1.5 points | Brackenfield (97.3%, 3.5 short, the only unit over) | Certified on every closed projection, and Brackenfield resembles Tarnside General | The theatre session log: 40% of Brackenfield's peak midnights follow elective lists, and its four theatres have used every session since last spring |
| 3 | **Decisive:** midnights split by what drives them, post-operative midnights (linked to elective lists through the session log) held at the theatres' capacity and the rest projected on age-sex weights without the elective trend | **Hold.** Highest unit Brackenfield at 79.9%, 5.1 points under the trigger | — | — |

* **Every candidate fails, and why.** Thornleigh (79.6%) and Greyford (79.3%) grew in price, not in midnights. Ostley (79.5%) is ageing past
  the years of heaviest critical-care use. Pennard (79.1%) never approached the trigger. Brackenfield (79.9%) grew fastest, but its growth
  was an elective programme that is now at its theatres' ceiling.
* **The blocking quantity.** The highest projected peak, Brackenfield's 79.9%, sits 6.0% (5.1 points) under the 85% trigger, and every unit
  has beds spare. It would become a build if Brackenfield's theatre capacity rose 16% within the three years, or if its other midnights grew
  15% instead of 4%.
* **Partial correction priced (L3).** A solver who finds the elective midnights but grows them with the elective waiting list (15% a year)
  builds at Brackenfield, 96.1% and 3.1 beds short, 13.1% over the trigger. One who holds them flat but leaves the five-year trend on the
  other midnights builds there at 89.6%, 1.3 beds short and 5.4% over. One who splits them on the 65+ share builds at Ostley, 90.0% and 5.9%
  over. Each is the only unit over its trigger, and none holds.
* **Grid.** Ageing (65+ share, age-sex weights) × elective treatment (none, waiting-list growth, flat with the trend kept, held at the
  theatres' capacity) gives 8 cells. Only age-sex weights with the capacity hold. The 65+ cells name Ostley or Brackenfield, and the nearest
  wrong cell is age-sex weights with the trend kept, Brackenfield at 89.6%, 9.7 points above the hold.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The session log and theatre register are operational records. No document links theatre sessions to critical-care
   midnights or says that Brackenfield's trend is elective work.
2. **Corpus blind for a computable reason.** *In every closed projection in the book, the hospital's elective programme ran the same
   sessions in every year of its window, so post-operative midnights were flat and the five-year trend was emergency demand alone.* The book
   certifies the age-sex projection with its trend 7 of 7.
3. **No arithmetic symptom.** Census, admissions and session log reconcile on every rung, and the trend is an exact average of five correct
   years.
4. **Not a row predicate.** Post-operative midnights come from linking each critical-care admission to an elective list that ended within
   three hours for the same patient, and their forward path is set by the theatres' capacity, which no row carries.
5. **The enumeration is arithmetic.** No field marks a midnight as post-operative. The share is computed from the link.
6. **No cutover date.** Sessions were added a few at a time over five years and filled every slot by last spring, so nothing steps on one
   date.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The regional capital programme's book of seven closed critical-care projections at hospitals in two neighbouring regions, each
  with its basis year's census, admissions and populations, and the peak occupancy realised three years on.
* **What it certifies.** The projection. Midnights per age-sex-weighted resident with the five-year trend reproduce the realised peak at 7
  of 7 hospitals within 1.5 points. The 65+ share reproduces 3 of 7 and overstates the four with the oldest catchments by 5 to 11 points.
  The deck's spending method reproduces none.
* **What it is blind to.** Growth fed by a capped programme (property 2).
* **Twin pair.** Brackenfield's pod B and Ostley's pod A are 10-bed pods identical on every census and admission column, including peak
  midnights (262) and their five-year growth (+70). Projected forward, pod A gains 21 midnights and pod B 10 (2.1×), because 45% of pod B's
  midnights follow elective lists that already fill every theatre session.
* **Resemblance points at the decoy.** Brackenfield most resembles Tarnside General in the book: 24 beds, a mixed medical-surgical unit and
  a catchment of retirees aged 65 to 79. Tarnside's projection came true within a point, and it took the region's last module.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The capital rule: "A critical-care module is approved for a unit whose projected peak occupancy exceeds 85% within three
  years; where several qualify, the largest shortfall in beds takes it." The census guidance: "Peak occupancy is the mean of the year's 28
  busiest consecutive midnights." The theatre register: "Brackenfield runs four theatres, each scheduled for ten elective sessions a week;
  no further theatre is in the capital programme."
* **Empirical pins.** The projection comes from the book's 7 of 7. The post-operative link comes from the session log's list end times.
* **Voices.** Strategy director: "Patients reach us sicker every year; you can see it in what each of them costs." Brackenfield's clinical
  director: "Our surgeons fill every bed we give them, and they want more." Ostley's chief nurse: "Our catchment is the oldest in the county
  and ageing fastest." Theatre manager: "Elective work will keep growing as fast as the waiting list." CFO: "Capacity should follow
  patients, not prices."
* **Licensed wrong basis.** The capital rule records that the board's finance committee reads critical-care cases through the deck's real
  spending per resident and will see this one on that basis.

## 8. Determinism by construction

* **Peak window.** Every unit's 28 busiest midnights fall in the first four weeks of January. Brackenfield's elective lists ran through
  January into ring-fenced post-operative beds, and post-operative midnights were 40% of its peak in each of the last two winters.
* **The link.** Every post-operative admission came within 90 minutes of its list's end, and no other admission came within three hours of
  a list for the same patient, so the link window cannot matter.
* **Theatre capacity.** All 40 weekly sessions ran in every week since last spring. Admissions per session and post-operative stay have
  each held within 2% for five years.
* **Projection.** Base-year weights taken from the book's rates or recomputed from Northvale's own stays agree within 0.3 points at every
  unit, and a five-year compound trend and a fitted trend agree within 0.4 points.
* **Beds and maturity.** Commissioned beds were unchanged over the five years, and no surge beds opened in any peak window. Every stay holding
  a peak-window midnight closed before the extract.

## 9. Prompt sketch and deliverables

> I have to give the board one line on our 12-bed critical-care module this round: which of our five units gets it, or that none does this
> time. Our strategy director reads the last five years as an intensity boom. Give me that line, with each unit's projected peak as a
> percentage of its beds to one decimal place and the beds it would be short or spare, also to one decimal. Send `module_case.xlsx`, a
> chart `unit_peaks.png`, and a two-page `board_line.pdf`.

* `module_case.xlsx` — the five units on every construction, the staffing sheet (ask A), the outreach sheet (ask B) and the book back-test
  (ask C).
* `unit_peaks.png` — for each unit, a stacked bar of the projected third-year peak split into post-operative and other midnights, a marker
  at the base-year peak, the 85% trigger as a labelled line, and a title that states the call.
* `board_line.pdf` — the call, the blocking quantity and what would turn the hold into a build.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each unit and each month from December to March, the share of rostered nursing shifts filled.
  *Device:* the rostering export lists a shift once per assignment, so a nurse moved between units mid-shift appears on both, while the fill
  measure counts the shift once, on the unit where it started, as the rostering guide states. Counting assignments overstates fill by 3 to 6
  points at the two units that lend nurses at night. Rosters never enter the census.
* **Ask B (device-carried).** For each hospital and quarter, critical-care outreach call-outs to the wards. *Device:* the outreach log
  records every visit, and the outreach standard counts a call-out as the first visit to a patient within 24 hours, with follow-up visits
  inside it. Counting visits overstates call-outs by about 60% at the two hospitals whose teams make scheduled follow-ups.
* **Ask C (validity).** For each of the seven closed projections, the realised peak beside what your construction gives from its basis year.
* **Decoupling.** Clearing the elective split or the age-sex weights changes no figure in asks A or B. Ask C cannot see a capped programme, by
  property 2.

## 11. Rubric arithmetic

5 units × 4 months (ask A) + 5 hospitals × 4 quarters (ask B) + 7 closed projections (ask C) + the hold, the blocking quantity and each
unit's projected peak and beds short or spare + 5 named chart parts + 3 files ≈ 67 criteria.

## 12. World-building constraints

* Commissioned beds are 48 / 28 / 24 / 20 / 16 for Thornleigh, Greyford, Brackenfield, Ostley and Pennard. Base-year peaks are 78 / 77 / 78 /
  75 / 76%.
* Three-year factors are 1.22 / 1.21 / 1.05 / 1.03 / 1.08 on the deck's spending, 1.03 / 1.04 / 1.08 / 1.20 / 1.05 on the 65+ share,
  1.02 / 1.03 / 1.248 / 1.06 / 1.04 on age-sex weights with the trend, and 1.02 / 1.03 / 1.024 / 1.06 / 1.04 on the decisive construction.
* Brackenfield's post-operative midnights are 40% of its peak. Its demographic factor is 1.04, and its trend factor of 1.20 is entirely the
  elective programme, which grew from two theatres' worth of sessions to four over the five years. No other unit's programme grew.
* Thornleigh's real spending per resident grew 6.5% a year and its midnights per resident 0.5%.
* The book holds 7 closed projections, each with a flat elective programme across its window.
* The twin pods are identical on every census and admission column, and pod B's post-operative share is 45%.
* Every non-hold grid cell names a build at least 5.4% over the trigger, and the hold sits 6.0% under it.
* Rosters and outreach visits never touch the census, the admissions or the session log.

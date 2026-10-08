# FC31 — How many agency nurse shifts to block-book for January, when the pool funds activation days and the agencies' surge code only mostly agrees with them

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Policy & Education · health-system administration (regional nurse staffing pool) |
| Mirrors | Pre-committing flexible capacity whose draw is defined by a trigger rather than by a booking code (cloud capacity reservations drawn when a service's utilisation trigger fires, Amazon's peak-season agency labour by site, hospital-system float pools), where the vendor's own coding mostly agrees with the trigger and ties on the total |
| Decision shape | One figure committed at a date: the January block filed with the two staffing agencies |
| Committed call | Agency nurse shifts to block-book for the four weeks from Monday 4 January, to the nearest 50 shifts |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · the population a flag suggests (measured #5), with the activation rule recovered from settled statements (Pattern B) and finer controls separating constructions (measured #12) at rung 2 |
| Gate G mechanism | method_or_model_selection, with forecasting support |
| Measured traps engaged | #5 takes the population a flag or filter suggests · #12 stops at the first control that passes · #13 validates on one population, applies to another |
| Calibration form | Settled-transaction ledger: the pool's settlement statements for the last two winters, every hospital's weekly reimbursement as settled and paid |
| Driving force | The pool funds agency shifts worked on a hospital's activation days, and a hospital activates on the third consecutive midnight at or above 92% occupancy and stands down after three consecutive midnights below 88%. The agencies code shifts "S" by the desk that took the booking, which matches activation days for about three shifts in four and ties on the pool's total two winters running. The community hospitals that book surge cover through routine channels are the ones whose baseline occupancy sits just under the trigger, and this January's forecast pushes them across it. |

## 1. Situation

A state hospital association runs a winter agency-nurse pool for 24 member hospitals. Each December it block-books the January weeks
with two staffing agencies at a discounted rate; shifts beyond the block are bought at spot rates and unused block shifts are charged at
60%. The pool contract says the pool funds agency shifts worked while a member hospital's surge plan is active, and the block is set at
the forecast pool draw. The association's surveillance unit publishes catchment-level admissions forecasts from wastewater signals. The
pack holds the agencies' settled shift invoices with their booking codes, each hospital's daily midnight census, the pool's settlement
statements and each hospital's surge plan.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: invoices, codes, census, settlement statements and the admissions forecast. No stakeholder's reading
  of their own numbers is overturned; the S-coded totals really have matched the pool total two winters running. The difficulty is that
  the population the pool funds is defined by a rule on the census, and the visible code is a different population with the same total.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the pool manager's view and every voice. S-coded shifts per admission still reproduce last winter's pool total
  exactly, and the S code still mislabels the hospitals that will draw most.
* **Instrument repair.** Clean-data test. One field is suspect: the agencies' surge code marks the desk that took the booking, a narrower
  thing than the pool's activation days. Recoded by activation day, rung 0 still returns 4,186 (last winter's activation-day total equals
  its S-coded total), rung 1 3,910 and rung 2 4,020 (activation-day shifts per surge admission, carried hospital by hospital, give the
  community hospitals only last winter's few activation days), none of them 4,700. The census and the settlement statements are complete,
  and the forecast of this January's activation days from forecast occupancy is still needed.
* **Lens swap.** The naive read and the answer are different populations at different moments: shifts coded by booking desk last winter,
  against shifts on the activation days this January's occupancy will produce.

## 3. The driving force

A strong solver scales last January's surge shifts by the forecast rise in admissions, nets the agencies' credit-and-rebill pairs, then
refines by hospital: S-coded shifts per surge admission at each hospital, applied to each hospital's forecast. The refined build
reproduces last winter's pool total to the shift. But the S code records which agency desk took the booking. The pool funds shifts on
activation days, and activation is a state each hospital enters on its third consecutive midnight at or above 92% and leaves after three
below 88%, a rule no document states and the settlement statements reproduce exactly. Two teaching hospitals book every agency shift
through the surge desk, so their routine shifts carry an S; seven community hospitals book surge cover through their routine desks.
Last winter the two errors cancelled on the total. This January the community hospitals, whose baseline occupancy sits at 88–90%, cross
the trigger in the first week and stay over it.

## 4. The ladder

| Rung | Construction | Lands on (block shifts) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Last January's S-coded shifts × the forecast rise in January admissions (1.15) | 4,186 (−10.9%) | The agencies' own surge records scaled by the surveillance forecast | The invoices carry credit-and-rebill pairs for rate corrections, each shift appearing three times |
| 1 | Hygiene: credit-and-rebill pairs netted, then scaled | 3,910 (−16.8%) | Every shift counted once, and the result reproduces last winter's pool total | Admissions rise unevenly: the forecast puts 70% of the increase in community-hospital catchments |
| 2 | S-coded shifts per surge admission at each hospital, applied to its own forecast admissions | 3,560 (−24.3%) | Hospital-level, and it reproduces last winter's pool total to the shift: the salient control passes | The settlement statements' finer lines: S-coded shifts reproduce 19 of 48 hospital-winter reimbursements and 0 of the weekly lines at the seven community hospitals |
| 3 | **Decisive:** pool shifts as shifts on activation days, activation recovered from the census by the run-length rule the statements reproduce, January activation days forecast per hospital from forecast occupancy | **4,700** | — | — |

* **Figure shape.** Rungs 0 to 2 walk the block down (−10.9%, −16.8%, −24.3%) and the decisive rung reverses past rung 0, so a solver who
  stops anywhere short under-books, and the shortfall is bought at spot rates.
* **Partial correction priced (L3).** A solver who finds the activation rule but carries last winter's activation days forward at the
  admissions ratio lands on rung 1's 3,910 (−16.8%), because last winter's activation-day total equals its S-coded total. One who
  forecasts activation from network-wide occupancy rather than hospital by hospital lands at 3,700 (−21.3%): the average never crosses
  92% in the second half of January. One who triggers on a single midnight at 92% overshoots to 5,500 (+17.0%).
* **Grid.** Population (S code raw, S code netted, single-midnight trigger, run-length rule) × calibration (pooled, by hospital) ×
  activation (carried, forecast per hospital) = 16 cells. Every wrong cell sits at least 10.9% from 4,700; the nearest is rung 0, and the
  only cell above the answer is the single-midnight trigger, which reproduces 27 of 48 statement lines.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The pool contract says the pool funds shifts while a surge plan is active; every surge plan describes activation
   as "when occupancy pressure requires". No document gives a threshold, a release level or a run length, and none says the agencies'
   code is assigned by booking desk.
2. **Reproduction (Pattern B).** Activation at the third consecutive midnight at or above 92%, ending after three below 88%, reproduces
   48 of 48 hospital-winter reimbursements and all 412 weekly lines. The best rival (the same levels with two-midnight runs) reproduces 41
   of 48, a single-midnight trigger 27, the S code 19. The rule is a construction, not a menu: it is a two-state machine with hysteresis
   run over each hospital's daily census and joined to settlement weeks, and nothing in the invoices or the plans carries it.
3. **No arithmetic symptom.** S-coded and activation-day shifts tie on both winters' pool totals, invoices reconcile to worked shifts, and
   the census reconciles to bed counts. The misclassifications cancel exactly where a solver checks.
4. **Not a row predicate.** Whether a day is an activation day depends on the two midnights before it and the hospital's state, so it
   needs a run over each hospital's census, not a filter on a shift or a day.
5. **The enumeration is arithmetic.** January's activation days are computed from forecast occupancy; no file flags a hospital as about
   to activate.
6. **No cutover date.** No outcome series steps at a date; activation spans start and end inside each hospital's own census.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The pool's settlement statements for the last two winters: 24 hospitals' weekly reimbursements, 412 lines, each settled and
  paid, with each hospital-winter total.
* **What it certifies.** The pool's totals, which the S-coded construction and the activation construction both reproduce, so a solver
  who checks the total is confirmed at rungs 1 and 2.
* **What it pins.** The activation rule (above), and each hospital's agency shifts per activation day, which is flat across its winters.
* **Twin pair.** Calder Valley and Mirren General are identical on beds, last winter's admissions, catchment wastewater series, S-coded
  shifts and agency spend. Their forecast January pool draws differ 2.2×, because Calder's baseline occupancy sits at 89% and it activates
  on the first week's rise, while Mirren's sits at 81% and activates only for the peak week. Only the run-length rule on the census
  separates them.
* **Resemblance points at the decoy.** By agency spend and S-coded share, the forecast January most resembles last January, which rungs 1
  and 2 reproduce to the shift.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The pool contract: the pool funds agency shifts worked while a member hospital's surge plan is active, and the block
  covers the four weeks from the first Monday of January, set at the forecast pool draw. The surveillance unit's catchment admissions
  forecast is the association's planning forecast. The block is filed to the nearest 50 shifts.
* **Empirical pins.** The activation rule and each hospital's shifts per activation day, from the settlement statements. Each hospital's
  January occupancy, from its baseline census and the catchment forecast.
* **Voices.** The pool manager: "The agencies code every surge shift, and their S totals have matched our pool spend two winters running."
  The chief nursing officer at the largest teaching hospital: "The teaching hospitals carry the surge; the community hospitals manage." The
  surveillance lead: "Wastewater says this January is bigger than last. Scale last January up and you'll be close."
* **Licensed wrong basis.** The pool contract records that the agencies quote next winter's block rate from their surge-desk reports and
  will present them at the block negotiation.

## 8. Determinism by construction

* **Thresholds.** No hospital's census in either winter sits within half a point of 92% or 88% on any midnight, so the rule's levels are
  unambiguous; neighbouring pairs (91/87, 93/89) reproduce at most 30 of 48 lines.
* **Occupancy forecast.** Every hospital's forecast January occupancy stays at least three points from 92% and from 88% except on the days
  it crosses them, and length-of-stay conventions from 4.5 to 5.5 days move no crossing.
* **Day boundary.** Shifts are attributed to the day they start, as the invoices record them, and no shift starts in the last hour before
  midnight.
* **Maturity.** Last winter's statements were settled by May and no line is open.
* **Rounding.** The block (4,700) sits mid-bin at the nearest 50 shifts.

## 9. Prompt sketch and deliverables

> The agencies need our January block by Monday and I sign it. Our pool manager says the agencies' surge totals have matched our pool's
> spend two winters running. Tell me how many agency nurse shifts to block-book for the four weeks from 4 January, to the nearest 50, as
> one figure I can put in the contract schedule. Send `january_block.xlsx` with the build and the sheets below, a chart
> `activation_calendar.png`, and a one-page `block_note.pdf`.

* `january_block.xlsx` — the block build for all 24 hospitals, the unit-mix sheet (ask A) and the confirmation-time sheet (ask B).
* `activation_calendar.png` — a hospital × day heat map of forecast January midnight occupancy, with the 92% and 88% levels marked in
  the colour scale, each hospital's activation spans outlined, hospitals ordered by forecast pool draw, and the block total annotated.
* `block_note.pdf` — the committed block and the alternatives the agencies will raise.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the twelve largest hospitals, last winter's agency shifts by unit type (critical care,
  medical, emergency, paediatric). *Device:* a float shift split across two units is invoiced once under the home unit, with the second
  unit in the unit-transfer table, as the staffing guide documents; counting by home unit misattributes 18% of critical-care hours.
  Hospital totals, and so the block, are unchanged.
* **Ask B (device-carried).** For each of the twelve, the median hours from shift request to agency confirmation in each winter month.
  *Device:* a request re-sent after an agency declines keeps its request number, with each re-send in the request-history table, as the
  agency portal guide documents; timing from the last re-send understates waits at eight hospitals.
* **Ask C (validity).** The block under each of the four rung constructions, and how many of the 48 hospital-winter statement lines each
  reproduces.
* **Decoupling.** Clearing the activation rule changes no figure in asks A or B.

## 11. Rubric arithmetic

12 hospitals × 4 unit types (ask A) + 12 × 3 months (ask B) + 4 constructions × 2 (ask C) + the committed block, the forecast activation
hospital-days and the twin hospitals' draws + 5 named chart parts + 3 files ≈ 103 criteria.

## 12. World-building constraints

* Last January: 3,400 pool-funded shifts, 3,400 S-coded (3,640 before netting rebills); 23% of S-coded shifts fell outside activation
  days and 23% of activation-day shifts were coded R, at different hospitals.
* Seven community hospitals with baseline occupancy of 88–90% book surge cover through routine desks; two teaching hospitals book every
  shift through the surge desk.
* Block figures: 4,186 / 3,910 / 3,560 / 4,700 across rungs; network-wide activation 3,700; single-midnight trigger 5,500. Recoded by
  activation day, rungs 0 and 1 are unchanged and rung 2 gives 4,020.
* Reproduction of 48 hospital-winter lines: 48 (rule), 41 (two-midnight runs), 27 (single midnight), 19 (S code).
* The twin hospitals are identical on every invoice, admissions and wastewater column.
* Unit transfers and re-sent requests touch no shift count, hospital total or census day.

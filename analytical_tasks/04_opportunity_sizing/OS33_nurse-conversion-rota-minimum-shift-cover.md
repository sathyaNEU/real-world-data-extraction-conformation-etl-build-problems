# OS33 — Where 30 new staff nurses replace agency shifts, when a staff post is a rota and the agency bill is mostly nights

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Economics · workforce cost management in long-term care |
| Mirrors | Commitment sizing where committed capacity comes in fixed bundles that must all be used (reserved cloud instances bought as fixed vCPU-and-memory shapes when demand is skewed to one resource, full-time hires on rotating shift patterns, carrier contracts with fixed lane mixes) |
| Decision shape | An allocation under a cap: 30 staff-nurse posts, recruited to replace agency hours, split across ten care homes |
| Committed call | Posts per home, and the annual net saving the split buys |
| Gap · Pattern | Gap 2 (population) over Gap 3 (objective) · E30 (a converted post clears only when every shift type in its rota has agency hours to displace), with E14 below it (position control caps conversions at each home's budgeted vacancies) |
| Gate G mechanism | binding_constraint, with method_or_model_selection |
| Measured traps engaged | #10 notes a binding limit as a risk · #2 counts file rows instead of the real unit · #4 never tests its reading against the control |
| Calibration form | Pilot log: last year's conversion pilot, 40 posts at five homes, with each post's displaced agency hours and idle hours by shift type over 26 weeks |
| Driving force | A staff nurse is a rota, not 36 loose hours: the collective agreement puts every full-time post on 12 weekday-day, 12 weekday-night and 12 weekend hours a week. A post pays only where agency hours exist in every one of those shift types. In the night-heavy urban homes, where the agency bill is biggest, the scarce weekday and weekend agency hours support three or four posts. The answer is a minimum over shift types for each home, which no invoice total shows. |

## 1. Situation

A care-home group spends heavily on agency nurses. HR can recruit 30 staff nurses next year to replace agency shifts, and the board wants
to know where they go and what they save. Agency rates and staff costs differ by home, so a converted hour is worth $21 to $46. Last year
the group piloted 40 conversions at five homes and logged every converted post's hours. The finance director wants most of the 30 at
Ashgrove, whose agency bill is the group's worst.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the agency invoices, the timesheets, the position-control register, the collective agreement and
  the pilot log. Ashgrove's bill really is the worst. Nothing reported is overturned. The difficulty is what one post can absorb, which
  depends on a shape the hours do not show.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the finance director's view and every voice. Agency hours by home still rank the night-heavy urban homes first,
  and no document says a post must find work in every shift type.
* **Instrument repair.** Suspect file: the agency invoices, whose billed hours include call-off fees and orientation. Repaired to hours
  worked, rung 0 gives Ashgrove 16, Bellmont 8 and Carrow 6 ($2.51M), and rung 1 becomes rung 2 (Carrow 13, $2.43M). Timesheets and the
  position-control register are complete. A post is still a fixed rota and the agency hours still sit mostly at night, so the rota minimum
  is still needed for $2.04M.
* **Lens swap.** The answer counts different hours, those in each home's scarcest shift type, which are a different population from the
  agency hours on the invoice.

## 3. The driving force

A strong solver converts agency hours into posts at 36 hours each, honours position control, strips call-off fees and orientation hours
from billed time, and fills the 30 in order of saving per hour. Each step is right, and the result sends the posts to the night-heavy urban
homes where the gap is widest. But a staff nurse cannot be rostered on nights only: the agreement's four-week rota gives every full-time
post 12 weekday-day, 12 weekday-night and 12 weekend hours a week. A post displaces agency hours only up to the scarcest of its three shift
types. Beyond that point it idles on days and weekends at $64 an hour while the agency still covers nights. Carrow buys 480 worked agency
hours a week, of which 406 are nights, so its weekday days support three posts, not thirteen. Shift type is not a column: it comes from
each timesheet's start time and day under the agreement's definitions.

## 4. The ladder

| Rung | Construction | Allocation (largest block) and annual saving | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Billed agency hours ÷ 36 = posts each home can absorb; fill 30 in order of saving per hour | A, Ashgrove 16 and Bellmont 14; $2.53M, +23.9% | The finance team's own rule, applied to the invoices at each home's real rates | The position-control register caps Ashgrove at 6 vacant budgeted posts, and group policy says position control must hold |
| 1 | The same, capped at each home's vacant budgeted posts | B, Bellmont 14 (Ashgrove 6, Carrow 10); $2.46M, +20.3% | Feasible under the group's own budget control | Timesheets: 220 of Bellmont's 520 billed hours a week are call-off fees and orientation, not shifts worked |
| 2 | Hygiene: worked hours from timesheets, not billed hours | C, Carrow 13 (Ashgrove 6, Bellmont 8, Dene Park 3); $2.43M, +18.9% | Clean hours, feasible posts and real rates | The pilot log: converted posts at night-heavy homes idled on 24 of their 36 rota hours |
| 3 | **Decisive:** posts per home = the scarcest shift type's worked agency hours ÷ the rota's 12 hours, capped by position control | **E, Elmstead 11** (Ashgrove 4, Bellmont 4, Carrow 3, Dene Park 5, Fairholme 3); **$2.04M** | — | — |

* **The answer.** Ashgrove 4, Bellmont 4, Carrow 3, Dene Park 5, Elmstead 11 and Fairholme 3, saving $2,042,352 a year, committed as
  $2,040,000. Elmstead gets no post on rungs 0 to 2.
* **Figure shape.** Every correction walks the saving down (−3.0%, −1.1%, −15.9%), and the answer is the minimum cell of the grid.
* **The deciding comparison.** The rung-2 plan's saving as realised under the rota is $0.29M, because 16 of its posts idle on days and
  weekends. The brief has to set that against $2.04M.
* **Partial correction priced (L3).** Every half-applied rota hands the largest block to a wrong home. Applying the group-wide shift mix
  (a quarter of agency hours on weekday days) to every home gives Carrow 9 posts against 6 each at Ashgrove and Bellmont, Elmstead only 4,
  and $2.32M (+13.6%); an exact quarter gives Carrow 10 and $2.34M. Taking the rota minimum on billed hours gives Bellmont 13 against 5
  each at Ashgrove and Dene Park, Elmstead 4, and $2.34M (+14.5%). Both are wrong allocations well outside the floor.
* **Grid.** Position control (ignored, applied) × hours (billed, worked) × post law (total ÷ 36, rota minimum) = 8 cells. The nearest
  wrong cell is the rota minimum with position control ignored, $2.28M (+11.5%), which puts 15 posts at Dene Park against its 5 budgeted
  vacancies. Every other cell is at least 14% away.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The agreement fixes the rota for staff nurses as a staffing rule. No document connects it to agency conversion or
   to savings.
2. **The corpus pins the law by reproduction.** The rota minimum reproduces every pilot post's displaced and idle hours (40 of 40 posts,
   five of five homes). Hours ÷ 36 predicts no idle hours anywhere and misses the three night-heavy pilot homes. Its loss curve is flat
   across divisors from 36 to 60, and no divisor fits more than two of five homes. The law is a construction (shift classification from
   start times, three per-type sums, a minimum), not a parameter a sweep reaches.
3. **No arithmetic symptom.** Billed, worked and invoiced hours reconcile, and posts sum to 30 under every rung.
4. **Not a row predicate.** Each home's capacity is a minimum over three sums, each built by classifying shifts against the agreement's
   day, night and weekend definitions.
5. **The enumeration is arithmetic.** The three biggest agency bills (Ashgrove, Bellmont, Carrow) hold 11 of the group's 76 useful posts,
   and no column holds shift type.
6. **No cutover date.** The shift mix is stable across the 26 weeks, and nothing steps.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The pilot log: 40 converted posts at five homes, with weekly agency hours displaced and idle hours by shift type for each post
  over 26 weeks.
* **What it certifies.** Position control (no pilot home exceeded its vacancies) and worked-hour accounting (displaced hours tie to
  timesheets, not invoices). A solver who back-tests rungs 1 and 2 on those columns is confirmed.
* **The absolute split (O2).** Posts within a home's rota minimum idled 0 hours in every week. Posts beyond it idled 24 hours in every week.
  No post idled anything in between.
* **Twin pair.** Pilot homes Harbour View and Kestrel Court are identical on billed and worked agency hours (420 a week each), beds, rates
  and vacancies. Harbour View absorbed 8 posts with no idle hours and Kestrel Court 4, because 76% of Kestrel Court's agency hours are
  nights. No hours-based rule reproduces both.
* **Resemblance points at the decoy.** Ashgrove and Carrow match Harbour View, the pilot's best home, on beds, rates and agency volume.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** HR's recruitment plan fixes 30 posts for next year. Group policy says position control must hold. The collective
  agreement sets the full-time rota at 12 weekday-day, 12 weekday-night and 12 weekend hours a week over four weeks, and defines weekend as
  Saturday 07:00 to Monday 07:00.
* **Empirical pins.** The rota law and the 24-hour idle pattern come from the pilot log. Agency hours by shift type come from timesheet
  start times.
* **Voices.** The finance director: "Ashgrove is where the agency money goes, so that's where staff go." The pilot manager: "Every post we
  converted was filled within six weeks." That is true.
* **Licensed wrong basis.** The recruitment plan records that the group's lenders size conversion savings as average weekly agency hours ×
  the rate gap, and will see that basis.

## 8. Determinism by construction

* **Shift classification.** Every shift starts at 07:00 or 19:00, so day, night and weekend assignment needs no convention.
* **Whole posts.** A post must find 12 hours of every shift type, so useful posts are the floor of the scarcest ratio by definition. No
  rounding rule enters.
* **Demand stability.** Weekly worked agency hours by shift type stay within ±4% of their 26-week mean, so mean, median and any
  cost-ratio quantile give the same posts.
* **Fill order.** Savings per hour differ between every pair of homes, so no tie decides the order.
* **Maturity.** 26 complete weeks of timesheets after the pilot, with every week's invoices settled.

## 9. Prompt sketch and deliverables

> HR can recruit 30 staff nurses next year to replace agency shifts, and our finance director wants most of them at Ashgrove, where the
> agency bill is worst. Tell me how many of the 30 go to each home and the annual net saving, to the nearest $10,000, in a form I can give
> the board. Send `conversion_plan.xlsx`, a chart `post_value.png`, and a one-page `board_brief.pdf`.

* `conversion_plan.xlsx`: posts and savings by home under the four rung bases, the occupancy sheet (ask A) and the turnover sheet (ask B).
* `post_value.png`: for each home, agency hours by shift type as a stacked bar, the 12-hour rota line multiplied by the posts allocated,
  the scarcest shift marked, homes ordered by saving per hour, and the allocation printed above each bar.
* `board_brief.pdf`: the committed split, the saving, and the rung-2 plan's realised saving beside it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the ten homes, occupancy and resident days in each of the last four quarters.
  *Device:* a hospital bed-hold keeps a bed occupied but is not a resident day, per the census guide, and holds are recorded as a separate
  status row. Counting held beds as resident days overstates resident days by 3–6% at the four homes nearest the acute hospital.
* **Ask B (device-carried).** For each home, last year's staff-nurse turnover and the median tenure of leavers. *Device:* a nurse rehired
  within 30 days keeps the employee number, and the HR file records the gap as a leave of absence, not a termination. Counting the gap as
  leaving and rejoining doubles turnover at three homes.
* **Ask C (validity).** The allocation and saving under each of the four rung bases, the pilot reproduction under the rota law (40 of 40
  posts) and under hours ÷ 36 (two of five homes), and the rung-2 plan's realised saving ($0.29M).
* **Decoupling.** Clearing the rota minimum changes no figure in asks A or B.

## 11. Rubric arithmetic

10 homes × 4 quarters × 2 (ask A) + 10 × 2 (ask B) + 4 bases × 2 + 3 validity figures (ask C) + 10 post counts, the saving and the
realised comparison + 5 named chart parts + 3 files ≈ 131 criteria.

## 12. World-building constraints

* Worked agency hours a week (weekday day, weekday night, weekend) and gap: Ashgrove 58/464/58 at $46, Bellmont 50/200/50 at $44,
  Carrow 37/406/37 at $42, Dene Park 186/190/190 at $41, Elmstead 136/138/136 at $29, Fairholme 96/100/96 at $27, with four smaller homes at
  $21 to $25. Vacant budgeted posts: Ashgrove 6, Bellmont 14, Carrow 13, Dene Park 5, Elmstead 12, Fairholme 8.
* Billed hours exceed worked by call-off fees and orientation: Bellmont 520 billed (160/200/160), Ashgrove 600, Carrow 490, others within
  4%.
* Rung savings are $2.53M / $2.46M / $2.43M / $2.04M, and no other cell of the 8-cell grid is within 11% of the answer.
* Pilot: 40 posts at five homes, idle hours 0 or 24 a week with nothing in between. Harbour View and Kestrel Court are identical on every
  invoice and register column.
* Bed-holds and rehires never touch agency hours, vacancies or the rota.

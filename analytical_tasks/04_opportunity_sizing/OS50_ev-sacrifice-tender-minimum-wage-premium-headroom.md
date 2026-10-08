# OS50 — What annual saving an electric-car salary-sacrifice tender commits to, when warehouse premiums do not count as minimum-wage pay

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Economics · employee benefits and payroll costs |
| Mirrors | Benefits capped on a narrower pay base than the pitch counts (employee share-purchase plans at large retailers and fulfilment networks that cap contributions at a share of base pay, leaving out shift premiums and overtime; earned-wage access limited to pay already earned net of protected deductions; marketplace seller advances repaid from net settlements after fees and refunds) |
| Decision shape | One figure committed at a date: the annual employee saving written into the tender response due on the 14th, which becomes the scheme's service-level target |
| Committed call | The annual income tax and National Insurance saving the scheme delivers to the distributor's employees, to the nearest £10,000 |
| Gap · Pattern | Gap 3 (objective) over Gap 2 (population) · Pattern C (serviceable share behind a join: the sacrifice must leave minimum-wage pay above the minimum wage, and minimum-wage pay counts basic-rate pay and leaves out night, weekend and overtime premiums, so the warehouse teams whose premiums lift them to £31,500–£35,800 can sacrifice nothing), with E25 below it (the funder's report suppresses the logistics £30–40k cell under its dominance rule, and the sector total less the other bands recovers it exactly) |
| Gate G mechanism | binding_constraint, with method_or_model_selection |
| Measured traps engaged | #7 uses the ready-made measure · #24 treats an unpublished figure as unknown · #3 stops at a close but inexact match |
| Calibration form | Existing-book actuals: the provider's book at 40 client employers, with the payroll partner's 41,600 screening decisions and each screened worker's earnings lines, every order's realised saving, and the funder's report of orders and eligible employees by client sector and pay band |
| Driving force | The scheme may not take any employee's pay below the minimum wage, and minimum-wage pay counts basic-rate pay for every hour and leaves out night, weekend and overtime premiums. The distributor pays its 6,600 warehouse workers the National Living Wage as their basic rate, and premiums lift them to £31,500–£35,800. Even after the sacrifice their gross pay clears the minimum wage, and they hold nearly two thirds of the saving on every lower rung. On minimum-wage pay their headroom is nil, so they can sacrifice nothing. Gross pay is the ready-made measure; minimum-wage pay is a sum over earnings lines that no file holds. |

## 1. Situation

An electric-car salary-sacrifice provider is tendering for a national grocery distributor's scheme, open to its 10,220 employees. An
employee gives up £420 a month of salary for the scheme's standard car, saves income tax and National Insurance on the sacrifice, and pays
tax on the car's benefit in kind. The tender response, due on the 14th, must commit to the annual saving the scheme delivers to employees.
The figure becomes the service-level target, with service credits if the scheme falls short. The provider runs schemes at 40 employers: its
payroll partner screened every employee there, and its funder reports orders by sector and pay band. The distributor's reward director
expects the warehouse night teams to be the scheme's biggest users.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the distributor's payroll extract and earnings lines, the tax pack, the partner's screening
  decisions, the realised savings and the funder's report. The warehouse workers' gross pay really does clear the minimum wage after the
  sacrifice. Nothing reported is overturned. The difficulty is which pay the minimum wage is tested on.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the reward director's view and every voice. The scheme's own minimum-wage clause, applied to gross pay, still
  admits the warehouse teams, and no document says premiums do not count.
* **Instrument repair.** Suspect file: the funder's report, whose logistics £30–40k cell is suppressed under its dominance rule. Published,
  the cell holds the 160 orders that the sector total less the other bands gives, so rung 2 stays at £408,424 and rungs 0 and 1, which use
  only the book-wide rate, stay at £168,361 and £307,664. The extract's earnings lines, the partner's decisions and the realised savings are
  complete, and gross pay is a correct field for a different attribute. No field claims to record minimum-wage pay, so the construction is
  still needed for £141,467.
* **Lens swap.** The answer counts a different population, the employees whose minimum-wage pay has room for the sacrifice, which leaves
  out the 6,600 warehouse workers the gross-pay test admits.

## 3. The driving force

A strong solver applies the scheme's clause to every employee (gross pay after the sacrifice must clear the minimum wage for the hours
worked) and computes each saving at marginal rates, band by band, with the benefit in kind taxed where it lands. That gives £1,011 a car for
a basic-rate worker, £1,253 for an engineer whom the sacrifice takes back under the higher-rate threshold, and £1,925 for a senior manager
in the personal-allowance taper. It sees that take-up climbs with pay, takes the funder's logistics rates by band, and recovers the
suppressed £30–40k cell from the sector total. Each step is right, and the warehouse teams carry nearly two thirds of the figure. But the minimum
wage is not tested on gross pay. Minimum-wage pay counts basic-rate pay for every hour worked and consolidated allowances. It leaves out
the premium part of night, weekend and overtime pay, and it falls by whatever salary is sacrificed. The distributor pays its warehouse
workers the National Living Wage as their basic rate, so their headroom is nil whatever their premiums. Drivers, supervisors, engineers,
managers and the better-paid office staff keep theirs. The partner's screening decisions follow the rule, and the earnings lines hold
everything needed to apply it.

## 4. The ladder

| Rung | Construction (annual saving = expected orders × saving per car) | Figure (annual saving, offset from the answer) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Each employee's average tax-and-NI rate × (sacrifice − benefit in kind); eligible where gross pay after the sacrifice clears the minimum wage for the hours worked; take-up 3.0% book-wide | A, £168,361, +19.0% | Each worker's own tax and NI as a share of pay, and the scheme's own clause | The tax pack: a sacrifice is relieved band by band at the rates it comes out of, and the benefit in kind is taxed at the rate it lands in |
| 1 | Saving at marginal rates, band by band | B, £307,664, +117.5% | Exact relief, including the threshold and the taper | The funder's report: take-up among eligible employees climbs from 1.6% at £20–30k to 7.0% above £70k in logistics |
| 2 | Take-up by pay band from the funder's logistics rows, the suppressed £30–40k cell recovered as the sector total less the other bands (E25) | C, £408,424, +188.7% | The sector's own rates at the right grain, with nothing treated as unknown | The partner's 41,600 screening decisions reproduce only when minimum-wage pay leaves out premiums and deducts the sacrifice (41,600 of 41,600; gross pay 38,650) |
| 3 | **Decisive:** eligible only where minimum-wage pay (basic-rate pay for every hour, consolidated allowances, no premiums, less the sacrifice) clears the minimum wage | **E, £141,467** | — | — |

* **The answer.** £141,467 a year, committed as £140,000: 122 cars (drivers 42, supervisors 12, engineers 13, office staff 20, managers
  28, senior managers 7). The 6,600 warehouse workers order none.
* **Figure shape.** The first two corrections walk the figure up (+82.7%, +32.8%), and the decisive move reverses them (−65.4%), landing
  16% below rung 0.
* **The deciding comparison.** The warehouse teams hold £266,957 (65%) of the rung-2 figure and none of the answer.
* **Partial correction priced (L3).** Leaving out only the night premium keeps the day teams, whose weekend and overtime premiums look like
  £477 a month of headroom: £258,766 (+82.9%). Leaving out every premium but not deducting the sacrifice admits everyone paid at least the
  minimum wage, which is rung 2 again: £408,424 (+188.7%).
* **Grid.** Rate (average, marginal) × take-up (book-wide, logistics by band) × minimum-wage test (gross pay, minimum-wage pay) = 8 cells.
  The nearest is rung 0 (+19.0%), and the marginal rate with book-wide take-up on minimum-wage pay gives £107,446 (−24.0%). Every other
  cell is at least 42% away.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The scheme's terms say the sacrifice may not take pay below the minimum wage. Nothing in the pack says minimum-wage
   pay leaves out premiums, and the extract's gross pay looks like the pay the clause means.
2. **The corpus pins the rule by reproduction (Pattern B).** Minimum-wage pay (basic-rate pay for every hour, consolidated allowances in,
   premiums out, the sacrifice deducted) reproduces all 41,600 screening decisions. Gross pay reproduces 38,650, and the same rule with
   overtime hours' basic pay left out reproduces 41,290. Every gross-pay miss approves a worker the partner declined, so it also misses the
   published count of 4,400 declines. The rule is a construction over earnings lines, not a column a sweep reaches.
3. **No arithmetic symptom.** Earnings lines sum to gross pay, tax and National Insurance reconcile, and every rung's figure ties to its
   groups.
4. **Not a row predicate.** Eligibility is a sum over a worker's earnings lines in a pay reference period, less the sacrifice, against the
   minimum wage for every hour worked.
5. **The enumeration is arithmetic.** No column holds minimum-wage pay. It is computed for 10,220 employees from 46,000 earnings lines in
   the last full month.
6. **No cutover date.** The rule has applied throughout the book's history, and nothing steps.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The provider's book at 40 client employers: the payroll partner's 41,600 screening decisions, each with the worker's earnings
  lines for the pay reference period it checked; every order's realised tax and National Insurance saving; and the funder's report of
  orders and eligible employees by client sector and pay band, with sector totals.
* **What it certifies.** Relief band by band (every order's realised saving matches it to the penny), take-up by band (1,116 orders from
  37,200 eligible employees, 3.0% overall) and the funder's totals. A solver who back-tests rungs 1 and 2 is confirmed.
* **The absolute split (O2).** Every declined worker's minimum-wage headroom is below the £420 sacrifice, and every approved worker's is at
  or above it, with no decision the other way.
* **Twin pair.** Two logistics clients' depots of 400 employees each are identical on gross pay bands, mean gross pay (£34,900), hours and
  grade titles. One pays its warehouse teams a consolidated £16.55 an hour; the other pays its night teams the National Living Wage plus a
  30% night premium. The partner approved 392 and 196 employees, and the funder records 16 and 8 orders, 2.0× apart.
* **Resemblance points at the decoy.** The distributor matches the book's logistics clients on gross pay bands, hours and depot size, so
  transferring their take-up by resemblance gives the rung-2 figure. Those clients pay 85% of their warehouse workers a consolidated rate;
  the distributor pays none.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The scheme's terms set the sacrifice at £420 a month for the standard car (list price £40,000) and bar any sacrifice
  that takes an employee's pay below the minimum wage. The tax pack gives the scheme year's income tax and National Insurance bands, the
  personal-allowance taper, a 5% benefit-in-kind rate and a National Living Wage of £12.71 an hour. The tender counts a full year's saving
  for every car ordered in the scheme's first year.
* **Empirical pins.** Take-up among eligible employees by sector and pay band, from the funder's report and the partner's decisions; the
  minimum-wage rule, from the decisions' reproduction.
* **Voices.** The distributor's reward director: "The night teams are our best-paid hourly staff; they'll be the scheme's biggest users."
  The provider's sales lead: "Nobody on thirty-five grand is anywhere near the minimum wage."
* **Licensed wrong basis.** The tender's evaluation guide compares bidders' savings for every employee whose gross pay stays above the
  minimum wage after the sacrifice, and the panel will see that basis.

## 8. Determinism by construction

* **Pay reference period.** The partner checked the last full month before each scheme launched, and the distributor's extract carries one
  full month for every employee. Hours and basic pay are contractual, and overtime adds basic-rate pay and hours together, so premiums never
  move headroom.
* **Ages.** Every employee is 21 or over, so the National Living Wage applies throughout.
* **Car.** Every order is the standard car, so the sacrifice and the benefit in kind are fixed.
* **Orders.** Expected orders are take-up × eligible employees, unrounded, as the funder's report computes them. At the answer every group's
  expected orders are whole cars.
* **Bands.** Pay bands are gross annual pay before the sacrifice, as the funder's report defines them.
* **Rounding.** £141,467 sits 3,533 below the £145,000 rounding boundary and 6,467 above £135,000.

## 9. Prompt sketch and deliverables

> We're bidding for the distributor's electric-car salary-sacrifice scheme, and their reward director expects the warehouse night teams to
> be its biggest users. Tell me the annual tax and National Insurance saving our scheme will deliver to their employees, to the nearest
> £10,000, in a sentence I can put in the tender response as our service-level commitment. Send `saving_model.xlsx`, a chart
> `saving_by_group.png`, and a one-page `tender_commitment.pdf`.

* `saving_model.xlsx`: the figure under the four rung bases, each group's eligible employees and saving per car, the screening reproduction
  sheet, the turnover sheet (ask A) and the charging sheet (ask B).
* `saving_by_group.png`: for each employee group, the saving under gross-pay and minimum-wage-pay eligibility as paired horizontal bars,
  groups ordered by headcount, the warehouse groups marked, each group's expected cars printed beside its bars, and the committed figure in
  the title.
* `tender_commitment.pdf`: the committed figure, the groups behind it and why the warehouse teams are not in it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the distributor's 14 depots, last year's leavers and turnover rate. *Device:* a worker
  who moves depot gets a leaver row and a starter row under the same employee number with a transfer reason, per the HR data guide, and is
  not a leaver. Counting those rows as leavers overstates turnover by about a quarter at the three depots that took staff from the closed
  Midlands site.
* **Ask B (device-carried).** For each depot, its workplace charge points and their average daily charging sessions last quarter.
  *Device:* a session paused and resumed within ten minutes keeps its session ID and adds an energy row, per the charge-point operator's
  export guide. Counting rows overstates sessions by about 15% at the depots with older chargers.
* **Ask C (validity).** The figure under each of the four rung bases; the screening reproduction under minimum-wage pay (41,600 of 41,600),
  gross pay (38,650) and minimum-wage pay without overtime hours' basic pay (41,290); and the warehouse share of the rung-2 figure (65%).
* **Decoupling.** Clearing the minimum-wage construction changes no figure in asks A or B.

## 11. Rubric arithmetic

14 depots × 2 (ask A) + 14 × 2 (ask B) + 4 bases + 3 reproduction counts + the warehouse share (ask C) + 9 groups' eligible employees and
9 savings + the committed figure + 5 named chart parts + 3 files ≈ 91 criteria.

## 12. World-building constraints

* Groups (headcount / gross pay / pay structure / band / saving per car / minimum-wage eligible): warehouse nights 3,700 / £35,800 /
  National Living Wage basic, 30% night premium, overtime premiums / £30–40k / £1,011.20 / no; warehouse days 2,900 / £31,500 / National
  Living Wage basic, weekend and overtime premiums / £30–40k / £1,011.20 / no; HGV drivers 1,400 / £47,000 / £17.20 basic over 2,450 hours
  with night and overtime premiums / £40–50k / £1,011.20 / yes; shift supervisors 400 / £41,500 / £16.10 basic / £40–50k / £1,011.20 /
  yes; engineers 260 / £52,000 salaried / £50–70k / £1,253.40 / yes; office staff 500 at £33,300 (yes) and 400 at £27,000 (no under either
  test); managers 560 / £64,000 / £50–70k / £1,316.80 / yes; senior managers 100 / £110,000 / £70k+ / £1,924.80 / yes.
* Logistics take-up among eligible employees: 1.6% (40 of 2,500), 4.0% (160 of 4,000, suppressed), 3.0% (90 of 3,000), 5.0% (60 of 1,200)
  and 7.0% (21 of 300), with a sector total of 371 orders; book-wide 1,116 of 37,200 (3.0%).
* Rung figures £168,361, £307,664, £408,424 and £141,467; grid cells and partials as stated, none within 19% of the answer.
* Screening: 41,600 decisions, 4,400 declines (2,950 of them premium-paid workers whose gross pay clears the minimum wage); reproduction
  41,600, 38,650 and 41,290. The twin depots are identical on every gross-pay column at 392 and 196 approvals and 16 and 8 orders.
* HR transfers and charging sessions never touch earnings lines, screening decisions or orders.

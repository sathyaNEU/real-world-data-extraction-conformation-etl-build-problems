# RC20 — How many quits the retention bonus programme will save next year, net, filed before finance decides whether to cut it

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Economics · labour markets and workforce planning |
| Mirrors | Retention and incentive programmes judged on recipients alone (retention grants at Google and Meta, pay-to-stay offers in Amazon's operations network, bonuses in Apple retail), where the effect on teammates who were passed over offsets part of the gain |
| Decision shape | One figure committed at a date (a component): the programme's net quits prevented next year, filed at the budget review on the 9th |
| Committed call | Voluntary quits the retention programme will prevent next year, net, as a whole number |
| Gap · Pattern | Gap 3 (objective) over Gap 2 (population) · E22 (the deciding comparison: quits prevented among recipients against quits induced among their unchosen teammates), with E14 (a binding limit applied in the figure: the policy's per-unit award pool) at rung 2 |
| Gate G mechanism | decomposition_attribution, with confirm_surface_read support |
| Measured traps engaged | #20 leaves the deciding comparison unstated · #10 notes a binding limit as a risk · #13 validates on one population, applies to another |
| Calibration form | Parallel-run overlap: the four months in which the old and new HR systems both recorded every separation, with the crosswalk of employee and manager ids |
| Driving force | Recipients' quit rate fell against matched non-recipients, a real effect. Teammates who were not chosen quit more than matched staff in teams with no recipient, and that rise is read one table at a time as market noise. Only setting the two side by side, with teams rebuilt from the new system's manager ids carried back through the parallel run's crosswalk, gives the programme's net effect, and it falls below the line the budget rule sets. |

## 1. Situation

A large employer funded retention bonuses for at-risk staff when quits were high. National quits have since fallen from 3.0% to 2.3% a month, and the
CFO wants to cut the programme because people have stopped quitting. HR says recipients barely leave. The budget rule keeps the programme next year
only if it prevents at least 80 voluntary quits a year net. The compensation policy caps retention awards in any business unit at 8% of its
payroll. The company moved to a new HR system last year; for four months both systems recorded every separation.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: separations in both systems, award records, the crosswalk, the policy cap and the national series. HR is
  right that the bonus keeps recipients, and the CFO is right that the market cooled. Nothing reported is overturned; the figure is the size of
  the component HR names, measured whole.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the CFO, HR and the licensed basis. The matched comparison of recipients, capped by the policy, still clears the
  budget line, and nothing in the pack mentions teammates.
* **Instrument repair.** Suspect file: the old HR system, which carries no manager id. Repaired so that every pre-award month records each
  employee's manager, the crosswalk is no longer needed, and rung 0 still returns 172, rung 1 118 and rung 2 94; none returns 64. Separations
  are complete in both systems. The answer still needs the deciding comparison: the teammates' extra quits are recorded already, and only
  setting them against the recipients' gain, both by matched difference in differences, gives the net.
* **Lens swap.** The naive figure is the recipients' gain; the answer is the gain less what the programme cost in teams it touched, a different
  population (recipients and their teammates) over the coming year.

## 3. The driving force

A strong solver does not compare recipients with everyone: recipients were chosen from high-quit job families, so it matches them to
non-recipients in the same family and tenure band and takes the difference in differences, before and after awards. The effect is 6.2 points.
It applies the effect to next year's at-risk staff, and it applies the policy's cap: two units would breach 8% of payroll, so 1,520 can be
awarded, not 1,900. That gives 94 quits prevented, comfortably over the line. Each table on the way is read alone. In the year after awards,
non-recipients in teams with a recipient quit 2.1 points more than matched non-recipients in teams without one. Read alone that is the market,
and it is the programme: passed-over teammates leave. Teams exist only through manager ids, which the old system lacked; the parallel run's
crosswalk carries them back to the pre-award months. Netting the 30 quits induced among next year's 1,450 teammates leaves 64.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Recipients' quit rate against all non-recipients' this year, applied to next year's 1,900 at-risk staff | 172 quits (+168%) | HR's comparison, made exactly on the new system's definitions | The award file: recipients came from job families whose quit rates were twice the company's before any award |
| 1 | Matched difference in differences (job family × tenure band, before and after), applied to all 1,900 | 118 (+83%) | Selection removed, the textbook programme evaluation | The compensation policy: two units would exceed the 8%-of-payroll award pool, so 1,520 can be awarded |
| 2 | The same applied to the 1,520 the cap allows | 94 (+47%) | Causal effect, binding limit applied, clear of the budget line | Team structure: non-recipients in recipients' teams quit 2.1 points more than matched non-recipients in teams without one |
| 3 | **Decisive:** quits prevented among recipients set against quits induced among their unchosen teammates, both by matched difference in differences | **64 quits** | — | — |

* **Figure shape.** Every correction walks the figure down (−31%, −20%, −32% per step), and the answer is the minimum cell, so every partial
  application keeps a programme the budget rule cuts.
* **Partial correction priced (L3).** A solver who looks for spillover but measures it company-wide (all non-recipients before and after)
  finds the market's fall swamps it, nets nothing and stays at 94 (+47%), rung 2's figure.
* **Grid.** Comparison (raw, matched) × cap (off, on) × spillover (off, on) gives eight cells from 64 to 172. The nearest wrong cell is 84
  (+30.5%), which needs the cap ignored after the decisive move.
* **The deciding comparison (#20).** 94 quits prevented among recipients against 30 induced among teammates is the line the budget paper has to
  carry; no single table in the pack shows either beside the other.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The people-analytics standard says programme effects are measured by matched difference in differences; it says
   nothing about who counts as affected. No document mentions teammates.
2. **Corpus blind for a computable reason.** *Every month of the parallel run predates the first award, so no employee in it had a recipient
   teammate and the overlap can certify the quit definition and the team crosswalk but cannot score a spillover.*
3. **No arithmetic symptom.** Separations reconcile across the two systems in every overlap month; headcounts, awards and quits tie.
4. **Not a row predicate.** Exposure is a property of a team, built from manager ids, carried back through a crosswalk, then compared
   within job family and tenure band.
5. **The enumeration is arithmetic.** No column marks a teammate as exposed; 1,450 next-year teammates are built from the award plan and the
   org chart.
6. **No cutover date.** Awards were made unit by unit over a quarter; the dated event (the national quits peak) is the CFO's decoy.
7. **Survives deletion.** With every voice gone, the capped matched figure still clears the line.

## 6. The calibration corpus

* **Form.** The parallel run: four months in which the old and new HR systems both recorded every separation, with the crosswalk of employee
  ids and the new system's manager ids.
* **What it certifies.** The quit definition (11% of old-system "voluntary" separations were transfers to the joint venture, which the new
  system records as transfers) and the team crosswalk (every old-system employee in the overlap maps to one manager).
* **What it is blind to.** Spillover (above).
* **Twin pair.** Units U-04 and U-09 had the same headcount, job-family mix, recipient share (11%) and pre-award quit rates. Net quits prevented
  were 41 and 20 (2.05×): U-04's recipients sat in a few teams and U-09's were spread across many, exposing three times as many teammates. Only
  the team-level comparison separates them.
* **Resemblance points at the decoy.** Next year's award plan matches this year's on units, families and recipient count, so every comparison
  with this year carries the recipients' gain forward unchanged.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The budget rule: the programme continues next year if it prevents at least 80 voluntary quits a year, net. The compensation
  policy: retention awards in a business unit are capped at 8% of its payroll. The people-analytics standard's method sentence.
* **Empirical pins.** The effect and the spillover, both by matched difference in differences; teams through the crosswalk.
* **Voices.** The HR director: "Recipients barely leave. The programme is the reason." The workforce analytics lead: "The national fall is
  leisure and hospitality; our industries are still hot."
* **Licensed wrong basis.** The policy records that the remuneration committee evaluates retention programmes on recipients' quit rates against
  the company average and will present that comparison.

## 8. Determinism by construction

* **Quit.** A voluntary separation under the new system's definition; the overlap fixes the restatement of earlier months.
* **Teams.** A team is a manager's direct reports on the award date; no recipient changed manager within the year.
* **Matching.** Job family × tenure band, the standard's cells; every recipient and exposed teammate has matched comparators.
* **Next year.** The award plan names recipients up to the cap; teammates are their teams' non-recipients on the plan date.
* **Rounding.** Whole quits; the answer sits 16 below the line.

## 9. Prompt sketch and deliverables

> Finance wants to cut the retention bonuses because quits have fallen everywhere. The CFO is convinced the market is doing the programme's job.
> Tell me how many quits a year the programme saves us, net, as the number I file at the budget review on the 9th. Send `retention_case.xlsx` and
> a chart `net_effect.png`.

* `retention_case.xlsx` — the four constructions, the national-industry sheet (ask A), the vacancies sheet (ask B) and the parallel-run
  reproduction (ask C).
* `net_effect.png` — a waterfall from recipients' quits prevented to the net figure, with bars for the cap and the teammates' induced quits, the
  80-quit budget line as a reference, and an inset of quit rates for recipients, exposed teammates and unexposed staff before and after awards.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 17 national private industries, the quits rate averaged over the last twelve months
  against the twelve before. *Device:* the published industry series are seasonally adjusted one by one and do not add up, as the survey's methods
  pages document; averaging the adjusted series misstates the change in three industries, and the unadjusted levels are the additive ones.
* **Ask B (device-carried).** For each business unit, median days to fill vacancies opened in the last six months. *Device:* a requisition
  reopened after a failed hire keeps its original open date and carries a reopen date, from which time to fill runs, as the recruiting system's
  guide documents; using the original date overstates the four units with most failed hires.
* **Ask C (validity).** For each overlap month, separations by type in each system and the restated count; and the figure under each of the four
  rung constructions.
* **Decoupling.** Clearing the spillover construction changes no figure in asks A or B.

## 11. Rubric arithmetic

17 industries × 2 periods (ask A) + 12 units (ask B) + 4 months × 3 counts + 4 constructions (ask C) + the committed figure, the induced quits and
the recipients' gross figure + 5 named chart parts + 2 files ≈ 90 criteria.

## 12. World-building constraints

* Effects: raw 9.06 points, matched 6.2; spillover +2.1 points on exposed teammates; 1,900 at-risk staff, 1,520 under the cap, 1,450 exposed
  teammates next year.
* Rung figures 172 / 118 / 94 / 64; grid as in section 4.
* 11% of old-system voluntary separations in the overlap are joint-venture transfers.
* U-04 and U-09 identical on every unit-summary column.
* Seasonal adjustment and requisition dates touch no separation, award or team record.

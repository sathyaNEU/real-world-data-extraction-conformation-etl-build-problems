# OS35 — Which water system gets the $14M lead-line tranche, when the fund pays each line only to a cap and the town pays the rest

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Policy & Education · public infrastructure programmes (drinking water) |
| Mirrors | Allocating a capped subsidy where each unit's excess over the cap falls on the recipient (device subsidy schemes with per-device caps and co-pays, cloud credits capped per workload, home-retrofit grants capped per property with the owner covering the rest) |
| Decision shape | Which of N gets one scarce thing, with the sizing graded: the principal-forgiveness tranche goes to one of six water systems |
| Committed call | The system that gets the tranche, and the number of lead service lines it replaces |
| Gap · Pattern | Gap 3 (objective) over Gap 2 (population) · S5 (a per-line cap that does not commute: each line's excess over the cap draws on a fixed local contribution, so averages hide which budget binds), with E15 below it (galvanised lines behind a recorded lead connector, the quiet trap behind the loud one of unknown lines) |
| Gate G mechanism | binding_constraint, with method_or_model_selection |
| Measured traps engaged | #1 reports a failed back-test, ships anyway · #11 beats the headline trap, misses the quiet one · #10 notes a binding limit as a risk |
| Calibration form | Published control set with a reproduction clause: last round's 12 published award determinations (lines funded per award), and the intended-use plan's clause that a sizing method must reproduce every one |
| Driving force | The fund pays each line up to $9,500 and the town pays the rest from a fixed local contribution. Corliss's average line costs $4,860, so averages say the cap never bites. But three in ten of its lines are long rural services at $12,000, each drawing $2,500 of local money, so its $450,000 runs out after about 600 lines, under a fifth of what the tranche could fund. Only per-line truncation, accumulated in the system's plan order, reproduces all twelve published determinations. |

## 1. Situation

A state revolving fund has one $14M principal-forgiveness tranche for lead service line replacement this round, and it goes to one of six
disadvantaged water systems. The intended-use plan caps eligible cost at $9,500 a line, funds lines in each system's approved plan order,
and records each system's committed local contribution. The legislature's oversight committee will ask how many lead service lines the
tranche takes out of the ground. The programme manager favours Corliss, an old mill town full of galvanised pipe.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the inventories, the verification samples, the connector register, the cost schedule, the plans,
  the local contributions and last round's determinations. Corliss really does have the most lines needing replacement. Nothing reported is
  overturned. The difficulty is which of two budgets runs out first, line by line.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the manager's view and every voice. The inventories, once unknown and galvanised lines are counted, still put
  Corliss far ahead, and every system's average cost sits under the cap.
* **Instrument repair.** Suspect files: the inventories' unknown lines and their galvanised lines recorded as non-lead behind a lead
  connector. Repaired, rungs 0, 1 and 2 all become the full-need, average-cost build and name Corliss (2,881). The cost schedule, plans and
  local contributions are complete, and Corliss's local money still runs out after 600 lines, so the per-line cap in plan order is still
  needed for Easton's 2,010.
* **Lens swap.** The answer counts lines that can actually be paid for, a subset of the lines that need replacing, and Corliss's subset is
  a fifth of its need.

## 3. The driving force

A strong solver refuses to treat unknown lines as non-lead and imputes them at the state's verified rates by age band. It then finds the
quieter population: galvanised lines that sit, or once sat, downstream of a lead gooseneck, which state guidance requires to be replaced.
That makes Corliss's need 3,050 lines, and $14M at its $4,860 average cost reaches 2,881 of them. But the fund pays min(cost, $9,500) per
line, and the system must cover each line's excess from its committed local contribution. A fixed local budget meets a cost distribution
whose average is under the cap and whose tail is far over it. Taking max(0, average − cap) gives zero, while the sum of max(0, cost − cap)
over Corliss's plan exhausts $450,000 after about 600 lines. The binding constraint differs by system and is visible only at line grain,
along each plan's order.

## 4. The ladder

| Rung | Construction (lines replaced = min(need, reach)) | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Need = reported lead lines; reach = $14M ÷ the system's average line cost | A, Ardley, 2,059 (1.29× Delmar) | The inventory's own lead count, priced at the cost schedule | The state's verification sample finds lead in 20–60% of unknown lines by age band, so unknown is not non-lead |
| 1 | Need adds unknowns × verified rate by age band | B, Brennan, 2,460 (1.19× Ardley) | The headline trap of the inventory, beaten with calibrated rates | The state's galvanised-line sample: every galvanised line with a gooseneck on the connector register, present or removed, required replacement |
| 2 | Need adds galvanised lines behind a recorded lead connector | C, Corliss, 2,881 (1.17× Brennan) | Both inventory traps beaten and each checked against its own sample | Last round's 12 determinations reproduce only when each line's excess over $9,500 is charged to the local contribution in plan order |
| 3 | **Decisive:** reach = the longest prefix of the plan whose capped costs fit $14M and whose excesses fit the local contribution | **E, Easton, 2,010 (1.26× Delmar)** (5th of 6 on rung 0) | — | — |

* **The answer.** Easton: its costs cluster at $7,000, almost nothing exceeds the cap, and the tranche replaces 2,010 lines.
* **Position table.** Easton ranks 5th on rung 0 and 4th on rungs 1 and 2, and leads only rung 3. It is never 2nd. Rung leaders beat their
  runners-up by 1.29×, 1.19×, 1.17× and 1.26×.
* **Discriminator dominance.** Corliss carries a 1.44× lead into rung 3 (2,881 against 2,000). Its reach falls to 0.21 of the average-cost
  figure while Easton keeps 1.00, an edge of 4.8×, far above 1.2 × 1.44 = 1.73.
* **The deciding comparison.** Corliss: 3,050 lines needed, $14M could fund 3,406 at capped cost, and the local contribution stops it at
  600. Easton: 2,100 needed and 2,010 funded, with $0.25M of local money barely touched.
* **Partial correction priced (L3).** Every half-applied cap names Corliss. Applying the per-line cap but assuming the excess is always
  met gives Corliss 3,050 lines against Brennan's 2,460 (1.24×), with Easton 4th at 2,010. Checking the local contribution against the
  average excess, max(0, $4,860 − $9,500) = 0, leaves rung 2 standing: Corliss 2,881 against Brennan's 2,460 (1.17×), Easton 4th.
* **Grid.** Unknowns (off, on) × galvanised (off, on) × reach (average cost, per-line cap, cap plus local contribution) = 12 cells. Every
  non-answer cell names Ardley, Brennan, Corliss or Delmar. Delmar, local-bound at 1,600, leads every cell that has the decisive reach
  without both need corrections.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The plan states the cap and records each local contribution. No sentence says the contribution must meet excess
   line by line, or that replacement stops when it is spent.
2. **The corpus pins the rule by reproduction.** The full rule reproduces 12 of 12 published determinations. Cap without the local limit
   reproduces 7, and average cost 4. Both rivals overstate every award they miss, so they also miss the round's total, by 22% and 35%. The
   rule is a construction: per-line costs from inventory length and surface type at the schedule, two truncated running sums along the
   plan order, and the first line at which either binds.
3. **No arithmetic symptom.** Total cost is identical under every reading, the tranche never over-spends, and need counts reconcile to the
   inventories.
4. **Not a row predicate.** Whether line 601 is funded depends on the excess of the 600 before it.
5. **The enumeration is arithmetic.** No column holds a line's excess or a system's reach.
6. **No cutover date.** Nothing steps; the cost tail is geography.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** Last round's 12 published determinations: award, system, lines funded and local contribution, with the systems' plans and
  inventories as filed then.
* **What it pins (Pattern B).** The funding rule (above). Every prior award was reach-bound, so the control set scores the funding rule and
  is silent on unknown and galvanised lines.
* **The quiet trap's own control.** The state's galvanised sample of 340 excavated lines: required replacement in 214 of 214 cases with a
  gooseneck on the connector register (present or removed), and in 0 of 126 without. The systems' own "non-lead" label misses all 214.
* **Twin pair.** Last round's awards to Hollister and Marsh Creek are identical on every published column: award ($10.5M), system size,
  average line cost ($6,900) and lead lines in plan. They funded 1,521 and 760 lines, 2.0× apart, because Marsh Creek's costs carry a
  long-service tail its local contribution could not meet. No average reproduces both.
* **Resemblance points at the decoy.** Corliss resembles Hollister, last round's best award, on town type and average line cost.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The intended-use plan caps eligible cost at $9,500 a line and funds lines in each system's approved plan order. Its
  reproduction clause requires any sizing method to reproduce last round's determinations. State guidance counts galvanised lines that are
  or ever were downstream of a lead connector as lead service lines.
* **Empirical pins.** Unknown-line rates by age band come from the verification sample. The connector rule comes from the galvanised
  sample. The funding rule comes from the control set.
* **Voices.** The programme manager: "The old galvanised towns are where the lead really is." The state drinking-water engineer: "Unknown
  lines are the whole story this round."
* **Licensed wrong basis.** The plan records that the oversight committee compares systems on inventoried lead service lines and will see
  that basis.

## 8. Determinism by construction

* **Line costs.** Every line's cost comes from the schedule by length and surface type, and no line is within $50 of the cap.
* **Unknown rounding.** Expected lead among unknowns rounds the same whether summed by age band or overall, in every system.
* **Connector history.** The register carries removal dates, and guidance says "is or ever was", so present-only and ever readings
  cannot both be defended.
* **Stopping line.** In every system the binding budget is exhausted at a whole line with at least $3,000 to spare on the other budget,
  so no partial-line rule arises.
* **Maturity.** Inventories as filed by the round deadline; no amendment is pending.

## 9. Prompt sketch and deliverables

> This round's $14 million principal-forgiveness tranche goes to one water system, and the oversight committee will ask how many lead
> service lines it actually takes out of the ground. Our programme manager is sure it belongs in Corliss. Tell me which system gets it and
> how many lines the tranche replaces, as a whole number, in a sentence for the intended-use plan. Send `tranche_case.xlsx`, a chart
> `lines_replaced.png`, and a one-page `iup_note.pdf`.

* `tranche_case.xlsx`: the six systems under the four rung bases, the per-line build for each plan, the verification sheet (ask A) and
  the work-order sheet (ask B).
* `lines_replaced.png`: for each system, cumulative tranche spend and cumulative local excess against lines in plan order, as paired
  lines, with the $14M and local-contribution ceilings drawn and the stopping line marked.
* `iup_note.pdf`: the committed system, its line count, and the Corliss comparison.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each system, the share of inventoried lines verified in the field rather than from records,
  in each of three building-age bands. *Device:* re-verification overwrites the method on the inventory row, and earlier methods sit in the
  verification history with dates, per the inventory guide. Reading only the current method overstates field verification by 11 points in
  the two systems that re-surveyed.
* **Ask B (device-carried).** For each system, the median days from customer notice to completed replacement in last round's work, and the
  share completed within the 45-day notice rule. *Device:* a work order reissued to a new contractor gets a new number and carries the
  original in a reference field. Treating reissues as new starts understates durations in three systems.
* **Ask C (validity).** Each system's lines replaced under the four rung bases, and the control-set reproduction under the three funding
  rules (4, 7 and 12 of 12).
* **Decoupling.** Clearing the local-contribution limit changes no figure in asks A or B.

## 11. Rubric arithmetic

6 systems × 3 bands (ask A) + 6 × 2 (ask B) + 6 × 4 bases + 3 reproduction counts (ask C) + the committed system, its line count, its
margin and the Corliss comparison + 5 named chart parts + 3 files ≈ 69 criteria.

## 12. World-building constraints

* Need (reported lead / plus unknowns / plus galvanised behind connectors): Ardley 2,300 / 2,360 / 2,360, Brennan 1,500 / 2,460 / 2,460,
  Corliss 900 / 1,100 / 3,050, Delmar 1,700 / 1,820 / 1,860, Easton 500 / 1,200 / 2,100, Fallow 450 / 570 / 630.
* Average line cost and mean excess over the cap per line: Ardley $6,800 / $1,330, Brennan $5,400 / $1,400, Corliss $4,860 / $750, Delmar
  $8,800 / $180, Easton $7,000 / $36, Fallow $7,600 / $400. Local contributions: $0.90M, $0.80M, $0.45M, $0.288M, $0.25M, $0.30M.
* Lines replaced at rung 3: Easton 2,010, Delmar 1,600, Ardley 677, Fallow 630, Corliss 600, Brennan 571.
* Twelve prior determinations, all reach-bound. Hollister and Marsh Creek are identical on every published column.
* Verification history and reissued work orders never touch need, costs, plans or local contributions.

# DS17 — Which verification sampling plan the regulator runs next year, when every option in the memo fails once risks are computed at the new method's rates

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Policy & Education · food-safety regulation and inspection programmes |
| Mirrors | Re-qualifying an audit or acceptance-sampling plan when the measurement method changes (Amazon and Apple supplier lot inspection, marketplace counterfeit sampling, cloud data-quality audit sampling after a new validator ships) |
| Decision shape | Which of N gets one scarce thing: next year's single sampling plan for raw chicken parts, run at every in-scope establishment |
| Committed call | The plan adopted (samples per 52-week window and the acceptance number) and the chance it passes an establishment at three times the standard, as a percentage to one decimal |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · measured #9's architecture (the admissible plan sits off the memo), with the population a status flag suggests (#5) at rung 2 and the lab's capacity limit (#10) carried as a risk on the way |
| Gate G mechanism | binding_constraint, with method_or_model_selection |
| Measured traps engaged | #9 picks from the offered options when none passes · #5 takes the population a flag or filter suggests · #10 notes a binding limit as a risk · #15 follows the requester's hunch over the rule |
| Calibration form | Parallel-run overlap: last quarter's split-sample run, in which every verification sample was tested by both the culture method and the new PCR method, with each half's set-up time |
| Driving force | Every option in the plan memo was drafted on culture-method rates, and each fails one condition once risks are computed at the rates next year's PCR method returns and within its lab capacity. Those rates come only from the parallel run's valid splits (both halves set up within 24 hours of collection, from the receipt log's timestamps), not from every split the status field marks as paired, a quarter of which lost culture positives in transit. The manual admits any single-stage plan in whole weekly batches of 13 samples, and exactly one, 39 samples with acceptance number 9, meets all three conditions. |

## 1. Situation

A food-safety regulator must sign off next year's Salmonella verification plan for raw chicken parts, run at its 180 in-scope
establishments. A plan takes n samples per 52-week window and flags an establishment when more than c are positive. The plan memo lists
five options: retain the current plan (52, 9), or move to (39, 7), (26, 5), (39, 10) or (52, 13). The memo's conditions are that a plan
flags an establishment exactly at the standard (10% positive on the culture method) no more than 5% of the time, passes an establishment at
three times the standard no more than 20% of the time, and fits the lab's contracted capacity. Among qualifying plans it takes the one with
the lowest chance of passing a failing establishment. From January the lab replaces culture with a PCR method, and last quarter it ran
both side by side on split samples. The deputy director has proposed cutting to 26 samples.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct and no stakeholder read is overturned. That covers the memo's risk figures (right at culture
  rates), the parallel-run results, the paired status, the receipt log, the lab contract's capacity schedules and the flagged-share history
  the deputy cites. The difficulty is that the memo was drafted for a method that ends in December, and the plan that qualifies under the
  new one is not in it.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the deputy's proposal and the flagged-share history. The memo's options, evaluated at the parallel run's rates,
  still point at (39, 10), and nothing fails a check.
* **Instrument repair.** Give the lab perfect set-up timing and a parallel run ten times larger. The valid-split rates do not move, every
  memo option still fails one condition, and the qualifying plan is still off the memo.
* **Lens swap.** The naive read ranks the memo's options at the current method's rates. The answer is a plan outside the memo, judged at
  next year's method's rates and capacity: a different candidate population at a different moment.

## 3. The driving force

A strong solver computes exact operating characteristics for the five options, applies the three conditions and keeps the current plan,
which protects best at culture rates. It then reads the lab's method notice, maps the standard through the parallel run and switches to the
PCR capacity schedule. Each step is competent, and (39, 10) is the one option that qualifies. But the manual counts a split only when both
halves were set up within 24 hours of collection, and the paired status marks every split with two results. A quarter of the paired splits
came by weekend courier, and their culture halves lost positives, which inflates the PCR-only rate from 3.5% to 6.0%. At the valid rate
(39, 10) passes 25.9% of failing establishments, and no option in the memo qualifies. The solver then takes the option that meets both risk
targets, (52, 13), and notes that it needs 9,360 samples against the lab's 7,200. The manual rules that out: when no memo option qualifies,
the plan is any single-stage plan in whole weekly batches of 13 that meets all three conditions, the current plan lapses on a method change,
and verification cannot be suspended. Exactly one plan in that family qualifies.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Exact binomial risks for the memo's options at the standard's culture rates (10% and 30%), culture-era capacity (9,360 samples) | A, retain (52, 9): passes 2.8% of failing establishments | The memo's own options, computed exactly, and the current plan protects best | The lab's method notice and the manual: risks are taken at the rates the method in use returns, and A then flags 26.0% of compliant establishments and needs 9,360 samples against PCR capacity of 7,200 |
| 1 | Standard mapped through the parallel run on every paired split (PCR-only rate 6.0%), PCR capacity | D, (39, 10): 19.0% | The new method's own rates, from the lab's own side-by-side data | The manual's validity rule: a split counts only when both halves were set up within 24 hours, and on valid splits D passes 25.9% of failing establishments |
| 2 | Valid-split rates (PCR-only 3.5%); no memo option qualifies, so take the one meeting both risk targets and carry its capacity overrun as a risk (#9, #10) | F, (52, 13): 18.2%, 9,360 samples | Every number is now right, and F is the only option that protects to target | The manual's plan-design clause: with no qualifying option, the plan is any single-stage plan in whole weekly batches of 13 meeting all three conditions; the current plan lapses; sampling cannot be suspended |
| 3 | **Decisive:** search the manual's family at valid-split rates and PCR capacity | **E, (39, 9): 15.8%, 7,020 samples** (4th of 6 on rung 0) | — | — |

* **Position table.** On rung 0's consumer risk E is 4th of the six named plans (A 2.8%, B 6.6%, C 16.3%, E 22.4%, F 26.7%, D 34.5%), and
  it fails the 20% condition there. On rung 1 it flags 6.2% of compliant establishments and fails the producer condition, so D stands
  alone. Rung 2 ranks the memo's options only, so E is not on its list. E is the sole qualifier on rung 3. Rung margins: A over B 2.37×; D
  the only qualifying option on rung 1; F over D 1.42× on rung 2; E the sole qualifier on rung 3, with the nearest family plan, (39, 10),
  at 1.64× its consumer risk.
* **Discriminator dominance.** F carries no advantage into rung 3: its consumer risk is 18.2% against E's 15.8% (E 1.15× better). On the
  condition F fails, capacity, E needs 7,020 samples where F needs 9,360 against 7,200, an edge of 1.33×. Product: 1.15 × 1.33 = 1.54,
  against a required 1.2 × 0.87 = 1.04, so the headroom is 1.48×. D, the rung-1 decoy, would need its consumer risk cut 1.30× to qualify.
* **Partial correction priced (L3).** Searching the manual's family at the all-paired rates names D, (39, 10), again: it is the family's
  only qualifier there, and E flags 6.2% of compliant establishments. Searching the family at culture rates names A, the current plan
  (2.8%, 2.0× ahead of (52, 10)). Searching it at valid rates with the culture-era capacity names (52, 11) (6.2%, 1.79× ahead of
  (52, 12)). Valid rates with PCR capacity on the memo alone names F. No half lands on E.
* **Grid.** Rates (culture, all paired, valid) × capacity (culture era, PCR) × scope (memo, manual's family) gives 12 cells. They name A, A,
  B, B (culture); F, (52, 12), D, D (all paired); F, (52, 11), none and E (valid). Only the valid-rate, PCR-capacity family cell names E.
  Its nearest wrong cells each cost one omission: the validity rule (D), the PCR capacity schedule ((52, 11)), or the plan-design clause (F).

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The memo lists five options and never says they are not the admissible set. The plan-design clause sits in the
   manual's chapter on plan construction, and no document says the memo's options lapse with the method.
2. **No sweepable corpus nominates it.** *In every plan review on file a memo option qualified, because the lab method and its capacity
   never changed between reviews.* The review archive therefore shows only picks from memos, and the parallel run, which ran under the
   current plan, certifies rates without saying which plan qualifies.
3. **No arithmetic symptom.** Every option's risks reconcile to exact binomial sums under each reading, the capacity schedules are the
   contract's own, and the memo's figures are right at culture rates.
4. **Not a row predicate.** It needs the valid-split rates (a join of each split to two set-up times), the standard mapped through them, and
   exact risks for every plan in the family checked against three conditions.
5. **The enumeration is arithmetic.** No file lists (39, 9). It is the unique solution of three inequalities over the manual's family.
6. **No cutover date.** The method change is a dated decoy that moves rates and capacity. What decides is which plans are admissible, and
   no outcome series steps.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The parallel run: one quarter in which every verification sample was split, one half to culture and one to PCR, giving 2,340
  splits from 180 establishments in six districts, each with both results, the paired status and each half's set-up time in the lab receipt
  log.
* **What it certifies.** On valid splits a culture-positive sample is PCR-positive 98% of the time and a culture-negative one 3.5% of the
  time, which reproduces the lab's published method-comparison figure. Across every paired split the PCR-only rate is 6.0%, because a
  quarter of them had the culture half set up more than 24 hours after collection.
* **What it is blind to.** Which plan qualifies (property 2). It ran under the current plan only.
* **Twin pair.** Districts North and East are identical on every visible column: 390 paired splits each, 39 culture positives, the same
  number of establishments and the same product mix. Their PCR-only splits are 12 and 25 (2.1×). Only the 24-hour rule separates them:
  East's samples travel by weekend courier, 30% of its culture halves were set up late, and on its timely splits East's PCR-only rate is
  3.5%, like North's.
* **Every rule exercised.** North has no late splits and East has many. Eleven splits had only the PCR half set up late, which tests that
  the rule is applied to both halves and not to the culture half alone.
* **Resemblance points at the decoy.** (39, 10) is the memo option nearest the qualifying plan, the one the all-paired reading certifies,
  and the one a solver who finds no qualifier will try to rescue.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The plan memo: the three conditions and the lowest-consumer-risk rule. The sampling manual: risks are taken at the rates the
  method in use returns for establishments at the standard and at three times it. The lab contract: 9,360 culture samples or 7,200 PCR
  samples a year. One sentence each.
* **Empirical pins.** The valid-split PCR-only rate, from the parallel run.
* **Voices.** The deputy director: "When we relaxed the plan last time the flagged share barely moved; 26 samples will do." The lab manager:
  "The new method is more sensitive, so it can only help us." The industry liaison: "Keep the plan everyone knows."
* **Licensed wrong basis.** The memo records that the agency's advisory committee reviews plans on the share of establishments flagged in
  the last two windows and will see that basis.

## 8. Determinism by construction

* **Risks.** The manual requires exact binomial sums, so no approximation is a fork.
* **Set-up times.** No set-up falls between 22 and 26 hours after collection, so "within 24 hours" has one reading.
* **Mapping.** The standard's rates are 10% and 30% on culture. The valid-split mapping gives 12.95% and 31.85% on PCR, and every plan's
  pass or fail is at least 0.4 points from its threshold.
* **Population and capacity.** The establishment register is frozen for the plan year at 180, and the contract's PCR schedule is 7,200.
* **Rounding.** The consumer risk is filed to one decimal (15.8%), and no other plan qualifies under any rounding.

## 9. Prompt sketch and deliverables

> I sign off next year's Salmonella verification plan for raw chicken parts next week. My deputy wants to cut to 26 samples, because the
> flagged share barely moved the last time we relaxed the plan. Tell me which plan we run next year and the chance it passes an
> establishment at three times the standard, as a percentage to one decimal, in a line I can put in the decision notice. Send
> `plan_decision.xlsx`, a chart `oc_curves.png`, and a one-page `decision_notice.pdf`.

* `plan_decision.xlsx` — every memo option and the adopted plan under each rate basis, the turnaround sheet (ask A), the serotype sheet
  (ask B) and the validity sheet (ask C).
* `oc_curves.png` — the probability of flagging against an establishment's culture-basis positive rate for the five memo options and the
  adopted plan at valid-split PCR rates, with the standard and three times it as reference lines and the two risk limits as shaded bands,
  plus a side panel of annual samples against the PCR capacity line.
* `decision_notice.pdf` — the committed plan, its consumer risk, and why no memo option is it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each district, last year's median days from collection to final result. *Device:* a result
  re-issued after a confirmation test carries a new result date under the original sample ID, as the results dictionary documents. Taking
  the first result date understates turnaround for every confirmed positive.
* **Ask B (device-carried).** For each quarter, the share of positive samples with a serotype result. *Device:* a sample with two isolates
  has two serotype rows. Counting rows instead of samples inflates two quarters by 6–9 points.
* **Ask C (validity).** Each memo option's producer and consumer risks under the culture, all-paired and valid-split rates, and the family
  plans that qualify at valid-split rates under each capacity schedule.
* **Decoupling.** Clearing the validity rule and the family search changes no figure in asks A or B. Result dates and isolates never enter a
  split or a plan.

## 11. Rubric arithmetic

5 options × 3 rate bases × 2 risks (ask C) + 2 capacity checks + 6 districts (ask A) + 4 quarters (ask B) + the committed plan, its consumer
risk, its producer risk and its annual samples + 5 named chart parts + 3 files ≈ 54 criteria.

## 12. World-building constraints

* Standard 10% and failing level 30% on culture. Valid splits: PCR-positive 98% of culture positives and 3.5% of culture negatives; every
  paired split: 6.0%. A quarter of paired splits had the culture half set up after 24 hours.
* Risks (flags at the standard / passes at three times it), culture rates: A 3.2 / 2.8, B 3.7 / 6.6, C 4.0 / 16.3, D 0.1 / 34.5,
  E 0.4 / 22.4, F 0.0 / 26.7. All-paired: A 26.0 / 0.7, B 23.3 / 2.5, C 19.3 / 8.6, D 2.7 / 19.0, E 6.2 / 10.9, F 2.1 / 12.0. Valid:
  A 12.9 / 1.4, B 12.4 / 4.1, C 11.1 / 11.8, D 0.9 / 25.9, E 2.4 / 15.8, F 0.5 / 18.2.
* 180 establishments; capacity 9,360 (culture) and 7,200 (PCR). (39, 9) is the only plan in the family meeting all three conditions at
  valid-split rates and PCR capacity.
* The twin districts are identical on every visible column. Re-issued results and serotype rows never touch splits, set-up times or plans.

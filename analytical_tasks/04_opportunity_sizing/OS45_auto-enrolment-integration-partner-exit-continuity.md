# OS45 — Which payroll partner gets the auto-enrolment integration, when a closing partner's clients are about to arrive at another

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Economics · retirement plans and workplace benefits |
| Mirrors | Integration and partnership bets sized on today's partner books when a closing partner's customers will continue on a successor (marketplace and app-store integrations chosen while a rival platform sunsets, payments partners picked before an acquirer absorbs a closing processor's merchants, cloud marketplace listings sized without the migrating customers of a retired product) |
| Decision shape | Which of N gets one scarce thing, with the sizing graded: this year's one integration build goes to one of six payroll partners |
| Committed call | The partner whose integration gets one-click auto-enrolment, and the new plan participants it adds in the first year, to the nearest 100 |
| Gap · Pattern | Gap 1 (time) over Gap 2 (population) · E24 (continuity across a closure: PayLine's payroll service ends on 31 December, and the remittance records of an earlier exit show such clients resuming within 45 days on the one integrated payroll their accounting platform still offers), with E16 below it (the outcomes report's size-band rows, finer than its total, separate the participation-gain models) |
| Gate G mechanism | forecasting, with method_or_model_selection |
| Measured traps engaged | #23 reads a closure notice as a market exit · #12 stops at the first control that passes · #15 follows the requester's hunch over the rule |
| Calibration form | Published control set with a reproduction clause: the company's published auto-enrolment outcomes report for the 2022–2023 adopters, and the campaign policy's clause that a sizing model must reproduce every figure in it |
| Driving force | PayLine's 120,000 employees in plans without auto-enrolment are off every partner's book on the closure reading. Two years ago Corvid Payroll closed the same way, and its remittances resumed within 45 days for 86% of its employees, all on Ledgerwise's feed under the same plan numbers. Both are payroll add-ons of one accounting platform, whose only remaining integrated payroll is Ledgerwise. A Ledgerwise build adds 3,291 participants from its own plans and 9,820 from PayLine's arriving plans. |

## 1. Situation

A retirement-plan recordkeeper administers small-business 401(k) plans whose contributions arrive through payroll partners' integrations.
This year its engineers can build one-click auto-enrolment into one partner's integration, and plans on that partner switch it on at the
rate earlier builds achieved. Six partners have live integrations. A seventh, PayLine, has given notice that its payroll service ends on
31 December. The campaign policy requires any sizing model to reproduce the company's published outcomes report. The head of partnerships
thinks Corvex, with the biggest employers, is where the participants are.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the plan register, the census, the outcomes report, PayLine's notice and the remittance records.
  Corvex does have the biggest employers. Nothing reported is overturned. The difficulty is where PayLine's clients will remit next year.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the partnerships head's view and every voice. The register still shows PayLine's plans on a partner that
  closes, and the band-calibrated build still names Hearthline.
* **Instrument repair.** No file is suspect. The register, the census and the outcomes report are complete and current, PayLine's plans
  are correctly PayLine's until 31 December, and the earlier exits' remittance records are complete. Where PayLine's clients remit next
  year is a forward population that no instrument records before it happens, so rungs 0, 1 and 2 still return Rotaline, Corvex and
  Hearthline, and only the continuity construction reaches Ledgerwise.
* **Lens swap.** The answer counts plans that will be on Ledgerwise's feed next year, a different population and moment from the plans on
  each partner's books today.

## 3. The driving force

A strong solver counts eligible employees from the census rather than headcount, refuses the cross-sectional gap between plans with and
without auto-enrolment, and calibrates the participation gain to the outcomes report. The report's total is reproduced by a pooled
difference-in-differences, but only gains by plan size band (34, 22 and 12 points) reproduce its band rows, and the policy requires both.
That build names Hearthline, whose clients are micro-businesses. PayLine's notice says only that its payroll service ends. Its clients'
plans do not end: they need a payroll, and their contributions will arrive on some feed. Two years ago Corvid Payroll closed. Its remittance
records stop on Corvid's feed and, for 86% of its employees, resume within 45 days on Ledgerwise's feed under the same plan numbers. Corvid
and PayLine are both payroll add-ons of the Tallybook accounting platform, and Ledgerwise is the only integrated payroll Tallybook still
lists. Maple Payroll, a standalone provider that closed in the same year, saw its clients scatter. Carried forward, PayLine's book adds 9,820
participants to a Ledgerwise build, and none to anyone else's.

## 4. The ladder

| Rung | Construction (first-year new participants: employees × participation gain × 40% plan uptake) | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Headcount in each partner's plans without auto-enrolment × the cross-sectional gap (30 points) | A, Rotaline, 24,000 (1.25× Corvex) | The book as integrated today and the gap every sales deck quotes | The plan documents and census: only employees aged 21 with a year's service are eligible, 30% of Rotaline's hospitality headcount |
| 1 | Eligible employees × 30 points | B, Corvex, 16,320 (2.00× Hearthline) | The right population for an enrolment default | The outcomes report, which the policy requires reproduced: adopters gained 24 points, and 34, 22 and 12 by size band; 30 reproduces none |
| 2 | Gains by size band (E16), the only model that reproduces the report's total and its band rows | C, Hearthline, 8,133 (1.20× Corvex) | Calibrated to every figure of the control set, on the right population | Corvid Payroll's exit: 86% of its employees' remittances resumed on Ledgerwise's feed within 45 days, under the same plan numbers |
| 3 | **Decisive:** PayLine's book carried to the successor its platform leaves, at Corvid's 86% | **E, Ledgerwise, 13,111 (1.59× Hearthline)** (5th of 6 on rung 0) | — | — |

* **The answer.** Ledgerwise. Its own plans give 3,291 new participants and PayLine's arriving plans 9,820: 13,111, committed as 13,100.
* **Position table.** Ledgerwise ranks 5th on rungs 0, 1 and 2, and leads only rung 3. It is never 2nd. Rung leaders beat their
  runners-up by 1.25×, 2.00×, 1.20× and 1.59×.
* **Discriminator dominance.** Hearthline carries a 2.47× lead into rung 3 (8,133 against 3,291). Continuity multiplies Ledgerwise's value
  by 3.98 and Hearthline's by 1.01, an edge of 3.93×, which is 1.32 times the required 1.2 × 2.47 = 2.97.
* **Partial correction priced (L3).** Every half-carried book names a wrong partner. Pooling all four past exits (Ledgerwise 27%, the rest
  spread by market share) names Hearthline, 9,731 against Corvex's 8,513 (1.14×), with Ledgerwise 4th at 6,374. Counting only clients that
  resumed within the same 30-day payroll cycle (a quarter of Corvid's continuers) names Hearthline, 8,247 against 6,800 (1.21×), with
  Ledgerwise 4th at 5,746.
* **Grid.** Population (headcount, eligible) × gain (cross-sectional, size band) × PayLine's book (closure reading, continuity) = 8 cells.
  Every non-answer cell names Rotaline, Corvex or Hearthline. The nearest is continuity without the band gains, Corvex at 16,320 against
  Ledgerwise's 14,028 (1.16×), reached by skipping the control set's band rows.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** PayLine's notice ends a payroll service. No document says where its clients go, and Tallybook's partner list is a
   web page about software, not about plans.
2. **Corpus blind for a computable reason.** *In every row of the outcomes report each plan kept its payroll partner, because no integrated
   partner closed in 2022 or 2023.* The control set reproduces rungs 0 to 2 identically with or without continuity, and it confirms the
   band-calibrated build exactly.
3. **No arithmetic symptom.** Plans, employees, contributions and the report's figures reconcile on every rung, and PayLine's plans tie to
   its feed until 31 December.
4. **Not a row predicate.** Continuity is read across a date: Corvid's plans stop on one feed and resume on another, matched by plan number,
   and then carried to a different closing partner through the platform both served.
5. **The enumeration is arithmetic.** No column says where a plan will remit next year. The 86% is computed from 2,200 plans' remittances.
6. **No cutover date.** PayLine's 31 December is the dated decoy. The decisive fact is that contributions continue across such a date.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The published outcomes report: participation before and after for the 2022–2023 adopters, in total (+24 points) and by plan
  size band (+34 under 25 eligible employees, +22 from 25 to 99, +12 at 100 or more), with the policy's reproduction clause.
* **What it certifies.** The gain model: the cross-sectional 30 points fails the total, a pooled difference-in-differences passes the
  total and fails all three band rows, and band gains pass all four figures.
* **What it is blind to.** Partner continuity (above). The remittance records of the four exits since 2024 supply it.
* **Twin pair.** Corvid and Maple Payroll, both closed in 2024, are identical on every column a lookup reaches: 2,200 plans, 58,000
  employees, size mix, plans without auto-enrolment and the wording of their closure notices. Their remittance records, closed and final,
  show 89% of Corvid's employees remitting on an integrated feed within 45 days (86% on Ledgerwise's) against 44% of Maple's, 2.0× apart.
  Only Tallybook's client list, joined to each provider, separates them.
* **Resemblance points at the decoy.** By size mix, region and plan count, PayLine's book resembles Maple's, so a solver transferring an
  exit by resemblance treats PayLine's clients as lost.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The campaign policy builds one integration a year and admits a sizing model only if it reproduces every figure in the
  outcomes report. A plan counts toward a partner if its contributions arrive on that partner's feed. Eligibility follows each plan
  document, from the census. PayLine's payroll service ends on 31 December.
* **Empirical pins.** Band gains from the outcomes report; plan uptake of 40% from the two earlier builds; continuation and successor from
  the exits' remittance records.
* **Voices.** The head of partnerships: "Corvex has the biggest employers; that's where the participants are." The chief executive:
  "PayLine's clients are gone the day it closes."
* **Licensed wrong basis.** The campaign policy records that the board's product committee compares partners on their current integrated
  headcount and will see that basis.

## 8. Determinism by construction

* **Resumption window.** Every Corvid client that resumed did so within 45 days, a quarter of them inside 30, and none between 46 and 180
  days, so any window from 45 to 180 days gives 86%.
* **Successor.** Every Corvid client that resumed on an integrated feed and ran payroll in Tallybook resumed on Ledgerwise's.
* **Size bands.** Bands use eligible employees on the census date, and no plan sits within two employees of a band edge.
* **Uptake.** Both earlier builds reached 40% of eligible plans within the first year.
* **Rounding.** 13,111 sits 39 from the nearest rounding boundary.

## 9. Prompt sketch and deliverables

> This year's integration build goes to one payroll partner, and our head of partnerships thinks Corvex, with the biggest employers, is
> where the participants are. Tell me which partner gets one-click auto-enrolment and how many new participants it adds in the first year,
> to the nearest 100, in a sentence for the product committee. Send `integration_case.xlsx`, a chart `partner_participants.png`, and a
> one-page `product_committee_note.pdf`.

* `integration_case.xlsx`: the six partners under the four rung bases, the outcomes report reproduced under each gain model, the
  deferral sheet (ask A) and the loan sheet (ask B).
* `partner_participants.png`: for each partner, first-year new participants as stacked bars (own plans, plans arriving from PayLine), the
  closure-reading value as a dot, partners sorted, the chosen partner highlighted and each partner's share of small plans printed.
* `product_committee_note.pdf`: the committed partner, its first-year participants and why Hearthline is not it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each partner, the average deferral rate of current participants in its plans without
  auto-enrolment, and the share deferring at the match cap. *Device:* a deferral change posts as a new election row with an effective
  date, and the rate in force is the latest election effective on the measurement date, per the recordkeeping guide. Averaging all rows
  overstates rates at the two partners whose clients run annual increase programmes.
* **Ask B (device-carried).** For each partner, the number of participants with an outstanding plan loan and the median balance. *Device:*
  a refinanced loan is a new loan record that names the loan it replaces, and the balance sits on the newest record, per the loan guide.
  Counting every record overstates loans by 18% at the two partners with refinance-heavy employers.
* **Ask C (validity).** Each partner's first-year participants under each of the four rung bases, and the outcomes report under the three
  gain models (total: fail, pass, pass; band rows: 0, 0 and 3 of 3).
* **Decoupling.** Clearing the continuity construction changes no figure in asks A or B.

## 11. Rubric arithmetic

6 partners × 2 (ask A) + 6 × 2 (ask B) + 6 × 4 bases + 3 reproduction results (ask C) + the committed partner, its participants and its
margin + 5 named chart parts + 3 files ≈ 62 criteria.

## 12. World-building constraints

* Partners (headcount in plans without auto-enrolment / eligible share / size mix under 25, 25–99, 100+): Rotaline 200,000 / 0.30 /
  0.50, 0.30, 0.20; Corvex 160,000 / 0.85 / 0, 0.05, 0.95; Hearthline 85,000 / 0.80 / 0.70, 0.25, 0.05; Paymill 62,000 / 0.75 / 0.40,
  0.40, 0.20; Tessera 40,000 / 0.70 / 0.30, 0.40, 0.30; Ledgerwise 45,500 / 0.80 / 0.30, 0.40, 0.30. PayLine 120,000 / 0.78 / 0.75, 0.20,
  0.05.
* Gains 34, 22 and 12 points by band (24 pooled, 30 cross-sectional); plan uptake 40%; PayLine's book continues 86% on Ledgerwise, 3% on
  other partners, 11% to manual remittance.
* Rung leaders Rotaline, Corvex, Hearthline and Ledgerwise with margins of 1.25×, 2.00×, 1.20× and 1.59×; half-carried books name
  Hearthline; all eight grid cells name as stated.
* Corvid and Maple, both closed in 2024, are identical on every lookup column; their observed 45-day continuation is 89% and 44%.
* Deferral elections and loan records never touch eligibility, the outcomes report or remittances.

# DS46 — Which drug plan a counsellor recommends to a client whose plan is leaving the market, when her pharmacy is preferred in some plans and not others

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Economics · retiree insurance choice |
| Mirrors | Choosing among plans priced through deductibles, tiers and caps, where the price a buyer actually pays depends on the channel they buy through (cloud commitments priced by region and marketplace, telecom plans with partner-store pricing, employer health plans with preferred and standard networks) |
| Decision shape | Which of N gets one scarce thing: the single plan the counselling programme recommends for next year, among five plans available in the client's county |
| Committed call | The plan recommended, and the client's expected cost for next year (premium plus out-of-pocket), in dollars to the nearest ten |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · E15, the quiet second trap (each plan prices every fill at a preferred and a standard pharmacy rate, and the client's town pharmacy is preferred in three plans and standard in two) behind the loud monthly-copay decoy, with a saturated coverage tie (E21) at rung 1 |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution |
| Measured traps engaged | #11 beats the headline trap, misses the quiet one · #19 breaks a big tie instead of questioning it · #1 reports a failed back-test, ships anyway |
| Calibration form | Settled-transaction ledger: the client's 94 settled pharmacy claims last year under her withdrawn plan, each with drug code, quantity, pharmacy, benefit phase, gross cost, plan paid and member paid |
| Driving force | Every plan publishes two prices for each fill, one at its preferred pharmacies and one at its standard ones, and plan comparisons default to the preferred price. The client fills everything at the only pharmacy in her town, which two of the five plans list as standard, and one of those two is the plan a careful phase-by-phase comparison picks. Its standard-pharmacy terms charge 45% of a $560 anticoagulant, and the year lands on the out-of-pocket cap. |

## 1. Situation

A nonprofit counselling programme helps retirees choose their drug plan at open enrolment. One client's plan is being withdrawn from the
market, so she must choose among the five plans offered in her county (A–E) for next year. Her protocol-defined cost is the year's
premiums plus what she pays at the pharmacy, with any drug a plan does not cover paid in cash outside the cap. She takes an
anticoagulant, an inhaler and six generics, and fills them all at the pharmacy in her town. The programme's advisory tool compares plans
on monthly copays.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the plan files, the formularies, the drug-code crosswalk, the pharmacy network files, the plan
  finder's coverage export and the client's ledger. No stakeholder read is overturned: the tool's copays are the plans' copays, and every
  plan does list her drugs' ingredients. The difficulty is what this client will actually pay where she fills.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the tool and every voice. A phase-by-phase year at the published preferred terms still names B on the
  coverage export and C once products are matched.
* **Instrument repair.** Suspect file: the plan finder's coverage export, which marks a drug covered when any product with its
  ingredients is listed, a narrower test than covering her product. Repaired to her exact products, rung 1 loses B and lands with rung 2
  on C at $636, and rung 0 still names A. No other file is suspect: the plan files carry both price columns correctly, the network files
  give every pharmacy's status, and the ledger is complete. Her cost under a plan she has never held is built, not repaired, so pricing
  her fills at her pharmacy's status in each plan is still needed to reach D.
* **Lens swap.** The naive read and the answer differ in rule, through a join: the preferred terms every comparison assumes, against the
  terms each plan's network file assigns to the one pharmacy she uses.

## 3. The driving force

A strong solver discards the tool's monthly-copay view, prices the client's year through each plan's benefit (deductible, initial
coverage, the $2,100 out-of-pocket cap), uses her own fills from the ledger, and checks every drug against each formulary at the level of
the exact product, which drops B: B lists her inhaler's ingredients only in another device, so its fills would be cash outside the cap.
That names C, the cheapest plan on her year at $636. Every step is right, and every step prices her fills at preferred-pharmacy terms,
because that is what the plan files lead with and what comparisons assume. But her town pharmacy is a standard pharmacy in C's
network. At standard pharmacies C charges 45% coinsurance on brand drugs instead of a $24 copay, so her anticoagulant costs $252 a fill and
the year runs to the $2,100 cap. Her ledger shows the same pattern under her withdrawn plan: every claim at the town pharmacy was priced
at that plan's standard column. D lists the town pharmacy as preferred and costs her $790.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The advisory tool: twelve months of premiums plus twelve fills of every drug at its initial-coverage copay | A, a low-premium plan with low copays ($480 against B's $564) | The programme's own tool, on the plans' published copays | The counselling protocol: the year is priced through each plan's benefit, deductible and cap included, which the tool skips (A's $615 deductible) |
| 1 | The protocol's screen and tie-break: the plan finder's coverage export shows all five plans covering her eight drugs, so the cheapest year decides, her fills priced through each plan's phases at its preferred terms | B ($520 against C's $636) | Every plan passes the official coverage check, and the year is priced through the benefit | The formulary files read through the drug-code crosswalk: B lists the inhaler's ingredients only in another device, so it covers 7 of her 8 products and her inhaler would be paid in cash |
| 2 | Product-level coverage; the client's own fills from the ledger priced through each plan's phases at the published preferred-pharmacy terms | C ($636 against D's $790) | Her real fills, the full benefit design, exact formulary matching | The ledger: all 91 claims at the town pharmacy reproduce at the withdrawn plan's standard-pharmacy column, and at its preferred column none of the 56 where the two differ |
| 3 | **Decisive:** each plan's year priced at the terms its network file assigns to the town pharmacy, joined on the pharmacy's provider number: preferred in A, B and D, standard in C and E | **D, $790** (4th of five on rung 0) | — | — |

* **Position table.** D is 4th of five on rung 0 ($842), 3rd on rung 1 ($790) and 2nd on rung 2 ($790, behind C by 1.24×, its only
  second place), and leads only rung 3. Rung margins: A over B 1.18×, B over C 1.22×, C over D 1.24×, D over A 1.32× ($790 against
  $1,041).
* **Discriminator dominance.** C carries a 1.24× cost advantage over D into rung 3 ($636 against $790). Priced at standard terms, C's year
  rises 3.47× to $2,208 while D's does not move, an edge of 3.47 against the required 1.2 × 1.24 = 1.49, past the 1.94 that headroom asks.
  D ends 2.79× cheaper than C.
* **Partial correction priced (L3).** No half-applied pricing names D. A solver who prices each plan at the town pharmacy's status but
  keeps the plan finder's ingredient-level coverage counts B's inhaler as covered and names B at $520, 1.52× under D. One who uses the
  pharmacy's status but the tool's monthly copays, skipping the phases, names A at $444, 1.78× under D, because A's deductible disappears.
  One who reads the status from the network file's chain-level entry, where the town pharmacy's buying group is listed as preferred in C,
  instead of its own row, names C at $636, 1.24× under D.
* **Grid.** Coverage (plan finder, product level) × pricing (tool copays, phases at preferred terms, phases at the status of the
  pharmacy's buying group, phases at the pharmacy's own status) = 8 cells. Ingredient-level coverage names A or B in every cell; product
  level names A under the tool, C at $636 under the preferred and buying-group terms, and D at $790 only under the pharmacy's own status.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The protocol says to price the client's year through each plan's benefit. The plan files list both columns, the
   preferred one first. No document says which column this client pays in any plan.
2. **The control pins it, and nothing else in the pack does.** The ledger's 91 claims at the town pharmacy reproduce at the withdrawn
   plan's standard column, 91 of 91, and at its preferred column 0 of the 56 claims where the columns differ; the three claims filled at a
   chain pharmacy reproduce only at preferred. The status for each candidate plan is a construction: the pharmacy's provider number joined
   to each plan's network file, whose chain-level entries disagree with the store's own row in C.
3. **No arithmetic symptom.** Every plan's year is positive and below the cap at preferred terms, and the formularies, crosswalk and
   ledger agree on every drug code.
4. **Not a row predicate.** The cost is a year-long path through deductible, initial coverage and the cap, fill by fill, at a column chosen
   by a join that differs plan by plan.
5. **The enumeration is arithmetic.** No column in any file says which price the client pays.
6. **No cutover date.** The withdrawal of her plan is the occasion for the choice, not its cause; the deciding fact is a standing network
   status, and no series steps.
7. **Survives deletion.** No wrong number exists to delete. Without the tool or any voice, the coverage export still passes B and the
   preferred-terms year still names C.

## 6. The calibration corpus

* **Form.** The client's 94 settled claims from last year under her withdrawn plan: drug code, quantity, days' supply, pharmacy provider
  number, benefit phase, gross cost, plan paid and member paid.
* **What it pins.** The pricing column: standard at the town pharmacy, preferred at the chain pharmacy near her daughter, 94 of 94. It also
  supplies her fills: twelve anticoagulant fills, ten inhaler fills (none in June or November) and twelve of each generic.
* **Twin pair.** Two of her statin fills are identical on every column but the pharmacy: same drug code, quantity, days' supply and phase,
  a month apart. She paid $5 for one and $10 for the other (2.0×): the first at the chain pharmacy, preferred in her old
  plan, the second at the town pharmacy, standard in it. Only the network join separates them.
* **Resemblance points at the decoy.** C's network file lists the town pharmacy's buying group as a preferred chain, and C's preferred
  terms are the closest of the five to her old plan's.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The counselling protocol: screen plans that cover every drug on the client's list; recommend the plan with the lowest
  expected cost for the year, premiums plus what she pays at the pharmacy, with uncovered drugs at the cash price outside the cap. The
  plan files for next year: premiums, deductibles and cost-sharing by tier at preferred and standard pharmacies; the $2,100 cap. The
  formularies by product, the drug-code crosswalk, the plans' pharmacy network files and the plan finder's coverage export.
* **Empirical pins.** The pricing column at each pharmacy, from the ledger; her fills, from the ledger.
* **Voices.** The tool's product owner: "Clients compare plans on the copay they see every month." The counselling supervisor: "The plan
  finder's coverage check is Medicare's own; we start there." The town pharmacist: "Every big plan has us in network."
* **Licensed wrong basis.** The protocol records that the client's file will carry the advisory tool's comparison sheet.

## 8. Determinism by construction

* **Fills.** The ledger's twelve months fix every fill; pricing twelve inhaler fills instead of her ten moves D to $842 and C to $684
  and leaves every ranking unchanged.
* **Network.** The town pharmacy has one row per plan network file, by provider number; the chain-level entry is a separate record type.
* **Cap.** D's year stays $1,528 under the cap; C's standard-terms year reaches it in May, so the timing of the two missed inhaler fills
  cannot move either.
* **Rounding.** D's cost is $790.40 ($218.40 of premiums and $572 at the pharmacy), clear of the nearest-ten edges.

## 9. Prompt sketch and deliverables

> One of our clients has to pick a drug plan for next year because hers is leaving the market, and five plans are offered in her county.
> Our advisory tool compares them on monthly copays. Tell me which plan we recommend and what it will cost her for the year, in dollars to
> the nearest ten, as the line for her file. Send `plan_comparison.xlsx`, a chart `annual_cost_by_plan.png`, and a one-page
> `client_letter.docx`.

* `plan_comparison.xlsx` — the five plans under the four rung constructions and the pharmacy's status in each network (ask C), the
  sessions sheet (ask A) and the volunteer sheet (ask B).
* `annual_cost_by_plan.png` — for each plan, the client's cumulative cost through the year at preferred terms and at her pharmacy's terms
  as paired lines, with the $2,100 cap drawn, the month C reaches it marked and D's year-end figure labelled.
* `client_letter.docx` — the recommended plan, its expected cost, and why the cheapest-looking plan would cost her far more.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each month of last year, the programme's counselling sessions and their median length in
  minutes. *Device:* a session resumed after a break opens a second appointment record under the same case number, as the scheduling
  guide documents. Counting records as sessions overstates sessions and roughly halves the median in the enrolment months.
* **Ask B (device-carried).** For each of the programme's 14 counties, last year's volunteer counselling hours. *Device:* a volunteer who
  covers two counties in one shift logs a single timesheet row under the first county with a split percentage, as the volunteer handbook
  sets out. Ignoring the split overstates the hub counties and understates the rural ones.
* **Ask C (validity).** For each of the five plans, the client's cost under the four rung constructions, and the town pharmacy's status in
  that plan's network file.
* **Decoupling.** Clearing the network join changes no figure in asks A or B. Appointments and timesheets touch no plan, formulary,
  network or claim record.

## 11. Rubric arithmetic

12 months × 2 (ask A) + 14 counties (ask B) + 5 plans × 4 constructions + 5 statuses (ask C) + the plan, its cost, the runner-up and the
margin + 5 named chart parts + 3 files ≈ 75 criteria.

## 12. World-building constraints

* Monthly premiums: A $4.00, B $3.00, C $9.00, D $18.20, E $22.00. Deductibles: A $615 on every tier, E $300 on brands, none elsewhere.
  Brand cost-sharing, preferred / standard: A $18 / $30, B $22 / $35, C $24 / 45%, D $26 / $33, E $30 / $40. Generics $0 preferred in
  every plan but E's tier 2 ($2), $5 to $15 standard.
* Fills: anticoagulant $560 × 12, inhaler $380 × 10, six generics × 12. Town pharmacy preferred in A, B and D, standard in C and E; C's
  chain-level entry lists its buying group as preferred. B lists the inhaler's ingredients in another device only.
* Costs: tool A 480, B 564, C 684, D 842, E 1,032; rung 1 (ingredient coverage, preferred terms, her fills) B 520, C 636, D 790, A 1,041,
  E 1,272; rung 2 C 636, D 790, A 1,041, E 1,272, B 4,100; rung 3 D 790, A 1,041, E 1,924, C 2,208, B 4,100.
* The ledger's 94 claims: 91 at the town pharmacy, 3 at the chain pharmacy. Appointments and timesheets are independent of every
  main-call record.

# OS46 — How a virtual-care company places 90,000 clinician hours, when its closed book has never seen a member deductible

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Economics · health-care services markets (virtual care) |
| Mirrors | Capacity split between a familiar channel and new ones whose counterparty keeps part of each price, sized on a closed book that never had a deduction (digital-health firms moving from employer contracts into insurer networks, apps entering carrier billing where the carrier nets a share, sellers listing on marketplaces that deduct fees the direct channel never charged) |
| Decision shape | An allocation under a cap: 90,000 clinician visit-hours next year across six payer contracts |
| Committed call | Visit-hours for each contract, and next year's net collections from them, to the nearest $100,000 |
| Gap · Pattern | Gap 2 (population) over Gap 1 (time) · E03 (the closed book of employer contracts reproduces revenue per hour exactly and is blind to member cost-sharing, because no employer contract ever had any; the insurer contracts are the first window where the deductible takes the payment), with E14 below it (clinicians may see patients only in states where they are licensed, and the licence register caps each contract's hours) |
| Gate G mechanism | binding_constraint, with forecasting |
| Measured traps engaged | #13 validates on one population, applies to another · #10 notes a binding limit as a risk · #7 uses the ready-made measure |
| Calibration form | Counterparty acknowledgement file: the employer payers' remittance acknowledgements for all 412,000 claims since 2021, each with allowed amount, payment, member responsibility and adjustment codes |
| Driving force | Every claim in the closed book was paid at the full allowed amount, because the company's employer contracts carry no member cost-sharing, so revenue per hour reproduces to the cent. Next year's three insurer contracts pay the allowed amount less the member's deductible or coinsurance, and the company has promised members it will never bill them. On Prairie's plans 85% of telehealth visits fall before the member meets the deductible, so a Prairie hour that looks like $126 earns $15. Only the insurers' accumulator files, set against each contract's visit months, say how much of the allowed amount will arrive. |

## 1. Situation

A virtual-care company provides therapy by video. Its demand spiked in 2021 and has settled since. Next year its clinicians can deliver
90,000 visit-hours. They go to three employer contracts it has run for years (Lakeshore, Front Range and Peachtree) and three insurer
contracts that start in January (Sunbelt, Prairie and Golden Coast). The company's member promise is that no member ever receives a bill. The
board wants the split and next year's collections. The chief executive points out that the insurer contracts pay more per visit than any
employer ever has.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the request series, the licence register, the fee schedules, the remittances and the accumulator
  files. The chief executive is right that the insurers' allowed amounts are the highest the company has had. Nothing reported is
  overturned. The difficulty is how much of an allowed amount reaches the company, which its closed book has never had to ask.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the chief executive's view and every voice. The closed book still certifies revenue per hour at the allowed
  amount on 412,000 claims, and the licence-capped plan still puts 26,000 hours into Prairie.
* **Instrument repair.** No file is suspect. The request series, licence register, fee schedules, remittances and accumulator files are
  complete and current, and the remittances record exactly what employers paid, which was the full allowed amount. Rungs 0, 1 and 2 still
  return $11.02M, $11.06M and $10.48M. What an insurer will pay for next year's visits is a forward quantity built from plan designs and
  members' deductible timing, which no claim yet records.
* **Lens swap.** The answer prices visits by insurer members, a different population from the employer members the book was paid for,
  under a counterparty that keeps part of each price.

## 3. The driving force

A strong solver refuses to size the 2021 spike and fits each contract's request series to its plateau. It caps each contract at the hours
its licensed clinicians can give, because a clinician may see a patient only in a state where they hold a licence. It then fills the
hours by revenue per hour, booked share times allowed amount, a figure the closed book reproduces exactly on every employer claim since
2021. That plan sends 26,000 hours to Prairie and 8,000 to Golden Coast, whose allowed amounts are the highest. An employer contract pays
the allowed amount; an insurer pays it less the member's deductible and coinsurance, and the company has promised never to bill members.
Prairie's and Golden Coast's members are mostly on high-deductible plans. Their accumulator files show the month each member met the
deductible last year, and set against the months in which telehealth visits happen, 85% of Prairie's and 75% of Golden Coast's visits fall
inside the deductible, where the insurer pays nothing. Sunbelt's members are mostly on low-deductible plans, so 10% do. Net of the member's
share, a Prairie hour earns $15.12 and a Peachtree hour $105.

## 4. The ladder

| Rung | Construction (fill 90,000 hours by revenue per hour; revenue per hour = 84% booked × payment per visit) | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Each contract's 2021 peak demand at its allowed amount | $11.02M, +42.8% (Sunbelt 53,000 hours) | The demand everyone remembers, at the prices in the contracts | The request series: demand decayed to plateaus, Sunbelt's from 70,000 hours to 25,000, while Prairie's rose to 45,000 |
| 1 | Each contract's fitted plateau at its allowed amount | $11.06M, +43.3% (Prairie 45,000) | The spike is gone and the decay is fitted, contract by contract | The licence register: licensed hours are 26,000 in Prairie's state, 18,000 in Peachtree's and 8,000 in Golden Coast's |
| 2 | Hours capped at licensed hours (E14) | $10.48M, +35.8% (Prairie 26,000) | Demand-true, legally deliverable, and priced at a revenue per hour the closed book reproduces exactly | The insurer contracts: payment is the allowed amount less the member's deductible and coinsurance, which the company's member promise never collects |
| 3 | **Decisive:** payment per visit = allowed × (1 − d − 0.2 × (1 − d)), with d each insurer contract's share of visits inside the deductible, built from its accumulator file and the visit months | **$7,717,920, committed as $7.7M** | — | — |

* **Figure shape.** The corrections walk the figure up by 0.4% and then down by 5.3% and 26.4%, and the answer is the minimum cell of the
  grid. Every rung short of it promises the board at least $2.7M too much.
* **The answer.** Peachtree 18,000 hours, Lakeshore 20,000, Front Range 15,000, Sunbelt 25,000, Golden Coast 8,000 and Prairie 4,000.
  Revenue per hour is $105.00, $99.96, $95.76, $84.67, $26.88 and $15.12.
* **Partial correction priced (L3).** Applying the insurers' pooled member share (68.5% of allowed amounts) to all three insurer contracts
  claims $6.81M (−11.8%) and sends 26,000 hours to Prairie ahead of Sunbelt. Netting coinsurance but not the deductible claims $9.09M
  (+17.8%), again with Prairie on 26,000 hours. Both stay more than 11% from the answer.
* **Grid.** Demand (peak, plateau, licence-capped plateau) × revenue basis (allowed amount, net of the member's share) = 6 cells. The
  nearest is the plateau netted but uncapped, $8.70M (+12.8%), reached by placing 30,000 hours in Georgia with licences for 18,000. Every
  allowed-amount cell is at least 35% above the answer.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The insurer contracts state a payment formula that leaves the member's share to each plan. No document says how much
   of a visit falls inside a deductible, and the member promise is a service standard, not a revenue rule.
2. **Corpus blind for a computable reason.** *In every one of the 412,000 closed claims the member's share was zero, because every contract
   the company has run is employer-paid with no member cost-sharing.* Revenue per booked hour at the allowed amount reproduces every
   employer contract's remittances to the cent, and rung 2's method passes every back-test the book allows.
3. **No arithmetic symptom.** Hours, visits, allowed amounts and remittances reconcile on every rung, and the insurer contracts have no
   claims yet to disagree with.
4. **Not a row predicate.** A visit's payment depends on where its member stands against the deductible in the visit's month, aggregated over
   each contract's members and visit months.
5. **The enumeration is arithmetic.** No column says what an insurer will pay. The three deductible shares are computed from the
   accumulator files.
6. **No cutover date.** The January start of the insurer contracts is the dated decoy. Deductibles absorb visits every year, whenever a
   contract begins.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The employer payers' remittance acknowledgements for all 412,000 claims since 2021, each with allowed amount, payment, member
  responsibility and adjustment codes, and the booking log behind them.
* **What it certifies.** Booked share (84% of released hours in every quarter) and payment at the allowed amount; with the request series,
  each contract's decay to its plateau. A solver who back-tests rungs 0 to 2 on the book is confirmed.
* **What it is blind to.** The member's share (above).
* **Twin pair.** Sunbelt employer groups 114 and 131 are identical on every column of the contract file a lookup reaches: allowed amount
  ($140), members, telehealth users and requested hours. Group 131's members are on an HSA plan, and half their visits fall inside the
  deductible, so a visit pays $112 for group 114 and $56 for group 131, 2.0× apart. Only the accumulator file separates them.
* **Resemblance points at the decoy.** Prairie resembles Lakeshore, the company's best employer contract, on demand growth, session length
  and age mix, so a solver transferring Lakeshore's revenue per hour lands on rung 2.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The member promise: no member is billed for any visit. A clinician sees patients only in states where licensed, from the
  licence register. Insurer contracts pay the allowed amount less the member's plan cost-sharing, and coinsurance is 20% in every insurer
  plan. Capacity next year is 90,000 visit-hours.
* **Empirical pins.** The booked share and the plateaus, from the book and the request series; each insurer contract's deductible share,
  from last year's accumulator files and the visit months.
* **Voices.** The chief executive: "The insurer contracts pay more per visit than any employer ever has." The head of clinical operations:
  "We can always recruit where the demand is."
* **Licensed wrong basis.** The planning policy records that the board's growth committee compares contracts on allowed amount per visit
  and will see that basis.

## 8. Determinism by construction

* **Booked share.** 84% in every closed quarter, within one point.
* **Plateaus.** Decay fits starting anywhere after the 2021 peak agree within 2% on every contract's plateau.
* **Deductible shares.** Visit months are within 3% of flat in every contract, so monthly and annual weighting give the same shares (10%,
  85% and 75%).
* **Licences.** The register is complete as of 1 October, with no application pending in any of the four states.
* **Rounding.** $7,717,920 sits $32,080 from the nearest $100,000 rounding boundary.

## 9. Prompt sketch and deliverables

> We have 90,000 clinician hours to place across our six contracts next year, and our chief executive says the insurer contracts pay more
> per visit than any employer ever has. Tell me how many hours go to each contract and what we will collect next year, to the nearest
> $100,000, in a form the board can approve. Send `capacity_plan.xlsx`, a chart `revenue_per_hour.png`, and a one-page `board_note.pdf`.

* `capacity_plan.xlsx`: the six contracts under the four rung bases, the fill, the deductible-share build, the waiting-time sheet (ask A)
  and the schedule sheet (ask B).
* `revenue_per_hour.png`: for each contract, revenue per hour at the allowed amount and net of the member's share as paired horizontal
  bars, the line where 90,000 hours run out, each bar labelled with its hours and deductible share, and licensed-hour caps marked.
* `board_note.pdf`: the committed split, next year's collections and the basis the growth committee will bring.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each contract, last year's median days from a member's first request to the first visit, and
  the share seen within seven days. *Device:* a rescheduled appointment keeps its ID and adds a slot row, and the visit date is the slot
  actually attended, per the scheduling guide. Taking the first slot understates the wait by four days at the two contracts with the most
  rescheduling.
* **Ask B (device-carried).** For each of the four states, clinicians' average weekly hours released to the schedule last year and the
  share left unbooked. *Device:* a schedule template applies until a newer template with a later effective date supersedes it, per the
  workforce guide. Summing every template double-counts hours in weeks when a template changed.
* **Ask C (validity).** Collections under each of the four rung bases, and the book's reproduction: revenue per booked hour at the allowed
  amount for each employer contract (3 of 3 to the cent).
* **Decoupling.** Clearing the deductible construction changes no figure in asks A or B.

## 11. Rubric arithmetic

6 contracts × 2 (ask A) + 4 states × 2 (ask B) + 4 bases + 3 reproductions (ask C) + 6 hour counts and the collections figure + 5 named
chart parts + 3 files ≈ 42 criteria.

## 12. World-building constraints

* Contracts (allowed per visit / deductible share of visits / plateau hours / licensed hours / 2021 peak hours): Sunbelt $140 / 0.10 /
  25,000 / 30,000 / 70,000; Prairie $150 / 0.85 / 45,000 / 26,000 / 22,000; Golden Coast $160 / 0.75 / 12,000 / 8,000 / 15,000;
  Lakeshore $119 / none / 20,000 / 30,000 / 35,000; Front Range $114 / none / 15,000 / 20,000 / 25,000; Peachtree $125 / none / 30,000 /
  18,000 / 40,000.
* Booked share 84%; coinsurance 20%; capacity 90,000 hours.
* Rung figures $11.02M / $11.06M / $10.48M / $7.72M; partials $6.81M and $9.09M; the other grid cells $9.14M and $8.70M.
* Every one of the 412,000 closed claims paid the allowed amount. Sunbelt groups 114 and 131 are identical on every contract-file column.
* Rescheduled slots and superseded templates never touch remittances, licences or accumulators.

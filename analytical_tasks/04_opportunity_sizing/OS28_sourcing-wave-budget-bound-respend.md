# OS28 — Which spend category gets the sourcing team's one wave, when cost centres that spend to their budgets buy more instead of saving

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Economics · corporate indirect procurement and cost management |
| Mirrors | Sourcing savings sized on negotiated prices when the budget holders spend whatever a lower price frees (indirect-procurement waves at large technology companies and retailers whose negotiated savings never reach the profit-and-loss account in teams that spend to budget, cloud discount programmes whose savings fixed-budget teams spend on more compute, agency rate cuts absorbed into more campaigns) |
| Decision shape | Which of N gets one scarce thing, with the sizing graded: the sourcing team's one wave next year goes to one of six spend categories |
| Committed call | The category that gets the wave, and the fall in operating spend it brings next year, to the nearest $0.1M |
| Gap · Pattern | Gap 2 (population) over Gap 3 (objective) · S2 (the decisive population is a residual between two correct records: the saving a budget-bound cost centre spends again, which is the audit's traced saving less the fall in its ledger), with E29 below it (a category's spend split by the contract each invoice runs under) |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #6 treats a mixed segment all one way · #7 uses the ready-made measure · #20 leaves the deciding comparison unstated |
| Calibration form | Gold-standard verification subsample: internal audit's savings-realisation sample from last year's pilot wave, 360 cost centres drawn at random, with every pilot-category invoice traced to contract prices and each cost centre's ledger spend for the year before and the year after |
| Driving force | A cost centre that spends its whole budget every year spends it whatever the prices. When a wave cuts what such a cost centre pays, it buys more with the money, and its ledger barely falls. That re-spend sits in no row: it is the exact gap between the audit's traced saving and the fall in the cost centre's ledger. It appears only where the cost centre's spend reached its budget in each of the last three years, a property built from the ledger against the budget file, cost centre by cost centre, and carried to each category through invoice → cost centre. Facilities spend sits in site cost centres that hold budget back; IT hardware is bought by departments that spend to the last dollar. |

## 1. Situation

The indirect-procurement team of a 26,000-employee consumer-electronics company can run one strategic-sourcing wave next year: tender one
spend category, negotiate and award new contracts. The finance committee scores a wave by the fall in actual operating spend it brings in
the plan year. Last year's pilot wave covered office supplies and courier services, and internal audit traced 360 of the 1,180 cost
centres that buy them. The chief procurement officer wants the wave in marketing services, the company's largest indirect category.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the spend cube, the contract register, the purchase orders, the audit, the ledger and the budgets.
  The negotiated reductions are real, and the CPO's read that agencies carry fat margins is right. Nothing is overturned; the difficulty
  is that the scored quantity is actual spend, and some cost centres spend their budgets whatever the prices.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the CPO's view and every voice. Channel-typed audited savings still name IT hardware, and nothing in the pack
  connects budgets to savings.
* **Instrument repair.** Suspect file: the audit's after-year trace, which follows only the pilot categories' invoices and so cannot show
  where a sampled cost centre's freed budget went. Repaired at three depths (every after-year invoice of the 360 cost centres traced; each
  one coded to the budget line that paid for it; each budget holder's own record of what the freed money bought), the re-spend becomes a
  visible row set in the pilot. Rungs 0, 1 and 2 use only the pilot-category invoices, which the repair leaves as they were, and still
  name Marketing services, Contingent labour and IT hardware. No forward category was in the pilot, so Facilities services still wins
  only through each category's bound share, built from three years of budgets against the ledger, and the answer stays at $2.70M.
* **Lens swap.** The saving a contract negotiates and the money a budget-bound cost centre spends again are different populations of
  dollars. The answer needs the second one, which is in no row.

## 3. The driving force

A strong solver sizes each category's spend, keeps only the spend whose contract ends before the wave can award, and prices it at the
audit's verified realisation by buying channel: releases against a contract land at the new price and free-text orders mostly do not.
That is the textbook savings build, verified invoice by invoice against a gold standard, and it names IT hardware. But the committee
scores actual spend, and in 151 of the 360 audited cost centres the ledger fell by only 8% of the traced saving. Those cost centres had
spent at least 99.5% of budget in each of the last three years, and the cheaper paper and couriers simply left room for more of
everything else. The re-spend shows only as the audited saving minus the ledger's fall. It occurs exactly where a cost centre's spend
meets its budget year after year, which is a cost-centre-level construction across three years of ledger and budget file. IT hardware
is bought by departments that spend to the limit; facilities spend sits in site cost centres that hold budget back.

## 4. The ladder

| Rung | Construction (next year's saving, $M) | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Category spend × the pilot's audited saving rate on all category spend (7.39%) | A, Marketing services, 4.88 (1.29× Contingent labour) | The company's own audited evidence, applied to the category everyone calls the biggest opportunity | The sourcing policy: a wave renegotiates only contracts that end before its award date, plus spend under no contract |
| 1 | Addressable spend only (a join from invoice to purchase order to contract end date) × the pilot's pooled rate on addressable spend (9.24%) | B, Contingent labour, 4.48 (1.32× IT hardware) | The policy's scope applied invoice by invoice, which is the category managers' own objection to spend-cube sizing | The audit: releases against a contract realised 0.95 of the 12% reduction and free-text orders 0.35 |
| 2 | 12% × each category's realisation by buying channel on its addressable spend | C, IT hardware, 4.06 (1.36× Facilities services) | Gold-standard realisation rates, reproduced by every sampled cost centre's invoices | The ledger fell by only 0.08 of the audited saving in 151 of the 360 sampled cost centres |
| 3 | **Decisive:** net of re-spend: × (1 − 0.92 × the category's bound share), the share of its addressable spend in cost centres that spent at least 99.5% of budget in each of the last three years | **E, Facilities services, 2.70 (1.28× Contingent labour)** (5th of 6 on rung 0) | — | — |

* **The answer.** Facilities services: a $2,703,600 fall in next year's operating spend, committed as $2.7M.
* **Position table.** Facilities services ranks 5th on rung 0, 4th on rung 1 and 2nd on rung 2 (1.36× behind IT hardware), and leads only
  rung 3. Rung leaders beat their runners-up by 1.29×, 1.32×, 1.36× and 1.28×.
* **Discriminator dominance.** IT hardware carries a 1.36× lead into rung 3. Facilities keeps 0.908 of its realised saving (bound share
  0.10) against IT hardware's 0.310 (0.75), an edge of 2.93×, which is 1.79 times the required 1.2 × 1.36 = 1.64.
* **The deciding comparison (#20).** For IT hardware, the memo must set $4.06M realised at the invoice against $2.80M spent again. For
  Facilities services it is $2.98M against $0.27M. Invoice savings alone never decide.
* **Partial correction priced (L3).** Every half-applied netting names a wrong category at least 1.30× ahead of Facilities services.
  Netting re-spend at the pilot's pooled 0.39 keeps IT hardware, $2.49M against Facilities' $1.83M (1.36×). Charging re-spend to every
  cost centre in a division that spent its full budget last year also keeps IT hardware, $2.75M against $1.06M (2.60×): the facilities
  sites sit in the Operations division, whose warehouses spend to the limit while the sites hold budget back. Netting the bound re-spend
  but skipping the channel rates names Contingent labour, $3.24M against $2.34M (1.39×). Netting it on all category spend, skipping the
  contract split, names Professional services, $4.14M against $3.18M (1.30×).
* **Grid.** Spend scope (all, addressable) × realisation (pooled, by channel) × re-spend (none, pooled, division, bound) = 16 cells. Every
  non-answer cell names Marketing services, Contingent labour, IT hardware or Professional services. The nearest is all spend by channel
  with the bound netting, which names Professional services at 1.30×.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The committee's guidance defines the scored quantity, and the sourcing policy defines what a wave can renegotiate.
   No document connects budgets to savings or says what a cost centre does with money it does not spend.
2. **Corpus pins it only as a residual.** *In every sampled cost centre's before year, its ledger spend equals the sum of its invoices
   exactly, because the ledger posts from invoices.* In the after year the audit traces only the pilot categories, so re-spend exists as
   the gap between each cost centre's audited saving and its ledger's fall, and in no row of either file. The audit alone confirms rung 2
   for all 360 cost centres.
3. **No arithmetic symptom.** Invoices, purchase orders, contracts, ledger and budgets reconcile on every rung. Audited savings tie to
   contract prices to the cent, and slack cost centres' ledger falls tie to their audited savings exactly.
4. **Not a row predicate.** Bound status needs a cost-centre-year group-by of the ledger against the budget file over three years, then a
   spend-weighted share per category through invoice → cost centre.
5. **The enumeration is arithmetic.** No column says "bound" or "re-spend". The category shares are computed over 2,140 cost centres.
6. **No cutover date.** Budgets bind year after year, re-spend starts with each cheaper invoice, and no aggregate series steps.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** 360 cost centres drawn at random from the 1,180 that bought office supplies or courier services last year. Every
  pilot-category invoice for the year before and the year after is traced to the old and new contract prices, beside each cost centre's
  ledger spend for both years.
* **What it certifies.** The 12% reduction on every renegotiated contract, and realisation by buying channel: 0.95 on releases against a
  contract and 0.35 on free-text orders, where buyers keep old suppliers and old prices. These reproduce every sampled cost centre's
  audited saving within 2%. A solver who back-tests rungs 1 and 2 is confirmed.
* **The absolute split (O2).** In the 209 cost centres that spent at most 94% of budget in each of the last three years, the ledger fell
  by exactly the audited saving. In the 151 that spent at least 99.5% in each year, it fell by 0.08 of it (0.05 to 0.11). No cost centre
  sits in between, and the 151 hold 42% of the audited saving.
* **Twin pair.** The sampled cost centres of the shared-service centres in Kraków and Manila are identical in aggregate on pilot-category
  spend ($2.0M each), headcount, release share and audited saving ($148,000 each). Their ledger spend fell by $134,400 and $66,300, 2.03×
  apart, at bound shares of 0.10 and 0.60. No invoice-level rate reproduces both.
* **Resemblance points at the decoy.** IT hardware is bought like the pilot's office supplies, through catalogue punch-outs by many
  departmental cost centres, so it is the category the pilot transfers to most naturally.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The finance committee's guidance scores a wave on the reduction in actual operating spend it brings in the plan year,
  against last year's actuals. The sourcing policy lets a wave renegotiate contracts that end before its award date and spend under no
  contract. The sourcing plan prices every renegotiated contract at a 12% reduction. The budget policy rolls every cost centre's budget
  forward at last year's level.
* **Empirical pins.** Realisation by channel and the 0.92 re-spend in bound cost centres come from the audit. Bound shares by category come
  from three years of ledger against the budget file.
* **Voices.** The CPO: "Marketing agencies carry the fattest margins we pay; that is where a wave pays." The IT category manager: "What we
  buy through the catalogue lands at the contract price, every time." That is true.
* **Licensed wrong basis.** The procurement charter records that the sourcing team reports savings to the board on the negotiated basis,
  the price reduction on last year's volumes, and the board will see that basis.

## 8. Determinism by construction

* **Bound threshold.** Every cost centre spent either at least 99.5% of budget in all three years or at most 94% in all three, so
  thresholds anywhere from 95% to 99.5%, and one-, two- or three-year definitions, return the same cost centres.
* **Contract scope.** Every contract carries an end date at a month-end, and none ends within 45 days of the wave's award date, so "ends
  before award" and "ends in the plan year" return the same invoices.
* **Channel.** Every purchase order is either a release against a contract or free-text. Card spend is under 1% of every category, and
  the policy codes it as free-text.
* **Volumes and budgets.** The guidance scores against last year's actuals and the budget policy rolls budgets at last year's level, so
  no growth or budget-capture convention arises. The budget file holds one approved budget per cost centre and year, and none was
  revised during a year.
* **Maturity.** Every sampled cost centre's after year is closed and audited, and no cost centre changed division or budget holder
  between the years.
* **Rounding.** The answer ($2,703,600) sits $46,400 from the nearest rounding boundary.

## 9. Prompt sketch and deliverables

> The sourcing team can run one category wave next year, and our CPO thinks marketing agencies are the obvious target. Tell me which
> category gets the wave and what it will save us next year, to the nearest $0.1M, in a sentence I can read to the finance committee.
> Send `sourcing_wave_case.xlsx`, a chart `category_saving_bridge.png`, and a one-page `committee_note.pdf`.

* `sourcing_wave_case.xlsx`: the six categories under the four rung bases, the supplier sheet (ask A) and the travel sheet (ask B).
* `category_saving_bridge.png`: for each category, a horizontal bridge from negotiated saving to operating-spend saving, with free-text
  leakage and re-spend as the two steps down and the final saving marked as a dot, categories sorted by final saving, the chosen
  category highlighted and its bound share printed on each bar.
* `committee_note.pdf`: the committed category, its figure and the deciding comparison.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the six categories, the number of active suppliers last year and the top-ten
  suppliers' share of the category's spend. *Device:* the vendor master holds one record per remit-to address and currency, each carrying
  its parent supplier number, as the vendor-master guide documents. Counting records as suppliers overstates the count by 34% in marketing
  services and contingent labour, where national agencies bill from regional offices, and splits their largest suppliers so the top-ten
  share falls.
* **Ask B (device-carried).** For each of the five divisions, trips booked last year and the average air fare per trip. *Device:* the
  travel agency reissues an exchanged ticket under a new number that carries the original's number and only the fare difference, as the
  agency's data guide documents. Counting ticket rows as trips overstates trips by 9% and understates the average fare by 8%.
* **Ask C (validity).** Each category's figure under each of the four rung bases. Also the audit sample's aggregate ledger fall as
  predicted by audited savings against the ledger's actual fall. Audited savings exceed the ledger fall by 63% (re-spend is 0.39 of the
  audited saving), and the bound netting reproduces every sampled cost centre within 3%.
* **Decoupling.** Clearing the re-spend construction changes no figure in asks A or B.

## 11. Rubric arithmetic

6 categories × 2 (ask A) + 5 divisions × 2 (ask B) + 6 × 4 bases + 1 reproduction figure (ask C) + the committed category, its figure, its
margin and the two deciding comparisons + 5 named chart parts + 3 files ≈ 60 criteria.

## 12. World-building constraints

* Category values: last year's spend ($M) Marketing services 66.0, Contingent labour 51.0, IT hardware 46.0, Professional services 42.0,
  Facilities services 32.8, Travel and meetings 31.0. Addressable shares 0.50 / 0.95 / 0.80 / 0.30 / 0.85 / 0.65. Contract-release
  shares of addressable spend 0.10 / 0.25 / 0.95 / 0.85 / 0.90 / 0.60. Bound shares 0.65 / 0.30 / 0.75 / 0.05 / 0.10 / 0.85. Shares in
  divisions that spent their full budget last year 0.55 / 0.40 / 0.35 / 0.40 / 0.70 / 0.80.
* Pilot: $18.0M of office supplies and courier services across 1,180 cost centres, addressable share 0.80 and release share 0.70, so
  0.12 × 0.80 × 0.77 = 7.39% and 0.12 × 0.77 = 9.24%. Of 360 sampled cost centres, 209 are slack (ledger fall equals audited saving) and
  151 are bound (ledger fall 0.08 ± 0.03 of it), holding 42% of the audited saving.
* Rung leaders are Marketing services, Contingent labour, IT hardware and Facilities services with margins of at least 1.28×, all sixteen
  grid cells name as stated, and every partial's wrong leader is at least 1.30× ahead of Facilities services.
* Kraków and Manila are identical on every invoice-, purchase-order- and audit-level column; only their budgets against three years of
  ledger differ.
* Vendor-master records and ticket exchanges never touch the spend cube, the contract register, the ledger or the budgets.

# DA17 — Which markets price annuities by pension size, when one annuitant can hold five contracts and the system stores contracts

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Demographic & Social Science · longevity and retirement-income pricing |
| Mirrors | Segmenting by customer value when one customer holds several contracts or subscriptions (Apple and Google subscribers on several individual and family plans, telecom customers priced line by line, bank and insurance customers with several products), where the per-contract view drops the best customers into the small bands |
| Decision shape | A structure the pricing committee adopts: which of the six markets the 2027 annuity basis prices by pension size, the rest keeping flat rates |
| Committed call | The list of markets that move to size-banded rates |
| Gap · Pattern | Gap 2 (population) over Gap 3 (objective) · E02 (S1), the unit the rule is written on (the annuitant) stored only in the annual tax statements, with E33 (the "in payment" status that keeps a dead annuitant alive through the guarantee period) below it and a screening overlap blind to the unit (L1) |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #2 counts file rows instead of the real unit · #18 joins only on the visible key · #5 takes the population a flag or filter suggests · #12 stops at the first control that passes |
| Calibration form | Parallel-run overlap: 2025, when the insurer's own death-notification process and each market's death-register screening service both checked every contract in force |
| Driving force | The committee's rule compares the life expectancy of annuitants by annual pension, and the policy system stores contracts. In Calbria, 1,250 well-off annuitants bought one annuity from each of three to five pension pots. Contract by contract they sit in the small and middle bands, where they live long and flatten the gradient. The policy system opens a new contract for every purchase and keeps no customer record across contracts. Only the annual tax statements, one per recipient, list which contracts belong to one person. Built that way, Calbria's gradient doubles. The screening overlap, run contract by contract, cannot tell the difference. |

## 1. Situation

A life insurer sells retirement annuities in six markets: Ostmark, Norvik, Calbria, Vellan, Sarda and Tirenne. Its rates are flat
within each market. For the 2027 basis the pricing committee will move a market to size-banded rates where the experience shows that
annuitants with large pensions live materially longer than those with small ones. The pack holds the policy system's contract file
(contract number, product, date of birth, sex, postal district, annual amount, commencement, guarantee period, status and
termination), the death-notification register, the 2025 screening results, the annual tax statements, the basis note and the
committee's rule. The committee adopts the structure on 11 March 2027.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: contracts, amounts, statuses, dates of death, the screening matches and the tax statements. The
  reinsurers' contract-size bands are right for the treaties they price, and nobody's reading of their own numbers is overturned. The
  difficulty is what one unit of the committee's rule is.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the head of pricing's view, the chief actuary's view and the reinsurers' basis. Calbria's contract-level
  experience is still flat, and every contract is still its own record.
* **Instrument repair.** Clean-data test. The suspect field is the contract status, which keeps a contract "in payment" through its
  guarantee period after the annuitant dies, a narrower record of death. Repair it by recording every death on its contract: rung 0
  then adopts Ostmark, Vellan, Sarda and Tirenne, rung 1 adopts rung 2's Ostmark, Vellan and Sarda, and rung 2 is unchanged. No other
  file is suspect: the contract file records contracts and claims no person, and the register and the tax statements are complete. The
  answer stays Ostmark, Calbria, Vellan and Sarda, and building annuitants from the statements is still needed, because a person with
  three pots really bought three annuities and only the statements say which contracts are one person's.
* **Lens swap.** The two reads count different units: 61,900 contracts against 51,710 annuitants, 4,410 of whom hold two to five
  contracts and change band once their contracts are added together.

## 3. The driving force

A strong solver takes the committee's rule at its word: period life expectancy at 65 for standard annuitants with an annual pension of
€12,000 or more against those under €2,000, by market. It drops enhanced annuities, which the rule excludes, and dates deaths from the
notification register rather than the contract status, because a contract in its guarantee period stays "in payment" after the
annuitant dies. That reproduces every death the 2025 screening matched, and it names Ostmark, Vellan and Sarda. The file holds one row
per contract and no customer record, and nothing in it says a person holds more than one. Annuitants who saved through several
employers bought one annuity per pot, and each purchase opened its own contract. In Calbria 1,250 annuitants did this. Each of their contracts pays
€1,200 to €3,500, so per contract they sit in the bottom and middle bands, raising those bands' life expectancy and leaving the top band
short of its longest-lived people. Added together they pay €12,000 to €16,000 and make up two-thirds of Calbria's top band. Only the tax
statements, one per recipient each year, say which contracts are one person's.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Every contract, deaths read from the status ("terminated – death"), bands on each contract's amount | Ostmark, Vellan, Tirenne | The book's experience on its own records, as the system holds them | The committee's rule covers standard annuitants, and enhanced annuities carry their own product code |
| 1 | Standard contracts only | Vellan | The rule's population, filtered on the authoritative product code | The overlap: status-based deaths miss 236 of the 1,412 deaths the screening matched, every one inside a guarantee period |
| 2 | Deaths dated from the notification register (E33) | Ostmark, Vellan, Sarda | Reproduces all 1,412 screening matches with their dates, and every contract is a distinct record | The tax statements: 4,410 recipients' statements each list two to five contracts |
| 3 | **Decisive:** annuitants built from the tax statements, each counted once and banded on the sum of their contracts (E02) | **Ostmark, Calbria, Vellan, Sarda** | — | — |

* **Structure shape.** Each rung adopts a different list, and only rung 3 adds Calbria. Gradients (top band minus bottom band, years)
  by rung: Ostmark 1.8 / 1.2 / 1.8 / 2.6, Norvik 1.2 / 1.1 / 1.2 / 1.2, Calbria 1.2 / 1.1 / 1.2 / 2.4, Vellan 2.0 / 1.9 / 2.2 / 2.3,
  Sarda 0.9 / 0.7 / 1.8 / 1.9, Tirenne 1.9 / 1.1 / 1.2 / 1.25, against the rule's 1.5.
* **Partial correction priced (L3).** Every half-applied construction adopts a wrong list. Grouping contracts by date of birth, sex and
  postal district merges strangers in Calbria's dense districts, holds its gradient at 1.25 and adopts rung 2's three. Linking through
  the statements but dating deaths from the status drops Sarda (Ostmark, Calbria, Vellan). Linking but leaving enhanced annuities in
  adds Tirenne (five markets). Counting each annuitant once but banding on their largest contract holds Calbria at 1.3 and adopts rung
  2's three again.
* **Grid.** Product scope (all or standard) × death source (status or register) × unit (contract or annuitant) gives 8 cells and 8
  different lists, of one to five markets. Only standard annuitants, register deaths and the statement link give the four.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The rule says "standard annuitants with an annual pension of €12,000 or more". The data dictionary says the policy
   system opens a contract for each purchase. No document says that a person can hold several contracts or
   connects the tax statements to the experience.
2. **Corpus blind to the unit.** The overlap certifies the death source exactly. *In every overlap case the unit is a contract, because
   the insurer submits each contract to the screening service as its own record and the service returns one result per record.* Run
   over the overlap, contract and annuitant constructions return the same 1,412 matches.
3. **No arithmetic symptom.** Contract numbers are unique, no contract repeats, and exposure and deaths reconcile to the contract file
   and the register under every rung. The tax statements' totals tie to annual payments.
4. **Not a row predicate.** An annuitant is a group of contracts assembled through another system's record, and its band is a sum over
   the group. No column on a contract says which group it belongs to.
5. **The enumeration is arithmetic.** 14,600 contracts collapse into 4,410 annuitants through the statements, and their bands are
   computed, not read.
6. **No cutover date.** Customers have bought one annuity per pot in every year of the window, and no series steps.
7. **Survives deletion.** No wrong number exists to delete. Without any voice, a contract still looks like a person.

## 6. The calibration corpus

* **Form.** The 2025 parallel run: the insurer's notification process and each market's death-register screening service both
  checked every contract in force. The screening matched 1,412 deaths, each with a date of death.
* **What it certifies.** The death source. Register dates reproduce all 1,412 matches. Status-based deaths miss 236, every one a contract
  in its guarantee period, so the status total is 16.7% short and no miss runs the other way.
* **What it is blind to.** The unit (above).
* **Twin pair.** Norvik and Calbria are identical on every contract-level column: 9,800 contracts each with the same distribution by
  band, age, product and guarantee, the same exposure and the same register deaths by band and age. Their contract-level gradients are
  both 1.2 years. In Calbria 1,250 annuitants hold three to five contracts each; in Norvik 140 do. Their annuitant gradients are 2.4 and
  1.2 years (2.0×). Only the statement link separates them.
* **Resemblance points at the decoy.** On every contract-level column Calbria matches Norvik, the market every rung leaves on flat rates.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The committee's rule: "A market moves to size-banded rates when the period life expectancy at 65 of standard
  annuitants with an annual pension of €12,000 or more exceeds that of standard annuitants with an annual pension under €2,000 by at
  least 1.5 years." The basis note: the investigation runs from 1 January 2021 to 31 December 2025, deaths count at the date of death,
  annual pension is measured at 1 January of each year, and the life table uses single-year central rates from 65 to 104 with a_x = 0.5
  and an open interval at 105.
* **Empirical pins.** The death source, from the overlap.
* **Voices.** The head of pricing: "Pot size tells you very little about how long someone lives." The chief actuary: "The screening
  reconciliation came back clean. I'd trust the experience file as it stands."
* **Licensed wrong basis.** The committee's rule records that the reinsurers price each contract on its own annual amount and will
  compare the structure with their bands.

## 8. Determinism by construction

* **The link.** Every contract appears on exactly one living recipient's statement in each year it pays its annuitant. No statement
  covers two people, and payments to an estate in a guarantee period appear on separate estate statements. Any year's statements give
  the same grouping.
* **Banding.** Totals are taken at 1 January. A contract bought during a year joins its annuitant's total from the next 1 January, and no
  total crosses a band boundary otherwise.
* **Products.** No annuitant holds both standard and enhanced contracts.
* **Deaths.** The register and the screening agree on every date in 2025. The screening's final 2025 run covers deaths to 31 December,
  so no 2025 death is unreported.
* **Threshold.** Every gradient in every cell of the grid and every partial sits at least 0.2 years from 1.5, and the pinned life-table
  conventions move no gradient by more than 0.05 years.

## 9. Prompt sketch and deliverables

> Which of our six markets should price annuities by pension size from 2027? The committee meets on 11 March, and our head of pricing
> doubts pot size says much about how long people live. Give me the list of markets that move to size-banded rates, as the committee
> would minute it, and send `size_banding.xlsx` with the sheets below and the chart `gradient_by_market.png`.

* `size_banding.xlsx` — life expectancy at 65 by band and market under each rung's construction with the gradients (ask C), the
  overlap reconciliation, the sales sheet (ask A) and the complaints sheet (ask B).
* `gradient_by_market.png` — for each market, top-band and bottom-band life expectancy per contract and per annuitant as paired dots,
  the 1.5-year line, the adopted markets marked, and Norvik and Calbria highlighted.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** New annuity sales by market and quarter of 2026. *Device:* a sale cancelled within the 30-day
  cooling-off period is reversed by a negative sale row dated at cancellation, as the sales ledger guide documents. Netting by the
  cancellation date moves 140 sales across quarters and changes 11 of the 24 cells.
* **Ask B (device-carried).** Complaints received and the share upheld, by market and quarter of 2026. *Device:* a complaint the customer
  takes to the ombudsman closes as "referred", and the ombudsman's decision arrives later keyed to the insurer's complaint number, as the
  complaints procedure documents. Reading "referred" as not upheld understates the uphold rate in 15 of the 24 cells.
* **Ask C (validity).** Each market's gradient under each of the four rung constructions, the overlap's reproduction counts for both
  death sources, and Norvik's and Calbria's life expectancy by band per annuitant.
* **Decoupling.** 2026 sales and complaints share no row with the 2021–2025 experience, the register or the tax statements. Clearing the
  statement link changes no figure in asks A or B.

## 11. Rubric arithmetic

6 markets × 4 quarters (ask A) + 6 markets × 4 quarters (ask B) + 6 markets × 4 constructions, 2 reproduction counts and 4 twin
figures (ask C) + 6 market decisions + 4 named chart parts + 2 files ≈ 90 criteria.

## 12. World-building constraints

* 61,900 contracts and 51,710 annuitants across the six markets; 4,410 annuitants hold two to five contracts (14,600 contracts).
  Calbria's top band holds 1,870 annuitants, 1,250 of them multi-contract.
* Gradients by rung as in section 4. Partials: Calbria 1.25 under date-of-birth grouping and 1.3 under largest-contract banding; Sarda
  0.8 when linked with status deaths; Tirenne 2.05 when linked with enhanced annuities left in. Nothing falls between 1.3 and 1.7.
* Rung lists: Ostmark, Vellan, Tirenne / Vellan / Ostmark, Vellan, Sarda / Ostmark, Calbria, Vellan, Sarda. The cell with every
  product, register deaths and contracts (rung 0 once the status is repaired) gives Ostmark 2.4, Norvik 1.3, Calbria 1.3, Vellan 2.3,
  Sarda 2.0 and Tirenne 2.0, adopting Ostmark, Vellan, Sarda and Tirenne.
* The overlap: 1,412 screening matches, 236 of them in guarantee periods and missed by status.
* Norvik and Calbria are identical on every contract-level column; their multi-contract annuitants number 140 and 1,250.
* Sales and complaints touch no contract in the experience.

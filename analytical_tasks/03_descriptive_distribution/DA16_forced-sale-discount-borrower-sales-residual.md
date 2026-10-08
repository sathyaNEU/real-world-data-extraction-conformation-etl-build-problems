# DA16 — What forced-sale discount the capital model carries for Kelbridge, when most homes sold in default were sold by their owners

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Economics · housing finance and mortgage credit risk |
| Mirrors | Measuring the loss on distressed exits when most of them never pass through the recovery desk (auto and buy-now-pay-later lenders whose borrower-arranged sales bypass the auction ledger, Amazon-style liquidation pricing where most excess stock leaves through sellers' own channels, device trade-in recovery values) |
| Decision shape | A figure: the forced-sale discount the capital model carries for Kelbridge from the recalibration filed on 30 April 2027 |
| Committed call | Kelbridge's forced-sale discount, as a percentage to one decimal |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · E09 (S2), a residual population (default episodes closed as repaid because the borrower sold the home) recovered between the default history and the land registry, with E14 (the valuation cap applied in every indexed value) below it and a recoveries ledger blind to borrowers' sales (L1) |
| Gate G mechanism | method_or_model_selection, with binding_constraint |
| Measured traps engaged | #5 takes the population a flag or filter suggests · #12 stops at the first control that passes · #10 notes a binding limit as a risk · #7 uses the ready-made measure |
| Calibration form | Existing-book actuals: the society's recoveries ledger, 412 possession sales in 2022–2026, each with sale price, carrying value of the collateral, balance and realised loss |
| Driving force | The discount is measured over defaults resolved by a sale of the collateral. The only lender file that pairs a defaulted loan with a sale price is the recoveries ledger, which holds the 412 homes the society repossessed and sold, and it reproduces the valuation policy to the pound. But 503 borrowers in default sold their homes themselves, and each sale repaid the loan in full, so the default history closes the episode as repaid and the ledger never sees it. Those sales exist only as the residual between the default history and the registry's transfers of the collateral titles. They sold 11.6% below indexed value, against 29.4% for possessions, and they are the majority of the sales the parameter is about. |

## 1. Situation

A regional building society recalibrates its internal-ratings capital model each spring. The forced-sale discount, set city by city,
converts the indexed value of a defaulted loan's collateral into the sale proceeds the loss model expects. For Kelbridge the pack holds the
loan book (with each collateral's registry title number and closure code), the monthly arrears history and the default-episode table,
the valuation register (surveyed and desktop valuations), the land registry's price-paid file for the city with title numbers, the
registry's monthly district series (median price and repeat-sales index), the recoveries ledger, the model documentation and the
valuation policy. The recalibration goes to the supervisor on 30 April 2027.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: sale prices, valuations, both registry series, the registry's transfers, the arrears history,
  the default episodes and the ledger's carrying values and losses. The supervisor's peer benchmark is correct on its own basis, and
  nobody's reading of their own numbers is overturned. The difficulty is which sales the parameter is measured over.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the head of credit risk's view, the validator's view and the benchmark. The recoveries ledger is still the
  only lender file that pairs a defaulted loan with a sale price, and the default table still labels exactly 412 episodes as ending in a
  sale.
* **Instrument repair.** Perfect the ledger and it still records only the society's own sales, because a borrower's sale posts no loss.
  Perfect the default table and the 503 episodes still close as repaid, because they were repaid. The sale itself is recorded by another
  system, the registry, to which the society is not a party.
* **Lens swap.** The two reads cover different populations: 412 possession sales against the 915 defaults resolved by a sale of the
  collateral (412 possessions and 503 borrowers' sales).

## 3. The driving force

A strong solver reads the model documentation: the discount is the mean shortfall of the sale price below indexed value, over the
defaults resolved by a sale of the collateral. The default table answers the question for it, with 412 episodes ending in "possession
sale". It indexes each one's surveyed valuation by the registry's repeat-sales index, applies the valuation policy's cap, and matches all
412 carrying values in the recoveries ledger. That is a complete, back-tested 29.4%, and it fits the belief that forced sales take the
worst of a falling market. But 600 episodes end "closed": the account closed with the balance repaid. A borrower three months behind does
not usually repay from savings. For 503 of them the registry shows a transfer of the collateral's title in the five days before the
account closed. The borrower sold, the solicitor redeemed the loan on completion, and the price never entered any of the society's
files. Borrowers' sales are marketed normally and need no possession, so they sell far closer to value. They are the larger half of the
defaults the definition covers, and only the title join to the registry finds and prices them.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Possession sales against surveyed valuations indexed by the registry's district median price | 38.6% (+96.9%) | The median is the city's headline house-price series, published monthly by the registry | The valuation policy indexes collateral by the registry's repeat-sales index for its district |
| 1 | Possession sales against repeat-sales-indexed valuations | 33.0% (+68.4%) | The policy's index, applied as written | The valuation policy caps every indexed value at the latest surveyed valuation, which binds for 141 of the 412 sales |
| 2 | The cap applied (E14) | 29.4% (+50.0%) | Reproduces all 412 carrying values in the recoveries ledger to the pound, and the ledger is the society's record of forced sales | The registry: 503 of the 600 episodes the default table closes as repaid end with a transfer of the collateral's title in the five days before closure |
| 3 | **Decisive:** possession sales and borrowers' sales together, each indexed and capped, borrowers' sales priced from the registry (E09) | **19.6%** | — | — |

* **Figure shape.** Every correction lowers the figure, and the answer is the minimum cell of the grid. A recalibration filed at any lower
  rung overstates the discount by half or more, and the capital it holds is held against losses the book does not make.
* **Partial correction priced (L3).** A solver who adds the borrowers' sales but indexes them uncapped lands at 23.5% (+19.8%). One who
  adds them on the median index lands at 23.8% (+21.6%). One who suspects other exits but carries the ledger's discount over to them,
  because they resemble the possessions on every lender column, files 29.4% again (+50.0%). One who prices them at the redemption amount,
  the only figure in the society's files, lands at 34.1% (+74.1%). One who builds the population from the loan book's ever-defaulted flag
  adds 702 cured loans later sold at market and lands at 11.7% (−40.3%). No half-applied construction comes within 19% of the answer.
* **Grid.** Index (median or repeat-sales) × cap (off or on) × population (possessions, or possessions and borrowers' sales) gives 8
  cells, from 19.6% to 38.6%. The nearest wrong cell is 23.5% (+19.8%), and every cell without the borrowers' sales sits at least 50%
  above the answer.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The model documentation defines the discount over defaults resolved by a sale of the collateral. The data
   dictionary defines "closed" as an account closed with its balance repaid. No document says how a defaulted balance gets repaid, and
   none links a default episode to the registry.
2. **Corpus blind to the population.** The ledger certifies the valuation basis exactly. *In every closed case in the recoveries ledger
   the seller is the society, because a borrower's sale in default repays the balance in full and posts nothing to the loss ledger.* Run
   over the ledger, every population rule returns the same 412 cases and the same 29.4%.
3. **No arithmetic symptom.** The default table reconciles: 2,940 episodes are 1,630 cured, 412 possession sales, 600 closed and 298
   open. The ledger ties to the general ledger's loss account, and every carrying value ties to the impairment system.
4. **Not a row predicate.** A borrower's sale is three records in three systems: an episode closed as repaid, the account's closure
   date, and a registry transfer of the collateral's title days before it. No row in any file carries it.
5. **The enumeration is arithmetic.** 503 sales are recovered by the title join and priced from the registry. No field counts them.
6. **No cutover date.** Borrowers in default sell in every month of the window, and no series steps.
7. **Survives deletion.** No wrong number exists to delete. Without any voice, the default table still names 412 sales.

## 6. The calibration corpus

* **Form.** The recoveries ledger, 2022–2026: 412 possession sales, each with completion date, sale price, the collateral's carrying
  value at sale, balance, costs and realised loss.
* **What it certifies.** The valuation basis. Capped repeat-sales indexing reproduces all 412 carrying values. Uncapped indexing
  reproduces the 271 where the cap does not bind and overstates the other 141, putting the ledger total 5.4% high. Median indexing
  reproduces none and is 15.0% high in total. The misses run one way, so no rival reconciles in aggregate.
* **What it is blind to.** Borrowers' sales (above): zero in every case.
* **Twin pair.** Districts 4 and 11 are identical on every column of the ledger, the loan book and the default table: 38 possession sales
  each at 30.1% below capped indexed value, the same loan counts, balances and LTV bands, and 93 episodes each closed as repaid. In
  District 4, 91 of the 93 closures follow a registry transfer of the title; in District 11, 2 do, and 91 were refinanced by the city's
  rescue-loan fund, with no transfer. Their discounts are 14.5% and 29.1% (2.0×). Rules without the borrowers' sales give both 30.1%.
* **Resemblance points at the decoy.** On every lender-visible column (LTV at default, arrears depth, property type), the borrowers who
  sold resemble the possession cases in their districts, so the ledger's discount looks transferable to them.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The model documentation: "The forced-sale discount is the mean shortfall of the sale price below the collateral's
  indexed value at the sale date, over the defaults resolved by a sale of the collateral completed in the observation window, 1 January
  2022 to 31 December 2026." The valuation policy: "Collateral is indexed from its latest surveyed valuation by the registry's
  repeat-sales index for its district, and its indexed value never exceeds that valuation." The default definition: three or more
  monthly payments in arrears at a month-end, until the loan cures, is sold in possession or its account closes.
* **Empirical pins.** The valuation basis, reproduced on the ledger.
* **Voices.** The head of credit risk: "Prices fell hard last year, and forced sales always take the worst of a falling market." The
  model validator: "The recoveries ledger is the one clean record we have of forced sales."
* **Licensed wrong basis.** The model documentation records that the supervisor will compare the parameter with its peer benchmark,
  built from eleven lenders' recoveries ledgers.

## 8. Determinism by construction

* **Matching window.** Every borrower's sale completes within five days before its account closes, and no collateral title transfers
  again within twelve months, so any window from five days to a year finds the same 503 sales.
* **Sale date and index month.** Each sale is indexed to its completion month. Indexing a borrower's sale to its closure month instead
  changes the month for 31 of 503 and moves the figure by under 0.05 points.
* **Valuation base.** Desktop valuations never reset the base, per the policy, and every sale has a surveyed valuation on the register.
* **Mean and costs.** The documentation's mean is unweighted, and sale costs are a separate parameter in the loss model.
* **Censoring.** The 298 episodes open at 31 December 2026 have no sale in the window. Possessions taken but not sold by then are not
  sales.
* **Price floor.** Every borrower's sale price covers the balance it redeemed, so no sale carries a shortfall that could have reached the
  ledger.

## 9. Prompt sketch and deliverables

> We file the capital-model recalibration with the supervisor on 30 April, and I need Kelbridge's forced-sale discount for it. Our head of
> credit risk thinks forced sales always take the worst of a falling market. Give me the discount as a percentage to one decimal, in a
> sentence I can drop into the recalibration note, and send `fsd_build.xlsx` with the sheets below and the chart `exit_discounts.png`.

* `fsd_build.xlsx` — the sales the figure rests on with their indexed values and discounts, the discount under each rung's construction
  with the ledger's reproduction counts (ask C), the claims sheet (ask A) and the applications sheet (ask B).
* `exit_discounts.png` — histograms of the discount for possession sales and borrowers' sales on the capped repeat-sales basis, the four
  rung figures as markers on a shared axis, the committed figure as a line, and Districts 4 and 11 annotated.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** Buildings-insurance claims on mortgaged homes by peril (flood, storm, subsidence, escape of
  water) and year, 2022–2026, for the recalibration's physical-risk annex. *Device:* the claims file keeps the peril as notified, and the
  loss adjuster's reclassification is a row in the claim-history table, effective from the adjuster's report, as the claims handbook
  documents. Counting by notified peril misplaces 212 of 3,960 claims and moves 13 of the 20 cells by 3% to 19%.
* **Ask B (device-carried).** New mortgage applications by channel (broker, branch, online) and month in 2026, for the capital plan's
  volume line. *Device:* an application declined and resubmitted with amended details keeps its case number and takes a new application
  number, as the origination guide documents. Counting application numbers overstates 29 of the 36 cells by 4% to 12%.
* **Ask C (validity).** The discount under each of the four rung constructions, the number of borrowers' sales, the ledger's
  reproduction count under each of the three valuation bases, and the discounts of Districts 4 and 11.
* **Decoupling.** Insurance claims and applications share no row with the default table, the ledger or the registry's transfers.
  Clearing the borrowers' sales changes no figure in asks A or B.

## 11. Rubric arithmetic

4 perils × 5 years (ask A) + 3 channels × 12 months (ask B) + 4 rung figures, the sale count, 3 reproduction counts and 2 district
discounts (ask C) + the committed discount, the number of sales it rests on and the nearest wrong figure + 4 named chart parts + 2 files
≈ 75 criteria.

## 12. World-building constraints

* 412 possession sales and 503 borrowers' sales complete in 2022–2026. Mean discounts (median uncapped / repeat uncapped / median capped
  / repeat capped): possessions 38.6 / 33.0 / 34.0 / 29.4; borrowers' sales 20.0 / 15.7 / 15.5 / 11.6. The answer is 19.6%.
* Grid cells with both populations: 28.4 / 23.5 / 23.8 / 19.6. Redemption-amount pricing gives 34.1; the ever-defaulted flag (adding 702
  cured loans later sold at a mean 1.4%) gives 11.7.
* Default table: 2,940 episodes = 1,630 cured + 412 possession sales + 600 closed (503 with a title transfer in the five days before
  closure, 97 refinanced with none) + 298 open.
* The cap binds for 141 of 412 possession sales and 224 of 503 borrowers' sales. Every borrower's sale price covers its balance.
* Districts 4 and 11 are identical on every lender column. District 4: 91 borrowers' sales at a mean 8.0%; District 11: 2 at 10.4%.
  Their discounts are 14.5% and 29.1%.
* Insurance claims and applications touch no loan in the default table.

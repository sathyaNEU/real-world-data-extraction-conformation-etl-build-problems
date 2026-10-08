# DA16 — What forced-sale discount the impairment model carries for Kelbridge, when the loans now in default will not sell the way the last five years' did

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Economics · housing finance and mortgage credit risk |
| Mirrors | Pricing the recovery on today's distressed book from the exits of past ones, when which exit a case takes depends on its current equity (auto and buy-now-pay-later lenders whose borrower-arranged sales bypass the auction ledger, marketplace liquidation of excess stock where the sale channel depends on what the stock is still worth, device trade-in recovery values) |
| Decision shape | A figure: the forced-sale discount the impairment model carries for Kelbridge from the recalibration filed with the year-end accounts on 30 April 2027 |
| Committed call | Kelbridge's forced-sale discount, as a percentage to one decimal |
| Gap · Pattern | Gap 1 (time) over Gap 2 (population) · E09, the residual population of borrowers' own sales (recovered between the default table and the land registry) projected onto the loans in default at the reporting date by the equity split that decides which sale each will end in, with E14 (the valuation cap applied in every indexed value) below it and a recoveries ledger blind to borrowers' sales (L1) |
| Gate G mechanism | forecasting, with method_or_model_selection |
| Measured traps engaged | #13 validates on one population, applies to another · #5 takes the population a flag or filter suggests · #10 notes a binding limit as a risk · #12 stops at the first control that passes |
| Calibration form | Existing-book actuals: the society's recoveries ledger, 412 possession sales in 2022–2026, each with sale price, carrying value of the collateral, balance and realised loss |
| Driving force | The model applies the discount to the loans in default at the reporting date, each at the discount of the sale it will end in. In the 2022–2026 window, which sale a default ended in was set by its equity: every default with 15% equity or more was sold by the borrower, with the society's consent, about 12% below indexed value; every one below was repossessed and sold about 29% below. The window's mix came from the 2023–24 trough, when 45% of sales were possessions. After the 2025–26 recovery only 22% of the loans now in default sit under 15% equity, so the sales ahead are mostly borrowers' own. The window's average, borrowers' sales included, is correct and describes a different book. |

## 1. Situation

A regional building society recalibrates its expected-credit-loss model for the year-end accounts. The forced-sale discount, set city by
city, converts the indexed value of a defaulted loan's collateral into the sale proceeds the loss model expects. For Kelbridge the pack
holds the loan book (with each collateral's registry title number and closure code), the monthly arrears history and the default-episode
table, the valuation register, the land registry's price-paid file with title numbers, the registry's district series, the recoveries
ledger, the model documentation and the valuation policy. The recalibration is filed with the accounts on 30 April 2027.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: sale prices, valuations, both registry series, the registry's transfers, the arrears history,
  the default table and the ledger. The window's average discount is a true statement about the window's sales, and nobody's reading of
  their own numbers is overturned. The difficulty is which sales the model is pricing.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the head of credit risk's view, the validator's view and the supervisor's basis. The window's sales still
  give a complete, back-tested average, and the society's files still record only its own sales.
* **Instrument repair.** Clean-data test. The suspect files are the default table, whose end state records a sale only when the society
  sold, and the recoveries ledger, which holds only those sales. Repair them at every depth (record every sale of defaulted collateral
  with its price): rung 2 becomes a direct read of 19.6%, rungs 0 and 1 stay at 38.6% and 29.4%, and the answer stays 15.5%, because
  projecting each open default onto the sale its equity sets is still needed. No other file is suspect: the loan book, the valuation
  register and the registry are complete.
* **Lens swap.** The two reads price different populations: the 915 sales of 2022–2026, 45% of them possessions, against the 298 loans in
  default on 31 December 2026, 22% of which are expected to end in possession.

## 3. The driving force

A strong solver reads the model documentation and builds the discount from the observation window. It indexes each surveyed valuation by
the registry's repeat-sales index, applies the valuation policy's cap and matches all 412 carrying values in the recoveries ledger. It
then sees that 503 defaults closed as repaid end with a registry transfer of the collateral days before closure: borrowers who sold with
the society's consent. Priced from the registry, the window's 915 sales give 19.6%, a complete figure. But the model prices the loans in
default now, each at the discount of the sale it will end in, and in the window the path was never random. The society consents to a
borrower's sale only when the price will clear the loan, and every default with 15% equity or more ended in one, while every default
below ended in possession. The window's sales came largely from the 2023–24 trough. After the 2025–26 recovery, 232 of the 298 loans in
default hold 15% equity or more.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Window possession sales against surveyed valuations indexed by the registry's district median price | 38.6% (+149.0%) | The median is the city's headline house-price series | The valuation policy indexes collateral by the repeat-sales index and caps every indexed value at the latest surveyed valuation |
| 1 | Possession sales on the policy's capped repeat-sales values (E14) | 29.4% (+89.7%) | Reproduces all 412 carrying values in the recoveries ledger to the pound | The registry: 503 defaults the table closes as repaid end with a transfer of the collateral's title in the five days before closure |
| 2 | Every sale of defaulted collateral in the window, borrowers' sales priced from the registry (E09's residual) | 19.6% (+26.5%) | Every sale in the observation window counted | The year-end default stock: 78% of the loans in default on 31 December hold 15% equity or more, against 55% of the window's sales |
| 3 | **Decisive:** each loan in default at the reporting date at the discount of the sale its equity sets (borrower sale at 15% or more, possession below), path discounts from the window | **15.5%** | — | — |

* **Figure shape.** Every correction lowers the figure, and the answer is the minimum cell of the grid. A provision filed at rung 2
  prices the year-end stock as if it were in the 2023–24 trough.
* **Partial correction priced (L3).** A solver who projects the open defaults but splits at zero equity, reading the consent rule as
  "price covers the debt" without the window's evidence, sends 268 of them to borrower sales and lands at 13.4% (−13.5%). One who
  projects on uncapped repeat-sales values lands at 19.5% (+25.8%), and one who applies the window's average to the open defaults is back
  at 19.6%.
* **Grid.** Valuation (median uncapped, repeat-sales uncapped, median capped, the policy's capped repeat-sales) × population (window
  possessions, every window sale, the year-end stock's projected sales) gives 12 cells, from 15.5% to 38.6%. The nearest wrong cell is
  13.4% (−13.5%), and every other is at least 25% away.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The model documentation says the discount is expected on the sales that will resolve the loans in default at the
   reporting date. The collections manual's consent clause says consent is given when the agreed price redeems the loan. No document
   says that equity at default decided every past path, or where the line sits.
2. **Corpus blind to borrowers' sales.** The ledger certifies the valuation basis exactly. *In every closed case in the recoveries ledger
   the seller is the society, because a borrower's sale repays the balance in full and posts nothing to the loss ledger.* Run over the
   ledger, every population rule returns the same 412 cases.
3. **No arithmetic symptom.** The default table reconciles (2,940 episodes: 1,630 cured, 412 possession sales, 600 closed, 298 open), the
   ledger ties to the general ledger, and the window average is computed cleanly on every sale.
4. **Not a row predicate.** Each open default's path is read from its current equity against a line the window's complete sales draw,
   and its discount is that path's window average.
5. **The enumeration is arithmetic.** 298 loans are classified on capped repeat-sales equity at year end; 66 fall under 15%.
6. **No cutover date.** The consent rule and the equity line held in every year of the window, and no series steps.
7. **Survives deletion.** No wrong number exists to delete. Without any voice, the window average is still the obvious estimate.

## 6. The calibration corpus

* **Form.** The recoveries ledger, 2022–2026: 412 possession sales, each with completion date, sale price, the collateral's carrying
  value at sale, balance, costs and realised loss.
* **What it certifies.** The valuation basis: capped repeat-sales indexing reproduces all 412 carrying values, uncapped indexing 271
  (the ledger total 5.4% high) and median indexing none (15.0% high).
* **What it is blind to.** Borrowers' sales (above), and so the path split: the split is drawn by the window's 915 sales once the
  registry has added the 503 borrowers' sales. Every one of those had 15% equity or more at default and every possession less, with no
  default between 12% and 18%.
* **Twin pair.** Districts 4 and 9 each hold 31 loans in default at year end and are identical on their window history (sale mix,
  discounts and an average of 19.6%), on arrears depth and on property types. District 4's open defaults kept their equity, 28 of 31 at
  15% or more; District 9's are newer loans bought near the peak, 7 of 31. Their projected discounts are 13.3% and 25.4% (1.9×), and every
  window-based rule gives both 19.6%.
* **Resemblance points at the decoy.** By arrears depth, LTV at origination and property type, the year-end stock most resembles the
  window's defaults, whose average is 19.6%.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The model documentation: "The forced-sale discount is the mean shortfall of the sale price below indexed value expected
  on the sales that will resolve the loans in default at the reporting date. Each loan takes the discount of the sale it is expected to
  end in, as the observation window, 1 January 2022 to 31 December 2026, shows." The valuation policy fixes the repeat-sales index and the
  cap at the latest surveyed valuation. The collections manual gives the consent clause.
* **Empirical pins.** The equity line and the path discounts (11.6% and 29.4%), from the window's complete sales.
* **Voices.** The head of credit risk: "Prices fell hard in 2023, and forced sales always take the worst of a falling market." The model
  validator: "The window is our evidence. Average it and you're done."
* **Licensed wrong basis.** The model documentation records that the auditors benchmark the parameter against peer lenders' five-year
  average discounts.

## 8. Determinism by construction

* **Equity.** Equity is one less the balance over the capped repeat-sales indexed value: at default for window cases, at 31 December
  2026 for the open stock. No window case and no open default falls between 12% and 18%, so any line in that range classifies the same.
* **Cures.** The model prices the sale each open default would end in; the cure probability is a separate parameter, so cures do not
  enter the discount.
* **Mean.** The documentation's mean is over loans, unweighted. A balance-weighted mean is a hazard it refutes.
* **Matching.** Every borrower's sale completes within five days before its account closes, and no title transfers again within twelve
  months, so any matching window from five days to a year finds the same 503.

## 9. Prompt sketch and deliverables

> We file the impairment model's recalibration with the accounts on 30 April, and I need Kelbridge's forced-sale discount for it. Our head
> of credit risk thinks forced sales always take the worst of a falling market. Give me the discount as a percentage to one decimal, in a
> sentence I can drop into the recalibration note, and send `fsd_build.xlsx` with the sheets below and the chart `exit_paths.png`.

* `fsd_build.xlsx` — the window's sales with their indexed values, paths and discounts, the year-end stock with its equity and expected
  path, the discount under each rung's construction with the ledger's reproduction counts (ask C), the claims sheet (ask A) and the
  applications sheet (ask B).
* `exit_paths.png` — the window's sales plotted by equity at default and discount, coloured by path, with the 15% line; the year-end
  stock's equity distribution beneath; the four rung figures as markers; and Districts 4 and 9 annotated.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** Buildings-insurance claims on mortgaged homes by peril (flood, storm, subsidence, escape of
  water) and year, 2022–2026, for the recalibration's physical-risk annex. *Device:* the claims file keeps the peril as notified, and the
  loss adjuster's reclassification is a row in the claim-history table, effective from the adjuster's report, as the claims handbook
  documents. Counting by notified peril misplaces 212 of 3,960 claims and moves 13 of the 20 cells by 3% to 19%.
* **Ask B (device-carried).** New mortgage applications by channel (broker, branch, online) and month in 2026. *Device:* an application
  declined and resubmitted with amended details keeps its case number and takes a new application number, as the origination guide
  documents. Counting application numbers overstates 29 of the 36 cells by 4% to 12%.
* **Ask C (validity).** The discount under each of the four rung constructions, the number of borrowers' sales, the ledger's
  reproduction count under each valuation basis, and the open stock's split at the 15% line.
* **Decoupling.** Insurance claims and applications share no row with the default table, the ledger or the registry's transfers.
  Clearing the projection changes no figure in asks A or B.

## 11. Rubric arithmetic

4 perils × 5 years (ask A) + 3 channels × 12 months (ask B) + 4 rung figures, the sale count, 3 reproduction counts and 2 split counts
(ask C) + the committed discount, the loans it rests on and the nearest wrong figure + 4 named chart parts + 2 files ≈ 75 criteria.

## 12. World-building constraints

* Window sales: 412 possessions and 503 borrowers' sales. Mean discounts (median uncapped / repeat uncapped / median capped / repeat
  capped): possessions 38.6 / 33.0 / 34.0 / 29.4; borrowers' sales 20.0 / 15.7 / 15.5 / 11.6. Every borrower's sale had 15% equity or more
  at default and every possession less.
* Year-end stock: 298 loans in default, 66 under 15% equity (30 of them under zero) and 232 above; none between 12% and 18%.
* Figures: 38.6 / 29.4 / 19.6 / 15.5%; zero-equity split 13.4%; uncapped projection 19.5%.
* Default table: 2,940 episodes = 1,630 cured + 412 possession sales + 600 closed (503 with a title transfer, 97 refinanced) + 298 open.
* Districts 4 and 9 are identical on window history and lookup columns; 28 and 7 of 31 open defaults above the line.
* Insurance claims and applications touch no loan in the default table.

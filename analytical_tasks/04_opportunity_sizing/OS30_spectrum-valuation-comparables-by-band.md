# OS30 — Valuing a spectrum holding from auction comparables: average $/MHz-pop across bands mixes apples and oranges

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | Valuation by comparables (real estate comps, M&A multiples, domain-name sales) where comparables differ in quality class and timing |
| Domain | Telecommunications / corporate finance |
| Task shape | 07 · Grid of cells (band class × auction → $/MHz-pop in constant dollars; the value placed on the company's holding) |
| Core method | Compute $/MHz-pop per auction as Σ net winning bids ÷ Σ (MHz × population of licence areas), weighting by MHz-pop (not averaging licence-level prices); deflate to constant dollars; group by band class (low < 1 GHz, mid 1–6 GHz, mmWave > 24 GHz); value the holding = its MHz-pop × band-class benchmark |
| Analytical stump | Averaging licence-level $/MHz-pop gives tiny rural licences the same weight as major metros; pooling low-band, mid-band and mmWave auctions produces a meaningless average; nominal prices from different years mislead. The valuation of a mid-band holding shifts by multiples depending on these choices |
| Primary sources | FCC auction results (licence-level results and bidder summaries for Auctions 73, 97, 107, 108, 110, 101/102/103 and others in scope) |

## 1. The real-world situation

A regional carrier holds mid-band spectrum and is negotiating a sale. The banker's deck valued it at the simple average $/MHz-pop across
all FCC auctions since 2008. The buyer's team argued for a mid-band-specific benchmark weighted by MHz-pop and adjusted for inflation.

## 2. The decision (one deterministic recommendation)

**The holding's valuation (USD millions, constant dollars of the memo's year) using the mid-band benchmark, with the band × auction grid.**

Rules (valuation memo):

* Auctions in scope listed in `auctions_in_scope.json`; licence-level results with net winning bid, frequency block bandwidth (MHz) and licence
  area population (from FCC data or Census per memo's crosswalk).
* Auction $/MHz-pop = Σ net bids ÷ Σ (MHz × pop) over licences sold.
* Deflate with GDP price index to the memo's base year.
* Band class benchmark = MHz-pop-weighted average of auction $/MHz-pop within the class (auctions as units weighted by their MHz-pop).
* Holding: MHz and population covered (memo) in mid-band.
* Valuation = holding MHz-pop × mid-band benchmark.
* Report the simple average across all licences and all auctions for contrast.

## 3. Why capable analysts get it wrong

* Simple averages are quick and look neutral.
* Licence size varies by orders of magnitude; MHz-pop weighting reflects value.
* Bands differ in propagation and capacity; prices differ accordingly.
* Auction timing spans 15 years of inflation and market cycles.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–8 | `auction_<n>_results.xlsx` (8 auctions) | XLSX | 1k–7k licences each | FCC Auctions (results public notices and data files) | U.S. Gov public domain | Licence-level bids |
| 9 | `licence_area_populations.csv` | CSV | ~4k areas | FCC / Census | Public domain | Population by market area |
| 10 | `auctions_in_scope.json` | JSON | 8 | Task author | — | Auctions and band classes |
| 11 | `gdp_price_index.csv` | CSV | ~20 | BEA | Public domain | Deflator |
| 12 | `valuation_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 13 | `banker_simple_average.xlsx` | XLSX | — | Task author | — | Naive valuation |
| 14 | `holding_profile.json` | JSON | — | Task author | — | Holding MHz and population |

## 5. Deterministic solution path

1. Load licences; attach populations and bandwidths; compute licence MHz-pop.
2. Auction-level $/MHz-pop; deflate; band classes.
3. Benchmarks; holding valuation; contrast.

## 6. Wrong paths (method errors, not misreadings)

**A — simple average across licences.** Rural licences dominate.

**B — pooling bands.** Mixes value classes.

**C — nominal prices.** Inflation ignored.

**D — gross bids instead of net (after bidding credits).** Overstates.

## 7. Why the stump is analytical, not semantic

Formulas and weights are specified. The trap is unweighted, unclassified comparables.

## 8. Draft task prompt (prose)

> What is our mid-band spectrum worth on auction comparables? Build MHz-pop-weighted, band-specific, inflation-adjusted benchmarks as the
> valuation memo specifies. Provide `comparables_grid.csv` (auction: band, MHz-pop, net bids, $/MHz-pop nominal and real), `benchmark_chart.png`,
> and a one-page `holding_valuation.pdf`.

## 9. Deliverables

* `comparables_grid.csv`, `benchmark_chart.png`, `holding_valuation.pdf`.

## 10. Where 25+ rubric criteria come from

* 8 auctions × (MHz-pop, $/MHz-pop real) = 16; 3 band benchmarks; valuation; contrast.

## 11. Golden-output checklist

* Net bids; populations; auction-level ratios; deflation; class weighting; valuation.

## 12. Build notes (scope tuning)

* Confirm the banker's figure differs from the mid-band valuation by ≥ 2×.

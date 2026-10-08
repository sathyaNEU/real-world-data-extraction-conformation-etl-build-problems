# OS20 — Remittance savings by corridor: average fees across providers are not what senders pay

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | Fintech market-entry sizing (cross-border payments, FX, payouts) where prices vary by send amount and provider, and volume concentrates in a few corridors and providers |
| Domain | Payments / financial inclusion |
| Task shape | 07 · Grid of cells (8 corridors × 2 send amounts → current cost versus the entrant's price; the corridor launched first by annual customer savings captured) |
| Core method | Corridor average cost for each send amount ($200, $500) as the *market-share-weighted* average across providers (weights per memo: provider type shares) rather than the simple average of quotes; annual savings = corridor volume × share of transfers at each amount × (current cost % − entrant cost %) × capturable share |
| Analytical stump | The simple average of provider quotes overweights expensive banks that carry little volume; fees are not proportional to amount, so cost percentages at $200 and $500 differ markedly. Sizing with an unweighted single average overstates savings and picks the wrong corridor |
| Primary sources | World Bank Remittance Prices Worldwide (RPW) dataset; World Bank bilateral remittance estimates |

## 1. The real-world situation

A money-transfer start-up will launch in one corridor first. The deck sized savings as corridor remittance volume × (average total cost from
RPW − the start-up's 2.0% price) and chose a corridor where banks dominate the quote list. Investors asked for a volume-aware estimate.

## 2. The decision (one deterministic recommendation)

**The launch corridor (highest annual savings captured in year 1), with the corridor × amount cost grid.**

Rules (strategy memo):

* RPW: latest quarter in memo; corridors in `corridors.csv`; total cost % (fee + FX margin) for $200 and $500 sends.
* Weights: provider-type shares (bank, money transfer operator, post, mobile operator) per corridor from `provider_type_shares.csv` (memo);
  within type, simple average of quotes.
* Corridor cost at amount A = Σ_type share × average cost of that type.
* Volume: bilateral remittance estimate (USD) per corridor; share of transfers at $200-equivalent versus $500-equivalent bands per memo (by
  volume).
* Entrant price: 2.0% at both amounts (cost floor) or the memo's fee schedule; savings % = max(0, corridor cost − entrant cost).
* Captured share in year 1 = 3% of corridor volume.
* Annual savings captured = volume × Σ_A band share × savings % × 3%.

## 3. Why capable analysts get it wrong

* RPW publishes simple averages across quotes; it is easy to use them as "the price".
* Market share is concentrated in low-cost operators in many corridors.
* Fixed fees make cost percentages depend strongly on the send amount.
* Volume figures are estimates; applying them consistently matters more than precision.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `rpw_dataset_<yyyy>_q<q>.xlsx` | XLSX | ~15k quotes | World Bank RPW | CC BY 4.0 | Quotes by corridor, provider, amount |
| 2 | `bilateral_remittance_matrix_<yyyy>.xlsx` | XLSX | ~200 × 200 | World Bank / KNOMAD | CC BY 4.0 | Corridor volumes |
| 3 | `rpw_methodology.pdf` | PDF | — | World Bank | CC BY 4.0 | Cost definition |
| 4 | `corridors.csv` | CSV | 8 | Task author | — | Corridors in scope |
| 5 | `provider_type_shares.csv` | CSV | 8 × 4 | Task author (from public central-bank and industry reports; cite) | Cite | Weights |
| 6 | `strategy_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 7 | `deck_sizing.xlsx` | XLSX | 8 | Task author | — | Naive sizing |
| 8 | `send_amount_bands.json` | JSON | — | Task author | — | Band shares |

## 5. Deterministic solution path

1. Filter RPW quotes; average by provider type and amount; weight by shares.
2. Corridor volumes; band shares.
3. Savings % per amount; annual savings captured; choose corridor.
4. Contrast with the deck.

## 6. Wrong paths (method errors, not misreadings)

**A — simple average of all quotes.** Bank-heavy overstatement.

**B — one amount only.** Fee structure ignored.

**C — negative savings counted.** Entrant more expensive in some cells.

**D — volume of the reverse corridor.** Direction error (sender → receiver per memo).

## 7. Why the stump is analytical, not semantic

The weights, amounts and formula are specified. The trap is unweighted price averages and nonlinear fees.

## 8. Draft task prompt (prose)

> Which corridor should we launch first? Size annual savings our customers would capture using volume-aware average costs as the strategy memo
> specifies. Provide `corridor_grid.csv` (corridor × amount: weighted cost, simple average, entrant, savings), `savings_by_corridor.png`, and a
> one-page `launch_corridor.pdf`.

## 9. Deliverables

* `corridor_grid.csv`, `savings_by_corridor.png`, `launch_corridor.pdf`.

## 10. Where 25+ rubric criteria come from

* 16 cells' weighted costs and savings; 8 annual savings; choice; deck contrast.

## 11. Golden-output checklist

* Quote filters; type averages; weights; amount bands; floor at zero; volume direction; choice.

## 12. Build notes (scope tuning)

* Confirm the deck's corridor differs from the weighted-cost choice.

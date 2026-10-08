# DA14 — A weekly price index from scanner data: chaining through sales makes prices drift

| Field | Value |
|---|---|
| Category | Descriptive & Distribution Analysis |
| Mirrors | Price-index products built from transaction data at retailers, grocery-delivery platforms and statistical agencies (e-commerce inflation trackers) |
| Domain | Retail pricing / price statistics |
| Task shape | 03 · Bridge between two totals (chained weekly Törnqvist index level after two years → GEKS-Törnqvist multilateral level; the gap explained by chain drift around promotions, item churn and window choice) |
| Core method | Bilateral Törnqvist between weeks; chained weekly index versus GEKS (Gini–Éltető–Köves–Szulc) multilateral index over a fixed window; bridging items: drift from sale-and-rebound cycles, new/disappearing items, window length |
| Analytical stump | High-frequency chaining with expenditure weights drifts: during a sale, quantities spike at low prices; when prices return, quantities fall back but weights differ, so the chained index does not return to its starting level although prices did. Multilateral indices are transitive and free of chain drift |
| Primary sources | Dominick's Finer Foods scanner data (University of Chicago Kilts Center for Marketing) |

## 1. The real-world situation

A grocery analytics team publishes a weekly price index for a category from store scanner data. After two years, its chained weekly
Törnqvist index showed prices down 30%, while shelf prices for most items were about where they started. The team must restate the series
with an approved method and explain the restatement to clients.

## 2. The decision (one deterministic recommendation)

**The restated two-year index level (GEKS-Törnqvist, base week = 100) for the category and the bridge from the chained level to it.**

Rules (index methodology memo):

* Data: Dominick's movement file for the category in the memo, all stores pooled, weeks w1 to w104 in scope; price = PRICE ÷ QTY (bundle
  pricing), quantity = MOVE; expenditure = price × quantity; drop records with OK flag = 0 or zero movement.
* Items: UPCs; matched items between two weeks for bilateral indices.
* Bilateral Törnqvist P(s,t) on matched items with average expenditure shares.
* Chained index: I_t = Π P(t−1, t).
* GEKS over the full 104-week window: P_GEKS(0,t) = Π_{k}[P(0,k) × P(k,t)]^{1/104}.
* Bridge items (in order): (1) chain drift on matched continuing items, (2) entry/exit of items, (3) promotion weeks (`sale_code`
  present) — computed per the memo's decomposition (re-computing the chained index excluding each effect sequentially).

## 3. Why capable analysts get it wrong

* Chaining is standard for monthly indices and seems best for frequent product churn.
* Weekly data with promotions create quantity spikes correlated with prices.
* Bilateral weights change between sale and non-sale weeks, so the chain does not close the loop.
* Multilateral methods use all weeks' information and are transitive.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `w<category>.csv` (movement file) | CSV | ~5–15M | Kilts Center, Dominick's dataset | Free for academic research (Kilts terms) | Store-UPC-week price and movement |
| 2 | `upc<category>.csv` | CSV | ~500–2k | Kilts Center | Same | UPC descriptions |
| 3 | `dominicks_manual.pdf` | PDF | — | Kilts Center | Same | Field definitions (PRICE, QTY, MOVE, OK, SALE) |
| 4 | `week_calendar.xlsx` | XLSX | ~400 | Kilts Center | Same | Week dates |
| 5 | `index_methodology_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `published_chained_series.csv` | CSV | 104 | Task author | — | Current series |
| 7 | `ivancic_diewert_fox_2011_citation.pdf` | PDF | — | Cite | Cite | GEKS on scanner data |
| 8 | `bilateral_check.json` | JSON | ~5 | Task author | — | Check values for two week pairs |
| 9 | `weekly_item_aggregates.parquet` | Parquet | ~150k | Derived | Same | Pooled item-week prices and quantities |
| 10 | `store_list.csv` | CSV | ~100 | Kilts Center | Same | Stores |

## 5. Deterministic solution path

1. Clean records; pool stores to item-week unit values and quantities.
2. Bilateral Törnqvist for all week pairs (matched items).
3. Chained and GEKS indices; levels at week 104.
4. Sequential decomposition for the bridge; restatement.

## 6. Wrong paths (method errors, not misreadings)

**A — keep the chained index.** Downward drift.

**B — fixed-base Törnqvist to week 1.** Matched set shrinks; new items ignored.

**C — unit values without bundle price correction.** Wrong prices for multi-unit deals.

**D — GEKS with a short rolling window without splicing rules.** Not the memo's method.

## 7. Why the stump is analytical, not semantic

The formulas and decomposition are specified. The trap is chain drift — an index-number property under high-frequency, promotion-driven data.

## 8. Draft task prompt (prose)

> Restate our category price index using the GEKS method in the methodology memo and explain the gap from the chained series. Provide
> `index_series.csv` (week: chained, GEKS), `bridge.png` (waterfall from chained to GEKS level at week 104), and a one-page
> `restatement_note.pdf`.

## 9. Deliverables

* `index_series.csv`, `bridge.png`, `restatement_note.pdf`.

## 10. Where 25+ rubric criteria come from

* Index values at 12 checkpoint weeks for both series = 24; the three bridge items; final levels; check values.

## 11. Golden-output checklist

* Cleaning and bundle pricing; pooling; matched-item Törnqvist; chaining; GEKS; decomposition order.

## 12. Build notes (scope tuning)

* Choose a category with frequent promotions (e.g., soft drinks or cereals) so chain drift is large.

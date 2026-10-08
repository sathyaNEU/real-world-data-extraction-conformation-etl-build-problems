# OS42 — B2B software TAM: a chain with 300 locations buys one contract

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | B2B SaaS market sizing (counting buying entities rather than sites, seats or legal units), enterprise versus SMB segmentation |
| Domain | Business software / go-to-market |
| Task shape | 07 · Grid of cells (industry × firm size class → buying entities and annual contract value; the segment prioritised by the sales team) |
| Core method | Use firm counts (enterprises) rather than establishment counts by employment size class of the firm; contract value per firm scales with total employees (seats) per memo pricing; TAM = Σ firms × price(seats); contrast with establishment-based TAM |
| Analytical stump | Establishment counts treat every location of a multi-site firm as a separate customer, multiplying the number of large-firm "buyers" and, if priced per location, inflating TAM; it also mis-assigns size classes (a small branch of a large firm looks like an SMB). Firm-level counts by firm size reflect how purchasing decisions are made |
| Primary sources | U.S. Census Bureau Statistics of U.S. Businesses (SUSB) — firms, establishments, employment by enterprise size and industry |

## 1. The real-world situation

A scheduling-software company sizes its market across restaurants, retail and healthcare. The deck used establishment counts from County
Business Patterns by establishment size and priced each establishment at the SMB plan. The sales leader asked for a buyer-based TAM by firm size.

## 2. The decision (one deterministic recommendation)

**The industry × firm-size segment prioritised (largest firm-based TAM among segments reachable by the current sales motion: firms with 20–499
employees), with the TAM grid.**

Rules (go-to-market memo):

* Data: SUSB annual tables (latest year) by 6-digit NAICS (industries in memo) and enterprise employment size class: firms, establishments,
  employment.
* Pricing: annual contract = $25 per employee per month × 12 for firms < 500 employees; enterprise tier flat $250k for ≥ 500 (memo).
* Firm-based TAM per cell = firms × price at average employees per firm in the cell.
* Establishment-based TAM (contrast) = establishments × SMB price at average employees per establishment.
* Priority: highest firm-based TAM among 20–99 and 100–499 size classes.

## 3. Why capable analysts get it wrong

* Establishment data are more familiar (CBP) and finer geographically.
* Multi-unit firms buy centrally; establishments are not buyers.
* Size classes defined by establishment size misplace branches of large firms.
* Pricing depends on firm employees (seats), not location counts.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `us_6digitnaics_<year>.xlsx` (SUSB) | XLSX | ~25k rows | Census SUSB | U.S. Gov public domain | Firms, establishments, employment by size |
| 2 | `susb_definitions.pdf` | PDF | — | Census | Public domain | Firm vs establishment definitions |
| 3 | `cbp<yy>us.txt` (County Business Patterns, national) | Text | ~25k | Census CBP | Public domain | Establishment-size counts (deck basis) |
| 4 | `industries_in_scope.json` | JSON | ~12 NAICS | Task author | — | Scope |
| 5 | `pricing.json` | JSON | — | Task author | — | Price schedule |
| 6 | `gtm_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 7 | `deck_establishment_tam.xlsx` | XLSX | — | Task author | — | Naive TAM |

## 5. Deterministic solution path

1. Filter industries; extract firm and establishment counts by enterprise size class.
2. Average employees per firm per cell; prices; firm-based TAM.
3. Establishment-based TAM contrast; priority segment.

## 6. Wrong paths (method errors, not misreadings)

**A — establishment counts.** Inflated buyer counts.

**B — CBP establishment-size classes.** Branches misclassified as SMBs.

**C — flat SMB price for all.** Misstates value.

**D — mixing NAICS levels.** Double counting across 4- and 6-digit rows.

## 7. Why the stump is analytical, not semantic

Definitions and pricing are specified. The trap is the unit of the buyer in B2B sizing.

## 8. Draft task prompt (prose)

> Which industry and firm-size segment should sales prioritise? Size the market by buying firms from SUSB as the go-to-market memo specifies.
> Provide `tam_grid.csv` (industry × size class: firms, establishments, employees, firm TAM, establishment TAM), `tam_heatmap.png`, and a one-page
> `segment_priority.pdf`.

## 9. Deliverables

* `tam_grid.csv`, `tam_heatmap.png`, `segment_priority.pdf`.

## 10. Where 25+ rubric criteria come from

* 12 industries × 2 target classes firm TAM = 24; totals; priority; contrast.

## 11. Golden-output checklist

* Firm-level classes; average employees; pricing tiers; NAICS level; priority.

## 12. Build notes (scope tuning)

* Confirm the establishment-based TAM exceeds the firm-based TAM by ≥ 40% overall.

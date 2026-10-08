# DA37 — Freight mode share: by shipments, by tons or by ton-miles — and always with the survey weights

| Field | Value |
|---|---|
| Category | Descriptive & Distribution Analysis |
| Mirrors | Logistics analytics choosing the weighting basis (orders, units, revenue, unit-distance) for "share" metrics; marketplace GMV versus order-count shares |
| Domain | Freight transportation |
| Task shape | 07 · Grid of cells (5 commodity groups × 4 modes → ton-mile share; the commodity group targeted by a rail-shift incentive) |
| Core method | Shipment-level microdata with sampling weights; ton-miles = weight × tons × routed distance; mode shares by ton-miles within commodity groups; comparison with unweighted shipment counts and weighted tons |
| Analytical stump | Unweighted shares describe the sampled shipments, which oversample certain establishments; shipment-count shares are dominated by small parcel shipments; ton shares ignore distance, which is where rail and truck compete. The incentive targets ton-miles moved by truck over long distances |
| Primary sources | U.S. Census Bureau / BTS Commodity Flow Survey (CFS) 2017 Public Use Microdata |

## 1. The real-world situation

A state freight office will fund a rail-shift incentive for one commodity group: the group with the most long-haul truck ton-miles that rail
could plausibly capture. The first analysis used unweighted shipment records and picked the group with the most truck shipments over 500
miles, which turned out to be mostly light, high-value parcels.

## 2. The decision (one deterministic recommendation)

**The commodity group targeted: highest weighted truck ton-miles on shipments over 500 miles among the 5 groups, with the 5 × 4 grid of
ton-mile mode shares.**

Rules (freight memo):

* Data: CFS 2017 PUM; weight `WGT_FACTOR`; tons = `SHIPMT_WGHT` ÷ 2,000; routed distance `SHIPMT_DIST_ROUTED`.
* Commodity groups: SCTG codes mapped to 5 groups (memo).
* Modes: truck (codes 4–5 per memo), rail, water, multiple modes (including parcel and truck–rail).
* Ton-miles = `WGT_FACTOR` × tons × routed miles.
* Shares within each commodity group by mode on ton-miles; long-haul truck ton-miles = truck ton-miles with routed distance > 500.
* Target = group with the largest long-haul truck ton-miles; report unweighted and tons-based figures for contrast.

## 3. Why capable analysts get it wrong

* Microdata rows look like a census of shipments; they are a stratified sample.
* "Share" needs a basis; shipments, tons and ton-miles give very different answers.
* Parcel shipments are numerous but light.
* Great-circle versus routed distance changes ton-miles; the memo specifies routed.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `CFS_2017_PUF_CSV.csv` | CSV | ~5.98M | Census Bureau / BTS | U.S. Gov public domain | Shipment records |
| 2 | `CFS_2017_PUF_Users_Guide.pdf` | PDF | — | Census Bureau | Public domain | Variables, weights |
| 3 | `cfs_2017_puf_data_dictionary.xlsx` | XLSX | — | Census Bureau | Public domain | Codes |
| 4 | `sctg_to_group.json` | JSON | ~45 | Task author | — | Commodity groups |
| 5 | `mode_groups.json` | JSON | ~20 | Task author | — | Mode mapping |
| 6 | `freight_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 7 | `first_analysis_unweighted.xlsx` | XLSX | 5 | Task author | — | Earlier choice |
| 8 | `cfs_published_tables_2017.xlsx` | XLSX | — | Census Bureau | Public domain | Validation |

## 5. Deterministic solution path

1. Load PUM; derive tons, routed miles, ton-miles; map groups and modes.
2. Weighted ton-mile shares per group × mode.
3. Long-haul truck ton-miles; target group.
4. Validate totals against published tables; contrast with unweighted/tons bases.

## 6. Wrong paths (method errors, not misreadings)

**A — unweighted shipment counts.** Sample composition.

**B — tons basis.** Distance ignored.

**C — great-circle distance.** Not memo's basis.

**D — parcel counted as truck.** Mode mapping error that changes the answer.

## 7. Why the stump is analytical, not semantic

Weights, basis and mapping are specified. The trap is the choice of weighting basis and sample weights in share metrics.

## 8. Draft task prompt (prose)

> Which commodity group should the rail-shift incentive target? Compute weighted ton-mile mode shares from the CFS microdata as the freight
> memo defines them. Provide `mode_share_grid.csv` (group × mode: ton-miles, share; long-haul truck ton-miles), `ton_mile_shares.png`, and a
> one-page `incentive_target.pdf`.

## 9. Deliverables

* `mode_share_grid.csv`, `ton_mile_shares.png`, `incentive_target.pdf`.

## 10. Where 25+ rubric criteria come from

* 20 cells' shares; 5 long-haul truck totals; target; validation; contrasts.

## 11. Golden-output checklist

* Weights; tons conversion; routed miles; mode mapping; shares; target.

## 12. Build notes (scope tuning)

* Confirm the unweighted shipment basis selects a different group.

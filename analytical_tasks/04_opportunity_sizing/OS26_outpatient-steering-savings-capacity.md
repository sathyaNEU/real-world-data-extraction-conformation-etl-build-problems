# OS26 — Steering patients to lower-priced hospitals: savings are bounded by choice sets and capacity

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | Re-routing demand to cheaper suppliers (cloud workloads to cheaper regions, freight to lower-cost carriers, purchases to preferred vendors) where substitutes must be nearby and can absorb only so much |
| Domain | Health insurance / provider networks |
| Task shape | 05 · Allocation to a fixed total (allocate the volume of 10 outpatient procedure groups across hospitals so that totals are preserved, capacity caps hold and payments are minimised; the savings figure in the plan) |
| Core method | For each hospital service area, choice set = hospitals within 30 miles providing the service; reallocate volume from higher-priced to lower-priced hospitals in price order, subject to each receiving hospital's cap (+20% of its current volume) and a 50% maximum switching rate per origin hospital; savings = Σ volume moved × price difference |
| Analytical stump | Pricing every service at the cheapest hospital in the state (or region) assumes unlimited capacity and that patients would travel anywhere. The feasible savings respect geography, capacity and realistic switching; they are a fraction of the theoretical figure, and the procedure groups worth targeting change |
| Primary sources | CMS "Medicare Outpatient Hospitals — by Provider and Service" (APC-level services, average payments) |

## 1. The real-world situation

A payer is designing a tiered network to steer outpatient procedures to lower-priced hospitals. The strategy deck repriced every claim at
the state's lowest average payment for that APC and claimed large savings. Network managers asked for an estimate that respects travel
distances and how much volume low-priced hospitals can take.

## 2. The decision (one deterministic recommendation)

**Annual feasible savings by procedure group and in total, and the 3 procedure groups prioritised for the tiered network (largest feasible
savings).**

Rules (network memo):

* Data: Medicare Outpatient by Provider and Service for the year in memo; 10 APC groups in scope; state in scope.
* Prices: average Medicare payment per service by hospital and APC; volume = services.
* Distances: hospital-to-hospital great-circle distances from CMS hospital addresses geocoded (provided).
* Reallocation per APC: process origin hospitals from highest to lowest price; move up to 50% of the origin's volume to cheaper hospitals within
  30 miles in ascending price order, each receiving at most +20% of its current volume across all inflows.
* Savings = Σ moved × (origin price − receiving price).
* Theoretical savings (contrast) = Σ volume × (price − state minimum price).

## 3. Why capable analysts get it wrong

* "Reprice at the minimum" is a quick upper bound mistaken for a forecast.
* Geography limits substitution.
* Receiving capacity constrains moves; the order of processing matters (specified).
* Some APC groups have few nearby substitutes, so their savings vanish.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `MUP_OUT_RY<yy>_P04_V10_DY<yy>_Prov_Svc.csv` | CSV | ~120k | CMS data.cms.gov | U.S. Gov public domain | Hospital × APC services and payments |
| 2 | `outpatient_methodology.pdf` | PDF | — | CMS | Public domain | Definitions |
| 3 | `hospital_geocodes.csv` | CSV | ~4k | Derived from CMS Hospital General Information | Public domain | Coordinates |
| 4 | `apc_groups_in_scope.json` | JSON | 10 | Task author | — | Procedure groups |
| 5 | `network_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `strategy_deck_theoretical.xlsx` | XLSX | 10 | Task author | — | Naive savings |
| 7 | `reallocation_check.json` | JSON | — | Task author | — | Toy example |

## 5. Deterministic solution path

1. Filter state and APCs; prices and volumes; distances.
2. Run the reallocation per APC in the specified order with caps.
3. Savings by group; total; top 3.
4. Contrast with theoretical savings.

## 6. Wrong paths (method errors, not misreadings)

**A — reprice at state minimum.** Theoretical, infeasible.

**B — no capacity caps.** Overstated.

**C — no switching limit.** Overstated.

**D — processing order not followed.** Different allocation.

## 7. Why the stump is analytical, not semantic

Choice sets, caps and order are specified. The trap is unconstrained substitution in savings sizing.

## 8. Draft task prompt (prose)

> How much can a tiered outpatient network realistically save, and which procedure groups should it target first? Reallocate volume within
> 30-mile choice sets under the caps in the network memo. Provide `steering_savings.csv` (APC group: volume moved, feasible savings, theoretical
> savings), `savings_waterfall.png`, and a one-page `tiered_network_case.pdf`.

## 9. Deliverables

* `steering_savings.csv`, `savings_waterfall.png`, `tiered_network_case.pdf`.

## 10. Where 25+ rubric criteria come from

* 10 groups × (moved, feasible, theoretical) = 30; total; top 3; toy check.

## 11. Golden-output checklist

* Filters; distances; reallocation order; caps; savings; ranking.

## 12. Build notes (scope tuning)

* Confirm feasible savings are < 30% of theoretical and the top-3 set differs.

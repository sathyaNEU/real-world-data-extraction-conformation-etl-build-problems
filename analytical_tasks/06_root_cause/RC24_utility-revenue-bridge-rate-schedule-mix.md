# RC24 — Utility revenue up 9% and "rate increases" get the credit: how much is price at the level where prices are actually set?

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | FP&A price–volume–mix bridges where the aggregation level decides what counts as price (SaaS plans vs tiers, airline fares by cabin vs fare class, hardware ASP by product family vs SKU) |
| Domain | Electric utilities / regulatory finance |
| Task shape | 03 · Bridge between two totals (retail electric revenue, reference year → current year, bridged into price, volume, mix and accounting items at rate-schedule level) |
| Core method | Revenue by rate schedule from FERC Form 1 (sales by rate schedule: MWh, revenue, customers); stable schedule IDs from a crosswalk; PVM at schedule level: price = Σ ΔP_s × Q_s,cur; volume = (Q_tot,cur − Q_tot,ref) × P̄_ref; mix = Σ (q_s,cur − q_s,ref) × Q_tot,cur × P_s,ref, with q the MWh share; schedules entering or leaving handled as mix; unbilled revenue and rate-refund provisions bridged separately from schedule revenue |
| Analytical stump | A bridge at customer-class level (residential, commercial, industrial) labels as "price" every movement of customers between schedules inside a class — for example large customers leaving a standard tariff for a discounted economic-development contract, or residential customers moving onto time-of-use rates. Prices are set per schedule; mix within a class must be separated at that level. Accounting accruals (unbilled revenue, refund provisions) also move revenue without any tariff change |
| Primary sources | FERC Form 1 via the Catalyst Cooperative Public Utility Data Liberation project (PUDL): sales of electricity by rate schedule (p. 304) and electric operating revenues (p. 300) |

## 1. The real-world situation

An investor-owned utility's retail electric revenue rose 9% year over year. Its investor-relations deck attributed the growth to "approved rate
increases". A consumer advocate preparing testimony believes most of the increase reflects customers moving between tariffs and an accounting
true-up, and wants a schedule-level bridge to show the commission.

## 2. The decision (one deterministic recommendation)

**Whether the "rate increases" claim is supported (supported if the schedule-level price effect is ≥ 50% of the revenue change), with the bridge:
price, volume, mix, new/ended schedules and accounting items.**

Rules (testimony memo):

* Data: PUDL FERC Form 1 sales by rate schedule for the memo's respondent (utility ID) for the two years; electric operating revenues (p. 300) for
  unbilled revenue and provision for rate refunds.
* Schedules: mapped to stable IDs using `rate_schedule_crosswalk.csv`; rows that are subtotals or "total" lines excluded; schedules with zero MWh in a
  year treated as absent.
* P_s = revenue ÷ MWh; Q_s = MWh; q_s = Q_s ÷ Σ Q over continuing schedules (shares and totals in the PVM use continuing schedules only).
* Continuing schedules (present in both years): price, volume and mix effects as defined in Core method.
* New and ended schedules: new = current revenue of schedules absent in the reference year; ended = −reference revenue of schedules absent in the
  current year; both reported as a "tariff migration" line together with mix.
* Accounting: Δ(unbilled revenue) + Δ(provision for rate refunds) from p. 300, reported separately.
* Closure: reference total + components = current total (difference reported as residual; must be 0 within rounding for continuing schedules).
* Supported if price ÷ total change ≥ 50%.

## 3. Why capable analysts get it wrong

* Class-level PVM is the default template.
* Schedule names in Form 1 are free text and change; without stable IDs, migration looks like price.
* Average revenue per MWh within a class moves with schedule mix.
* Accruals sit in a different schedule of the form.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `core_ferc1__yearly_sales_by_rate_schedules_sched304.parquet` | Parquet | ~150k (all respondents, years) | PUDL (Catalyst Cooperative) from FERC Form 1 | CC BY 4.0 (PUDL); FERC data public domain | Sales by rate schedule |
| 2 | `core_ferc1__yearly_electric_operating_revenues_sched300.parquet` | Parquet | ~80k | PUDL | CC BY 4.0 | Revenue lines incl. unbilled and refunds |
| 3 | `core_pudl__assn_ferc1_pudl_utilities.csv` | CSV | ~400 | PUDL | CC BY 4.0 | Respondent IDs |
| 4 | `rate_schedule_crosswalk.csv` | CSV | ~120 | Task author (from the utility's published tariff book; cite) | Cite | Stable schedule IDs |
| 5 | `testimony_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `ir_deck_revenue_slide.xlsx` | XLSX | — | Task author | — | Class-level "rate increase" bridge |

## 5. Deterministic solution path

1. Filter the respondent and years; drop subtotal rows; map schedules; build P, Q, q.
2. Continuing-schedule PVM; new/ended schedules; accounting items.
3. Closure; price share; decision.
4. Re-run PVM at class level to show how much mix it labels as price; contrast with the IR deck.

## 6. Wrong paths (method errors, not misreadings)

**A — class-level PVM.** Within-class tariff migration is counted as price.

**B — no schedule crosswalk.** Renamed schedules appear as one ended and one new schedule; migration is overstated.

**C — including subtotal rows.** Double-counts revenue and MWh.

**D — ignoring p. 300 accruals.** Unbilled true-ups and refund provisions are absorbed into price.

## 7. Why the stump is analytical, not semantic

The crosswalk resolves naming; the formulas and level are fixed. The trap is the aggregation level at which "price" is measured.

## 8. Draft task prompt (prose)

> The utility says rate increases drove its 9% revenue growth. Build the schedule-level revenue bridge in the testimony memo and tell me whether the
> claim holds. Provide `revenue_bridge.csv` (component: $, share), `revenue_bridge_waterfall.png`, and a one-page `testimony_exhibit.pdf`.

## 9. Deliverables

* `revenue_bridge.csv` — price, volume, mix, tariff migration, accounting, residual; plus schedule-level detail.
* `revenue_bridge_waterfall.png` — schedule-level bridge next to the class-level bridge.
* `testimony_exhibit.pdf` — decision, bridge, and why the class-level view overstates price.

## 10. Where 25+ rubric criteria come from

* Data filtering and mapping (rows dropped, schedules mapped, continuing/new/ended counts): 5.
* P, Q for the 5 largest schedules in both years: 10 (scored in groups).
* Components and closure: 7.
* Price share and decision: 2.
* Class-level contrast: 2+.

## 11. Golden-output checklist

* Subtotals removed; crosswalk applied; zero-MWh schedules absent.
* PVM definitions exactly as specified; migration line separate.
* Accruals from p. 300; closure to the current total.

## 12. Build notes (scope tuning)

* Choose a respondent and year pair with large customer migration between schedules (e.g., new economic-development or time-of-use schedules) and a
  visible unbilled-revenue swing; confirm that the class-level price share exceeds 50% while the schedule-level share does not.

# RC17 — The state's corn yield missed trend by 9 bushels: bad hybrids, or corn planted on worse ground?

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | Average-KPI declines driven by mix (average revenue per user falling because growth came from lower-value markets; fleet fuel economy falling because sales shifted to trucks) |
| Domain | Agriculture / seed and crop-input businesses |
| Task shape | 12 · Drill-down to one leaf (state yield shortfall → irrigated vs dryland practice → crop reporting district → county; the leaf named for the field-performance review) |
| Core method | Shift-share decomposition of the state yield shortfall against county trend yields: within-county effect at base harvested-acre weights, mix effect from changes in acreage shares, and interaction; repeated at each level of the hierarchy, drilling into the node with the largest negative within contribution |
| Analytical stump | A state average yield is an acreage-weighted mean, so it falls when acreage shifts toward dryland and marginal counties even if every county hits its trend. High prices pull corn onto dryland acres. Comparing county yields without weights, comparing with last year instead of trend, or ignoring practice-level data misattributes a mix shift to genetics |
| Primary sources | USDA NASS Quick Stats — county-level corn for grain: area planted, area harvested, yield and production, by irrigation practice where published |

## 1. The real-world situation

A seed company's regional team saw the state's corn yield come in 9 bu/acre below trend in a year with near-normal weather. Sales blamed a new hybrid
family that had taken significant share. Agronomists noted that corn acres had expanded onto dryland after a price rally. Product management needs
to know whether a field-performance review is warranted, and where.

## 2. The decision (one deterministic recommendation)

**The county named for the hybrid field-performance review (the leaf reached by drilling into the largest negative within contribution at each
level), with the state-level split of the shortfall into within, mix and interaction.**

Rules (agronomy memo):

* Data: NASS county estimates for corn for grain, the memo's state, current year and the 15 prior years; "OTHER (COMBINED) COUNTIES" rows treated as
  one pseudo-county per district.
* Practice level: irrigated and non-irrigated series where published; counties without a practice split are assigned to the practice that holds
  ≥ 80% of their acreage in the prior 3 years (else to "mixed").
* Trend yield per practice-county: OLS of yield on year over the 15 prior years; expected yield = prediction for the current year.
* Base weights: mean harvested-acre shares over the 3 prior years.
* Shift-share at each node: within = Σ w0 (y − ŷ); mix = Σ (w − w0) ŷ; interaction = Σ (w − w0)(y − ŷ); the three sum to actual minus base-weighted
  expected yield.
* Drill-down: state → practice → district → county, choosing at each level the child with the most negative within contribution (Σ w0 (y − ŷ) for
  that child, expressed in state bu/acre).
* Report all three components at the state level and the leaf's within contribution.

## 3. Why capable analysts get it wrong

* The headline is one number; the instinct is to look for a product cause.
* Year-over-year comparisons ignore the steady trend gain.
* Practice mix is a large, hidden lever in states with irrigation.
* Suppressed counties are grouped by NASS and must be kept in the weights.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `nass_corn_county_yield_<state>.csv` | CSV | ~30k | USDA NASS Quick Stats API | U.S. Government work (public domain) | Yields by county and practice |
| 2 | `nass_corn_county_acres_<state>.csv` | CSV | ~40k | USDA NASS Quick Stats | Public domain | Planted and harvested acres |
| 3 | `nass_county_district_codes.csv` | CSV | ~3,100 | USDA NASS | Public domain | County → district mapping |
| 4 | `nass_state_corn_<state>.json` | JSON | ~80 | USDA NASS Quick Stats | Public domain | State totals for reconciliation |
| 5 | `agronomy_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `sales_hybrid_complaint.xlsx` | XLSX | — | Task author | — | The hybrid explanation |
| 7 | `shift_share_method_note.pdf` | PDF | — | Task author (from standard shift-share references; cite) | Cite | Method |

## 5. Deterministic solution path

1. Assemble practice-county panels; handle combined counties; reconcile to state totals.
2. Fit trends; compute expected yields; base weights.
3. Shift-share at the state level; drill through practice, district and county.
4. Name the leaf; report its contribution and the mix share; contrast with the sales explanation.

## 6. Wrong paths (method errors, not misreadings)

**A — unweighted mean of county yield changes.** Gives small counties equal say; ignores mix.

**B — comparison with last year's yield.** Ignores trend; the shortfall is mis-sized.

**C — all-practice county yields only.** Hides the irrigated-to-dryland shift inside counties.

**D — dropping combined counties.** Weights no longer sum to the state; shares are biased.

## 7. Why the stump is analytical, not semantic

The hierarchy, trends, weights and drill rule are specified. The trap is a weighted average whose weights moved.

## 8. Draft task prompt (prose)

> The state corn yield missed trend by 9 bushels and sales blames our new hybrids. Decompose the shortfall as the agronomy memo specifies and tell me
> which county, if any, deserves a field-performance review. Provide `yield_shift_share.csv` (node: within, mix, interaction), `drilldown_tree.png`,
> and a one-page `yield_shortfall_rca.pdf`.

## 9. Deliverables

* `yield_shift_share.csv` — components for every node visited and its siblings.
* `drilldown_tree.png` — the drill path with contributions at each level.
* `yield_shortfall_rca.pdf` — the leaf, the mix share, and why the hybrid explanation is or is not supported.

## 10. Where 25+ rubric criteria come from

* Reconciliation to state totals: 2.
* Trend yields for a sample of counties: 4.
* State components (within, mix, interaction) and closure: 4.
* Practice, district and county level components along the path: 9.
* Leaf and its contribution: 2.
* Mix share and the sales contrast: 4+.

## 11. Golden-output checklist

* 15-year trends per practice-county; 3-year base weights on harvested acres.
* Combined counties as pseudo-counties; practice assignment rule.
* Drill by most negative within contribution in state bu/acre.

## 12. Build notes (scope tuning)

* Choose a state with irrigation (e.g., Kansas or Nebraska) and a year with a large rise in non-irrigated corn acreage; confirm that mix explains at
  least half the state shortfall while one district still shows a concentrated within shortfall.

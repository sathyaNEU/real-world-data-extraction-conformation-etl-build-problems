# RC06 — Air traffic delay tripled with 5% more flights: blame capacity, staffing, weather — or saturation?

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | Latency blow-ups in systems running near capacity (APIs, databases, warehouses) where small load increases cause large delay increases |
| Domain | Air traffic management |
| Task shape | 18 · Hypotheses versus evidence (traffic growth, capacity reduction, staffing-related regulations, weather → evidence lines; the cause that explains the summer delay increase in one area control centre) |
| Core method | Per area control centre (ACC): daily en-route ATFM delay and flights; regulation reasons (capacity, staffing, weather, other); estimate a delay–traffic relation from the previous summer (convex, e.g., delay ∝ (traffic ÷ capacity)^k); counterfactual delay at this year's traffic with last year's capacity; attribute residual to capacity/staffing/weather via regulation reason codes |
| Analytical stump | A 5% traffic increase looks too small to explain a tripling of delay, so analysts blame staffing; but near capacity, delay is highly nonlinear in load. Conversely, reason codes alone (as recorded by ANSPs) don't separate traffic-driven saturation from reduced capacity. Both the nonlinear relation and the reason codes are needed |
| Primary sources | EUROCONTROL Aviation Intelligence Portal — ATFM en-route delay and traffic by ACC (daily) |

## 1. The real-world situation

An air navigation service provider's ACC saw en-route delay triple from one summer to the next while traffic rose 5%. Media blamed controller
staffing shortages. The provider's analysts were asked to quantify the contributions of traffic growth, capacity, staffing and weather.

## 2. The decision (one deterministic recommendation)

**The cause acted on (largest attributed share of the delay increase among traffic saturation, capacity, staffing, weather), with the attributed
minutes for each.**

Rules (analysis memo):

* Data: EUROCONTROL daily ATFM en-route delay by ACC and reason category; daily IFR flights by ACC; summers (June–August) of the two years.
* Delay–traffic model fitted on last summer: log(delay + 1) = a + k × log(flights) + weekday effects (OLS).
* Traffic-saturation counterfactual: predicted delay this summer at this summer's flights using last summer's model.
* Attribution: Δ delay = traffic component (counterfactual − last summer) + residual; residual allocated to reason categories in proportion to
  their excess (this summer − last summer) minutes by reason.
* Act on the largest component.

## 3. Why capable analysts get it wrong

* Linear intuition underestimates the effect of load near capacity.
* Reason codes reflect the regulation trigger, not the counterfactual.
* Weekday patterns and daily variation need controls.
* Attribution must sum to the total change.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `atfm_delay_en_route_<years>.csv` | CSV | ~60k (ACC × day × reason) | EUROCONTROL Aviation Intelligence Portal | EUROCONTROL data terms (free reuse with attribution; verify) | Delay by reason |
| 2 | `ifr_flights_by_acc_<years>.csv` | CSV | ~25k | EUROCONTROL | Same | Traffic |
| 3 | `atfm_reason_codes.pdf` | PDF | — | EUROCONTROL | Public | Reason definitions |
| 4 | `analysis_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 5 | `media_staffing_claim.xlsx` | XLSX | — | Task author | — | Claim summary |
| 6 | `acc_scope.json` | JSON | 1 | Task author | — | ACC in scope |
| 7 | `performance_review_report_citation.pdf` | PDF | — | EUROCONTROL PRR (cite) | Public | Context |

## 5. Deterministic solution path

1. Extract ACC daily delay by reason and flights for both summers.
2. Fit last summer's model; counterfactual for this summer.
3. Attribute components; choose the largest.

## 6. Wrong paths (method errors, not misreadings)

**A — linear scaling of delay with traffic.** Understates saturation.

**B — reason codes only.** Ignores counterfactual load effect.

**C — fitting the model on both summers.** Absorbs the change.

**D — ignoring weekday effects.** Biased k.

## 7. Why the stump is analytical, not semantic

Data, model and attribution are specified. The trap is linear thinking about congestion.

## 8. Draft task prompt (prose)

> What drove the summer delay increase in our ACC? Attribute the change to traffic saturation, capacity, staffing and weather as the analysis memo
> specifies. Provide `delay_attribution.csv` (component: minutes, share), `delay_vs_traffic.png`, and a one-page `atfm_delay_rca.pdf`.

## 9. Deliverables

* `delay_attribution.csv`, `delay_vs_traffic.png`, `atfm_delay_rca.pdf`.

## 10. Where 25+ rubric criteria come from

* Model coefficients (k, weekday); components (4) and shares; monthly breakdown (3 months × components); decision.

## 11. Golden-output checklist

* Data extraction; model fit; counterfactual; allocation; decision.

## 12. Build notes (scope tuning)

* Choose an ACC where traffic saturation explains > 40% while staffing reasons are visible.

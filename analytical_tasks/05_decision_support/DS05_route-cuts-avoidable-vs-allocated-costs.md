# DS05 — Cutting loss-making routes: allocated overhead does not disappear when the route does

| Field | Value |
|---|---|
| Category | Decision Support |
| Mirrors | Product-line and market-exit decisions at companies using fully allocated P&Ls (shared engineering, marketing, platform costs) |
| Domain | Passenger rail / transport finance |
| Task shape | 01 · Ranked list under a cap (routes suspended to close a $150M operating gap, ranked by avoidable loss per passenger-mile) |
| Core method | Separate route costs into avoidable (train crews, fuel/power, on-board services, route-specific maintenance) and shared/allocated (overheads, stations shared with other routes, system-wide costs) per the cost-category table; avoidable contribution = revenue − avoidable costs; suspend routes with negative avoidable contribution, most negative per passenger-mile first, until the gap is closed |
| Analytical stump | Ranking routes by fully allocated operating loss and cutting the "worst" ones shifts allocated costs to the remaining routes without saving them; some routes with large allocated losses cover their avoidable costs and their suspension increases the system deficit |
| Primary sources | Amtrak Monthly Performance Reports (route-level revenue, costs and ridership) |

## 1. The real-world situation

A passenger-rail operator must close a $150M operating gap. The board paper ranked routes by fully allocated operating loss per passenger and
proposed suspending the bottom five. Finance staff argued that much of each route's reported cost is allocated overhead that would remain.

## 2. The decision (one deterministic recommendation)

**The routes suspended (by avoidable contribution per passenger-mile, until savings ≥ $150M), the realised saving, and the routes the board paper
would have cut that actually lower the deficit if kept.**

Rules (finance memo):

* Data: Amtrak Monthly Performance Report for the fiscal year in memo — route-level ticket and other revenue, cost categories, ridership and
  passenger-miles.
* Avoidability by cost category from `cost_avoidability.csv` (e.g., train & engine crew 100%, fuel 100%, on-board services 100%, equipment
  maintenance 80%, station costs 0–50% by sharing, general & administrative 0%).
* Avoidable contribution = total route revenue × (1 − revenue leakage to other routes per memo, 10% for connecting passengers) − Σ avoidable costs.
* Candidates: routes with negative avoidable contribution; order by contribution ÷ passenger-miles (most negative first); suspend until
  cumulative savings (−contribution) ≥ $150M.
* Report the board paper's five routes with their avoidable contribution.

## 3. Why capable analysts get it wrong

* Fully allocated P&Ls are the reporting format and look complete.
* Allocated costs are shared; cutting a route does not remove them.
* Network effects (connecting revenue) partially disappear with a route.
* Per passenger-mile normalisation compares routes of different lengths.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–12 | `Amtrak_Monthly_Performance_Report_<month>_FY<yy>.pdf` | PDF (tables) | ~40 routes per report | Amtrak (public reports) | Public (cite) | Route financials and ridership |
| 13 | `route_financials_fy.xlsx` | XLSX | ~40 routes × ~20 cost lines | Task author (extracted from the year-end report tables) | Public source | Structured extraction |
| 14 | `cost_avoidability.csv` | CSV | ~20 categories | Task author (from published route-costing methodology; cite) | — | Avoidability factors |
| 15 | `finance_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 16 | `board_paper_ranking.xlsx` | XLSX | ~40 | Task author | — | Allocated-loss ranking |
| 17 | `priia_209_methodology_citation.pdf` | PDF | — | Amtrak/FRA cost allocation methodology (cite) | Public | Cost categories |

## 5. Deterministic solution path

1. Extract/verify route figures; map cost lines to categories.
2. Avoidable costs and contributions; candidates; ordering; cumulative savings.
3. Suspension list; savings; contrast with the board paper.

## 6. Wrong paths (method errors, not misreadings)

**A — fully allocated loss ranking.** Cuts routes that cover avoidable costs.

**B — ignoring revenue leakage.** Overstates savings.

**C — per-passenger rather than per passenger-mile.** Long routes penalised inconsistently with the memo.

**D — counting G&A as avoidable.** Overstates savings.

## 7. Why the stump is analytical, not semantic

Categories and factors are specified. The trap is fully allocated costing in an incremental decision.

## 8. Draft task prompt (prose)

> Which routes should we suspend to close the $150M gap? Use avoidable contribution per passenger-mile as the finance memo specifies and test the
> board paper's list. Provide `route_contribution.csv` (route: revenue, avoidable cost, allocated cost, contribution, per passenger-mile, suspend),
> `contribution_waterfall.png`, and a one-page `suspension_plan.pdf`.

## 9. Deliverables

* `route_contribution.csv`, `contribution_waterfall.png`, `suspension_plan.pdf`.

## 10. Where 25+ rubric criteria come from

* Suspended routes; contributions for 12 routes; savings; board-paper routes' contributions (5); leakage treatment.

## 11. Golden-output checklist

* Category mapping; avoidability; leakage; ordering; cumulative rule; contrast.

## 12. Build notes (scope tuning)

* Verify the extraction against report totals; confirm at least two board-paper routes have positive avoidable contribution.

# DA12 — Latency budgets across microservices: per-hop P99s do not add up to the user's P99

| Field | Value |
|---|---|
| Category | Descriptive & Distribution Analysis |
| Mirrors | SRE latency-budget allocation for request paths that cross many services (search, feeds, checkout) at large internet companies |
| Domain | Distributed systems / SRE |
| Task shape | 05 · Allocation to a fixed total (split an end-to-end P99 budget of 300 ms across the services on one call path so that the scaled per-service targets reproduce the end-to-end P99 exactly) |
| Core method | Build per-request critical-path latency from call graphs; measure the end-to-end P99; each service's contribution at the tail = its mean share of critical-path time among requests at or above the end-to-end P99 ("tail attribution"); budget = 300 ms × tail share |
| Analytical stump | Summing per-service P99s over-allocates (each service's tail rarely coincides with the others'); splitting the budget by mean latency shares under-allocates to services whose latency spikes drive the tail. The budget must be allocated from the composition of the *tail requests* |
| Primary sources | Alibaba cluster-trace-microservices-v2021 (call-graph traces with response times) |

## 1. The real-world situation

A platform team sets latency objectives for the services on its most important request path. The user-facing objective is 300 ms at the
99th percentile. The previous allocation gave each service a P99 target proportional to its own current P99; the targets summed to far more
than 300 ms, so every team could meet its target while the user objective failed.

## 2. The decision (one deterministic recommendation)

**The per-service latency budgets (ms, one decimal) for the services on the chosen call path, summing exactly to 300 ms.**

Rules (SRE memo):

* Data: one hour of call-graph traces for the online service (entry service) named in the memo.
* Requests: trace IDs whose root call is the entry service; drop traces with missing spans per the memo's completeness rule.
* Critical path: for each request, walk the call tree; at each node, the child with the largest finish time on the synchronous path is on
  the critical path; service time on the path = own response time minus time in critical children (non-negative).
* End-to-end latency = root response time; P99 over requests.
* Tail set: requests with end-to-end latency ≥ P99.
* Tail share of service s = Σ over tail requests of s's critical-path time ÷ Σ of end-to-end latency over tail requests.
* Budget_s = 300 × tail share, rounded to 0.1 ms with the largest-remainder method so the sum is exactly 300.0.
* Report also Σ per-service P99 and the mean-share allocation for contrast.

## 3. Why capable analysts get it wrong

* Per-service dashboards show P99s; adding them seems natural.
* Percentiles are not additive; tails of components are partially independent.
* Mean shares describe the typical request, not the requests that breach the objective.
* Asynchronous calls do not add to user latency; critical-path extraction matters.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–6 | `MSCallGraph_<n>.tar.gz` (one-hour slice) | CSV | ~20–40M calls total | Alibaba clusterdata (cluster-trace-microservices-v2021) | Alibaba clusterdata terms (research; cite) | Calls: trace ID, RPC ID, caller, callee, response time, type |
| 7 | `MSResource_<n>.tar.gz` | CSV | ~1M | Same | Same | Context |
| 8 | `trace_schema.md` | Markdown | — | Same | Same | Field definitions |
| 9 | `entry_service.json` | JSON | 1 | Task author | — | Path in scope |
| 10 | `sre_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 11 | `previous_allocation.xlsx` | XLSX | ~15 | Task author | — | Previous targets |
| 12 | `critical_path_examples.json` | JSON | ~5 | Task author | — | Hand-checked trees |
| 13 | `requests_e2e.parquet` | Parquet | ~500k | Derived | Same | End-to-end latencies |

## 5. Deterministic solution path

1. Filter traces for the entry service; completeness rule.
2. Reconstruct call trees; extract critical paths; service times.
3. End-to-end P99; tail set; tail shares.
4. Budgets with largest-remainder rounding; contrasts.

## 6. Wrong paths (method errors, not misreadings)

**A — sum of P99s.** Over-allocation.

**B — mean-share allocation.** Tail drivers under-budgeted.

**C — including asynchronous calls in path time.** Inflated services.

**D — proportional rounding without largest remainder.** Total ≠ 300.0.

## 7. Why the stump is analytical, not semantic

The trace semantics and allocation rule are specified. The trap is quantile non-additivity and tail composition.

## 8. Draft task prompt (prose)

> Allocate our 300 ms P99 objective across the services on the main request path using the tail-attribution rule in the SRE memo. Provide
> `latency_budgets.csv` (service: P99, mean share, tail share, budget), `tail_composition.png` (stacked critical-path time for tail versus typical
> requests), and a one-page `budget_allocation.pdf`.

## 9. Deliverables

* `latency_budgets.csv`, `tail_composition.png`, `budget_allocation.pdf`.

## 10. Where 25+ rubric criteria come from

* ~12 services × (tail share, budget) = 24; end-to-end P99; Σ P99s; mean-share contrast; sum check.

## 11. Golden-output checklist

* Trace filtering; tree reconstruction; synchronous critical path; tail set; shares; rounding.

## 12. Build notes (scope tuning)

* Choose an entry service with 8–15 services on its path and a tail driven by one service with modest mean latency.

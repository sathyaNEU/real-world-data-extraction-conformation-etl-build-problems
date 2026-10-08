# FC29 — Sizing LLM serving capacity: forecast tokens per minute, not requests times an average

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Mirrors | Generative-AI providers planning GPU serving capacity (prefill vs decode load, mixed code/chat workloads) |
| Domain | AI infrastructure / capacity planning |
| Task shape | 04 · Setting one dial (number of serving replicas for next week's peak) |
| Core method | Per-minute workload in cost units (prefill tokens × prefill cost + generated tokens × decode cost), combined across workloads minute by minute, tail percentile, growth projection |
| Analytical stump | Request counts × average tokens per request assumes token size is independent of time and workload mix; it is not. Percentiles of per-workload peaks cannot be added; the combined minute-level series must be built first. Prefill and decode have different costs, so a single "tokens" total misstates load |
| Primary sources | Azure LLM inference traces (Azure Public Dataset) |

## 1. The real-world situation

An AI platform team sizes the number of model-serving replicas for next week so that the 99th-percentile minute of demand fits
within capacity. The capacity analyst forecast requests per minute (the familiar dashboard metric), multiplied by the global average
tokens per request, and added the code-assistant and chat workloads' separate peaks. The number of replicas came out both too high in
some hours and too low at the true peak, which arrives when long-context code requests surge.

## 2. The decision (one deterministic recommendation)

**Replicas to provision for next week = ceil(P99 of minute-level combined workload × growth ÷ capacity per replica).**

Rules (capacity memo):

* Traces: the one-week code and conversation traces (timestamp, context tokens, generated tokens per request).
* Workload units per request = context tokens × 1.0 + generated tokens × 12.0 (relative cost of a decode token vs a prefill token,
  from the memo's benchmark).
* Combined minute series: Σ units over both traces for each minute (timestamps aligned on the shared clock).
* P99 = 99th percentile over all minutes of the week (inclusive interpolation).
* Next week's growth factor g = 1.08; one replica serves 2.4 million units per minute.
* Replicas = ceil(P99 × g ÷ 2.4M).

## 3. Why capable analysts get it wrong

* Requests are the metric on every dashboard; tokens per request vary widely and shift with workload and hour.
* Decode tokens are far more expensive per token than prefill; summing raw tokens hides the load.
* Separate workload peaks occur at different minutes; adding them overstates, while averaging their sizes across the week
  understates the coincident tail.
* Hourly aggregation smooths the minute-level peaks that capacity must absorb.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `AzureLLMInferenceTrace_code_1week.csv` | CSV | ~ millions | Azure Public Dataset (LLM inference 2024) | CC BY 4.0 | Code workload |
| 2 | `AzureLLMInferenceTrace_conv_1week.csv` | CSV | ~ millions | Same | CC BY 4.0 | Conversation workload |
| 3 | `AzureLLMInferenceTrace_code.csv`, `…_conv.csv` (2023 one-hour traces) | CSV | ~20k each | Same (2023 release) | CC BY 4.0 | Context / sanity check |
| 4 | `llm_trace_readme.pdf` | PDF | — | Azure Public Dataset | CC BY 4.0 | Schema |
| 5 | `splitwise_isca2024_citation.pdf` | PDF | — | ISCA 2024 (cite) | Cite | Prefill/decode phases |
| 6 | `benchmark_cost_ratio.json` | JSON | — | Task author (from a public serving benchmark, cited) | — | Decode/prefill cost ratio |
| 7 | `minute_series_combined.parquet` | Parquet | ~10k minutes | Derived | CC BY 4.0 | Combined series |
| 8 | `capacity_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 9 | `analyst_request_based_plan.xlsx` | XLSX | ~30 | Task author | — | Request-based sizing |
| 10 | `replica_spec.json` | JSON | — | Task author | — | Units per replica, growth |

## 5. Deterministic solution path

1. Parse both traces; compute units per request; bin into minutes; sum across workloads.
2. P99 over minutes; apply growth; compute replicas.
3. Contrast with request × average-token sizing and with sum of per-workload P99s.

## 6. Wrong paths (method errors, not misreadings)

**A — requests × average tokens.** Ignores size–time correlation; wrong peak.

**B — raw token totals.** Decode cost hidden.

**C — sum of separate P99s.** Overstated.

**D — hourly bins.** Peak smoothed; under-provisioned.

## 7. Why the stump is analytical, not semantic

Units, cost ratio, percentile and capacity are specified. The traps are aggregation order (minute-level combination before the
tail) and the mean-of-product fallacy — analytical errors.

## 8. Draft task prompt (prose)

> How many serving replicas do we need next week? Follow the capacity memo: convert every request in the code and conversation
> traces into workload units, combine them minute by minute, take the 99th-percentile minute, apply growth and divide by replica
> capacity. Provide `minute_workload_summary.csv` (percentiles from 50th to 99.9th of combined and per-workload units),
> `workload_heatmap.png` (minute-of-day × day of combined units) and a one-page `capacity_memo_answer.pdf` with the replica count
> and how the request-based plan compares.

## 9. Deliverables

* `minute_workload_summary.csv`, `workload_heatmap.png`, `capacity_memo_answer.pdf`.

## 10. Where 25+ rubric criteria come from

* Percentile ladder for combined and two workloads (≈18 values); P99; replicas; request-based and sum-of-P99 contrasts; peak minute.

## 11. Golden-output checklist

* Correct units; minute alignment; combined series; P99; growth; ceiling.

## 12. Build notes (scope tuning)

* Verify the 2024 trace file names and timestamp format; confirm the request-based plan differs by ≥ 2 replicas.
* Cite the benchmark from which the decode/prefill cost ratio is taken.

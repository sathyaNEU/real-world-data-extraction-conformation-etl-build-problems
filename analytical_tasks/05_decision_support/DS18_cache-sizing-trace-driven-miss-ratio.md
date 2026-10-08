# DS18 — How much cache memory to buy? A Zipf fit forgets that requests come in bursts

| Field | Value |
|---|---|
| Category | Decision Support |
| Mirrors | Cache and CDN capacity planning at social networks and content platforms (in-memory key-value caches, edge caches) |
| Domain | Distributed systems / infrastructure cost |
| Task shape | 04 · Setting one dial (cache size per cluster that meets a 95% hit ratio at least cost) |
| Core method | Trace-driven miss-ratio curve (MRC) with LRU via reuse (stack) distances computed on the request trace (object size-aware, per memo's approximation), versus an independent-reference model (IRM) estimate from a Zipf fit to object popularity; choose the smallest size reaching 95% hit ratio on the trace-driven MRC |
| Analytical stump | Fitting popularity to a Zipf distribution and computing the hit ratio under the independent reference model ignores temporal locality (bursts, diurnal working sets) and object sizes; it mis-sizes caches by large factors. Trace-driven simulation of the actual reference stream answers the question |
| Primary sources | Twitter production cache traces (Twemcache clusters; Yang et al., OSDI 2020) |

## 1. The real-world situation

A platform team plans memory for three cache clusters. The capacity model fitted a Zipf distribution to object request counts and computed the
expected hit ratio of an LRU cache under independent requests; it recommended 2.5 TB per cluster. A reliability engineer replayed a day of traffic
and saw different hit ratios.

## 2. The decision (one deterministic recommendation)

**The cache size per cluster (GB, rounded up to 64 GB) achieving ≥ 95% request hit ratio under LRU on the trace, and the total memory difference
versus the Zipf/IRM model.**

Rules (capacity memo):

* Data: Twitter cache traces for the 3 clusters in memo; one day per cluster; requests with key, value size, operation.
* Hit ratio over GET requests; SET/DELETE handled per memo (SET inserts; DELETE removes).
* Trace-driven LRU: simulate exact LRU by object bytes at sizes 64 GB to 4 TB (64 GB steps) or via reuse-distance computation (memo allows either,
  results must match to 0.1 percentage points).
* IRM model: fit Zipf α by MLE to GET counts per key; Che approximation for LRU hit ratio with average object size.
* Choose the smallest size with trace-driven hit ratio ≥ 95%.
* Warm-up: first 2 hours excluded from hit-ratio measurement.

## 3. Why capable analysts get it wrong

* Zipf/IRM models are textbook and quick.
* Real traces have temporal locality and churn; IRM misestimates.
* Object sizes vary; counting objects rather than bytes mis-sizes memory.
* Warm-up distorts measured hit ratios.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–3 | `cluster<NN>.sort.zst` (3 clusters, one day each) | CSV (compressed) | ~100M–1B requests each | Twitter cache-trace repository | CC BY 4.0 (repository licence; verify) | Requests |
| 4 | `cache_trace_format.md` | Markdown | — | Same | Same | Field definitions |
| 5 | `yang_2020_osdi_citation.pdf` | PDF | — | Cite | Cite | Trace analysis |
| 6 | `capacity_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 7 | `zipf_irm_model.xlsx` | XLSX | 3 | Task author | — | Current model |
| 8 | `che_approximation_reference.pdf` | PDF | — | Cite | Cite | IRM LRU approximation |
| 9 | `mrc_check_values.json` | JSON | — | Task author | — | Small-trace checks |

## 5. Deterministic solution path

1. Parse traces; filter operations; warm-up.
2. Trace-driven LRU MRC by bytes; IRM model via Zipf and Che.
3. Choose sizes; totals; contrast.

## 6. Wrong paths (method errors, not misreadings)

**A — Zipf/IRM sizing.** Misestimated.

**B — object-count capacity.** Ignores sizes.

**C — including warm-up.** Understated hit ratio.

**D — ignoring deletes/sets.** Wrong cache state.

## 7. Why the stump is analytical, not semantic

The simulation and rules are specified. The trap is modelling a correlated reference stream as independent.

## 8. Draft task prompt (prose)

> How much memory should each cache cluster get? Compute trace-driven miss-ratio curves under LRU and pick the size for a 95% hit ratio, as the
> capacity memo specifies, and compare with the Zipf model. Provide `mrc_by_cluster.csv` (size: hit ratio trace and IRM), `miss_ratio_curves.png`, and
> a one-page `cache_capacity.pdf`.

## 9. Deliverables

* `mrc_by_cluster.csv`, `miss_ratio_curves.png`, `cache_capacity.pdf`.

## 10. Where 25+ rubric criteria come from

* 3 clusters × (size, hit ratio at size, IRM size) = 9; MRC points at 6 sizes × 3 = 18; totals; contrast.

## 11. Golden-output checklist

* Operation handling; bytes; warm-up; LRU simulation; Zipf fit; choice.

## 12. Build notes (scope tuning)

* Use a subsample if traces are huge (deterministic key sampling, memo's rate); confirm the IRM model mis-sizes by ≥ 30% for at least one cluster.

# DS49 — Sizing an API rate limiter: average request rates say nothing about bursts

| Field | Value |
|---|---|
| Category | Decision Support |
| Mirrors | Rate limiting and throttling at API platforms (payment APIs, developer platforms, social APIs) where legitimate clients burst |
| Domain | Web infrastructure / API platform |
| Task shape | 04 · Setting one dial (token-bucket burst size B for a fixed refill rate r, so that ≤ 0.1% of legitimate clients' requests are throttled) |
| Core method | Replay each client's request timestamps (client = host) through a token bucket (rate r tokens/s, capacity B); throttled share of requests; choose the smallest B meeting the target; compare with sizing B from mean rate × window or from the 99th percentile of per-minute counts |
| Analytical stump | Average rates are tiny relative to bursts (page loads fetch dozens of objects within a second); per-minute percentiles smooth sub-second bursts; the token bucket's behaviour depends on the arrival sequence. Only replay of actual sequences gives the throttling rate for a given B |
| Primary sources | Internet Traffic Archive web server logs (ClarkNet and University of Saskatchewan HTTP traces) |

## 1. The real-world situation

An API platform introduces per-client token-bucket limits. Engineering proposed refill r = 10 requests/s and burst B = 20, derived from the 99th
percentile of requests per minute ÷ 60 × 2. A replay test showed many legitimate browsing sessions throttled.

## 2. The decision (one deterministic recommendation)

**The smallest burst size B (integer) such that, with r = 10 req/s, at most 0.1% of requests from legitimate clients are throttled, and the throttled
share under the proposed B = 20.**

Rules (platform memo):

* Data: ClarkNet (two weeks) and Saskatchewan (memo period) HTTP logs; client = remote host; timestamps at 1-second resolution (ties spread uniformly
  within the second per memo, seed 3).
* Legitimate clients: hosts with < 10,000 requests per day and not in `crawler_hosts.json` (crawlers excluded).
* Token bucket: starts full; refill continuously at r; each request consumes one token; if none, the request is throttled (not queued).
* Throttled share = throttled requests ÷ total legitimate requests, both logs pooled.
* Search B from 1 to 500.
* Contrast: proposed B = 20; B from mean rate × 10 s; B from 99th percentile per-minute count ÷ 60 × 2.

## 3. Why capable analysts get it wrong

* Mean rates look like the right scale for limits.
* Burstiness at sub-second scale dominates throttling.
* Aggregation into minutes hides bursts.
* Sequence matters: tokens refill between bursts.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `clarknet_access_log_Aug28.gz`, `clarknet_access_log_Sep4.gz` | Text (Common Log Format) | ~3.3M | Internet Traffic Archive (ClarkNet-HTTP) | ITA terms (public research use; verify) | Requests |
| 2 | `UofS_access_log.gz` | Text | ~2.4M | Internet Traffic Archive (Saskatchewan-HTTP) | Same | Requests |
| 3 | `ita_trace_descriptions.html` | HTML | — | ITA | Public | Trace notes |
| 4 | `crawler_hosts.json` | JSON | ~50 | Task author (by user-agent-free heuristics: request rate and robots.txt fetches) | — | Exclusions |
| 5 | `platform_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `engineering_proposal.xlsx` | XLSX | — | Task author | — | Proposed sizing |
| 7 | `token_bucket_reference.pdf` | PDF | — | Cite (RFC 2697/2698 concepts) | Public | Algorithm |

## 5. Deterministic solution path

1. Parse logs; identify clients; exclude crawlers and heavy hosts; spread ties.
2. Replay token bucket per client for each B; throttled shares.
3. Choose B; report contrasts.

## 6. Wrong paths (method errors, not misreadings)

**A — B from mean rate.** Far too small.

**B — per-minute percentile.** Smooths bursts.

**C — queueing instead of throttling.** Different semantics from memo.

**D — including crawlers.** Distorts legitimate burst profile.

## 7. Why the stump is analytical, not semantic

The algorithm and parameters are specified. The trap is sizing on averages and coarse aggregates for a sequence-dependent mechanism.

## 8. Draft task prompt (prose)

> What burst size should our token bucket allow? Replay the HTTP traces through the limiter as the platform memo specifies and find the smallest B
> meeting the 0.1% target. Provide `burst_sweep.csv` (B: throttled share), `burst_profile.png`, and a one-page `rate_limit_policy.pdf`.

## 9. Deliverables

* `burst_sweep.csv`, `burst_profile.png`, `rate_limit_policy.pdf`.

## 10. Where 25+ rubric criteria come from

* Chosen B; throttled shares at 10 B values; contrasts (3 rules); client counts; tie handling.

## 11. Golden-output checklist

* Parsing; client definition; exclusions; tie spreading; bucket replay; search.

## 12. Build notes (scope tuning)

* Confirm the proposed B = 20 throttles ≥ 1% of legitimate requests.

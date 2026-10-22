## Tags

**Domain:** General Statistics & Data Science (missing data, censoring and measurement error).
**Analytical objective:** Descriptive & Distribution Analysis.

## 1. Final Recommendation

**The platform teams should fix five of the 24 public API endpoints before the 4 December code freeze: EP01 (POST /v2/payroll-runs), EP02 (GET /v2/payroll-runs/{id}/preview), EP05 (POST /v2/filings), EP16 (POST /v2/direct-deposits) and EP22 (POST /v2/accounting-sync/exports).**

At the forecast January peak each of the five has a 99th-percentile response time above 800 ms for the requests customers send, the nearest, EP05, at about 0.9 seconds, once every pod's garbage-collection pauses in its run of record are met by requests that keep arriving while a pod is paused. Not the three the load test's recorded percentiles name (EP02, EP16, EP22, at 874, 963, 1,084 ms): each test client waited for its response before sending again, so a paused pod's clients sent nothing and the record holds one slow request per blocked client. Not the ten HdrHistogram's back-fill names: it credits each blocked client with every request it would have sent while its pod was paused, as if that pod were the only one, and so also names EP06, whose full collections hold one pod in five, and EP07, EP08, EP19 and EP20, whose slowest requests are slow on their own.

## 2. Critical Components

1. The runs of record are the last complete run of each of the **24** endpoints, minutes 3 to 13; the first runs of EP05, EP13, EP20 stopped early and are set aside.
2. Each pod's stop-the-world pauses come from the GC log export, each line ending its pause; the freeze-list endpoints' pods are paused, on average, for **2.8 to 3.6 percent** of each measurement.
3. Over the requests customers send, **five endpoints** exceed 800 ms at the 99th percentile: EP01, EP02, EP05, EP16, EP22; recorded, EP01 sits at **574 ms** and EP05 at **740 ms**.

## 3. Step-by-Step Solution

1. Conformed loadtest_jmeter_results_2026-11-10_to_12.jtl (timeStamp is the start, plus elapsed) and loadtest_k6_results_2026-11-16_to_19.csv (timestamp is the completion, less metric_value) into one request log by endpoint and pod, and kept each endpoint's last complete run, minutes 3 to 13 (standard 3.2): 24 runs.
2. Built every pod's pauses from perf_gc_log_export_2026-11-10_to_19.log: Pause lines only, each ending at its stamp, wall-clock stamps at UTC-05:00, uptime stamps placed from the JVM start that perf_cluster_pod_events_2026-11.csv gives, after each pod's restart.
3. Took each recorded request's own service time: its response time less the pause time on its pod while it was in flight.
4. Rebuilt the response times customers would see (standard 1.2, 2.1, 2.2): 2,000,000 arrivals spread evenly over each measurement window, each to one of the service's pods with equal chance, each taking a recorded service time and held by its pod's pauses; the 99th percentile exceeds 800 ms for EP01, EP02, EP05, EP16, EP22.
5. Compared the recorded 99th percentiles: over 800 ms only for EP02, EP16, EP22.
6. Forecast peak-hour volume (standard 4.1, 4.2): each endpoint's busiest clock hour of January 2026 in edge_requests_hourly_2026-01.csv on the route that served it (the old path up to the rename in developer_portal_changelog_2026.html, the new path from it), less the monitors in edge_uptime_monitors.yaml created before January, times the employers on its plans on 1 November in crm_employer_accounts_2026-11-01.csv over those on 1 January, found by undoing every event in billing_subscription_events_2026.csv, latest first.
7. Service credits (standard 5.2): legacy_billing_credits_2026-01_to_04.csv (cents, void credits out) and billing_credits_2026-05-01_to_11-19.json (credits and reversals) for incidents in status_page_incidents_2025-12_to_2026-11.xlsx that began from 1 January to 31 October 2026 (Eastern), by the route each hit, each legacy credit carried forward into the new system counted once at the amount issued.
8. Five endpoints go on the freeze list: EP01, EP02, EP05, EP16 and EP22.

## 4. Deliverable Answers

### yearend_readiness_2027.xlsx

1. Verdicts, every endpoint:
   - EP01: fix before the freeze
   - EP02: fix before the freeze
   - EP03: meets the standard
   - EP04: meets the standard
   - EP05: fix before the freeze
   - EP06: meets the standard
   - EP07: meets the standard
   - EP08: meets the standard
   - EP09: meets the standard
   - EP10: meets the standard
   - EP11: meets the standard
   - EP12: meets the standard
   - EP13: meets the standard
   - EP14: meets the standard
   - EP15: meets the standard
   - EP16: fix before the freeze
   - EP17: meets the standard
   - EP18: meets the standard
   - EP19: meets the standard
   - EP20: meets the standard
   - EP21: meets the standard
   - EP22: fix before the freeze
   - EP23: meets the standard
   - EP24: meets the standard
2. Forecast peak-hour volume for January 2027, whole requests an hour:
   - EP01: 22,706
   - EP02: 17,452
   - EP03: 14,131
   - EP04: 31,303
   - EP05: 30,284
   - EP06: 18,440
   - EP07: 68,147
   - EP08: 16,349
   - EP09: 11,307
   - EP10: 50,368
   - EP11: 36,247
   - EP12: 23,044
   - EP13: 27,980
   - EP14: 37,032
   - EP15: 22,912
   - EP16: 31,925
   - EP17: 28,116
   - EP18: 17,824
   - EP19: 43,320
   - EP20: 26,523
   - EP21: 19,401
   - EP22: 35,149
   - EP23: 51,862
   - EP24: 24,536
3. Service credits for breaches from 1 January to 31 October 2026, net of reversals, to the nearest dollar:
   - EP01: $6,989
   - EP02: $10,299
   - EP03: $11,205
   - EP04: $11,073
   - EP05: $12,630
   - EP06: $20,317
   - EP07: $18,653
   - EP08: $9,776
   - EP09: $12,750
   - EP10: $3,793
   - EP11: $27,160
   - EP12: $15,032
   - EP13: $12,434
   - EP14: $15,165
   - EP15: $14,865
   - EP16: $8,844
   - EP17: $10,414
   - EP18: $6,103
   - EP19: $35,416
   - EP20: $22,067
   - EP21: $31,046
   - EP22: $23,872
   - EP23: $30,890
   - EP24: $16,900

### yearend_readiness_2027.png

1. Bar chart of every endpoint's 99th-percentile response time at the forecast peak against the 800 ms line, the 5 freeze-list endpoints highlighted and the recorded percentile marked on each bar.

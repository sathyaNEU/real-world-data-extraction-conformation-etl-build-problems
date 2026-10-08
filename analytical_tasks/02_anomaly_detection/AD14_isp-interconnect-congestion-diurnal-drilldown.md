# AD14 — Is the ISP congested or the interconnect? Evening slowdowns hide inside daily averages

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Mirrors | Streaming services and ISPs diagnosing peak-hour degradation at interconnection points (the 2013–2014 streaming/ISP peering disputes) |
| Domain | Internet performance / network peering |
| Task shape | 12 · Drill-down to one leaf (national → ISP → transit/server site → metro) on a diurnal degradation ratio |
| Core method | Per-test throughput medians by hour; diurnal ratio = peak-hour median ÷ reference-hour median; stratification by ISP × server-site transit network × metro; drill on the worst ratio with minimum-sample rules |
| Analytical stump | Daily average throughput barely moves when congestion lasts four evening hours; national or ISP-level aggregates mix congested and uncongested interconnects (Simpson's paradox across paths). Means are dominated by fast connections; medians and path-level stratification reveal the problem |
| Primary sources | Measurement Lab (M-Lab) NDT speed-test data (BigQuery public dataset) |

## 1. The real-world situation

A video-streaming company saw evening complaints concentrated among subscribers of some broadband providers. The ISP's dashboard showed
healthy daily average speeds. The streaming company's network team needs to show where the degradation lives: the access network, or the
interconnection between the ISP and a particular transit provider.

## 2. The decision (one deterministic recommendation)

**The leaf (ISP × transit network × metro) with the worst diurnal degradation, and the owning relationship (which interconnect to
escalate).**

Rules (network analytics memo):

* Tests: NDT download tests in the study months; client ISP from client ASN (mapping in folder); server site → transit network (M-Lab
  site metadata); metro from server site.
* Hours in the client's local time; weekdays only. Peak = 20:00–23:59; reference = 10:00–13:59.
* Diurnal ratio for any node = median download throughput in peak ÷ median in reference (tests pooled over the study months); nodes with
  < 300 tests in either window are not eligible.
* Drill: national → ISP (lowest ratio) → transit network within that ISP (lowest) → metro (lowest). Escalate if the leaf ratio < 0.5.

## 3. Why capable analysts get it wrong

* Daily or monthly averages smooth a four-hour evening problem into a small dip.
* Paths through different transit networks behave differently; pooling them hides the congested link.
* Mean throughput is dominated by the fastest tiers; medians reflect the typical test.
* Hour-of-day must be local to the client, or peaks are misplaced across time zones.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–6 | `ndt_downloads_YYYYMM.parquet` (six study months) | Parquet | 1–5M tests each | M-Lab NDT (BigQuery `measurement-lab`) | CC0 1.0 | Test-level throughput, RTT, client ASN, server site |
| 7 | `mlab_site_metadata.json` | JSON | ~150 sites | M-Lab | CC0 | Site → transit network, metro |
| 8 | `asn_to_isp_mapping.csv` | CSV | ~500 | Task author from public registries (RIR WHOIS) | Public | ISP grouping |
| 9 | `client_timezones.csv` | CSV | ~400 metros | Derived (IANA tz) | Public domain | Local time conversion |
| 10 | `mlab_interconnection_report_2014.pdf` | PDF | — | M-Lab public report | CC BY (verify) | Context |
| 11 | `bigquery_extraction.sql` | SQL | — | Task author | — | Queries |
| 12 | `network_analytics_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 13 | `isp_daily_average_dashboard.xlsx` | XLSX | ~200 | Task author | — | Daily-average view |

## 5. Deterministic solution path

1. Map tests to ISP, transit, metro and local hour; filter weekdays.
2. Compute ratios at each level with eligibility; follow the drill path.
3. Report the leaf, its ratio and escalation decision; show the same ISP's daily average trend.

## 6. Wrong paths (method errors, not misreadings)

**A — daily averages.** No visible problem.

**B — ISP-level ratio only.** Diluted by uncongested paths.

**C — means instead of medians.** Skewed by fast tiers.

**D — UTC hours.** Peaks misaligned.

## 7. Why the stump is analytical, not semantic

The metric and drill rule are defined. The traps are temporal aggregation and path aggregation — analytical ways a localized problem
disappears.

## 8. Draft task prompt (prose)

> Show me where the evening slowdown lives. Using the M-Lab test data and the analytics memo, compute peak-versus-midday median throughput
> ratios and drill from national to ISP to transit network to metro. Provide `diurnal_drilldown.xlsx` (one sheet per level: tests, peak and
> reference medians, ratio, eligible) and `hourly_profiles.png` (hourly median throughput for the leaf path vs another transit path of the
> same ISP), plus a one-page `escalation_memo.pdf`.

## 9. Deliverables

* `diurnal_drilldown.xlsx`, `hourly_profiles.png`, `escalation_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* Ratios at each level (≈ 6 ISPs, 4–6 transits, 5 metros); leaf; escalation; daily-average contrast; sample counts.

## 11. Golden-output checklist

* Local time; weekdays; medians; eligibility; drill rule; threshold.

## 12. Build notes (scope tuning)

* Choose study months known for interconnection congestion (e.g. early 2014) and confirm the leaf ratio < 0.5 while the ISP daily average
  changes < 10%.
* Document the ASN-to-ISP mapping and site metadata version.

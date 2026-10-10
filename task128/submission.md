# task128: November patch ticket split across six estates

## Tags

**Domain:** Business & Operations Analytics, field service and maintenance (patch crews' monthly change tickets and the colocation provider's maintenance windows).
**Analytical objective:** Opportunity Sizing & Decision Support (exploitable host exposures November can realise, sized from the open pool through the provider's drain limit).

## 1. Final Recommendation

**Give payments 1 ticket, checkout 1, search 76, media 75, internal tools 77 and the data pipeline 70, which takes out 13,360 exploitable host exposures in November.**

The deciding quantity is what a colocated drain removes: the provider can drain 96 payments hosts and 120 checkout hosts in November, each drained host comes back clear of every open exploitable finding, so one glibc ticket per colocated estate naming its most exposed hosts takes out 1,410 and 1,740. Not the bulk on payments the CISO wants: no number of tickets drains more than 96 payments hosts. Not one ticket per dense package on the colocated estates: that credits each drain with one package and spends tickets that buy no extra drains.

## 2. Critical Components

1. November drains are **96** payments hosts and **120** checkout hosts
2. The 96 most exposed payments hosts carry **1,410** open exploitable exposures and the 120 most exposed checkout hosts **1,740**
3. The 298 cloud tickets take out **2,610** on search, **2,650** on media, **2,430** on internal tools and **2,510** on the data pipeline
4. November takes out **13,360** exploitable host exposures in total

## 3. Step-by-Step Solution

1. Counted a finding as exploitable when its latest score in `epss_score_history_2026.parquet` is at least 0.10 (vulnerability management standard s.2; the cut-day reading of the same rule reproduces all 12 cells of `q3_2026_remediation_closeout.pdf` from `cloud_q3_closed_findings.csv`).
2. For each window in `november_window_calendar.csv`, concurrent drains are November `hosts_in_service` less ceil(peak forecast tps over the window's own local hours / `per_host_tps`) less `failure_domain_hosts`, times `drain_cycles` (SRE maintenance standard s.2; reproduces all 412 acknowledgements): payments 96, checkout 120.
3. Every host in `accepted_host_ids` has `in_service_since` equal to its latest accepted window, and no feed finding was first seen on or before its host's `in_service_since`, so a drain returns the host on the current image and takes out every open exploitable finding on it.
4. Ranked colocated hosts in `colocation_managed_host_findings_2026-10-23.jsonl` by open exploitable findings and drained the top 96 and 120 under one ticket each on glibc, the only package open on every one of them and the highest-scoring (standard s.3): payments 1,412, checkout 1,742.
5. Valued each cloud estate and package in `vuln_findings_2026-10-23.csv` at its exploitable findings, ranked them and kept the top 298: last in search sudo at 9, first below media libc6 at 8.
6. Patch pace from `crew_deployment_log_2026.csv`: days from `vendor_first_release` to the ticket's last `succeeded` run, tickets whose last succeeded run falls 1 May to 23 October, over target when above 35 days (standard s.5).
7. Coverage from `cloud_asset_register_2026-10-23.csv` (running instances) joined to `scanner_coverage_2026-10.csv` on `instance_id`, unscanned when there is no authenticated scan on or after 9 October (standard s.6).
8. Recommendation: 1 / 1 / 76 / 75 / 77 / 70 tickets, 13,360 exposures taken out.

## 4. Deliverable Answers

### november_ticket_cut.csv
1. 300 rows in rank order with estate, package, hosts reached in November and exposures taken out: rank 1 Checkout glibc, 120 hosts, 1,742; rank 2 Payments glibc, 96 hosts, 1,412; ranks 3 to 300 the 298 cloud updates, ending rank 300 Search sudo, 9 hosts, 9.
2. Tickets per estate in the file:
   - Payments: 1
   - Checkout: 1
   - Search: 76
   - Media: 75
   - Internal tools: 77
   - Data pipeline: 70

### ticket_split_review.pptx
1. The split, tickets and exposures taken out in November to the nearest ten:
   - Payments: 1 ticket, 1,410
   - Checkout: 1 ticket, 1,740
   - Search: 76 tickets, 2,610
   - Media: 75 tickets, 2,650
   - Internal tools: 77 tickets, 2,430
   - Data pipeline: 70 tickets, 2,510
   - Total: 300 tickets, 13,360
2. Last ticket that made the cut: Search, sudo, takes out 9.
3. First ticket that missed: Media, libc6, would take out 8.
4. Chart on slide 2, one pair of bars per estate in ticket order (internal tools, search, media, data pipeline, checkout, payments), November's figure beside the open exploitable exposure on 23 October:
   - Internal tools: 2,430 against 2,460 open
   - Search: 2,610 against 2,626 open
   - Media: 2,650 against 2,681 open
   - Data pipeline: 2,510 against 2,547 open
   - Checkout: 1,740 against 4,688 open, annotated 120 hosts
   - Payments: 1,410 against 2,960 open, annotated 96 hosts
   - Title carries the total, 13,360
5. Estate card, median days from first fix release to the ticket's last host (tickets completed since 1 May) and tickets over target:
   - Payments: 24.0 days, 3
   - Checkout: 28.0 days, 7
   - Search: 23.0 days, 4
   - Media: 25.0 days, 1
   - Internal tools: 26.0 days, 4
   - Data pipeline: 22.0 days, 1
6. Estate card, hosts in service on 23 October and hosts with no authenticated scan in the 14 days before:
   - Search: 610 in service, 99 unscanned
   - Media: 870 in service, 149 unscanned
   - Internal tools: 361 in service, 49 unscanned
   - Data pipeline: 696 in service, 92 unscanned

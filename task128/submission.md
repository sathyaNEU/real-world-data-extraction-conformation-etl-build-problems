# task128: November patch ticket split across six estates

## Tags

**Domain:** Business & Operations Analytics, field service and maintenance (patch crews' monthly change tickets and the colocation provider's maintenance windows).
**Analytical objective:** Opportunity Sizing & Decision Support (exploitable host exposures November can realise, sized from the open pool through the provider's drain limit).

## 1. Final Recommendation

**Give payments 4 tickets, checkout 5, search 72, media 75, internal tools 77 and the data pipeline 67, which takes out 13,300 exploitable host exposures in November.**

The deciding quantity is what a colocated ticket can reach: a ticket rides one provider change request, a request is for one window, and each November window drains 24 hosts, each coming back clear of every open exploitable finding, so one glibc ticket per window on the most exposed hosts takes out 1,410 on payments and 1,740 on checkout. Not the bulk on payments the CISO wants: no number of tickets drains more than 96 payments hosts. Not one ticket per colocated estate: a ticket cannot reach past its own window. Not one ticket per dense package: that credits each drain with one package.

## 2. Critical Components

1. November drains are **24** hosts in each office window, **96** payments hosts over 4 windows and **120** checkout hosts over 5
2. A colocated ticket reaches only its own window, so payments needs **4** tickets and checkout **5**
3. The 96 most exposed payments hosts carry **1,410** open exploitable exposures and the 120 most exposed checkout hosts **1,740**
4. The 291 cloud tickets take out **2,580** on search, **2,650** on media, **2,430** on internal tools and **2,480** on the data pipeline
5. November takes out **13,300** exploitable host exposures in total

## 3. Step-by-Step Solution

1. Counted a finding as exploitable at a score of at least 0.10, the latest score in `epss_score_history_2026.parquet` for a cloud finding and the feed's `epss` for a colocated one (vulnerability management standard s.2; the cut-day reading of the same rule reproduces all 12 cells of `q3_2026_remediation_closeout.pdf` from `cloud_q3_closed_findings.csv`).
2. For each window in `november_window_calendar.csv`, concurrent drains are the November `hosts_in_service` less ceil(peak forecast tps over the window's hours, start hour to the hour before its end, / `per_host_tps`) less `failure_domain_hosts`, times `drain_cycles` (SRE maintenance standard s.2; reproduces all 412 acknowledgements): 24 per window, payments 96, checkout 120.
3. Every host in `accepted_host_ids` has `in_service_since` equal to its latest accepted window, and no feed finding was first seen on or before its host's `in_service_since`, so a drain returns the host on the current image and takes out every open exploitable finding on it.
4. Every colocated ticket in `crew_deployment_log_2026.csv` carries exactly one `change_request`, runs only on that request's window, and on exactly its `hosts_accepted` (the 8 part-accepted ones never reached their declined hosts); with the provider schedule's s.3 (a request is for one window), one ticket per November window: payments 4, checkout 5.
5. Ranked colocated hosts in `colocation_managed_host_findings_2026-10-23.jsonl` by open exploitable findings (ties by `host_id`) and gave each window's glibc ticket, in window date order, the next 24 (glibc is open on all of them and scores highest, standard s.3): payments 1,412, checkout 1,742.
6. Valued each cloud estate and package in `vuln_findings_2026-10-23.csv` at its exploitable findings, ranked them and kept the top 291: last in data pipeline libjpeg-turbo8 at 10, first below search libunistring2 at 9.
7. Patch pace from `crew_deployment_log_2026.csv` (days from `vendor_first_release` to the ticket's last `succeeded` run, that run dated 1 May to 23 October, over target above 35 days, standard s.5) and coverage from `cloud_asset_register_2026-10-23.csv` running instances joined to `scanner_coverage_2026-10.csv` on `instance_id`, unscanned without an authenticated scan on or after 9 October (standard s.6).
8. Recommendation: 4 / 5 / 72 / 75 / 77 / 67 tickets, 13,300 exposures taken out.

## 4. Deliverable Answers

### november_ticket_cut.csv
1. 300 rows in rank order with estate, package, hosts reached in November and exposures taken out: ranks 1 to 9 the nine colocated glibc tickets, one per November window, 24 hosts each (payments together 1,412, checkout together 1,742); ranks 10 to 300 the 291 cloud updates, ending rank 300 Data pipeline libjpeg-turbo8, 10 hosts, 10.
2. Tickets per estate in the file:
   - Payments: 4
   - Checkout: 5
   - Search: 72
   - Media: 75
   - Internal tools: 77
   - Data pipeline: 67

### ticket_split_review.pptx
1. The split, tickets and exposures taken out in November to the nearest ten:
   - Payments: 4 tickets, 1,410
   - Checkout: 5 tickets, 1,740
   - Search: 72 tickets, 2,580
   - Media: 75 tickets, 2,650
   - Internal tools: 77 tickets, 2,430
   - Data pipeline: 67 tickets, 2,480
   - Total: 300 tickets, 13,300
2. Last ticket that made the cut: Data pipeline, libjpeg-turbo8, takes out 10.
3. First ticket that missed: Search, libunistring2, would take out 9.
4. Chart on slide 2, one pair of bars per estate in ticket order (internal tools, media, search, data pipeline, checkout, payments), November's figure beside the open exploitable exposure on 23 October:
   - Internal tools: 2,430 against 2,462 open
   - Media: 2,650 against 2,682 open
   - Search: 2,580 against 2,627 open
   - Data pipeline: 2,480 against 2,539 open
   - Checkout: 1,740 against 4,688 open, annotated 120 hosts
   - Payments: 1,410 against 2,960 open, annotated 96 hosts
   - Title carries the total, 13,300
5. Estate card, median days from first fix release to the ticket's last host (tickets completed since 1 May) and tickets over target:
   - Payments: 22.0 days, 4
   - Checkout: 24.0 days, 3
   - Search: 26.0 days, 7
   - Media: 24.0 days, 1
   - Internal tools: 24.0 days, 3
   - Data pipeline: 23.0 days, 0
6. Estate card, hosts in service on 23 October and hosts with no authenticated scan in the 14 days before:
   - Search: 610 in service, 99 unscanned
   - Media: 870 in service, 149 unscanned
   - Internal tools: 361 in service, 49 unscanned
   - Data pipeline: 696 in service, 92 unscanned

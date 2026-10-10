# solver round: round 1, plain

**Proxy score 93.4 / 100** (recommendation 35.0 of 35, instruction 7.0 of 7, asks 51.4 of 58). Main call LANDED. 6 of 8 ask items cracked (80 per cent of tokens).

## Main call

golden: Give payments 1 ticket, checkout 1, search 76, media 75, internal tools 77 and the data pipeline 70, which takes out 13,360 exploitable host exposures in November.

solver: Sign a November split of 300 tickets as: tools 77, search 76, media 75, data pipeline 70, payments 1 and checkout 1. Santiago wants the bulk on payments, but that can't work. The provider can only drain 3 payments hosts per cycle against the November forecast peak (460 in service, minus 417 needed for 21,684 tps at 52 tps each, minus a 40-host rack). Over 8 cycles and 4 windows that is 96 hosts. Checkout gets 120 the same way (582 − 539 − 40 = 3 per cycle, over 5 windows). One glibc ticket per colocated estate uses all of that capacity, so payments takes out 1,410 exposures on 96 hosts and checkout 1,740 on 120 hosts. Media takes out 2,650, search 2,610, the data pipeline 2,510 and tools 2,430. The split takes out about 13,360 exploitable host exposures in November (exactly 13,362).

tokens matched 2 of 4 (77, 13,360, Give, November)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| november_ticket_cut.csv | 1 | 13 | 14 | 93% |
| november_ticket_cut.csv | 2 | 6 | 11 | 55% |
| ticket_split_review.pptx | 1 | 20 | 20 | 100% |
| ticket_split_review.pptx | 2 | 1 | 1 | 100% |
| ticket_split_review.pptx | 3 | 1 | 1 | 100% |
| ticket_split_review.pptx | 4 | 24 | 26 | 92% |
| ticket_split_review.pptx | 5 | 16 | 17 | 94% |
| ticket_split_review.pptx | 6 | 12 | 16 | 75% |

## Solver's path

1. Exploitable: latest EPSS (2026-10-22) of 0.10 or more, joined from the parquet to the cloud findings by CVE; the scanner's exploit_available flag was ignored. Colocated findings use the EPSS in the JSONL, which is 0.10 or more for all 7,648. Open exploitable exposure: search 2,626, media 2,681, tools 2,460, pipeline 2,547, payments 2,960, checkout 4,688.
2. Cloud tickets: one ticket per estate and package, counting every host in the scanner export (the 262 exposures on standby hosts included). This gives 313 candidates, with no duplicate host/CVE rows.
3. Drain capacity: calibrated against the acknowledgements. Accepted hosts per window = 8 × (hosts_in_service − ceil(peak forecast tps over the window hours / per_host_tps) − 40-host rack), which reproduces the caps of 88, 64 and 24. November: payments 460 − 417 − 40 = 3 per cycle × 8 × 4 windows = 96. Checkout 582 − 539 − 40 = 3 × 8 × 5 = 120 (the window crosses midnight; the peak is 18,326). The YAML ceiling of 7 and the historical 11 per cycle were not used.
4. Colocated take-out: a drained host is rebuilt from the current image. Hosts rebuilt after a CVE's disclosure don't carry it, so draining clears every finding on the host. The best use is the 96 payments and 120 checkout hosts with the most exposures (1,412 and 1,742). All of them carry glibc CVE-2026-24054 (EPSS 0.9712), so each estate needs a single glibc ticket. A second colocated ticket would reach no hosts.
5. Ranked the 2 colocated and 313 cloud candidates by exposures taken out and kept the top 300. The cut falls cleanly between search sudo (9) and media libc6 (8).
6. Estate card: from crew_deployment_log, completion = the last successful run (the is_last_host row). The fix's release date was taken from the log, except for DEP-PAY-0003: its date (2026-05-13) equals the containerd advisory's latest_revision, so it was replaced with first_published (2026-04-22). Kept tickets completed on or after 2026-05-01; days = completion − release; the target is missed when days > 35.
7. Scan coverage: cloud_asset_register power_state = running, joined to scanner_coverage on instance_id (140 renamed media hosts break a hostname join). Covered when last_authenticated_scan ≥ 2026-10-09; a blank counts as not covered.
8. Q3 close-out check: the closed findings scored on the cut date come within ±2 per estate-month of the close-out when an unscored CVE takes its first later score. This confirms the threshold and the score-date convention, but the close-out doesn't reproduce exactly.

confidence: Medium-high on the 300-ticket split (counts per estate, and the 9-versus-8 boundary between search sudo and media libc6). Medium on how many exposures the colocated tickets take out: 1,412 and 1,742 assume a drained host is cleared entirely and that the hosts with the most exposures are drained first. Counting glibc alone would give 96 and 120 exposures, with the same ticket counts. High on the estate card and the scan-coverage figures.

notes: The folder doesn't say which hosts the provider drains. I assumed the hosts with the most exposures go first; the totals don't depend on how ties at 11 (payments) and 12 (checkout) exposures are broken. Except for one ticket, the release dates in the deployment log don't match the advisory feed, so I used the log's dates as given. The Q3 close-out reproduces to within ±2 per estate-month, not exactly.

### november_ticket_cut.csv (solver's answers)
- row count and rank order: 300 rows, ranked by exposures taken out in November (descending), ties broken by the highest EPSS. Rank 1: checkout, glibc, 120 hosts, 1,742 exposures. Rank 2: payments, glibc, 96 hosts, 1,412 exposures. Rank 3: media, dbus, 89 hosts, 89 exposures. Rank 300: search, sudo, 9 hosts, 9 exposures.
- tickets per estate: tools 77, search 76, media 75, data pipeline 70, payments 1, checkout 1; total 300
- hosts reached in November (column totals): payments 96; checkout 120; search 2,612; media 2,652; tools 2,432; pipeline 2,512; total 10,424. For cloud tickets the hosts reached equal the exposures, because each package has one exploitable CVE per host.
- exposures taken out (column totals): payments 1,412; checkout 1,742; search 2,612; media 2,652; tools 2,432; pipeline 2,512; total 13,362

### ticket_split_review.pptx (solver's answers)
- opening split (tickets and exposures per estate, nearest ten): Tools 77 tickets / 2,430; Search 76 / 2,610; Media 75 / 2,650; Data pipeline 70 / 2,510; Payments 1 / 1,410 (96 hosts); Checkout 1 / 1,740 (120 hosts); Total 300 tickets / 13,360 exposures
- last ticket that made the cut: Rank 300: search, sudo, 9 hosts, 9 exposures
- first ticket that missed: Rank 301: media, libc6, 8 hosts, 8 exposures
- chart bars: November take-out vs open exploitable exposure today: In ticket-count order: tools 2,432 of 2,460; search 2,612 of 2,626; media 2,652 of 2,681; pipeline 2,512 of 2,547; payments 1,412 of 2,960 (annotated 96 hosts); checkout 1,742 of 4,688 (annotated 120 hosts). Open total today is 17,962. Title total: 13,360 exposures (exact 13,362).
- estate card: median days from vendor first release to last-host success, tickets completed since 1 May (1 dp): payments 24.0; checkout 28.0; search 23.0; media 25.0; internal tools 26.0; data pipeline 22.0
- estate card: tickets that missed the 35-day target: payments 4; checkout 7; search 4; media 1; internal tools 4; data pipeline 1. Tickets completed since 1 May: payments 30, checkout 21, search 30, media 21, tools 25, pipeline 22.
- cloud hosts in service on 23 Oct and how many had no authenticated scan in the prior 14 days: search 610 in service, 99 without a scan; media 870, 149; internal tools 361, 49; data pipeline 696, 92

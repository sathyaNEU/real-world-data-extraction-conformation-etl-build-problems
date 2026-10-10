# solver round: round 2, plain

**Proxy score 55.3 / 100** (recommendation 3.0 of 35, instruction 7.0 of 7, asks 45.3 of 58). Main call missed. 5 of 8 ask items cracked (80 per cent of tokens).

## Main call

golden: Give payments 4 tickets, checkout 5, search 72, media 75, internal tools 77 and the data pipeline 67, which takes out 13,300 exploitable host exposures in November.

solver: Sign a November split of checkout 1 ticket, payments 1, media 77, data pipeline 68, search 74 and internal tools 79. It takes out about 13,360 exploitable host exposures: checkout 1,740, payments 1,410, media 2,670, data pipeline 2,490, search 2,600 and internal tools 2,450. Payments cannot carry the bulk Santiago asked for. Drain headroom lets it drain only 96 hosts in its four windows (3 hosts at a time × 8 cycles × 4 windows), and a single glibc ticket uses all of that. Checkout has room for 120 hosts across five windows, and its one glibc ticket uses all of that too. Every other ticket goes to cloud packages, down to the 8-exposure tier.

tokens matched 3 of 5 (4, 77, 13,300, Give, November)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| november_ticket_cut.csv | 1 | 6 | 12 | 50% |
| november_ticket_cut.csv | 2 | 5 | 13 | 38% |
| ticket_split_review.pptx | 1 | 15 | 22 | 68% |
| ticket_split_review.pptx | 2 | 1 | 1 | 100% |
| ticket_split_review.pptx | 3 | 1 | 1 | 100% |
| ticket_split_review.pptx | 4 | 21 | 26 | 81% |
| ticket_split_review.pptx | 5 | 16 | 17 | 94% |
| ticket_split_review.pptx | 6 | 15 | 16 | 94% |

## Solver's path

1. Read the prompt, the standard (.docx), the SRE standard, the provider schedule, the drain orchestrator yaml, the planning email and the data dictionary. A finding counts as exploitable when its latest score is at least 0.10. A ticket updates one package and names every host that carries it. Colocated work happens only by draining hosts while keeping one rack (40 hosts) above the forecast peak over the window's hours.
2. Drain capacity: hosts that can drain at once = hosts in service − ceil(window peak tps / per-host tps) − 40. The checkout window runs 22:00–02:00, so hours 0–1 come from the next date. This formula reproduced accepted host totals in all 82 historical windows (88 = 11×8 through September, 24 = 3×8 for payments in October). For November: payments 460 − ceil(21684/52) − 40 = 3, giving 3×8×4 = 96 hosts; checkout 582 − ceil(18326/34) − 40 = 3, giving 3×8×5 = 120 hosts. The yaml limit of 7 parallel drains does not bind.
3. Rebuild check: every drained host has in_service_since equal to its last accepted drain date, and none of its findings predate that date. Hosts drained on 20 and 22 October lack the glibc CVE that every other host picked up from 14 October. So a drain clears all findings on a host. The colocated take-out is therefore all exposures on the 96 (payments) and 120 (checkout) hosts with the most exposures, which comes to 1,412 and 1,742; all colocated provider-feed scores are at least 0.16. One glibc ticket per estate (glibc is the top score at 0.9712, and every chosen host carries it) uses all of that estate's capacity, so any further colocated ticket takes out nothing.
4. Cloud: joined the 215,867 scanner findings to the latest EPSS score (22 October) from the parquet file and kept scores of at least 0.10, ignoring the exploit-available flag. Grouping by estate and package gives 313 candidate tickets with exposures; hosts = distinct hosts carrying the package. Open exploitable exposure today: media 2,682, pipeline 2,539, search 2,627, tools 2,442+20=2,462, plus the colocated estates checkout 4,688 and payments 2,960.
5. Ranked the 2 colocated and 313 cloud tickets by exposures taken out (ties by highest score) and kept the top 300, giving 1 + 1 + 298 cloud. The cut falls exactly between the 8-exposure group (ranks 295–300) and the 7-exposure group (ranks 301–315). Estate totals: 1,742 / 1,412 / 2,668 / 2,490 / 2,599 / 2,448, total 13,359, which rounds to 13,360.
6. Estate card: from crew_deployment_log I took each ticket's last-host row (succeeded) with run_date on or after 1 May (157 tickets in total). Days = run_date − vendor first release. Two log dates match the advisory feed's latest_revision rather than first_published (DEP-SEA-0051 containerd and DEP-SEA-0079 openssl), so I corrected them to first_published; this moves search from 26.0 days and 7 missed to 27.0 and 8. A ticket misses when days exceed 35.
7. Scan coverage: joined the asset register to scanner_coverage on instance_id, because 140 media hosts were renamed and a hostname join would mis-count them. Kept hosts with power_state running and counted those with no authenticated scan on or after 9 October: search 99 of 610, media 149 of 870, tools 49 of 361, pipeline 92 of 696.

confidence: medium

notes: The colocated take-out assumes a drain clears every finding on the host. If a ticket cleared only its own package, payments and checkout would take out 96 and 120 and the total would fall to about 11,160. In that case the ticket counts and the 8/7 cut stay the same. Which tickets sit at ranks 300 and 301 depends on the tie-break by highest score; the 8 and 7 do not. The estate card treats part-accepted colocated change requests as completed tickets, as the log does. If those eight tickets were excluded, payments would read 21.0 days with 2 missed and checkout 24.0 with 2 missed. The Q3 close-out figures did not reproduce exactly under any score-date rule I tried.

### november_ticket_cut.csv (solver's answers)
- row count and order: 300 rows, one per ticket, ranked by the exploitable exposures each takes out in November (descending). Ties are broken by the package's highest latest score (descending), then by hosts
- rank 1: checkout, glibc: reaches 120 hosts in November and takes out 1,742 exposures (the drained hosts are rebuilt, which clears every finding on them)
- rank 2: payments, glibc: reaches 96 hosts in November and takes out 1,412 exposures
- ranks 3 onward: Cloud package tickets. Rank 3 is media dbus (123 hosts, 89 exposures). Next come pipeline openssl (91 hosts, 87), media wget (127 hosts, 87) and search libmount1 (90 hosts, 87). The list runs down to rank 300, media libxml2 (131 hosts, 8)
- tickets per estate: checkout 1, payments 1, media 77, pipeline 68, search 74, tools 79 (total 300)
- exposures per estate in the cut (exact): checkout 1,742; payments 1,412; media 2,668; pipeline 2,490; search 2,599; tools 2,448; total 13,359

### ticket_split_review.pptx (solver's answers)
- opening split, exposures taken out in November to the nearest ten: checkout 1 ticket, 1,740; payments 1 ticket, 1,410; media 77 tickets, 2,670; data pipeline 68 tickets, 2,490; search 74 tickets, 2,600; internal tools 79 tickets, 2,450; total 300 tickets, 13,360
- last ticket that made the cut: Rank 300: media libxml2, 131 hosts, takes out 8 exposures
- first ticket that missed: Rank 301: pipeline libedit2, 107 hosts, would take out 7 exposures. Ranks 295 to 300 all take out 8 and ranks 301 to 315 all take out 7, so the cut falls cleanly between 8 and 7
- chart: November take-out vs open exploitable exposure today, estates in ticket order: checkout 1,742 vs 4,688 (annotated 120 hosts reached); payments 1,412 vs 2,960 (annotated 96 hosts reached); media 2,668 vs 2,682; pipeline 2,490 vs 2,539; search 2,599 vs 2,627; tools 2,448 vs 2,462. Title total about 13,360 taken out (exact 13,359) against 17,958 open today
- estate card: median days from vendor first release to last host, tickets completed since 1 May (1 dp), and tickets that missed the 35-day target: checkout 24.0 days, 3 missed (23 tickets); payments 22.0 days, 4 missed (25); search 27.0 days, 8 missed (31); media 24.0 days, 1 missed (21); internal tools 24.0 days, 3 missed (30); data pipeline 23.0 days, 0 missed (22)
- estate card: cloud hosts in service on 23 Oct and how many had no authenticated scan in the 14 days before: search 610 in service, 99 without a scan; media 870 in service, 149 without; internal tools 361 in service, 49 without; data pipeline 696 in service, 92 without

# DS29 — The p95 latency the CDN writes into next quarter's APAC SLA, when a new site serves only the networks that peer with it

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Product Analytics · edge network latency commitments |
| Mirrors | Committing a regional latency figure after an edge build-out where traffic arrives at a new site only through networks connected there (Cloudflare, Akamai and Google edge expansions, Meta and Netflix edge caches), and nearest-site models overstate the gain |
| Decision shape | One figure committed at a date: the request-weighted p95 latency in the SLA schedule effective 1 October, with the quarter's one new PoP in service |
| Committed call | The SLA p95 in whole milliseconds, with the city of the new PoP it assumes |
| Gap · Pattern | Gap 2 (population) over Gap 1 (time) · E15's quiet second trap (a new site's served population is set by peering, not distance) behind the loud probe-weighting decoy, with a saturated tie (E21) at rung 1 |
| Gate G mechanism | forecasting, with method_or_model_selection |
| Measured traps engaged | #11 beats the headline trap, misses the quiet one · #19 breaks a big tie instead of questioning it · #13 validates on one population, applies to another |
| Calibration form | Pilot log: the six-week trial PoP in city C, with every real-user beacon's client network, serving PoP and RTT |
| Driving force | Users reach a new anycast site only if their network peers with the CDN there. Everyone else keeps the path they had, however close the new site is. The trial PoP's beacons show it absolutely: users of networks peering at the trial site all moved, and the rest none. Nearest-site assignment credits a new PoP with users it will never see, and the city that wins on distance loses on who actually arrives. |

## 1. Situation

A CDN sells an enterprise tier across 14 APAC countries and must put a p95 latency figure into the SLA schedule that takes effect on
1 October. Customers are credited when the quarter's measured p95 exceeds it, so sales wants it low and finance wants it met. One new PoP
goes live in September, in one of four shortlisted cities (A–D). The planning team picked its city on average latency across the
measurement-probe network. A six-week trial PoP ran in city C last spring.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: probe RTTs, real-user beacons, the peering register, the IXP membership lists and the planning
  memo's coverage scores. No stakeholder read is overturned: probe averages do favour A, and the trial site did cut latency for the users
  it served. The difficulty is which users a new site will serve.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the planning team's choice and the coverage scores. User-weighted p95 under nearest-site assignment still
  names C and commits 51 ms.
* **Instrument repair.** No file the ladder uses is suspect: probes, beacons and the exchange member lists are complete, and every beacon
  records its serving PoP. Perfect RTT measurement to every candidate leaves rung 0 on A, rung 1 on B and rung 2 on C at 51 ms, because who
  arrives at a new site is set by route-server peering, a forward population no measurement of today's paths contains.
* **Lens swap.** The naive read and the answer are different populations at a different moment: today's users assigned to their nearest
  site, against next quarter's users on the paths their networks will actually take.

## 3. The driving force

A strong solver ignores the probe average, weights by user requests as the SLA schedule defines, assigns each user to the lowest-RTT PoP
with each candidate added, and takes the request-weighted 95th percentile. That beats the decoy the planning team fell for, and it names C
at 51 ms. But the CDN announces one anycast prefix everywhere, and a user's network decides which site its packets reach. A network that
peers with the CDN at the new site sends its users there. One that reaches the CDN through a transit provider keeps the route that
provider already prefers. The trial at C shows it without exception: every beacon from a network on C's exchange route server, where the
trial site peered, was served at C, and no beacon from any other network was, including the exchange's members that peer only off the
route server. The tail of the APAC distribution is mobile users on three large networks, and they peer at D's
exchange, not at C's. A new site at C reaches 41% of the users nearest-site assignment gives it; at D the figure is 88%.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Probe-weighted mean latency reduction picks the city; p95 over probes, nearest-site service | A; 46 ms (−22.0%) | The planning team's established method on the measurement network everyone uses | The SLA schedule defines the measure as the request-weighted 95th percentile over users |
| 1 | User weighting, then the planning memo's coverage score (countries whose median falls within 60 ms); B, C and D all reach 14 of 14, and the memo's tie-break (cheaper colocation) picks B | B; 53 ms (−10.2%) | The memo's own score and tie-break, now on the right population | The SLA's measure is the 95th percentile, not the median; ranked on it, the tie breaks to C |
| 2 | Request-weighted p95 with each candidate added and every user on the nearest site | C; 51 ms (−13.6%) | Exactly the SLA's measure, with the right weights and the best city | The trial log: beacons from networks without a peering session at C's exchange never reached C |
| 3 | **Decisive:** each network moves to a candidate only if it is on that city's exchange route server; everyone else keeps today's serving PoP; p95 recomputed per candidate | **D; 59 ms** | — | — |

* **Figure shape.** The natural stops land 10% to 22% below the answer. The partial applications (below) land above it, so the answer is
  bracketed, with no cell within 8%.
* **Partial correction priced (L3).** No half-applied construction names D. A solver who applies the peering rule but keeps rung 2's city
  files 64 ms for C (+8.5%), and one who applies it to the tie-broken city files 67 ms for B (+13.6%). A solver who builds catchment from
  the exchange member lists but counts every member, not only those on the route server, credits C with 21 networks that never reached the
  trial site and names C at 53 ms (−10.2%), 1.11× ahead of D, whose exchange has no members off its route server and stays at 59 ms.
* **Grid.** Assignment (nearest site, exchange membership, route-server peering) × city rule (probe mean, coverage tie-break, request p95),
  request-weighted, = 9 cells, plus the cell that fixes C by distance and then prices it under peering. Only route-server peering with the
  p95 gives D and 59 ms. The other cells name A, B or C at 51 to 67 ms, and the nearest are 53 and 54 ms (−10.2%, −8.5%) and 64 ms (+8.5%).
* **Which guard binds.** Under nearest-site assignment C and D sit 1 ms apart (51 against 52), a thin city margin that is harmless:
  either city by distance files 51–52 ms, 12–14% below the answer. For a figure graded to the millisecond the separation floor is the
  guard that binds. What the decisive rung must do is move the figure, and it does: peering gives D 88% of its nearest-site users and C
  41%, a 2.15× edge against a required 1.2 × 1.02 = 1.22 (1.59 with headroom), which carries C to 64 ms and D to 59 ms.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The routing note says the prefix is announced at every PoP. The peering register lists sessions. No document says
   which users a new site will serve.
2. **The control pins it, and nothing else in the pack does.** In the trial log the route-server rule reproduces the serving PoP of
   1,912,400 of 1,912,400 beacons. Nearest-site assignment reproduces 41% of the beacons it sends to C, and every miss runs the same way
   (users credited to C who never arrived), so it fails on the totals as well; counting every exchange member misses the 21 members off
   the route server. The rule is a construction: client networks from the beacons, joined to each city's member list and its route-server
   column, then today's serving PoP for every network that is not on it.
3. **No arithmetic symptom.** Beacons, probes, sessions and request counts reconcile on every rung, and the nearest-site model fits
   today's served RTTs, because today every network already reaches a PoP it peers at or its transit prefers.
4. **Not a row predicate.** Catchment needs the client network of each request, a join to each candidate's exchange membership, and a
   recomputed RTT distribution per country for each candidate.
5. **The enumeration is arithmetic.** Which networks move to which candidate is computed. No column says "would move".
6. **No cutover date.** The trial was a closed window of six weeks, and no series steps at its edges.
7. **Survives deletion.** No wrong number exists to delete. Without the planning team's choice, nearest-site p95 still names C.

## 6. The calibration corpus

* **Form.** The trial log: six weeks of real-user beacons from the 14 countries, each with client network, serving PoP and RTT, while a
  temporary PoP ran in city C.
* **What it pins.** The peering rule (above), absolutely: 100% of beacons from the 37 networks on C's exchange route server were served
  at C, and 0% of beacons from the other 212 networks, whatever their RTT to C, the 21 exchange members off the route server among them.
* **What it does not show.** How D's exchange would draw. D's catchment has to be built from D's membership list.
* **Twin pair.** Two networks in the same country carry the same request share (2.4%), the same probe count and the same median probe RTT
  to C (19 ms). In the trial one was served at 38 ms at the 95th percentile and the other at 77 ms (2.0×): the first peers at C's
  exchange, the second reaches the CDN through a transit provider that prefers the existing northern PoP.
* **Resemblance points at the decoy.** C is the trial city, and its own metro's users were served at 9 ms there, the best figure in the
  file.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The SLA schedule: the commitment is the request-weighted 95th percentile of user RTT over the quarter, with each
  network-country cell's RTT taken as the median of its beacons, rounded to the whole millisecond. The capacity plan: one new PoP this
  quarter, from cities A–D. The planning memo: candidates are scored on countries whose median falls within 60 ms, with ties going to the
  cheaper colocation.
* **Empirical pins.** Catchment by route-server peering, from the trial log and the exchange member lists, each with a route-server
  column. Each network's RTT to a candidate, from probes in that network.
* **Voices.** The head of network planning: "Averages over thousands of probes don't lie." The peering manager: "Every network that
  matters can reach us anywhere." The sales director: "Customers buy the number on the page."
* **Licensed wrong basis.** The planning memo records that the infrastructure council reviews the build on its coverage score and will
  see that table.

## 8. Determinism by construction

* **Quantile.** The schedule fixes the weighted 95th percentile as the smallest RTT at or above which 5% of requests fall. The answer is
  59.3 ms, mid-bin, and interpolated definitions agree to the whole millisecond.
* **Catchment.** The split is absolute, so no fractional-catchment convention arises. No network gains or loses a session at D or C during
  the extract.
* **RTT for movers.** Every moving network has at least 20 probes with RTTs to the candidate's anchor, and median and trimmed-mean
  aggregation give the same p95.
* **Weights.** Request shares come from beacons over the last full quarter; the prior quarter's shares give the same city and the same
  figure.

## 9. Prompt sketch and deliverables

> Sales needs the APAC p95 latency for the enterprise SLA schedule that starts on 1 October, and this quarter's one new PoP goes live
> before then. Our planning team picked the city on average latency across the probe network. Give me the p95 we commit to, in whole
> milliseconds, with the city it assumes, as one line I can put in the schedule. Send `apac_latency_commit.xlsx`, a chart
> `served_latency_cdf.png`, and a one-page `sla_commitment.pdf`.

* `apac_latency_commit.xlsx` — the four candidates under each rung construction (ask C), the cache sheet (ask A) and the transit sheet
  (ask B).
* `served_latency_cdf.png` — the request-weighted RTT distribution today and with each candidate under nearest-site and peering
  assignment, with the 95th percentile marked on each curve, the committed figure labelled and the 60 ms objective drawn.
* `sla_commitment.pdf` — the committed figure and city, and why the nearest-site figure would breach.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 14 countries, last quarter's cache-hit ratio and origin-fetch volume at the PoPs
  that served it. *Device:* tiered caching logs a miss twice, once at the edge and once at the shield with a tier field, as the log
  dictionary documents. Counting log lines as requests understates hit ratios by 4 to 11 points.
* **Ask B (device-carried).** For each of the nine existing APAC PoPs, the 95th-percentile transit egress in each month of the quarter.
  *Device:* each PoP buys transit on two to four ports, and the billing guide sets the percentile on the PoP's summed five-minute series.
  Summing per-port percentiles overstates every multi-port PoP.
* **Ask C (validity).** The committed figure under each of the four rung constructions, and each country's share of requests served by
  D's site under nearest-site and peering assignment.
* **Decoupling.** Clearing the peering rule changes no figure in asks A or B. Edge logs and transit counters never enter the beacon
  distribution.

## 11. Rubric arithmetic

14 countries × 2 (ask A) + 9 PoPs × 3 months (ask B) + 4 rung figures + 14 countries × 2 shares (ask C) + the committed figure, its city
and its margin to 60 ms + 5 named chart parts + 3 files ≈ 98 criteria.

## 12. World-building constraints

* Rung figures 46 / 53 / 51 / 59 ms (−22.0%, −10.2%, −13.6%, answer). Request-weighted p95 by assignment: nearest site A 54, B 53, C 51,
  D 52; membership A 65, B 65, C 53, D 59; route-server peering A 66, B 67, C 64, D 59. No cell a construction files sits within 8% of
  59 ms. C's exchange has 58 members, 37 on the route server; every member of D's exchange is on its route server.
* Trial log: 1,912,400 beacons; 37 networks peer at C's exchange (100% served at C), 212 do not (0%). Three mobile networks carry 31% of
  tier requests, sit in the slowest decile today and peer at D's exchange but not at C's.
* Coverage score: B, C and D reach 14 of 14 under every assignment; A reaches 13. B's colocation is cheapest.
* Today every network's serving PoP is also its lowest-RTT existing PoP, so nearest-site assignment reproduces today's served RTTs exactly
  and only the trial log separates the two rules.
* The twin networks match on every probe and request column.
* Shield log lines and transit ports touch no beacon, probe or peering record.

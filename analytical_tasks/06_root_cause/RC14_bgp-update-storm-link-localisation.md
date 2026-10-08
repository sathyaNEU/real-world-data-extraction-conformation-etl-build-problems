# RC14 — A BGP update storm across thousands of prefixes: which network link actually failed?

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | Network incident localisation at large operators and CDNs (Google, Meta, Cisco, Cloudflare): routing churn floods monitoring, and the noisiest prefixes and peers are victims rather than causes |
| Domain | Internet routing / network operations |
| Task shape | 12 · Drill-down to one leaf (all updates → routing events per peer and prefix → AS links that disappeared from the stable paths → the single autonomous system and link most consistent with the storm) |
| Core method | Parse MRT RIB dumps and update files from public route collectors; group updates into routing events per (peer, prefix) with a quiet-time rule; compare each event's stable path before and after; candidate cause links = adjacencies in the old path absent from the new one; greedy set cover over links weighted by events explained and confirmed by many distinct peers; report the AS common to the covering links |
| Analytical stump | Counting updates by prefix, origin AS or peer points at whoever had the most path exploration — prefixes with many alternate paths and peers with many transient routes — and the origin ASes of the noisiest prefixes are victims. One failed link produces many updates per event and many events per prefix. Only before/after stable paths aggregated across vantage points localise the failure |
| Primary sources | RIPE NCC Routing Information Service (RIS) raw MRT data; University of Oregon RouteViews MRT archives |

## 1. The real-world situation

A content provider's network operations centre saw a burst of BGP churn for two hours and degraded reachability to several regions. The on-call
engineer's dashboard ranked origin ASes by update count; the top three were large access networks, so tickets were opened with them. Post-incident,
the head of networking asked for an evidence-based localisation of the link or network that actually failed, to decide which provider gets the
escalation and the SLA claim.

## 2. The decision (one deterministic recommendation)

**The autonomous system named as the root-cause location (with its most implicated link), the share of routing events the covering links explain,
and the number of distinct peers that observed them.**

Rules (NOC memo):

* Data: RIB dump at window start and all update files for the memo's incident window (UTC) from the memo's RIS and RouteViews collectors; IPv4
  unicast only.
* Path normalisation: collapse prepending (consecutive duplicate ASNs); drop paths with AS-SETs; drop private and reserved ASNs from paths.
* Events: per (collector, peer, prefix), consecutive updates ≤ 240 s apart form one event.
* Old path = the path in effect immediately before the event (from the RIB plus earlier updates); new path = the path in effect at the end of the
  event, or "withdrawn".
* Candidate links of an event: AS adjacencies in the old path that are absent from the new path (all old-path links if withdrawn). Events whose old
  and new paths are identical are excluded as churn without change.
* Link score: number of events whose candidate set contains the link; eligible only if those events come from ≥ 10 distinct peers.
* Greedy set cover: pick the eligible link with the highest score; remove its events; repeat until ≥ 80% of events are covered or no eligible link
  remains.
* Root-cause AS: the ASN appearing in the most covering links (ties: the one in the first-chosen link).

## 3. Why capable analysts get it wrong

* Update volume is the metric on every dashboard.
* Path exploration multiplies updates per event and is uneven across prefixes and peers.
* The failed link is an interior adjacency; the origin of the noisiest prefixes is not where it broke.
* One vantage point sees only its own paths; localisation needs many peers.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `rrc*/bview.<start>.gz` | MRT (binary) | ~1M routes per peer set | RIPE NCC RIS raw data | RIPE NCC RIS data terms (free use with attribution; verify) | RIB at window start |
| 2 | `rrc*/updates.<time>.gz` | MRT | ~2M updates | RIPE NCC RIS | Same | Updates during the window |
| 3 | `routeviews/<collector>/updates.<time>.bz2` | MRT | ~1M updates | RouteViews | Free for research and operational use with attribution (verify) | Additional vantage points |
| 4 | `asn_names.csv` | CSV | ~100k | RIPE NCC / CAIDA AS names (public listing; verify) | Verify | ASN labels for reporting |
| 5 | `noc_memo.pdf` | PDF | — | Task author | — | Rules in §2, collectors and window |
| 6 | `oncall_dashboard_export.xlsx` | XLSX | ~50 | Task author (update counts by origin AS) | — | On-call ranking |
| 7 | `provider_postmortem_citation.pdf` | PDF | — | Public post-incident report for the chosen incident (cite) | Cite | Validation only |

## 5. Deterministic solution path

1. Decode MRT files (bgpdump or pybgpstream); normalise paths; build per-peer RIB state.
2. Group updates into events; derive old and new paths; drop no-change events.
3. Compute candidate links and link scores with the peer-diversity rule.
4. Run the greedy cover; name the root-cause AS and link; report coverage.
5. Contrast with the on-call ranking; validate against the cited post-incident report.

## 6. Wrong paths (method errors, not misreadings)

**A — rank origin ASes or prefixes by update count.** Picks victims with the richest path exploration.

**B — rank peers by update count.** Picks the vantage point with the most transient paths.

**C — links in the new paths.** Identifies the detour that absorbed traffic, not the failure.

**D — no event grouping.** Every transient path during exploration contributes "removed" links, inflating unrelated adjacencies.

## 7. Why the stump is analytical, not semantic

ASN names play no role in the method; the windows, rules and scoring are fixed. The trap is treating message volume as evidence of cause rather than
reconstructing state changes across vantage points.

## 8. Draft task prompt (prose)

> During yesterday's routing storm our dashboard pointed at three access networks. Use the NOC memo's method on the public collector data to find
> where the failure actually was. Provide `link_cover.csv` (link: events explained, peers, order chosen), `storm_localisation.png`, and a one-page
> `routing_incident_rca.pdf`.

## 9. Deliverables

* `link_cover.csv` — eligible links with scores and the cover sequence.
* `storm_localisation.png` — AS-level graph of covering links, sized by events explained, with the root-cause AS highlighted.
* `routing_incident_rca.pdf` — conclusion, coverage, and why the dashboard ranking misled.

## 10. Where 25+ rubric criteria come from

* Parsing and normalisation counts (updates, events, no-change events dropped): 5.
* Top covering links with scores and peer counts: 9.
* Coverage achieved and number of links: 2.
* Root-cause AS and link: 2.
* Dashboard contrast (rank of the true AS in update counts): 2.
* Validation against the post-incident report: 2.
* Visual elements: 3+.

## 11. Golden-output checklist

* Prepending collapsed; AS-SETs and private ASNs removed.
* 240 s event rule per (collector, peer, prefix).
* Old/new stable paths; removed-link candidates; ≥ 10 peers.
* Greedy cover to 80%; tie rules.

## 12. Build notes (scope tuning)

* Choose a transit-provider incident with a public post-incident report, in which the top origin ASes by update count are customers of other
  networks. Confirm that the cover's first link involves the reported provider and that the dashboard's top three origins are not in any covering
  link.

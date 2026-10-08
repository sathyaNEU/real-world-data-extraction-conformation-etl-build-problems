# RC14 — Which provider gets the escalation and the SLA claim for the routing storm, when one provider's planned drain ran through the same two hours

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Product Analytics · network reliability and incident response |
| Mirrors | Network incident localisation at large operators and CDNs (Google, Meta, Cisco, Cloudflare), where one provider's planned maintenance and another's failure overlap inside a single storm of routing churn |
| Decision shape | Which of N root causes gets the fix: one escalation, with the SLA claim, to one network |
| Committed call | The network and link the escalation names, and the affected prefixes its failure explains |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · E29 (a mixed segment split through a join: path changes on the transit link divided by the drain community the withdrawn routes carried), inside a reproduction-gated control set (Pattern B), with E25 (a suppressed cell, bounded) at rung 2 |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution |
| Measured traps engaged | #6 treats a mixed segment all one way · #24 treats an unpublished figure as unknown · #1 reports a failed back-test, ships anyway |
| Calibration form | Published control set with a reproduction clause: sixteen certified incidents, each with its root-cause link and affected-prefix count |
| Driving force | Every path change on the first transit provider's link is recorded the same way, and four in ten of them were planned. The provider drained that link for maintenance during the storm, tagging the routes with its maintenance community before withdrawing them. The SLA contract excludes notified maintenance; only the community on the withdrawn route, read through the provider's published community list, separates drain from failure. With the drain removed, the second provider's backbone link explains the storm, once its observing peers are counted from the collector's suppressed cell. |

## 1. Situation

A content provider saw a two-hour burst of routing churn and degraded reachability to several regions. The on-call dashboard ranked origin networks by
update count and tickets went to two access networks. The head of networking will escalate to one network, with an SLA claim, and fix traffic
engineering around its failed link: access network X (A), access network Y (B), transit provider T1's link at the exchange (C), transit provider T2's
backbone link in the southern region (D), or the content provider's own edge router, whose session reset during the storm (E). The NOC runbook
governs how a localisation supports a claim, and its incident record certifies sixteen past localisations.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the collectors' updates, the dashboard's counts, the providers' community lists, the collector's
  published peer summaries and the certified incidents. T1's link did change state and T2's did fail; nothing reported is overturned. The
  decision turns on which state changes were failures.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the dashboard, the on-call engineer's tickets and the licensed basis. The removed-link cover on the collector data
  still names T1's link, with every event counted alike.
* **Instrument repair.** Perfect collectors record the same withdrawals with the same communities; the drain is real routing, not noise. The
  split is a reading of the contract against an attribute, not a gap in the data.
* **Lens swap.** The naive cover attributes every withdrawal on T1's link to a failure; the answer removes the planned ones, so the failure
  population behind the storm is a different set of events.

## 3. The driving force

A strong solver ignores update counts, groups updates into events per peer and prefix, finds the links each event removed, and covers the
events greedily with links seen by at least ten peers. One link is seen by only seven named peers, because the regional collector suppresses
counts for its confidential peer group. Its published total of thirteen, minus the seven named, puts six in the suppressed cell, so the link is
eligible. With every eligible link in, T1's exchange link covers the most events. The SLA contract excludes maintenance notified in advance, and
T1 drained that link during the storm. It tagged the routes with its maintenance community before withdrawing them, as its published community
list documents. That community sits on the route that was withdrawn, so it is read from the previous announcement through the community list,
not from anything on the withdrawal itself. 62% of T1's events were drains. Without them T2's backbone link explains 4,900 affected prefixes,
T1's own failures 2,300.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Updates per origin network, the dashboard's ranking | A, access network X (412k updates) | It is the on-call view and the counts are exact | The certified incidents: update counts name the certified link in 2 of 16, always a victim with rich path exploration |
| 1 | Updates grouped into events; the links each event removed; greedy cover without a peer threshold | B, access network Y's uplink (5,400 prefixes) | Path state, not message volume, as the runbook's localisation section describes | B's events come from two peers; the certified record reproduces 7 of 16 with no threshold and never certifies a link seen by fewer than ten peers |
| 2 | The cover restricted to links seen by at least ten peers, the suppressed peer cell bounded from the published total | C, T1's exchange link (6,100) | Eligibility applied exactly, no peer left uncounted, 11 of 16 incidents reproduce | T1's community list: 62% of its events carried its maintenance community on the withdrawn route |
| 3 | **Decisive:** path changes on each link split by the community on the withdrawn route, planned drains removed under the contract's exclusion | **D, T2's backbone link (4,900)** (5th of 5 on rung 0) | — | — |

* **Position table.** D ranks 5th on rung 0, 3rd on rung 1 and 2nd on rung 2, 1.30× behind T1, and leads only rung 3. Rung leaders beat their
  runners-up by 1.58×, 1.32×, 1.30× and 1.88×.
* **Discriminator dominance.** T1 carries a 1.30× lead into rung 3 (6,100 against 4,700). The failure share of each link's events is 0.38 for
  T1 and 1.0 for T2 (which also picks up events T1's drains had claimed), an edge of 2.77×, above the required 1.2 × 1.30 = 1.56; the net margin
  is 2.13×.
* **Partial correction priced (L3).** A solver who looks for the maintenance community on the route after the change rather than on the route
  withdrawn finds it on 9% of T1's events, because a withdrawal has no new route, and still names C at 5,800. Removing T1's events inside the
  notified window alone misses the drains that began 40 minutes early and also names C.
* **Grid.** Signal (counts, cover) × eligibility (none, suppressed cell as zero, bounded) × drains (kept, split) gives seven feasible builds.
  They name A, B, C, C, B, E and D: splitting the drains while reading the suppressed cell as zero leaves T2's link ineligible and names the
  content provider's own router (2,600). Only the bounded, split build names D.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The SLA contract excludes notified maintenance; T1's community list defines its maintenance community; the runbook
   describes the cover. No document connects them or says the community is read on the withdrawn route.
2. **The control set pins a construction, not a menu.** The bounded, split cover reproduces 16 of 16 certified links and affected-prefix
   counts; the bounded cover without the split 11, the split with the suppressed cell read as zero 14, the unrestricted cover 7. Every rival's
   misses over-attribute to a network that was maintaining or under-observed, so none reconciles on the sixteen-incident total either. The
   split is a join from each event's previous announcement to a provider's community list, not a parameter.
3. **No arithmetic symptom.** Updates, events, peers and prefixes reconcile under every build; drains and failures produce identical
   withdrawal records.
4. **Not a row predicate.** The community is not on the withdrawal row; it is on the last announcement before it, found by ordering each
   peer-prefix's updates and stepping back.
5. **The enumeration is arithmetic.** Which of T1's events were drains is built across two records and a dictionary; no column marks them.
6. **No cutover date.** Both changes sit inside the same two hours; the dated event (the edge router's session reset at 14:12) is the decoy.
7. **Survives deletion.** With every voice gone, the eligible cover still names T1.

## 6. The calibration corpus

* **Form.** The NOC's certified incident record: sixteen closed incidents, each with its window, the certified root-cause link and the
  affected-prefix count, the collector data for each window, and the runbook's clause that a localisation supports an SLA claim only if its
  method reproduces every certified incident.
* **What it pins.** The construction (above), including the bounded suppressed cell, which decides eligibility in two incidents, and the drain
  split, which decides five.
* **Twin pair.** Incidents INC-04 and INC-12 are identical on update count, event count, observing peers, duration, region and the providers
  involved. Their certified affected prefixes are 4,100 and 2,000 (2.05×), because half of INC-12's path changes on the certified link were a
  provider's drain. Only the community split reproduces both.
* **Resemblance points at the decoy.** This storm's profile matches INC-07, a certified T1 exchange-link failure, on region, duration and the
  shape of the update burst.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The runbook: the escalation and SLA claim go to the network whose failed link explains the most affected prefixes, on a
  method that reproduces every certified incident. The SLA contract: maintenance notified in advance is excluded. T1's published community
  list.
* **Empirical pins.** The cover and the eligibility rule, from the certified record; each event's community, from the previous announcement.
* **Voices.** The on-call engineer: "Access network X lit up the dashboard for two hours; that's where it broke." The peering manager: "T1's
  exchange link is the one that always goes; I'd bet the claim on it."
* **Licensed wrong basis.** The runbook records that T1's account team localises incidents by withdrawals per link without regard to
  communities and will present that analysis when the claim is discussed.

## 8. Determinism by construction

* **Events.** Updates for one peer and prefix less than 240 seconds apart form one event; no gap in the window falls between 200 and 300
  seconds.
* **Eligibility.** Ten distinct observing peers; the suppressed cell is the published total minus the named peers, and no link sits at nine,
  ten or eleven by either count except T2's (seven named, thirteen total).
* **Communities.** Every withdrawn route's previous announcement is in the window or the dump that opens it; T1's maintenance community has one
  value.
* **Cover.** Greedy by events explained to 80% coverage; ties do not occur at any step.
* **Rounding.** Affected prefixes to the nearest hundred; the committed figure sits mid-bin.

## 9. Prompt sketch and deliverables

> After yesterday's routing storm I'm escalating to exactly one network, with the SLA claim, and the on-call team has already ticketed the two
> access networks. Tell me which network and link we escalate to and how many affected prefixes its failure explains, to the nearest hundred, in
> one sentence for the claim letter. Send `storm_localisation.xlsx` and a chart `link_cover.png`.

* `storm_localisation.xlsx` — the five candidates under each construction, the peering-session sheet (ask A), the latency sheet (ask B) and
  the certified-incident reproduction (ask C).
* `link_cover.png` — a network graph of the eligible links sized by affected prefixes, T1's link drawn split into drain and failure segments,
  the observing-peer count printed on each link, and the escalated link highlighted.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the content provider's 18 peering sessions, session flaps and total down-minutes over the
  last 30 days. *Device:* a session that drops and re-establishes inside the router's dampening interval is logged as one flap with a
  suppressed-reflap counter, as the router's log format documents; counting log lines understates flaps on the four busiest sessions.
* **Ask B (device-carried).** For each of the 12 serving regions, median and 95th-percentile round-trip time to users in the storm window and
  the same window a week earlier. *Device:* the measurement agents report in batches with the batch time, not the probe time, and each row
  carries the probe offset, as the agent schema documents; using the batch time shifts probes across the window edge.
* **Ask C (validity).** For each of the sixteen certified incidents, the certified link and prefixes and what each of the four constructions
  returns; and each candidate's prefixes under each construction.
* **Decoupling.** Clearing the community split and the suppressed-cell bound changes no figure in asks A or B.

## 11. Rubric arithmetic

18 sessions × 2 figures (ask A) + 12 regions × 2 windows × 2 percentiles (ask B) + 16 incidents × 4 constructions + 5 candidates × 4
constructions (ask C) + the escalated network, its prefixes and the runner-up's + 4 named chart parts + 2 files ≈ 175 criteria.

## 12. World-building constraints

* Prefixes explained by rung (A / B / C / D / E): counts 412k / 260k / 150k / 90k / 180k updates; 1,200 / 5,400 / 4,100 / 2,900 / 2,600;
  1,200 / ineligible / 6,100 / 4,700 / 2,600; 1,200 / ineligible / 2,300 / 4,900 / 2,600.
* 62% of T1's events carried its maintenance community on the withdrawn route; T1's drains began 40 minutes before its notified window.
* T2's link: 7 named observing peers, 13 in total.
* INC-04 and INC-12 identical on every incident-summary column.
* Dampened re-flaps and probe offsets touch no collector update, community or peer summary.

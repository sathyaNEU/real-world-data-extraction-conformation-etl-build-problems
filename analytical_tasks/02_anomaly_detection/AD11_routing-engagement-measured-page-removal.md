# AD11 — Which customer gets next quarter's one routing-hygiene engagement, when the pages it removes are the ones the revision log has already measured

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Product Analytics · network operations at a cloud platform |
| Mirrors | Spending one remediation where it removes the most alert noise, measured from past remediations rather than assumed (alert-noise programmes in AWS and Google SRE teams, route-origin hygiene at CDNs, rule tuning in payment-fraud monitoring) |
| Decision shape | Which of N gets one scarce thing: network engineering's single routing-hygiene engagement next quarter |
| Committed call | The one customer engaged, and the pages a quarter the engagement removes |
| Gap · Pattern | Gap 4 (rule) over Gap 1 (time) · change-log natural experiments (E26): the engagement's effect measured from fourteen closed engagements, with a mixed segment split through a join at the lower rung (E29) |
| Gate G mechanism | method_or_model_selection, with forecasting support |
| Measured traps engaged | #25 assumes an effect the log could measure · #6 treats a mixed segment all one way · #7 uses the ready-made measure |
| Calibration form | Retry or revision log: the routing-policy revision log, every ROA and filter revision since 2023, with fourteen closed engagements and each customer's pages 90 days either side |
| Driving force | Publishing a customer's ROAs makes the origins it authorises valid and every other origin invalid, and invalid origins still page. The revision log's fourteen engagements show what that does: an engagement removes exactly the pages from origins that recurred on two or more days in the prior 90 days, the customer's own multi-homing and scrubbing origins, and leaves one-off origins paging, sometimes more than before. The rule of thumb that ROAs clear not-found pages ranks customers by not-found pages; the measured rule ranks them by recurring-origin pages, a count over origin-days no field carries. |

## 1. Situation

A cloud platform's network engineering team has one routing-hygiene engagement next quarter: it works with one customer to publish ROAs
for the customer's prefixes and align our filters. The NOC's paging policy pages on origin-change events for monitored prefixes: on RPKI
invalid at 5% visibility, or on not-found at 10% visibility lasting five minutes. The engineering plan judges an engagement by the pages it
removes over the following quarter. Eight customers are candidates. The pack carries the pager log, the origin-change events, the RIR
delegation file, the monitored-prefix list and the revision log.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: each page, each event's origin and visibility, every delegation and every logged revision. The
  engineering lead's rule of thumb is right about what an ROA does to a not-found origin. Nothing reported is overturned; the difficulty is
  that the engagement's effect on pages has already been measured fourteen times and differs from what the rule of thumb implies.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the lead's rule of thumb. Ranking the actionable not-found pages, the natural reading of what ROAs fix, still
  names C.
* **Instrument repair.** No file the ladder uses is defective. The one field open to doubt is the monitored-prefix list's customer label,
  which marks the customer a prefix is monitored for, not who holds it; relabelled by holder from the RIR file, rung 0 becomes rung 1 and
  names B (1,390), rung 1 still names B and rung 2 still names C (1,040). The pager log, the events, the delegations and the revision log
  are complete. No row records which origins a customer will authorise, which its ROAs state only after an engagement, so the recurrence
  rule measured from the fourteen engagements is still needed for E.
* **Lens swap.** The naive read counts last quarter's pages; the answer counts the pages that will not occur next quarter, a different moment
  and, within each customer, a different population of origins.

## 3. The driving force

A strong solver ranks customers by pages, notices that pages on prefixes we sub-allocate are fixed by our own ROA team without an
engagement and drops them, then applies what ROAs do: a not-found origin becomes valid or invalid, so the engagement removes the not-found
pages and leaves the invalid ones. That names C, and it is a sound reading of RPKI. The revision log holds the experiment run fourteen
times. After each engagement the pages from origins the customer authorised disappeared, and the origins it authorised were the ones that
had recurred: its own second ASN, its scrubbing provider, its backup transit. One-off origins, leaks and fat-fingers, turned from not-found
to invalid, and since invalid pages at a lower visibility, they kept paging or paged more. C's not-found pages are 63% one-off origins from
a stream of leaks; E's are 93% its own two ASNs flapping. Reading the log as experiments, and splitting each customer's pages by whether
the origin recurred on two or more days in the 90 days before, is the step nothing invites.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Pages last quarter on each customer's monitored prefixes | A (1,840) | The pager is what the engagement is meant to quiet | The runbook: prefixes we sub-allocate are covered by our own ROA team's quarterly run, and 72% of A's pages fall on them |
| 1 | Pages on prefixes the customer holds itself, split from the uniformly labelled list through the RIR delegation file | B (1,390) | The segment the engagement can act on, identified prefix by prefix | The pager log: 60% of B's pages are already RPKI invalid, origins B's existing ROAs refuse, and an engagement changes nothing for them |
| 2 | Not-found pages on customer-held prefixes, all assumed removed | C (1,040) | Exactly what an ROA does to a not-found origin, and the engineering lead's rule | The revision log: across fourteen engagements, not-found pages fell by between 31% and 98%, and three customers paged more afterwards |
| 3 | **Decisive:** the effect measured from the fourteen engagements, pages from origins seen on two or more days in the prior 90 days, applied to each candidate | **E (640)** (5th of 8 on rung 0) | — | — |

* **Position table.** E ranks 5th on rung 0 (930), 4th on rung 1 (900) and 3rd on rung 2 (690), and leads only rung 3, 1.36× D. Intermediate
  leaders hold margins of 1.25×, 1.24× and 1.25×.
* **Discriminator dominance.** C carries a 1.51× advantage over E into rung 3 (1,040 against 690). The measured effect keeps 640 of E's
  pages and 380 of C's (93% and 36.5%), an edge of 2.54 against the 1.2 × 1.51 = 1.81 required, 1.40× headroom; E leads C by 1.68×.
* **Partial correction priced (L3).** A solver who measures the engagements' pooled effect, 58% of not-found pages, and applies it to every
  candidate keeps rung 2's order and names C (603 against D's 483, 1.25×). A solver who counts recurrence over the base quarter instead of
  the 90 days before each page names D (790 against E's 640, 1.23×), because D's leaking neighbour repeats each mistake once within the
  quarter and two days in a quarter pass where one prior day does not. Neither half lands on E.
* **Grid.** Prefix scope (all or customer-held) × effect (all pages, not-found, pooled rate, recurring origins) gives eight cells. All-prefix
  cells name A or C; customer-held cells name B, C, C and E. Only customer-held prefixes with the measured recurring-origin effect name E,
  and the nearest wrong construction, recurrence counted over the quarter (D), needs only the lookback taken from the wrong window.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The revision log records revisions and page counts; no document states what an engagement removes, and the runbook
   describes ROA publication without mentioning recurrence.
2. **The corpus pins a construction, not a menu.** The recurring-origin rule reproduces the pages removed in 14 of 14 engagements within 5%;
   the not-found rule 4 of 14 and the pooled rate 6 of 14, both over-predicting every miss, so both over-state the log's total removal (by
   41% and 18%). The rule is a construction: an origin's recurrence is a count of distinct days per prefix and origin over a window before
   each page, and no field carries it.
3. **No arithmetic symptom.** Pages tie to events, events to the collectors, delegations to the RIR file; every rung reconciles.
4. **Not a row predicate.** It needs, for every page, the count of distinct days its origin announced that prefix in the preceding 90 days: a
   self-join on prefix and origin over time, then a sum per customer.
5. **The enumeration is arithmetic.** Legitimate origins appear on at least ten days in any 90; a leaked origin appears on one day, or on
   two when the leaking network repeats itself, so it never has more than one prior day. Every threshold from two to nine prior days, and
   lookbacks of 60 to 120 days, select the same pages.
6. **No cutover date.** The engagements are past experiments at fourteen different dates; the candidates' pages are steady through the
   quarter, and no series steps.
7. **Survives deletion.** With every voice removed, the answer and the difficulty are unchanged.

## 6. The calibration corpus

* **Form.** The routing-policy revision log: every revision to customer ROAs and our filters since January 2023, timestamped, among them
  fourteen closed engagements, each with the customer's pages in the 90 days before and after.
* **What it pins.** Pages removed equal the pre-engagement pages from origins that recurred on two or more days in the prior 90 days, 14 of
  14 within 5%. Three engagements show more pages afterwards, all at customers whose not-found pages were mostly one-off.
* **Twin pair.** Engagements R-06 and R-11 are identical on pages before (410), not-found pages (330), prefixes, customer type and median
  visibility. R-06 removed 212 pages and R-11 104 (2.04×); R-06's not-found pages came from its own backup transit, R-11's from a run of
  leaks.
* **Every rule exercised.** One engagement's customer added a scrubbing provider during the window, so the 90-day lookback is tested; one
  customer's prefixes were partly sub-allocated, so the scope split is tested.
* **Resemblance points at the decoy.** By page volume and not-found share, C most resembles the two engagements with the largest removals.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The engineering plan: an engagement is judged by the pages it removes over the following quarter. The runbook: prefixes we
  sub-allocate are covered by our own ROA team's quarterly run. The paging policy's thresholds.
* **Empirical pins.** The recurring-origin effect and its window, from the revision log.
* **Voices.** The engineering lead: "ROAs turn not-found pages into valid ones; that's the whole effect." The NOC manager: "Whoever pages
  us most is who we should be fixing."
* **Licensed wrong basis.** The plan records that the RPKI vendor's account team sizes engagements by not-found pages and will present that
  sizing at the planning review.

## 8. Determinism by construction

* **Recurrence.** The empty band between one and nine prior days makes the threshold and lookback immaterial.
* **Quarter.** The base quarter is the last complete one; the following quarter's page rate is stationary for every candidate, so pages a
  quarter carry forward without a trend convention.
* **Scope.** No prefix changed holder in the RIR file during the window.
* **Pages.** One page per event under the policy's de-duplication; the pager log carries the event ID, so counting pages is a key count.

## 9. Prompt sketch and deliverables

> Network engineering has one routing-hygiene engagement for next quarter, and it goes to one customer. Our engineering lead says ROAs
> simply turn not-found pages into valid ones. Tell me the customer and how many pages a quarter the engagement takes off the pager, in one
> line for the quarterly plan, with `engagement_choice.xlsx` holding the sheets below, the chart `page_removal.png`, and a short
> `quarterly_plan_note.md`.

* `engagement_choice.xlsx` — the customer build, the session-flap sheet (ask A), the traffic sheet (ask B) and the engagement back-test (ask C).
* `page_removal.png` — the fourteen engagements' predicted against actual pages removed under the not-found and recurring-origin rules, with
  the three that paged more marked, beside the eight candidates' expected removals, the chosen customer highlighted.
* `quarterly_plan_note.md` — the committed customer, the pages removed, and why the pager's leader and the not-found reading are not it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each candidate, BGP session flaps on our edge last quarter and total minutes down. *Device:* a
  router with two routing engines logs each session event from both engines under different engine IDs, as the router logging guide
  documents. Counting messages doubles every flap on the four customers attached to dual-engine routers. The paging build never reads
  session syslog.
* **Ask B (device-carried).** For each candidate, last month's 95th-percentile inbound traffic in Gbps. *Device:* a customer on an aggregated
  link is billed on the percentile of the summed 5-minute samples, per the billing guide. Summing each port's own percentile overstates the
  three customers on aggregated links.
* **Ask C (validity).** For each of the four rung bases, the engagements whose pages removed it reproduces within 5%, out of 14.
* **Decoupling.** Clearing the recurrence construction changes no figure in asks A or B.

## 11. Rubric arithmetic

8 customers × 2 (ask A) + 8 customers × 2 (inbound and outbound, ask B) + 4 bases (ask C) + the committed customer, its pages removed and the
margin over D + 5 named chart parts + 3 files ≈ 47 criteria.

## 12. World-building constraints

* Rung leaders are A, B, C, E. E is 5th / 4th / 3rd / 1st; intermediate margins are at least 1.24×; E leads rung 3 by 1.36×.
* A's pages fall 72% on sub-allocated prefixes; B's are 60% already invalid; C's not-found pages are 63% one-off origins; E's are 93%
  recurring (its own two ASNs).
* Legitimate origins announce on at least ten of any 90 days; leaked origins on one day, or two when the leak repeats (D's neighbour).
* Rung 2: C 1,040, D 832, E 690. Rung 3: E 640, D 470, C 380. Recurrence counted over the quarter: D 790, E 640.
* The log holds fourteen engagements; three paged more afterwards; R-06 and R-11 are identical on every pre-engagement column.
* Session syslog and billing samples never touch the pager log or the event feed.

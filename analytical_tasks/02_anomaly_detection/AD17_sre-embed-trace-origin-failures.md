# AD17 — Which service gets next quarter's SRE embed, when the failures users see are returned by one service and caused by another

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Product Analytics · site reliability engineering |
| Mirrors | Embedding reliability engineers where user-facing failures originate rather than where they surface (Google SRE engagements, AWS service-team operational reviews, dependency-attributed incident reviews at Meta) |
| Decision shape | Which of N gets one scarce thing: two SREs embedded with one service for a quarter |
| Committed call | The one service the SREs embed with, and the failed user requests the embed should remove next quarter |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · S7, every screen is right and the answer is what nothing flags (E11), at call-chain grain, with Pattern B (the existing book pins the trace construction) and a catalogue flag overridden by a two-hop route join at the lower rung (E33) |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #5 takes the population a flag or filter suggests · #1 reports a failed back-test, ships anyway · #18 joins only on the visible key |
| Calibration form | Existing-book actuals: the ten past embeds, each with the service embedded and the measured fall in failed user requests the quarter after |
| Driving force | Every per-service screen counts a failure at the service that returned it, so a timeout is booked to the caller whose deadline expired. The internal session cache, which the catalogue marks internal and whose own SLO is green, stalls during eviction storms, and the requests it serves late succeed in its logs and fail in four callers'. Walking each failed request's trace to the innermost span still open at the deadline credits those failures to the cache, and only that attribution reproduces what past embeds actually removed. |

## 1. Situation

A consumer platform can embed two site-reliability engineers with one service for next quarter. The SRE charter judges an embed by the
fall in failed user requests over the following quarter. The SLO dashboard exports, per service, error-budget consumption, burn-rate pages,
latency-SLO breach minutes, saturation alerts and on-call toil, each correct for last quarter and labelled as such, and each high somewhere
for a documented reason. The pack carries the dashboard export, the incident register, the service catalogue, the API gateway's route
table, the public facade's forwarding map, last quarter's traces (every failed request is traced in full), and the book of past embeds.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: every budget, page, breach, alert and trace, and every realised result in the book. Each high flag
  has a documented legitimate cause. The SRE lead's reading of the error budget is a correct reading of it. Nothing reported is
  overturned; the answer is a population, chains of calls, that the dashboard's per-service grain cannot express.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the SRE lead's preference and the dashboard export. Counting failed requests by the service that returned them,
  the natural build from the gateway logs, still credits the cache's failures to its callers.
* **Instrument repair.** Suspect file: the service catalogue's user-facing flag, which marks a service, not a request, and misses two
  internal services reachable through the facade. Corrected for those two, rung 1 still names B (410,000); replaced by a label on every
  request saying whether it entered on a public route, rung 1 becomes rung 2 and names C (390,000). Rung 0 still names A (212%) and rung 2
  C. The dashboard, gateway logs, route table, forwarding map and traces are complete, and no field claims to record where a failure began,
  so the innermost-open-span walk is still needed for E.
* **Lens swap.** The naive read groups failed requests by returning service; the answer groups them by the innermost span open at the
  deadline, a different population for each service: the cache owns 520,000 failures it returned almost none of.

## 3. The driving force

A strong solver discounts the payments API's budget burn to a documented processor outage, restricts to user requests because the charter
counts user failures, and finds that the catalogue's user-facing flag does not define them: a user request is one that enters on a public
route, and public routes reach services through the gateway's route table or, two hops on, through the facade's forwarding map. It ranks
services by the user failures they returned. That names the mobile gateway, and each step is competent. But the dashboard and the
gateway logs book a failure where it surfaced. The session cache serves every authenticated call. During eviction storms it answers
slowly and successfully, so its own availability SLO stays green, while four callers hit their 1.5-second deadlines and return 504s. A
trace records every hop: walking each failed request's span tree to the innermost span still open when the outermost deadline expired
moves 520,000 failures to the cache. Nothing in the pack invites a tree walk, and the book of past embeds reproduces only under it.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Error-budget consumption last quarter, all services | A, payments API (212% of budget) | The SLO policy's own headline and the dashboard's first column | The incident register: 81% of A's burn was one documented outage at the external card processor, since resolved |
| 1 | Failed user requests returned at the edge by the services the catalogue flags user-facing, documented external incidents excluded | B, search API (410,000) | The charter counts user failures, and the catalogue says which services serve users | The gateway's route table joined to the facade's forwarding map: 46% of B's failures came from internal batch callers that never touch a public route, and two services the catalogue marks internal sit behind public facade paths |
| 2 | Failed user requests, those entering on a public route through the gateway or the facade's map, by the service that returned them | C, mobile gateway (390,000; 1.30× F) | The charter's population, built by the route join, every failure counted once | The book of past embeds: failures by returning service reproduce 5 of 10 realised falls and overstate the book's total by 46% |
| 3 | **Decisive:** each failed request's trace walked to the innermost span still open at the deadline, failures credited to that span's service | **E, the session cache (520,000)** (5th of 8 on rung 0) | — | — |

* **Position table.** E ranks 5th on rung 0 (97% of budget), is outside rung 1's population (internal) and 8th on rung 2 (60,000 returned on
  its one facade path), and leads only rung 3, 2.26× C. Intermediate leaders hold margins of 1.26×, 1.24× and 1.30×.
* **Discriminator dominance.** C carries a 6.5× advantage over E into rung 3 (390,000 against 60,000). Trace attribution multiplies E's
  failures by 8.7 and C's by 0.59, an edge of 14.7 against the 1.2 × 6.5 = 7.8 required, 1.88× headroom.
* **Partial correction priced (L3).** A solver who walks traces one level, crediting a failure to the returning service's immediate callee,
  names F, the recommendations API, which sits between the edge and the cache on most chains (330,000 against C's 280,000, 1.18×). A
  solver who walks traces but credits the first span to log an error names C again (390,000 against F's 300,000, 1.30×): when the edge's
  deadline passes, the inner spans end as cancelled and the edge logs the only error. Neither half lands on E.
* **Grid.** Population (catalogue flag or route join) × attribution (returning service, immediate callee, first error, innermost open span)
  gives eight cells. Catalogue-flag cells never admit the cache as a candidate and name B or C; route-join cells name C, F, C and E. Only
  the innermost open span names E, and the nearest wrong cell (F) needs the walk stopped one hop short.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The charter counts failed user requests. The tracing guide says every failed request is traced. No document says
   where a failure belongs, and the cache's runbook describes eviction storms as a capacity note.
2. **The corpus pins a construction, not a menu.** Innermost-open-span attribution reproduces all 10 realised falls within 5% at a fixed
   0.62 of the embedded service's originated failures; returning-service attribution reproduces 5 and over-predicts every miss, so it also
   overstates the book's total by 46%. The attribution is a construction: a span-tree walk per failed request against its deadline, with no
   column naming an origin.
3. **No arithmetic symptom.** Failed requests tie to gateway logs, spans to traces, budgets to the dashboard; every failure is counted once
   under every attribution.
4. **Not a row predicate.** It needs each trace's spans assembled into a tree by parent ID, the deadline of the outermost span, and the
   deepest span still open at that time.
5. **The enumeration is arithmetic.** Which service owns each failure is computed trace by trace; the cache's share appears in no metric.
6. **No cutover date.** Eviction storms recur at scattered times all quarter; no series steps. The only dated event, the card processor's
   outage, sits under rung 0.
7. **Survives deletion.** With every voice and the dashboard removed, the answer and the difficulty are unchanged.

## 6. The calibration corpus

* **Form.** The book of past embeds: ten quarters, each with the service embedded, its dashboard figures that quarter, and the measured fall
  in platform-wide failed user requests the quarter after, adjusted for traffic, with that quarter's traces.
* **What it pins.** Realised falls equal 0.62 of the failures originating at the embedded service under innermost-open-span attribution, 10
  of 10 within 5%. Returning-service attribution 5 of 10; error-budget rank 4 of 10.
* **Twin pair.** Embeds X-3 and X-8 are identical on budget consumed, burn pages, breach minutes, saturation alerts and failures returned.
  X-3 removed 182,000 failures and X-8 88,000 (2.07×): X-3's failures originated in itself, X-8's in a dependency it called.
* **Every rule exercised.** One past embed was at an internal service, so internal services' origination is tested; one embedded service sat
  mid-chain, so the walk's depth is tested.
* **Resemblance points at the decoy.** By dashboard profile E most resembles the internal services that were never embedded; C most resembles
  X-3, the largest realised fall.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The SRE charter: an embed is judged by the fall in failed user requests over the following quarter. The tracing guide:
  every failed user request is traced in full. The incident register's documented external incidents are excluded from every service's
  record.
* **Empirical pins.** The innermost-open-span attribution and the 0.62 realisation rate, from the book.
* **Voices.** The SRE lead: "The error budget is the contract; the embed goes where it burned." The product VP: "Customers only see our
  user-facing services, so that's where the engineers should be."
* **Licensed wrong basis.** The charter records that the quarterly executive reliability review ranks services on error-budget consumption
  and will present that ranking.

## 8. Determinism by construction

* **Attribution.** In 99.6% of failed traces the innermost open span at the deadline belongs to the same service as the span whose stall
  consumed most of the deadline; the rest split evenly and change no rank.
* **Deadlines.** Every outermost span carries its deadline in its attributes, so no timeout convention exists.
* **Population.** Every gateway and facade request carries its trace ID, so the route join is exact and no request is counted twice.
* **Window.** The cache's storms are steady across the quarter, so last quarter or its second half alone gives the same leader.
* **Rate.** The 0.62 realisation rate is uniform across the book, so the expected fall is a fixed share of originated failures.

## 9. Prompt sketch and deliverables

> Two of our SREs can embed with one service for next quarter. The SRE lead wants them wherever the error budget burned hardest. Name the
> service and the fall in failed user requests we should expect, in a sentence for the quarterly plan, with `embed_choice.xlsx` holding the
> sheets below, the chart `failure_origins.svg`, and a short `planning_note.md`.

* `embed_choice.xlsx` — the service build under each attribution, the deploy sheet (ask A), the paging sheet (ask B) and the book back-test
  (ask C).
* `failure_origins.svg` — a returning-service by originating-service matrix of last quarter's failed requests, the cache's column
  highlighted, each service's own error-budget consumption as a side bar, and one storm's trace drawn as an inset with the deadline marked.
* `planning_note.md` — the committed service, the expected fall, and why the budget leader and the edge services are not it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each service, deploys last quarter and the share rolled back. *Device:* a canary aborted
  before full rollout is logged as "aborted", not "rolled back", and the change policy counts it as a rollback. Reading the rollback flag
  alone understates the share for the four services that canary every deploy. The failure attribution never reads the deploy log.
* **Ask B (device-carried).** For each service, pages last quarter and the share acknowledged within five minutes. *Device:* a page
  escalated to the secondary after no acknowledgement is logged as a second page with the same incident key, per the paging guide.
  Counting pages doubles every escalation and understates the acknowledged share.
* **Ask C (validity).** For each of the four rung constructions, the past embeds' realised falls it reproduces within 5% out of 10.
* **Decoupling.** Clearing the trace walk changes no figure in asks A or B.

## 11. Rubric arithmetic

8 services × 2 (ask A) + 8 services × 2 (ask B) + 4 constructions (ask C) + the committed service, its originated failures, the expected fall
and the margin over C + 5 named chart parts + 3 files ≈ 48 criteria.

## 12. World-building constraints

* Rung leaders are A, B, C, E. E is 5th / absent / 8th / 1st; intermediate margins are at least 1.24×; E leads rung 3 by 2.26×.
* The cache originates 520,000 failed user requests and returns 60,000 itself; its availability SLO is met all quarter.
* A's burn is 81% one external outage; 46% of B's failures come from internal batch callers; the cache (E) and F, both marked internal,
  sit behind public facade paths.
* Rung 2: C 390,000, F 300,000, E 60,000. One-level walk: F 330,000, C 280,000. First-error walk: C 390,000, F 300,000.
* The book holds ten embeds at a uniform 0.62 realisation; X-3 and X-8 are identical on every dashboard column.
* Canary aborts and secondary escalations never touch traces or gateway logs.

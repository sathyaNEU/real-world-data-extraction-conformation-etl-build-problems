# task268 design note: Rotalinha's 2027 reliability programme, the internal services whose 2026 latency SLI breached its budget

Architecture 6, a re-root begun 2026-11-07 in Descriptive & Distribution Analysis (the number's objective), after architecture
5 (Corcally's Roastery 2027 sampling, marketing-consumer-research / segmentation-market-structure) landed on the portal with
both responses on the golden (STATUS commit 134d71b8). Architectures 1 to 5 are in the card's lineage and in
`## Tried and rejected`; architecture 5's design sections are in git history at 6e745ade.

## Draw

- **Card.** `.claude/skills/fingerprint/cards/task268.json`, architecture v6, re-registered 2026-11-07 after the edge-sampler
  redraw (the first registration, 21:54:53Z, carried the per-service sampler now in `## Tried and rejected`). `guard.py check`
  on the filed card: WARN only, `repeat.gate_g` (method_or_model_selection against task127 v4) and `overuse.gate_g` (5 of the
  last 12). Answer: the gate names the decisive step, the choice of inclusion probability for a cluster sample of traces;
  task127 (a bank's support packages valued by the write-off they keep off the book) shares no world, driver or shell.
  Three axes were redrawn after task127 v4 was registered at 22:27Z with the same values: context artifact monitoring_export
  to operations_log (the decisive file is the trace store's span export, an event log of every call a kept request made),
  forum line_manager_or_team to executive_team (the engineering leadership group approved PR-SLO-3 and staffs the reliability
  programme the call assigns engineers in), forcing event period_close to budget_or_appropriation (the call is the January
  allocation of reliability engineers for the first half of 2027). The older same-puzzle and same-driver signatures (task245,
  task265, task139 v1, task182 v4, task270 v1 and v6, task452 v2), task264 and the slot's own superseded registration carry
  one differentiation line each on the card.
- **Pairing.** general-statistics-data-science / missing-data-censoring-measurement-error / descriptive-distribution. The
  setting is the platform reliability team of Rotalinha, a Lisbon marketplace selling intercity bus and ferry tickets in
  Portugal and Spain; the statistics is the field: a population share estimated from a cluster sample of traces whose
  inclusion probability is set where each trace starts and recorded nowhere.
- **Decision.** Which internal services ran over their 2026 latency error budget. Each one that did gets a reliability engineer
  for the first half of 2027. Retrospective by design: the SLO year closed on 31 December 2026 and the programme starts in
  January.
- **The quantity.** Each service's 2026 latency SLI as the annual review reads it, over December in Lisbon time (PR-SLO-3
  section 3.1): the share of the requests it handled whose server-side duration exceeded its threshold, against its error
  budget (both in the standard).
- **Data-native sentence.** The trace store's sampler sits at the edge: each edge service keeps a share of its requests that
  it resets at the top of every hour from its previous hour's traffic, and a kept request's whole trace is kept with it, so
  an internal service's kept spans carry the keep share of whichever edge service started their trace; partner-gateway's
  slow availability lookups are made by journey-search's searches, the busiest edge service and the one kept at the smallest
  share, while seat-map and booking, kept at far larger shares, make its fast calls. The load balancer counts every request
  each service handled per hour; no file records a keep share.
- **Abstraction sentence (nearest builds).** The nearest approved builds are task275 (an invariant total raised to unobserved
  trips) and task253 (a count past a line as the sum of probabilities), and neither shares the move. A reviewer holding
  task452 v2 (delivered) would say both weight a sample by its inclusion probability: there the probability belongs to a
  drawn stratum, recorded in the design, and the trap is a reclassification after the draw; task264 weights a sampled person
  by a probability proportional to their own visits. Here the probability belongs to another unit, the edge service whose
  request started the trace, is recorded nowhere, and is recovered hour by hour from that unit's load balancer count.
  task258 (approved) is the nearest world (web performance) and shares no step.
- **Shape.** 14, cuts of a distribution per segment: for each internal service its SLI and whether it breached, the call, the
  chart, the files, and the asks.
- **Strategy.** population_selection, gate method_or_model_selection, generators G9 (the measured outcome is the kept one),
  G6, G13; gap population; Layer 2 estimation_fit.
- **Prototype on the world's own kept spans (`generator/seed_sweep.py 2700 2950`, 2026-11-07).** 205 of 250 seeds hold the ladder
  and the one-decimal corridor. Seed 2886: the golden puts journey-search 1.3, places 1.5, seat-map 1.5, partner-gateway 2.9
  and notifications 1.6 over budget; reweighting each service's spans hour by hour by its own count passes partner-gateway at
  1.44 against 2.0, pooling by hour of day at 1.26, and the kept share and a day reweighting pass journey-search, places,
  seat-map and partner-gateway (0.69, 0.71, 0.74, 0.84). Smallest golden ratio to budget 1.32; partner-gateway 0.28 under
  its budget on the per-service rung; every graded one-decimal figure at least 0.018 from a rounding line under
  Horvitz-Thompson on the balancer's count, Hajek, hour-calibrated, own-hour weights and either orphan handling.

### Spent insights on this objective (`guard.py mechanisms --objective descriptive-distribution`, 2026-11-07)

One line per insight a live or lineage card has spent, so no candidate re-screens them.

- task253: a count of units past a line is the sum of their probabilities, not the count of shrunken predictions.
- task254: a path's passage time through stages whose delays build during the unit's own passage.
- task255: the upper tail of a two-kind size distribution under per-item floors, a moving ceiling and open items.
- task256: the share inside a multivariate box carried from a reference group by its conditional distribution.
- task257: latent dimensions of categorical items where Pearson correlations on codes mislead.
- task258: an intervention moves only the units whose served document carries the reference its step needs.
- task259: a level at a reference date carried from earlier reports by the level's own movement in the same units.
- task260: an interval for a shared-sample improvement must resample raters and items together.
- task261: a subgroup difference's error from one clustered sample, the subgroups sharing clusters.
- task262: a slope on a long-run average measured in full only for a subsample selected on its level.
- task263: each source's level recovered from mixtures run in changing proportions.
- task264: distinct members from events sampled in proportion to each member's events; v1 the price setter as the unit.
- task265: survival from a record that began after many units started (delayed entry).
- task266: cumulative incidence with competing ways a spell ends, many still open.
- task267: a rule's capture rate when the check went to every flagged member and a random fifth of the rest.
- task269: compliance read from staff observers who sample mostly well-covered periods.
- task270: (v1 to v10) selection on a weighted sum; a reporting cost; practice effects; part against composite; correlated
  errors of two changes; slot landings; losses recorded when made good; fixed-schedule suppliers; a variogram of moves;
  free servers away from base; (now) remaining time from a group published only as one total.
- task271: impact of events that stand alone, read from events mostly inside sequences; risk from earlier episodes;
  members unreachable at the call hours; penetrance with testing selected on outcome; rates carried by supply-zone geometry.
- task272: drift between resets under sparse checks; dependence on the previous decision within sessions; a seasonal
  quarter scaled to the year.
- task274: groups below a line with an instrument bias under one calibration and a remeasured subsample; age with missing
  start dates.
- task275: observed trips land undersized fish and avoid nursery grounds, so the unwanted catch per hour by ground is raised.
- task279: substance lost from a compressible medium read off the surface lowering.
- task280: probes silenced by members' own activity, the activity rising with load.
- task281: wear-out before a fixed age with a part that never wears out; a year's need rebuilt with planned gaps.
- task101: the decision's own earlier payments sit in the distribution it cuts from.
- task114: demand that takes a room only when two parties share a site (co-presence under consolidation).
- task126: a succession link that both continues a unit and opens a new one on a carried file.
- task93: a floor's cost as a shortfall per person per pay period under flat all-in pay.
- task73: a capped slate bound by a processing allocation with re-assigned review intervals.
- task65: capped sums over entities constituted from child records by the child's own location.
- task57: archives whose union nulls a third of records; filed place limits binding below the money.
- task53: eligible volume pooled per account against a scale break.
- task38, task34, task24, task19, task14, task10, task9, task8, task7, task5, task4, task3, task2, task1: the legacy
  surface-read, identity and stated-rule forms (pre-10/10, not drawable now).
- task182 v4 (another lane, same objective family): durations seen only in snapshots, length-biased.
- task452 v2 (shipped): weight each reference observation by the stratum it was drawn in, not the revised one.
- task127 v2 (landed on the portal): an intervention removes only the replaced step's excess over a concurrent step.
- task472 v2 (shipped): saved work counts only where it brings a release into an earlier fixed window.
- task181 (approved): an eventual count completed by each reporting route's own delay.
- This slot: v1 daytime presence carried from commuting flows; v2 a stock's fall from preferential collectors against a
  survey; v3 survival with censoring that follows worsening; v4 claims completed by notifying route; v5 duplication of
  purchase at the home, homes linked by a shared payment card.

## Default path

Every figure below is built by `generator/analysis.py` from the shipped pack and asserted in `generator/checks.py`
(seed 2886).

1. Read PR-SLO-3: a service's latency SLI is the share of the requests it handled whose server-side duration exceeded its
   threshold (2.1); a request is any call it handled, whether or not the tracing store kept a span for it, the balancer's
   probes excluded (2.2); the duration is the service's own server span (2.3); the review reads December in Lisbon time,
   which is UTC all month (3.1); a breach is an SLI over the budget (3.2); thresholds and budgets are in section 4.
2. Join the service catalogue's tracing names and target groups to the trace export and the load balancer's July to
   December export; keep the server spans, drop the health probes and the re-sent rows.
3. Count kept server spans against the balancer's requests hour by hour: each service's kept spans run at a flat few dozen
   an hour while its requests swing from a few hundred to 57,000, so the sample thins in the busy hours, when requests are
   slow.
4. Correct for it the standard way, post-stratifying each service's kept spans by hour on its own count (each hour's slow
   share times the hour's requests, summed over December, over December's requests). Check it: the weights rebuild every
   service's hourly count, and the weighted 5xx share matches the balancer's 5xx counts for every service.
5. Compare each SLI with its budget: journey-search 1.3, places 1.5, seat-map 1.5 and notifications 1.6 against 1.0 are
   over; partner-gateway is at 1.4 against 2.0, fares, booking, payments, tickets and accounts under.

Ends on: four services: journey-search, places, seat-map and notifications (partner-gateway 1.4 against its 2.0 budget).

Golden: five services: journey-search, places, seat-map, partner-gateway (2.9 against 2.0) and notifications.

## Stump sentence

A competent analyst who sees the trace store's sample thin in the busy hours post-stratifies each service's kept server
spans by hour on that service's own load balancer count, which lands every edge service, and files four services, with
partner-gateway at 1.4 against its 2.0 budget; the step that lands it there is weighting a partner-gateway span by
partner-gateway's own hourly keep share, when the store keeps or drops whole traces at the edge, so each span was kept
at the share of the edge service whose request started its trace, and journey-search's searches, which make the slow
availability lookups, are kept at a fraction of seat-map's and booking's share; weighted by each trace's own edge keep
share, partner-gateway is at 2.9 and the review names five services.

## Three rules

- **Task type:** general-statistics-data-science `missing-data-censoring-measurement-error`, which serves Descriptive &
  Distribution Analysis: a population share estimated from records missing by design (the requests the store did not
  keep), whose inclusion probability has to be recovered before the share is read.
- **Domain test:** the deciding quantity is each service's latency SLI, a population proportion over every request it
  handled, estimated from the store's sample; the statistician's estimator is a design-weighted share in the
  Horvitz-Thompson form, each kept unit counted at the inverse of its inclusion probability; replace it with the kept
  spans' own share, or with each service's spans post-stratified by hour, and the call changes (partner-gateway 0.8 or
  1.4 against 2.9).
- **Swap:** "which services ran over their latency error budget" becomes "which wards ran over their infection budget";
  a ward has no trace store keeping whole request paths at a rate the entry point sets, no balancer count and no
  downstream unit whose observation rides on another unit's sampling decision, so the sentence stops making sense.
- **Layer 1:** the balancer's two exports (the old billing tool's layout to June with CRLF lines and processed gigabytes,
  the FinOps export from July with renamed target groups, bytes, LCUs and 5xx counts), the trace export's re-sent
  batches, its kept health probes, client spans beside server spans, nanosecond epoch clocks, and on the asks' rows the
  incident tool in UTC against the status page in Lisbon time, USD marketplace lines at each invoice's rate, VAT and the
  support plan, team tags before the retags and the delivery pipeline's staging and failed attempts; each is produced by
  the platform's own systems, none is placed to be caught, and none carries the call.
- **Layer 2:** estimation_fit, a population share from a sample with unequal inclusion probabilities, where the sampling
  unit is the trace and its probability belongs to the edge service that started it; the choice that flips the call is
  which unit's keep share weights a downstream service's span.
- **Decisive step:** recognising that the store keeps or drops whole traces at the edge, so a partner-gateway span was
  kept at the keep share of the edge service whose request began its trace, in the hour that request began, and counting
  each span at that edge service's balancer count over its kept root spans for the hour.
- **Not semantics:** every field read correctly (server spans only, probes and re-sent rows dropped, the catalogue's
  names and target groups joined, December in Lisbon time, the section 4 thresholds) still files four services under the
  per-service hourly correction; no column, code or unit changes when a trace's edge keep share is used, because no file
  stores a keep share, a sampling rule or a trace's edge service.
- **Not rule application:** no filed rule says how kept spans are weighted; executing PR-SLO-3 and every convention leaves
  the estimator open. The enumerated family (the kept share, a day weighting, an hour-of-day pooling, each service's
  spans post-stratified by its own hourly count, and the trace-edge weighting in Horvitz-Thompson, Hajek and
  hour-calibrated forms with the root's hour or the span's own) spans 0.84 to 2.90 for partner-gateway and files one,
  four or five services; the standing family (the trace-edge weightings the whole traces leave defensible) spans 2.87 to
  2.90 and files five in every member; the ruling-out is quiet: the whole traces and each edge service's flat count of
  kept root spans show only when spans are linked to their trace's root and the root to the balancer's count.
- **Analyst test:** a strong analyst who drops probes and re-sent rows, reads the catalogue, sees the sample thin in the
  busy hours and post-stratifies each service's kept spans by hour on its own balancer count files four services:
  journey-search, places, seat-map and notifications, with partner-gateway at 1.4 against its 2.0 budget, the default
  path's `Ends on:`.
- **Estimand:** PR-SLO-3 sections 2.1 to 2.4, 3.1 and 3.2: for each internal service, the share of the requests it handled
  in December 2026 in Lisbon time, from any caller and whether or not the store kept a span for it, whose server-side
  duration exceeded its section 4 threshold, against its section 4 error budget; the file is
  `PR-SLO-3_service_level_objectives_2026.docx`.
- **No decoy:** nothing is planted to be caught: the sampler is the store's own edge sampler, the README describes fields
  and says only that the store keeps a sample, no document states a keep rate, a weighting or an SLI, nothing ranks the
  services, and the capacity review and the app reviews are context the solution never reads.
- **No certified replay:** the method is not recovered by reproducing certified figures; no shipped table prints an SLI
  or a keep share, and the balancer's 5xx counts tie under every weighting, so they confirm no route over another.
- **Lesson:** in a trace sample the sampling unit is the trace, so a downstream service's spans carry the inclusion
  probability of whichever edge service started each trace, and post-stratifying a service's own spans by its own count
  treats a cluster sample as a simple random sample of that service's requests; no build on file prices an inclusion
  probability inherited from another unit's sampling decision.

## Survivor anatomy

- **Actor:** each kept span's inclusion probability decides, a property no column stores: it belongs to the request that
  began the trace (the server span with a blank parent), is set from that edge service's previous hour of traffic, and is
  recovered as that service's balancer count over its kept root spans in the hour (test: the trace export's 12 columns
  and the balancer's 6; none holds a keep share, a sampling rule or a trace's edge service, and none is one join away).
- **Link:** the signal is read through two links no key offers and no sentence invites: a span to its trace's root
  through `trace_id` and the parent chain (server, client, root server), and the root's service and hour to its target
  group's hourly count through the catalogue; the README describes fields only.
- **Reflex:** the field's correction for a sample that thins under load, post-stratifying each service's kept spans by
  hour on its own count, is rung 3 and files four services (partner-gateway 1.4); the tracing tool's own share beneath it,
  rung 0, files notifications alone.
- **Back-test:** the textbook route validates: rung 3's weights rebuild every service's hourly balancer count exactly, and
  every route's weighted 5xx share matches the balancer's 5xx counts for every service (partner-gateway 0.80 per cent
  under each), because errors do not move with load.
- **Second use:** every file the decisive step reads has its own reason to be in the review folder: the trace export is
  the SLI's only latency record, the balancer's export is the count of requests handled that every route's denominator
  needs, the catalogue joins the systems' names and carries the asks' tags and components, and PR-SLO-3 files the
  estimand; deleting the decisive step drops no file.
- **Shock:** partner-gateway's breach reads as ordinary explained movement: an operator-facing gateway slow under peak
  search traffic is everyday reliability news, its December volume is second to places, its rung 3 figure sits well under
  its 2.0 budget, and sorted on every shipped statistic (December requests, kept spans, 5xx share, threshold, budget) the
  five golden services are not an interval.
- **Pins:** the WHAT sits in PR-SLO-3 (2.1 to 2.4 the population, outcome and unit; 3.1 the window; 3.2 the comparison;
  section 4 the thresholds and budgets), and no filed sentence names the sampler, a keep share, a sampling unit, a weight
  or a trace; deleting any filed sentence removes part of the estimand, never a hint.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Dedicated organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 the kept spans' own share | 2.1 names a share | the spans | yes, the tracing tool's view | 2.2 says kept or not | no | yes | no | readable |
| R1 each day's kept spans weighted by the day's requests | 2.4 names days | the balancer's hours summed | yes | rebuilds daily counts | no | yes | no | readable |
| R2 hour-of-day pooled weights | none | the balancer's hours | no | rebuilds hour-of-day totals | no | yes | no | readable |
| R3 each service's spans post-stratified by its own hourly count | none | the balancer's hours | yes, the field's correction | rebuilds every hourly count; 5xx ties | no | yes | no | readable |
| R4 (decisive) each span counted at its trace's edge keep share | none: no sentence names a trace, a keep share or the edge | no column holds a keep share or a trace's edge service | no: the reflex weights a service by its own count | none: the 5xx and count benches pass under R3 too | no | no: a trace-root link per span, then the root's hourly share | no: the balancer export is the denominator every rung reads | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternatives and their call | Ruled out by |
|---|---|---|---|---|
| SF1 | request | any call the service handled, kept or not | the kept spans as the requests: rung 0, one service | 2.2 ("whether or not the tracing store kept a span for it") |
| SF2 | server-side duration | the service's own server span | the caller's client span for an internal service: partner-gateway 2.93, same call | 2.3; same call asserted |
| SF3 | health probes | not requests | kept probes counted: every SLI about 8 per cent lower, same call | 2.2; same call asserted |
| SF4 | re-sent rows | a span once, by `span_id` | both copies: same call | README; same call asserted |
| SF5 | the review month | December 2026 in Lisbon time | December in UTC: identical, Lisbon is UTC in December | 3.1; same call asserted |
| SF6 | a child's hour | the root's start hour sets the keep share | the child span's own start hour: same figure to one decimal | same call, asserted |
| SF7 | a span whose trace began before 1 December | none in the export | weighted at its own service's hourly share or dropped: identical | same call, asserted (count) |
| SF8 | breach | the SLI to one decimal over the budget | the unrounded SLI over the budget: the same five | 3.2; same call asserted |
| SF9 | errors | counted like any request | 5xx dropped from both sides: same call | 2.4; same call asserted |
| SF10 | the denominator | the balancer's December requests | the weighted kept count (Hajek): same figure to one decimal | same call, asserted (corridor) |
| SF11 | hourly calibration | each span at its edge share, summed | weights calibrated hour by hour to the service's count: same figure to one decimal | same call, asserted (corridor) |
| SF12 | exceeded | strictly over the threshold | at or over: identical (durations are continuous) | 2.1; same call asserted |
| SF13 | 404 responses | requests like any other | dropped: same call | 2.4; same call asserted |
| SF14 | a retried call | each try is a request the service handled | first tries only: same call | 2.2; same call asserted |

## Ladder

| Rung | Construction | journey-search | places | seat-map | partner-gateway | notifications | Set | Dies to |
|---|---|---|---|---|---|---|---|---|
| R0 | the kept spans' own share | 0.69 | 0.71 | 0.74 | 0.84 | 1.58 | 1: notifications | SF1, 2.2 |
| R1 | each day's spans weighted by its requests | 0.75 | 0.81 | 0.79 | 0.89 | 1.59 | 1: notifications | the busy hours inside each day |
| R2 | hour-of-day pooled weights | 1.13 | 1.28 | 1.26 | 1.26 | 1.57 | 4, no partner-gateway | the campaign evenings and the edge share |
| R3 | each service post-stratified by its own hourly count | 1.32 | 1.50 | 1.48 | 1.44 | 1.61 | 4, no partner-gateway | the edge keep share (decisive) |
| R4 | each span at its trace's edge keep share (golden) | 1.32 | 1.50 | 1.48 | 2.90 | 1.61 | 5 | |

Fares, booking, payments, tickets and accounts stay under their budgets on every rung (fares at most 0.61 against 1.0,
booking 0.37 and payments 0.31 against 0.5, tickets 0.61 and accounts 0.67 against 1.0). The golden's smallest ratio to a
budget is 1.32 (journey-search); partner-gateway sits 0.28 of its budget under it on R3.

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | every request each service handled in December, kept or not, probes out | filed 2.2; SF1, SF3 |
| 2 | Unit of account | the request (a server span when kept) | filed 2.1 and 2.3; SF2 |
| 3 | Attribution window | the hour a request began, for the window | filed 2.4; nothing on 1 December's edge moves the call (SF7) |
| 4 | As-of dating | the store as held on 1 January 2027 | README; one export, C1 |
| 5 | Version basis | one export, no revisions | C1 |
| 6 | Denominator | the balancer's December requests | filed 2.2; SF10 corridor (C3) |
| 7 | Weighting | each span at its trace's edge keep share | the decisive step, forced by the whole traces (C4: R3 1.44 against 2.90) |
| 8 | Window length | December, 31 days | filed 3.1 |
| 9 | Boundary inclusivity | strictly over the threshold | filed 2.1; SF12, C1 |
| 10 | Rounding path | the SLI to one decimal, compared with the budget | prompt; SF8, C1 |
| 11 | Tie-break | none needed | C1, no service within 0.3 of its budget |
| 12 | Maturity and censoring | none: the month is closed | C1 |
| 13 | Order of operations | dedupe, drop probes, link roots, weight, sum | C1, each order gives the same weights |
| 14 | Row order | export order | C1, asserted over a shuffled read |
| 15 | Duplicate resolution | a re-sent span once | SF4, C1 |
| 16 | Identity normalisation | tracing names and target groups through the catalogue | the catalogue's own crosswalk |
| 17 | Netting against gross | none | C1 |
| 18 | Dimensional units | nanoseconds to milliseconds, per cents | the README's units |
| 19 | Code and status semantics | 5xx and 404 count as requests | filed 2.4; SF9, SF13 |
| 20 | Integerisation | none | C1 |
| 21 | Clause scope | section 4's table for every service | filed |
| 22 | Forward window contents | none: the call reads a closed month | C1 |

## Literal reader

Executed word for word, PR-SLO-3 gives the golden: 2.2 puts every request in the population whether or not a span was
kept, so the kept spans are a sample and the share has to be estimated; the export keeps whole traces (every internal
server span has its client span and its root in the store) and each edge service's kept root spans run flat each hour
against a swinging count, so a span's inclusion is its trace's edge share for the hour; counted at that share, the five
services breach. The readings that differ violate a quotable sentence (SF1 against 2.2, SF2 against 2.3, SF3 against
2.2) or converge on the same call (SF4 to SF14, asserted).

## Oracles

- The balancer's hourly counts: rung 3's weights rebuild them exactly by construction and the golden's to within
  sampling noise; they arbitrate no route.
- The balancer's 5xx counts: every route's weighted 5xx share matches them for every service; a control that ties under
  every handling, never only under the golden.
- The catalogue's crosswalk of names, target groups, components and tags: identity only.
- No shipped figure is an SLI, a keep share, a weighting or a ranking of the services.

## Ask sheet

Three asks, 60 figures, beside the call's own figures (each service's SLI, budget and verdict, and the chart). All three
are the annual reliability review's own items (PR-SLO-3 section 5), wanted from the same review folder; none reads a row
the call reads (the trace export and the balancer's July to December counts carry no ask device). Each ask rides one
reconstruction across a second system that no sentence states, with mass in every cell, over the hazards a careful
solver handles.

**Ask A: each service's releases and rollbacks in 2026** (20 figures, counts).
- H18 home: the review's change record beside the SLI (section 5.1); use: the reliability engineers' briefing.
- Files and columns: `production_deployments_2026.json` (service, environment, version, commit, finished_at, outcome),
  `cluster_rollout_history_2026.csv` (deployment, revision, image, changed_at_utc, changed_by), the catalogue.
- Primary device (D4 with D7, absence evidenced in a file no habitual join reaches, the true key elsewhere): on-call
  engineers undo bad releases by hand and apply hotfix images by hand during incidents; neither passes through the
  delivery pipeline, so neither is in its log, and the cluster's rollout history, which holds every change, tags images
  by short commit hash, never by version. A manual undo is a rollback only if the image it restores was first released
  before the running one, which needs each hash mapped to its version through the pipeline's `commit` field; a hotfix
  hash no pipeline record carries is a new version reaching production, a release. Every service has at least one
  manual undo and one hotfix, so all 20 figures move.
- Hazards: staging deploys, failed attempts and their retries, config redeploys of the running version, a bad version
  re-shipped after its config is fixed (neither), pipeline deploys present in both files, and rollout restarts that
  re-apply the running image (neither).
- Pin test: the asking sentence pins the service, the year and the two counts; section 5.1 defines both in terms of
  production's running version; no pin names the rollout history, a hash, an undo or a hotfix.

**Ask B: each service's cloud cost in each half of 2026** (20 figures, nearest euro).
- H18 home: section 5.3's cost line; use: the programme's cost per engineer-month set against each service's spend.
- Files and columns: `cloud_billing_2026.csv` (usage_date, invoice_id, resource_id, resource_tags, line_type,
  currency, cost), `cloud_invoices_2026.csv` (invoice_id, usd_eur_rate), `cloud_resources_2026.csv` (resource_id,
  deleted, replaces, tags_now), the catalogue's cost and team tags.
- Primary device (D7, a prior-id chain): resources replaced during the year ran under the team's tag until their
  replacement took over, and every team tag covers two or three services; only the replacement, which names the old
  resource in `replaces`, carries the service tag. Each service has one resource replaced in each half, so every cell
  carries team-tagged lines.
- Hazards: marketplace software billed in US dollars at each invoice's own rate, VAT, the shared support plan,
  sustained-use credits on compute.
- Pin test: section 5.3 pins the charge, the currency, credits, VAT, shared costs and dating by the day the resource
  ran; no pin names a replaced resource or a chain.

**Ask C: each service's customer-facing incident minutes in each half of 2026** (20 figures, nearest minute).
- H18 home: section 5.2's incident line; use: the engineers' first-week reading list.
- Files and columns: `incidents_2026.csv` (incident_id, declared_at_utc, services), `incident_timeline_2026.csv`
  (incident_id, at_utc, event, detail), `status_page_history_2026.json` (posts' components and created_at, components'
  status changes, Lisbon time), the catalogue's status page components.
- Primary device (a state rebuilt from an event log): the export's `services` column is the incident's list when it
  was closed; the responders name services one by one after the declaration, minutes to most of an hour apart, and only
  the timeline says when; section 5.2 counts the minutes in which a customer-facing incident named the service. Every
  service has a posted incident in each half, so every cell moves.
- Second reconstruction on the same cells: the incident tool and the status page share no key, so a post is matched
  to its incident by component and time.
- Hazards: the status page's Lisbon clock against the tool's UTC (summer time in the first half's end and the second's
  start), the tool's administrative close after the review against the page's return to operational, overlapping
  incidents on one service counted once.
- Pin test: section 5.2 pins customer-facing, the start, the end and counting once; section 5.4 pins the halves in
  Lisbon time; no pin names the timeline or a service's naming time.

**Main population, zero counts:** the trace export and the balancer's July to December counts carry no ask device
and no ask hazard; the asks' records (deployments, rollout history, billing, invoices, resources, incidents, timeline,
status page) are files the call never reads (asserted, `SEP` in `checks.py`).

**Referee:** none arbitrates a device; the pipeline's staging and failed attempts, the invoices' rates and the
status page's posts tie under every handling.

| Path (cracker = lands the call, runs the battery, executes filed documents) | Kept of 20 | Verdict |
|---|---|---|
| Ask A, cracker: section 5.1 on the delivery pipeline's log | 0 of 20 | miss |
| Ask B, cracker: section 5.3 by tag, team-tagged lines to no service | 0 of 20 | miss |
| Ask B, cracker variant: team-tagged lines shared evenly in the team | 0 of 20 | miss |
| Ask C, cracker: section 5.2 with the export's services named from the declaration | 0 of 20 | miss |
| Ask A, one crack: the rollout history alone, its cutover revision a release | 7 of 20 | miss |

The cracker keeps none of the 60 ask figures. A response that finds one ask's reconstruction keeps that ask's 20 (a
third of the ask weight); that is the full includer's ground on one ask, not the reflex.

Mirror leakage: 0.0 per cent of ask weight (the mirror takes the cracker's ask paths off the call).

Pair ceiling: 28.5 (cracker on the call 45.0, mirror off it 12.0); with one ask cracked by both, 46.8.

Measured by: generator/ceiling.py, run on the cut pack.

## Layer 1 inventory

Each item is written by the platform's own systems; each is asserted neutral in `generator/checks.py` (the call
unchanged under its natural mishandling).

| Item | System and file | Natural mishandling | Assertion |
|---|---|---|---|
| Re-sent rows | the tracing store's export job, `trace_spans_2026-12.parquet` (a span twice under one `span_id`) | both copies counted | SF4 |
| Kept health probes | the store keeps about one load balancer probe in 720, same file (`GET /healthz`) | probes counted as requests | SF3 |
| Client spans beside server spans | every call leaves a client span in the caller | the caller's span read as the callee's duration | SF2 |
| Error and not-found responses | the services' own statuses, same file and the balancer's 5xx counts | dropped from the SLI | SF9, SF13 |
| Retried partner calls | callers retry a 5xx from the partner gateway once | first tries only | SF14 |
| Nanosecond epoch clock against a Lisbon review | the store's clock, the standard's window | Lisbon offset applied in December | SF5 |
| The balancer's two exports | the old billing tool to June (CRLF, processed gigabytes), the FinOps metrics export from July (renamed target groups, bytes, LCUs, 5xx counts) | the January to June file read for December, or the old target group names joined | the call reads December from the July to December export through the catalogue's July names (SEP) |

On the asks' rows, the delivery pipeline's staging and failed attempts and config redeploys, the rollout history's
restarts, USD marketplace lines, VAT, the support plan, the status page's Lisbon clock and the incident tool's
administrative close are hazards each ask's golden handles (the ask sheet).

## Pre-ship check

- **Three rules.** Domain: a population share estimated from a cluster sample of traces whose inclusion probability is
  set where each trace starts (general-statistics-data-science, missing data by design); the decisive step is an
  estimate the field's correction gets wrong here (rung 3 files four services, partner-gateway 1.4 against 2.0); no
  plant, no field reading and no executed rule decides it (checks: the analyst test on the clean truth, cheap routes
  0 of 4).
- **Free gates.** Generator checks 0 failures; verify PASS; two builds byte-identical; figures_check 117 of 117;
  precut 61 checks, 0 FAIL; voice-check exit 0; leak.py REVIEW (ruled below); guard surface exit 0; heart exit 0 with
  the WARN `repeat.gate_g` and `overuse.gate_g` answered in `## Draw`.
- **leak.py REVIEW lines, ruled.** The capacity review is Platform Infrastructure's own record (harmless); the budgets
  1.0, 0.5 and 2.0 in PR-SLO-3 are the standard's filed inputs, not answers (harmless); two figures inside hexadecimal
  span ids in the parquet are coincidence (harmless); PR-SLO-3 sharing the call's words is its own section 3.3
  decision rule (harmless); its six stump terms (requests, the balancer, its counts, December, partner-gateway) name
  the population and the services, never the move (harmless); its column vocabulary (commit, component, cost,
  deployment) is the standard's own section 5 (harmless).
- **Distractors.** `capacity_review_2026-Q4.md` (Platform Infrastructure's pods, CPU and memory), `app_store_reviews_2026-H2.xlsx`
  (customers' reviews of the app) and `lb_target_group_requests_2026-H1.csv` (the balancer's January to June counts,
  ruled out by PR-SLO-3 3.1, which reads December): each relevant enough to weigh, none read by the call or an ask,
  and none answers a graded quantity; `checks.py` deletes each in turn and asserts the call and every ask unchanged.
- **Stage 4.** Leak reader: Q1 to Q4 none, Q5 the literal estimand (the golden's), Q6 an analytical choice, every
  sweep line harmless; its two realism tells (13 review texts repeated 55 to 244 times; six pods for every service)
  fixed in the generator (composed reviews in each country's language, pods scaled to each service's load and named
  for each revision's replica set); its re-read on the shipped cut found nothing (Q1 to Q4 none, Q6 analytical, no
  realism tell). Determinism judge: DETERMINISTIC, APPROVE; Gate G statistical_rigor,
  analytical_non_defect; Gate H domain, layers pass, decisive step analytical; its one low finding (the January to
  June distractor's deletion test) closed by the assertion above.
- **Container.** Producer metadata scrubbed in the pack and the goldens (scrub audit clean); the parquet carries no
  writer name.

## Tried and rejected

- The seed's own stump, residential density against daytime presence, rejected at the draw on 2026-10-18: with the estimand filed as the people present, choosing presence over residents is reading the estimand (data semantics); left unfiled, the call is not determinate.
- Network ride times against straight-line catchments (urban network analysis), rejected at the draw: a filed twenty-minute ride makes the street network the literal method, so the decisive step would be rule application.
- The plug-in bias of the weighted density from noisy survey counts per tract, rejected at the draw: the same insight as task253 (sampling noise counted as signal).
- Attendance conditioned on commute distance as a continuous covariate, rejected at the draw: the functional form opens forks on every graded figure; the county type of residence carries the same structure with nothing to choose.
- A mobile-device presence panel, rejected at the draw: a column holding the deciding quantity scaled, which R1 forbids and which reads the call off.
- Six distinct winners on six rungs, tried in the prototype on 2026-10-18: consecutive corrections move the cores too little to clear 1.15x margins at every rung; the ladder keeps three rungs with their own winners (every job present, the share by industry group, the share by industry group and county type) and the work-from-home reflex as a hazard landing on rung 0's metro.
- The draw's prototype shares (other services 0.80, 0.45, 0.20 against a survey mix of 0.45, 0.30, 0.25 in every industry), set aside at stage 2 on 2026-10-18: a quarter of every industry's workers living outside their workplace's metro is not the national pattern; with the survey's mix by industry (other services 0.48, 0.30, 0.22) and the realistic shares, two office cores cannot both clear 1.15, so Corrisford became a port and logistics core whose drivers and remote sales staff, living mostly outside the metro, are seldom on the premises.
- The draw's registration slot, set aside at the end of stage 2 on 2026-10-18: the draw-time `guard.py check` ran before the pull that brought in task165 (composition_mix, operations_director, registered at 14:10) and task167 v2 (population, E, method_or_model_selection, 06:59), so the card filed at 16:11 carries ban.strategy, ban.role and test.same_driver BLOCKs against them; three conditioning-transfer drivers in one batch is the template the bans exist for, and the composition stump is this seed's own pitfall, so the design is kept and the card re-registered once the batch has moved past them.
- Architecture 1 (the survey's share of weekdays on the premises carried onto each commuting flow within industry group and the type of county the worker lives in), spent at stage 4 on 2026-10-18: the isolated reader, working the cut pack cold at medium effort, carried the share by industry group and HOMEREL onto every flow as a matter of course and committed Tessavon at 28,805 against Corrisford's 21,709 (`score_reader.py` exit 1, the call 5 of 5, every core density); the decisive rung was readable through the schema, because the survey carries the residence relation as a column the codebook defines against the workplace's metropolitan area, which types every flow through the delineation file, and an analyst carrying a survey rate onto counts carries it on every classifier the two sources share, so the stratum the design called decisive is the careful analyst's reflex. The judge found the call forced and Gate H passing, and two ask forks (a workplace outside any metropolitan area is HOMEREL 4 in the codebook where the golden typed those flows 3; Ask B's partner-shop rule unfiled). In this world a stratification the survey's own columns invite cannot carry the stump; the re-root draws a decisive step no classifier the sources share can reach.
- The seed DA18's world itself, set aside at the re-root on 2026-10-18: every lever the weekday-presence measure offers is a rate carried within strata the survey and the counts share (residence relation, commute distance, shift times, firm size), which the careful analyst stratifies on by reflex, or a choice the board paper already files (residents, primary jobs, latest releases, the core's tracts).
- Length-biased sampling (a census-day stock of stays weighted by inverse length, a stop's random-arrival wait), set aside at the re-root draw: task264 in this lane already weights members sampled in proportion to their events, and a wait read with the inspection paradox is the transit field's standard excess-wait formula, a reflex for a strong solver.
- Measurement-error deconvolution of a distribution's tail, set aside at the re-root draw: task246 deconvolves measurers' error and task253 in this lane shrinks noisy unit averages.
- Values below varying detection limits, detection-corrected counts, dual-list capture and capacity-censored demand, set aside at the re-root draw: task189, task242 and task462, task196 and task448, task168 carry them.
- A return-wave nowcast for leavers whose window is open (the seed DA19's natural stump) and a nowcast conditioned on whether a leaver's post is held, set aside at the re-root draw: task157 carries the calendar-gated return wave, and the held-post nowcast is a composition shift (`composition_mix`), banned against task165 in the window and spent three times in this lane.
- The stage-2 contraction model (each cell's density proportional to its habitat quality to a power solved each year), set aside at stage 3 on 2026-10-18: a large power pulls the deep band's own cells apart, so the band does not hold together and the survey's plain mean sat within noise of the stratified mean (Halmorie Deep 39 to 47 per cent against Brettach Bank's 48 in the structural runs); replaced by band multipliers, the basin read by depth band, with Halmorie Deep enlarged to 80 cells so its deep band is a tenth of the area, which puts the plain mean 14 points under the stratified mean before any noise.
- Torn and weather-missed survey stations placed anywhere, set aside at stage 3 on 2026-10-18: on Halmorie Deep or Brettach Bank a balanced-panel or imputation reading moved a graded fall across its rounding edge in most seeds; the torn stations are on Vallaskie Hole (rough edges to the hole) and the missed one on Cullardy Patch, and the call, both falls and the gap are asserted unchanged under either reading.
- Seeds 1 to 200 searched on cut packs for the ladder's margins, every graded figure 0.12 or more from its rounding edge, the gap the same from unrounded and rounded falls, the convergent readings printing alike and every ask figure missed by the cracker and the over-cleaners: seeds 22, 40, 67, 69, 94 and 184 passed; 69 kept, the widest clearance (0.31 points) with every rung's margin 1.18 or more.
- Architecture 2 (the members' catch rates against the autumn survey's fixed stations, each depth band weighted by its share of the ground's stock area), spent at stage 4 on 2026-10-18: the isolated reader, cold at medium effort, went to the survey first and weighted the bands by area as a matter of course, reading plan 4.2's "weight of haddock on its stock area" with the manual's equal stations per band, and committed Halmorie Deep at 63 per cent against Brettach Bank's 52 with every fall (`score_reader.py` exit 1); it never weighed the logbooks. The judge found the call forced and Gates G and H passing. A survey whose design document describes its strata and allocation, under an estimand filed as a total over an area, makes the design-based estimator the careful analyst's default rather than a stump; the preferential-sampling rung below it is never reached by a reader who reads the plan first.
- Architecture 3's first draft (a motor mutual's 2027 telematics pilot region by January to September claims frequency, the claims not yet notified completed claim by claim on their own notification channel's development, pooled or regional development over-completing the region that moved to the app), dropped before registration on 2026-10-18: it is task181 v2's per-route delay completion, which a solver landed once the estimand was filed, with task451's handler-speed change on top; a channel column makes the per-channel development the careful analyst's reflex.
- Re-root screens on 2026-10-18 before this draw, each set aside with its record: values below detection limits (task189, task190, task183, task248, task246), Pareto interpolation within an income band (task264's own rejection: no decision rests on it), a concentration-discharge rating curve's retransformation (task135 v1 and task452 v1: the textbook construction was the default), anchor equating of two test forms (task450, task464), demand censored at capacity (task168, task147), dual-list capture (task248, task253), informative dropout in a growth curve (task257: multiple imputation lands without the insight), the dissimilarity index's small-unit bias and tempo-adjusted fertility (each estimand names its method), beta-binomial reach extrapolation (two collinear forms fit four insertions alike) and classification consistency at a cut score (classical and IRT estimators split the figures).
- The first informative-censoring prototype (the retirement hospital's patients diagnosed later, 2026-10-18): with a worse class mix at diagnosis its true survival sat so far below the urban hospital's that Kaplan-Meier found it too; its difference now lies in age (death rates 1.10 to 1.18 times and worsening 1.25 to 1.4 times the others') on a mix like theirs, and the cardiology group's departure ends follow-up for over half of Wrenhaven's patients, so the worst-case and complete-case routes fall on Wrenhaven, not Gullhaven.
- The stage-3 world with Gullhaven's moves high in every class (a north intercept of -5.2 to -5.5, a death multiplier of 1.22 to 1.25), set aside at stage 3 on 2026-10-18: a third or more of Gullhaven's patients moved north within two years, more than a retirement coast's return of the frail carries; the moves now concentrate on class IV visits (a quarter of them end in a move) with the death multiplier at 1.16, so 22 per cent move, 96 per cent of them in class III or IV.
- Seeds searched under the kept world on cut packs (2 to 81, 302 to 347, 502 to 547, 2026-10-18): every rung's pick and margin, every form of the decisive estimator printing the same whole percent for every hospital, the golden 0.1 or more from its edges and every ask figure missed by the cracker; 28 and 515 passed, 28 kept (515's truth separated Gullhaven from Fennick by 0.7 points only). Seeds 2 to 123 of the earlier world, searched alongside, were dropped with that world.
- Ask B's re-enrolments under the new record number as its primary device, set aside at stage 4 on 2026-10-19: every solver maps the record numbers through the crosswalk to link the Florida deaths, and with every number current the re-enrolments show as one patient enrolled twice; the round-1 reader left all 143 out and hit all ten figures. They stay as a hazard.
- The overwritten diagnosis dates at the 2025 year end (a November 2025 module update), set aside the same day: they took December 2025 diagnoses out of a count by the date shown while the re-enrolments put patients in, and on the registry as it stands the two cancelled on one of Fennick's figures; at the 2024 year end both move the count the same way.
- Brenmoor's first mix at diagnosis (34 per cent in class III or IV), set aside at stage 4: the default path's gap, Fennick to Brenmoor at 2.26, printed 2 like the golden's Gullhaven to Fennick at 2.08, so a Kaplan-Meier response stated the graded gap's number.
- The relocation recorded on the date of the visit where it was reported, set aside at stage 4 on 2026-10-19 (the round-2 judge's SEND_BACK, margin_or_boundary_fragility): an analyst who takes the class from the visits before the loss date drops that visit and carries a third of Gullhaven's movers from the milder class of the visit before, which put the landmark and fixed-class estimators at 66.9 to 67.3 against the golden's 64.9 and the gap at 2, 1 or 0. The registry now records a relocation when it processes that visit's note, one to four days later (manual 3.3), so the last visit precedes the loss date under every convention.
- A move allowed only after a quarter in the same class, tried the same day to close that convention instead: it made the move depend on the class history, so weights by the class at the visit no longer matched the moves and the projection fell 0.4 to 1.1 points below the weighting in every seed searched.
- The re-consent deadline of 1 April 2024, moved to 1 January 2025 the same day: 942 withdrawals with up to twenty months left carried Wrenhaven's figure from 71 to 73 across the estimators; with a year at most left it holds at 72 under every one, and leaving the withdrawn out still names Wrenhaven.
- The round-1 and round-2 world (Gullhaven's class-specific death rate 1.16 times the others', class IV improving 8 per cent a quarter, moves at 2.2 per cent of class III visits and 24 per cent of class IV), rejected after stage 4 round 2: the judge's class-adjusted estimators put Gullhaven between 64.9 and 67.3 per cent; pooled outcome models imported the other hospitals' death rate and the fixed-last-class and landmark models misread the movers' improvement, so the gap read 2, 1 or 0 by method.
- A seed search in that world with the relocation dated after the reporting visit (450 seeds), rejected: two seeds kept every by-hospital form in one bin, none with the pooled forms agreeing, and their leads were a point; luck in the seed was not a forced answer.
- Wrenhaven's re-consent on 1 January 2025 with three in four withdrawing, rejected in fix pass 2: its 2023 patients carried up to a year past the withdrawal spread the estimators 0.5 points on Wrenhaven; the deadline moved to 1 May 2025 with nine in ten withdrawing, the spread 0.3, the dropped and dead-counted readings still on Wrenhaven.
- A later deadline with Wrenhaven's mix unchanged (1 March or 1 May 2025), or 1 June with it sicker, rejected in fix pass 2: too few withdrawals for the dropped and the dead-counted readings to land on Wrenhaven rather than Gullhaven, and the complete-case route then lands Gullhaven within a point of the golden's figure.
- The discrete projection counting a death only within 91 days of a visit, corrected in fix pass 2: a visit kept late or missed dropped about one death in twelve, so the projection ran 0.2 to 0.5 points high on Gullhaven.
- Ask A asked as "the NT-proBNP tests its laboratory reported", replaced in fix pass 3: read literally every released row is a reported test, so counting a corrected specimen once rested on a supersession rule no file states (stage 4 round 3's judge); the unit is now the specimen, filed in the prompt, and no correction crosses the referral level.
- Portal round 1 (2026-10-28): both responses missed the call (rubric average 12.5); both determinism judges failed it as answer_contradicts_files, reading the charter's 3.2 ("Every patient ... counts, including patients the registry no longer follows") as the deaths on file over every patient, a lost patient counted alive (R0, Fennick). Not a redesign: closing the reading leaves the default path (Kaplan-Meier, Fennick) where it was. Repaired at the WHAT only: 3.2 now puts every patient in the share and says the registry does not learn of the deaths of the patients who left follow-up; SF13 asserted; the write-up's steps say why the deaths on file cannot stand for survival and why the class at the move carries a lost patient's chance of dying. No estimator filed.
- Determinism repair, round 1 of the portal (2026-10-28), sent back: with 3.2 reworded the re-judge (pass 5) accepted the crude reading as closed, then returned NOT_DETERMINISTIC, SEND_BACK. Gate C: plain Kaplan-Meier, every move as ordinary censoring, is a standard reading every filed rule allows and names Fennick (61.16 against Gullhaven 62.35), while carrying the lost from their class is filed nowhere; Gate G: the mechanic classed single_conceptual_flip, a standard statistic rejected as misleading. Two corrections of one graded quantity (determinism-check section 3): filing the class-carried estimator makes the decisive step rule application, filing Kaplan-Meier makes Fennick the answer, so the stump lives in the fork and no closure keeps it. Redesign of the decisive step at stage 2 (/build task268 from 2): keep the registry world if a split off the censoring treatment can be found, else re-root. Carry forward: 3.2's wording that closes the crude reading (every patient in the share as they were at two years; the lack of a death on the registry's files does not show a lost patient alive; a first wording, "whose deaths the registry does not learn of", was still read as alive by default), the deck's embedded-workbook stamps pinned, the Linux-only rebuild, and block 1's Wrenhaven count, 347, which did not reproduce (931 every CNR event, 336 those inside the two-year window).
- Architecture 4's first card labels, Gate G `forecasting` and strategy `composition_mix`, withdrawn on 2026-10-28 before any data was cut: the vocabulary defines forecasting as a forecast the correctly read past does not pin, and this design's closed years pin the development; composition_mix and the executive forum then met task270 v11's bans. Redrawn to method_or_model_selection, forecast_method_backtest and committee_or_panel, each the honest key.
- A notifying-channel column on the claims extract (Policyholder, solicitor, claims-management company and the rest as one field), rejected at stage 2 on 2026-10-28: with the Standard's back-test filed, every grouping the extract's own columns offer is an enumerable model class behind a shipped test, which the library records as an answer key (task38). The extract keeps the claims system's coarse notified-by field, and the firm type lives on the representatives table.
- Region-level development as the default, with no filed selection criterion, rejected at the draw: task127 v3 and this slot's architecture 3 died at the judge for leaving the method open. The Standard files the back-test in general terms and puts regional estimates on the whole book's factors (3.2), so each region's own development is against the text as well as failing 2022.
- A Severn own-damage rate at its first value and a Pennine wave of 0.55 per 100 car-years, measured on the prototype on 2026-10-28: the route split itself named Mersey and Severn (Pennine 8.03 against 8.25). The wave became 0.85 per 100 car-years and Severn's own-damage rate 7 per cent lower; seed 5 is the first of six where every route-based development prints the same five figures and the back-test separates at 1.1 against 6.8 per cent.
- Ask B (private-car claims notified on 2026 accidents by region, injury against the rest, the online notification journey's abandoned first records as its device), retired at stage 4 on 2026-10-28: the determinism judge's first pass found the call and Ask A uniquely forced and Ask B open, because no shipped file says the abandoned record is the phoned claim and the Standard's 2.1 ("every claim notified counts once, including claims closed without payment") reads literally for counting it. The device cannot be both determinate and silent: identity filed or carried on the row, the careful solver executes 2.1 and the cracker keeps the ask; left unfiled, it is a fork. The twins were taken out of the world (2026 rows only, no figure of the call moved) and the ask layer became the cars on cover by all three covers, the reconstruction the judge confirmed.
- Architecture 4 (a motor insurer's 2027 telematics pilot regions, the claims not yet notified developed by notifying route, the route built by joining each claim's representative to the representatives table), spent 2026-10-31 on the learning loop's paper screen: the route sits one join away (the notified-by field and the representatives table) and development by notification channel is the reserving field's own refinement, so the decisive rung was a reflex; the slot moves to marketing-consumer-research (segmentation-market-structure), a new world, dataset, generator and prompt shell.
- Marketing draws screened on paper before this one, 2026-10-31: excess duplication judged over shoppers whose stores stock both brands (task281's note: filing the co-availability population is rule application, leaving it unfiled forks the call); a receipt-scanning panel whose submissions rise in a brand's bonus weeks (the correction needs a submission model, so the estimator family is open); a sub-panel's cross-media duplication applied to the full panel (one consistency check of the sub-panel's TV reach against the full panel's lands it); an exposure crediting quirk in the as-run log (reading what a record means, data semantics); mystery-shopper audits inflated by detection (the calibration against the CCTV census is the natural data-fusion reflex and reaches the golden).
- The bank-card reference carried on the till lines themselves (a card alias beside the Rewards card on every row), set aside at stage 2 on 2026-10-31: a self-join on a column of the main file is the one line of code the survivor anatomy's Link test refuses, so the card reference lives only in Faircourt's settlement file, reached by a match on terminal, time and amount.
- A card acceptance cost by store and quarter as the settlement file's own ask, set aside at stage 2 on 2026-10-31: the cost belongs to another owner (finance) and the organisation already has it on Faircourt's monthly statements (H18); the settlement file's second use is the counter's card payments instead.
- The Roastery's own loose beans at the counter, set aside the same day: a home buying them would open a fork on what buying the Roastery means; the counter sells guest roasters only.
- A link standing on any single shared payment, measured on the prototype on 2026-10-31: with one in three couples' links resting on one or two shared payments, a reading that needs two or three moved Oro Rosso's share by six points and named Nordhavn at three; a home's shared card is now a habit (used three times or more by each card it links, the weaker uses falling back to the member's own card), so one, two and three shared payments build the same homes.
- Counter labels matched only to card payments, set aside the same day: the counter's card takings would tie to the sold labels (an oracle for both devices); cash customers pay at the main tills and the counter terminal also takes accessories, so no total ties.
- Seeds 1 to 81 and 101 to 266 screened on the in-memory world on 2026-10-31 for every rung's winner and margin (1.15, the decisive 1.2), the runner-up a point clear of third, every share off its rounding edge (the call and runner-up by 0.15), the gap rounding alike from unrounded and rounded shares, link thresholds identical, online accounts alone never naming the call, both asks' figures off their edges and the cracker missing every ask figure: seeds 263 and 276 passed; 263 kept (its one-line adjustment stop keeps 4 of 20 against 276's 11).
- The counter's card terminal as the only way to pay, and a scale clock reset in April, set aside in the stage 3 build on 2026-10-31: with no cash route the counter's takings tied to the sold labels, and a two-week April reset moved only three cells; cash labels now go to the main tills, the reset runs 22 June to 14 July across the second and third quarters, and the funding rates are odd cents so no quarter sits on a half euro.
- Multibuy deals whose cheapest pair cost less than the deal price, found in the stage 3 build: a pair of Cafetto Original 200g at 14.98 against a two-for-15.00 deal produced negative savings; every deal now lists packs of one price.
- The counter's matching left to windows the pack never stated (stage 4 judge, FIX_NOW): 122 card sales read two ways at
  one total and 114 cash lines had two same-priced labels; the board now files the 25 minutes, the same day and the
  void at closing, and the generator re-weighs any label that allows a second reading under any window near them.
- Architecture 5 (the rival whose buying homes least often also bought the Roastery, homes assembled from the Rewards cards and online accounts that share a bank-card token in Faircourt's settlement file), spent at its first portal round on 2026-11-07: both responses named Oro Rosso, each building homes through the settlement file's card reference (one response lists its "household-linkage" assumptions). The prompt and the brief file the unit as the home, which determinism requires, and once the home is filed the shared payment card is the only record that joins two cards, so the linkage ran as a work order: filing the estimand announced the rung, and the construction is the join that cleaning the data already asks for (Layer 1 carrying the stump). No closure keeps it, since leaving the unit unfiled forks the call between cards and homes. The slot re-roots to architecture 6 in another world, dataset, generator and prompt shell, with a decisive step that no filed unit or join announces.
- Architecture 6's first candidate, set aside at the draw on 2026-11-07 before registration: a Lisbon ticketing marketplace's internal service latency SLIs read from a trace store kept under head-based sampling set per entry route, each downstream span inheriting its trace's entry rate (checkout in full, search at one per cent), so the services checkout calls look slow until each span is weighted by the inverse of its trace's entry rate. The setting and driver hit no slot note, but task452 v2 (shipped) already teaches the insight: weight each sampled record by the inclusion probability of the stratum it was drawn in, not the grouping it is analysed by. One sentence covers both, so the draw would read as a clone. The guard also showed the signature crowded: gap population with method_or_model_selection is spent on G14 (ten builds), G9 (five), G6 (nine) and E (the slot's own architecture 1), and G12 is banned against task190.
- Architecture 6's second candidate, set aside at the draw on 2026-11-07: a ride-hailing platform's 2027 background-check vendor, which moves a driver sign-up inside the activation target only where the check cleared last, the other requirements (documents, vehicle inspection, training) running alongside it. The slot screen found it spent: task127 v2 (the portal landed it) credits an intervention only with the replaced step's excess over a concurrent step, and task472 v2 credits saved work only where it moves a release into an earlier window.
- Architecture 6 first drawn with a per-service hourly sampler (2026-11-07, registered 21:54:53Z, pack built and golden
  reproduced on seed 2718): it cleared the ladder on 51 of 60 seeds (golden ratio 1.31, wrong-route margin 0.14) and was
  superseded before stage 2, because once a service's kept spans read flat at the sampler's target each hour, the hourly
  reweighting is one join from the load balancer's counts and both top responses would take it; it is rung 3 here.
- SLIs to two decimals on the edge-sampler world (2026-11-07): the standing estimators (Horvitz-Thompson on the balancer's
  count, Hajek, hour-calibrated) spread 0.01 to 0.08 points on the internal services, so almost no seed held all three on one
  two-decimal figure; SLIs are reported to one decimal, the precision 744 hours of about 24 kept traces an edge service carry
  (the golden and the world's truth differ by 0.05 to 0.1).
- accounts' sign-in texts sent through notifications (2026-11-07): 4 per cent of sign-ins, about one kept text an hour, each
  weighted at about 150 requests, moved notifications' estimate 0.3 points between seeds and opened the corridor to 0.08;
  removed from the call graph.
- Partner-gateway's seat inventory read set to a target slow share (2026-11-07): 0.25 per cent at 1,000 ms forced a 340 ms
  median, which alone put 19 per cent of seat maps over their 500 ms line; set to a fixed 85 ms read.

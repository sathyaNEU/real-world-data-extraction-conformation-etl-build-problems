# task214 design note

Seed AD37 (wave 8, Anomaly Detection & Diagnostics), header and Situation only: the world (a cloud batch platform
turning on speculative backups for the second half), the decision (which job families the scheme admits under the
capacity policy's 5 per cent extra-instance cap) and the quantity (the net saving, SLA credits avoided net of backup
compute). The seed's own devices (an admission procedure with a tie-break, a planted four-way tie, the scheduler
team's preference as a decoy, the pilot as a certified record) are not used as the decisive step.

## Draw

Status: no card registered. Candidate 1 is spent (## Tried and rejected); the next candidate is screened before
any card is registered. What stays valid for the next candidate:

- **Pairing:** `business-operations-analytics` / `service-operations-sla`, client domain General Statistics & Data
  Science, task type `exploratory-data-analysis-distribution-assessment` (AD). The seed's product-analytics tag serves
  no AD task type; GSDS x anomaly-detection is held by task212 in flight (ban.pairing); an SLA register with settled
  credits against internal chargeback is service-operations SLA work.
- **World:** Almring Bank Group (Vienna), its private-cloud batch platform Larix; six job families (card
  settlement, payments clearing, transaction search index, regulatory reporting, risk aggregation, customer
  analytics scoring) run nightly batch against SLA deliverables; a missed deadline settles an SLA credit against the
  family's chargeback; backups (a second copy of a slow instance on the reserve pool) start 1 July 2027 for the
  families the capacity policy admits under its 5 per cent extra-instance cap, counted as backups launched against
  instances run. `generator/world.py` is the clean-truth simulator of this world (placement, anti-affinity, the
  storage nodes, fail-slow episodes, heavy shards, co-tenant contention, feeds, Vienna wall-clock schedules across
  the March clock change); its mechanism block is candidate 1's and is replaced with the next candidate's.
- **Guard probes (2026-11-07, draft card in scratch t214/task214_card.json):** gap population with G8 and
  decomposition_attribution BLOCKs test.same_driver (task402 lineage, task303); gap objective clears it; forum
  committee_or_panel (task211), executive_team (task212) and line_manager_or_team (task213) are held, so the call
  goes to the platform operations desk that switches the scheme on (operations_desk), WARN only after that
  (objective, shape 01 and Gate G overuse; question form which against task212).
- **Personas:** `guard.py names --geo austria --seed 214`: Dilara Riener, Danilo Heinz (drawn, not yet placed).

## Tried and rejected

- 2026-11-07, paper: data skew read from input size (a column; the Mantri reflex reaches it).
- 2026-11-07, paper: upstream lateness from the dependency log as the decisive step (one join; critical path is the
  field's own method, so it sits at rung 1).
- 2026-11-07, paper: the trigger's launch delay as the decisive step (a stated rule executed: rule application).
- 2026-11-07, paper: the backup's remote-read penalty (a locality column makes it schema-readable).
- 2026-11-07, paper: credits avoided across families through the dependency graph (the step settles which credits
  count, the population: the WHAT screen kills it).
- 2026-11-07, paper: the cap as concurrent slots in correlated bad nights (a stated cap executed: rule application);
  commit-lock waits (indeterminate); cold image pulls on deploy days (an aggregate spike around dated events).
- 2026-11-07, prototype v1 to v8 (scratch t214/proto): the golden's before and after windows starved on fail-slow
  hosts; the naive culprit rules (slowest co-tenant, contemporaneous magnitude) landed the call while disk-bound
  shards of the winning families shared fail-slow hosts with each other; fixed by the platform's own placement
  (anti-affinity within a job, the search index on its dedicated storage nodes) and workload mix (CPU-bound general
  families), not by wording.
- 2026-11-07, candidate 1 SPENT at screen 4(c), never registered: the reverse-causality straggler (a heavy
  card-settlement shard slows its own host's co-tenants while it runs, so the bad-machine check credits a backup
  that would rerun the same work; the golden read the host's co-tenants before the shard started and after it
  ended). v9, 20 redraws: golden = clean truth = payments clearing + regulatory reporting 20/20, lead min 1.197,
  median 1.391; credits paid, every late job with a straggler, the textbook replay, the host check, magnitude,
  slowest co-tenant, per-record host x hour residual and host-night straggler count all wrong 20/20; but the
  per-record reader with host x night cells, reading the residual as the shard's own work, reached the golden set
  20/20, and the golden's both-sides variant held only 14/20. v10 (skew 3 to 18 times, fail-slow 4 to 72 hours):
  host x 4-hour and x 8-hour residual readers 20/20, host x night 16/20, golden lead median 1.158 (14/20 under
  1.2), both-sides variant 0/20. Why it dies: the information that decides (the host's state outside the
  straggler's run) is a host-by-time aggregate, and any cell wider than a heavy shard's run and narrower than a
  fail-slow episode separates the two; no realistic setting separates them in time without starving the golden's
  own before and after test. A copy escapes exactly the host component, so a correct host-versus-rest
  decomposition by cells is a correct method, which is the blind route.
- 2026-11-07, queued on paper after candidate 1 (not yet screened): (a) a commit wait behind another family's write
  to a shared output table read from heartbeat trajectories (risk: output-table x time cells recover it); (b)
  shard-level input waits through the catalogue's shard-to-part mapping (risk: the field's critical path at shard
  level is a reflex); (c) a self-dependent job whose late night pushes the next night's start (risk: a careful
  dependency replay is the field's method). Preferred next: transient stalls (escaped by any fresh copy) against a
  shard's heavy nights set by its clients' own cycles through the client-to-shard table (repeated by every copy),
  which no host-time cell, day-of-month interaction or lag reveals (pipeline.json resume).

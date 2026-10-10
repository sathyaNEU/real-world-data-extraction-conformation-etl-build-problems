# task128: November's 300 patch tickets across six estates, when a colocated drain rebuilds the whole host (realises analytical_tasks note DS02, analytical_tasks/05_decision_support/DS02_patch-tickets-window-drain-headroom.md)

Stage 1 (draw), drawn 2026-10-10. This is the build's one design note; the design stage extends it. The note is the idea and this build is its first realisation. Its decision and most of its world are kept; its decisive rung (drains per window) is kept as the stop rung, and a new decisive rung sits above it, because the note's own move fails the pilot's test (see Changes and Tried and rejected).

## Draw

```
DRAW  (independent draws, checked with .claude/skills/fingerprint/guard.py)
  Card filed with guard.py register before the ladder was written? registered by the coordinator in task-number order after task127, with the registration redraws recorded under ## Guard   Verdict: see ## Guard (registration)
  Shape: 01 ranked list under a cap   Gate G mechanism: binding_constraint
  Gap: objective (decisive), rule   Pattern: none at the decisive rung (G1 carries it), C at rung 2, B at rung 1
  Domain: business-operations-analytics   Subdomain (enumerated): field-service-maintenance   Objective: opportunity-sizing-decision
  Pairing repeated from last build? No. The last three on file are task125 (accounting-audit-forensic x anomaly-detection), task126 (policy-education x descriptive-distribution) and task127 (nonprofit-grant-making x opportunity-sizing-decision); business-operations-analytics x opportunity-sizing-decision has never been built
  Stakeholder role: remediation planner in the vulnerability management office, who splits the patch crews' 300 monthly change tickets across six production estates (capacity_planner)
  Context-artifact type: monitoring_export, the vulnerability scanner's exploitable-exposure export the planner works from and the CISO's belief rests on (the office's quarterly close-out of the four cloud estates still ships, as rung 1's corpus)
  Calibration form: closed_decision_corpus, the hosting provider's 412 closed determinations on change requests over six months, each accepted, part-accepted or declined against a window, whose drain rule the solver recovers
  Decision type: allocation_to_total, tickets per estate summing to 300, with the exploitable host exposures they take out in November
  Decisive mechanism: G1 unit-of-value swap. The provider rebuilds every colocated host it drains from the estate's current platform image, so the unit that takes exposure out on payments and checkout is the drained host, not the ticket's package. G2 supports (host rather than package as the unit of removal); G8 carries rung 2 (the drains), G16 rung 1 (the cut-day EPSS rule)
  Repeats from prior builds: none inside the ban window; G1 has never been the decisive generator on any card

  Niche: an online travel platform's vulnerability office splitting the patch crews' monthly change tickets across two colocated and four cloud production estates, sized by the exploitable host exposures the tickets take out in November when the colocation provider can drain only so many hosts a window and rebuilds every host it drains
  Forum: operations_desk (the crews' dispatch desk keys the cut list on Monday 2 November)   Forcing event: launch_or_rollout (November is the first month the crews' 300 tickets are allocated on exploitable exposure, the rollout that replaces the even spread by CVSS band)   Organisation family: hospitality_or_tourism
  Scoring unit: per resolved case (an exploitable host exposure taken out)
  World: Spain (Malaga); EUR; an online travel booking platform with a colocated payments platform and four cloud estates. Provisional invented names: Sendalia Viajes (the platform), Centro de Datos Guadalhorce (the colocation provider)
  People, drawn with guard.py names --geo Spain --seed 128, first six in draw order: Reina Guzmán (remediation planner, the requester), Santiago Vidal (CISO, the prompt's one belief), Prudencio Cañete (SRE lead for the colocated estates), Fabio Montalbán (data platform lead), Felicia Infante (the provider's service delivery manager), Eva Mas (patch crews' dispatch lead)
  Spine (planned): vuln_findings_2026-10-23.csv, about 210,000 rows, one open finding (one CVE on one installed package on one host), grain host x package x CVE, synthetic over real CVE identifiers with FIRST EPSS scores (licence and date recorded at stage 3)
  Deliverables (planned): november_ticket_cut.csv (the 300-ticket cut list the crews key off, one row per ticket), ticket_split_review.pptx (the split, the figure and the chart for the CISO)
  Opening move (provisional): deliverable-first (number-first opens task126; the design stage picks)
  Criteria arithmetic (shape 01): every candidate package update ranked by what it takes out in November and cut at 300. 6 estates x 2 (tickets that make the cut, exploitable exposures they take out in November) = 12, each estate's strongest ticket left below the line and what it would take out (6), the hosts the cap on drains lets each colocated ticket reach in November, the tickets the cap trims (2), the last ticket in and the first below the line with what each takes out (4), the total taken out (1), five named chart parts and two files, 32 before any device-carried ask; two six-estate device asks at stage 2 bring it to about 44. The committed call stays the split, so the decision type is allocation_to_total and the capped list is its structure
```

As-of date: 2026-10-23

Similarity claim: no prior build is this puzzle, because none values one use of a binding resource at everything that use resets on the member rather than at the item the request names; the nearest drivers on file score 0.07 (task108, task44 v2, task87 v8), and no card has ever carried G1 as its decisive generator.

Objective check: the headline figure is a sized opportunity built up from the addressable pool (every exploitable exposure on the six estates) to what November can realise (the hosts the provider can drain on the two colocated estates, valued at what a rebuild removes, and the crews' in-place updates on the four cloud estates), and that sizing drives the committed split. Nothing is predicted from a history, so the prompt cannot be retagged Forecasting without changing the ask, and it is not a description of a distribution, so Opportunity Sizing & Decision Support is the honest tag. The call faces forward (November, not yet open).

## Stump sentence

A competent solver recovers the cut-day EPSS rule from the close-out, builds each colocated estate's drains per window from the capacity register, the hourly forecast and the window calendar (the only reading that reproduces all 412 of the provider's acknowledgements), spends payments' 96 drains and checkout's 120 on the package updates with the most exploitable exposure per drained host, re-spends the rest of the cap on the cloud estates and files payments 5, checkout 6, search 71, media 102, internal tools 31 and data pipeline 85, taking out 4,050 exposures; the step that lands it there is crediting each colocated drain with only its ticket's package, when the provider rebuilds every drained host from the estate's current platform image, so one ticket on a package every host carries lets it drain the most exposed hosts and take out everything on them the November image fixes, which roughly quadruples what the two colocated estates' drains take out and frees nine tickets for the cloud estates.

(The figures are the source note's rung-3 answer, carried as the stump's wrong answer; stage 2 retunes every figure and asserts it.)

**Stage 2 restatement (supersedes the figures above).** A competent solver recovers the cut-day scoring rule from the close-out, builds each colocated estate's drains per window from the capacity register, the hourly forecast and the window calendar (the only reading that reproduces all 412 acknowledgements), spends payments' 96 drains and checkout's 120 on the package updates with the most exploitable exposure per drained host, re-spends the rest of the cap on the cloud estates and files payments 5, checkout 5, search 74, media 89, internal tools 47 and data pipeline 80, about 5,840 exposures; the step that lands it there is crediting each colocated drain with only its ticket's package, when every drained host comes back carrying nothing the current image already fixes, so one ticket per colocated estate naming its most exposed hosts takes out about 2,800, frees eight tickets for the cloud estates, and the split is 1 / 1 / 76 / 91 / 49 / 82 for about 8,210.

## Decisive rung

Measured trap **#25, assumes an effect the log could measure** (`.claude/skills/stumping/references/traps/_measured.md`): decided 1 of the client's 64 measured tasks, 0 of them under 0.50, so the record is thin and the rung is a stated bet. Its recipe is several past instances of the same intervention recorded in a log, a consistent effect across them, and an assumed effect that gives a different answer. Here the intervention is a drain on a colocated host. The solver assumes a drain installs the ticketed package and nothing else; the records measure what every past drain did: every colocated host carries only exposures whose fix was released after its last rebuild, and every host accepted in a past window shows a rebuild on that window's date, so a drain returns the host on the estate's current platform image.

Behind it, **#11, beats the headline trap, misses the quiet one** (4 of 64, 2 under 0.50): a solver who refutes the CISO's payments belief and builds the drains has beaten the loud trap and treats what a drain does as routine. The stop rung is **#10, notes a binding limit as a risk** (4 of 64, 3 under 0.50), reached through #12 and #4 on the acknowledgements.

Why the bet is taken over the top four: their architecture is a published control set that refutes the obvious construction, which is exactly what the pilot's plain solver reproduces and treats as a search signal, and the author's rule bars a corpus that refutes the stop rung. The decisive rung instead follows the architecture that held in the pilot (task117's final rung): an operational fact in records the solver has no reason to read for the question it is answering.

Gate G, in a sentence: every reported figure is correct (the scanner's exposures, the capacity register, the forecast, the acknowledgements, the close-out's ticketed exposure) and no stakeholder conclusion about its own numbers is overturned; the difficulty is that a colocated drain removes more than the ticket names, which no file states and no total shows. Flags: surface_read_dependency no; stumping_family analytical_non_defect; sole_data_defect no (no file is incomplete or wrong; the close-out answers its own labelled question, ticketed exposure closed, and no shipped instrument reports November's removal). The per-host value is not a second lens on one record: it is what the provider's operation does, pinned by an identity across every colocated host, and it moves the answer to different hosts and different tickets.

## Ladder sketch

Figures are the source note's, carried as targets; stage 2 retunes and asserts each one. The corrections walk the figure down until the decisive rung turns it back up, so the answer is bracketed between rungs 1 and 2.

- **Rung 0, the natural pipeline.** Rank package updates by exploitable exposure using the scanner's exploit-available flag on every host carrying each package, and fill the 300 greedily. Candidate: payments-heavy, the CISO's direction (payments 81, checkout 120, about 7,630). Satisfying because it is the office's own scanner ranked on the office's own objective. Killed by: the close-out's estate figures, which the flag reproduces only in total; only EPSS of at least 0.10 on the day each ticket was cut reproduces every one.
- **Rung 1, exploitability as the close-out pins it.** Candidate: payments 88, checkout 110, about 6,690. Satisfying because it reproduces every close-out figure. Killed by: the provider's acknowledgements: only per-window headroom one rack above the forecast peak of the window's own hours reproduces all 412 requests, and under it payments can drain 96 hosts in November and checkout 120, so most colocated tickets would complete in a later month.
- **Rung 2, the stop rung: drains per window.** Spend each colocated estate's drains on the package updates with the most exposure per drained host, then re-spend the cap on the cloud estates. Candidate: payments 5, checkout 6, search 71, media 102, internal tools 31, data pipeline 85, 4,050 exposures (the note's answer). Satisfying because the acknowledgements reproduce 412 of 412, every total ties and the CISO's belief has been refuted on evidence. Killed by: the host inventory read against the scanner: no colocated host carries an exposure whose fix predates its last rebuild, and every host accepted in a past window was rebuilt on that window's date, so a drain takes out everything on the host that the current platform image fixes.
- **Rung 3, decisive.** Value each colocated drain at the whole fixable exposure of the host it rebuilds; one ticket on a package every host carries lets the provider drain the 96 and 120 most exposed hosts, and the nine freed tickets go to the cloud estates. Candidate: payments 1, checkout 1, the four cloud estates 298 between them, roughly 5,400 exposures (about 470 on the colocated estates at rung 2 against roughly 1,800 here; set at stage 2 so the answer clears rung 2, rung 1 and every partial cell by the separation floor).

Partial cell to price at stage 2: a solver who finds the rebuild but keeps rung 2's five and six package tickets drains the hosts with the richest single package, not the most exposed hosts, and lands below the answer on the figure with rung 2's split; the build decorrelates single-package richness from whole-host exposure so that cell clears the floor.

## Why it survives the solver

Against `pilot_lessons.md`: the plain solver reads every document and executes every rule, so the SRE standard's headroom rule and the acknowledgements' reproduction take it to rung 2, which is where it is meant to stop; no document states that a drain rebuilds the host, and the provider's service schedule and runbook stay silent on it. It finds any join whose keys line up, but no join hands this over: the evidence is a per-host comparison of each exposure's fix-release date with the host's last-rebuilt date, and the coincidence of rebuild dates with past windows, both constructions rather than lookups (no platform-image manifest ships, and every exploitable colocated exposure has a released fix, so the November image's content needs no file). It replays records at the finest grain, and replaying the requests reproduces counts that do not depend on what a drain installs. It reconciles to control totals, and no shipped total measures what a colocated drain removed, because the close-out covers only the cloud estates the crews patch themselves. What held in the pilot was an operational fact sitting in a record the solver had no reason to open for the question asked (task117's pool-car hand-offs), and this is that architecture: a solver valuing tickets has no reason to ask what else a drain changes on a host. The residual risk is a solver that profiles the colocated hosts' exposure by last-rebuilt date; if round 1 lands the call that way, that is the hardening axis.

## Nearest exemplars

1. *Commit to 102 seniors brought to a regular diploma by the 2027-28 recovery schedule* (Policy & Education, Credit Recovery Program Planning), measured mean **0.45**. Nearest on the decision: what a fixed allocation actually realises under a capacity it cannot exceed; the model counted area by area and treated the period clash as a scheduling risk (#10), which is this build's stop rung.
2. *Merge the copied prospecting campaigns on 1 July instead of reverting the Anvil bid change* (Product Analytics, Paid User Acquisition), measured mean **0.58** (0.71, 0.72, 0.55, 0.45). Nearest on the decisive trap: the model beat the loud dated lure 4 of 4 and never measured the effect of the intervention from the seven past merges in the account's own change log (#25), which is this build's decisive rung.

Organ neighbour: *Award CROSSDOCK_CENTRAL_EPSILON to the Midwest Regional Corridor* (Supply Chain & Logistics, Parcel Sortation Facility Allocation), mean 0.47, a capacity limit in an operational log treated as a waiver, the stop rung's family.

## Guard

Verdict against the corpus as it stands at the end of the draw (121 cards; last three task122, task124, task125): **PASS**, exit 0, no WARN, on the scratch card. Nearest drivers 0.07 (task108, task44 v2), then 0.06 (task87 v8 lineage, task95).

BLOCKs met and cleared on the way, each by redrawing the axis it named:
- test.same_driver_older against task87 v9, on the first redraw (a data-cluster maintenance cycle as the decisive rung, time, G7, binding_constraint). Not differentiated, because its insight is task50 v4's (how much of a candidate's exposure a forward service order reaches inside the funded window); the redraw was abandoned (Tried and rejected).
- ban.shape 05 against task124, registered during the draw: shape 01, which is how the 300 are chosen (every candidate ranked by what it takes out in November, filled to the cap, the colocated tickets trimmed by the drain budget, the first ticket below the line).
- ban.artifact close_out_summary against task124, then ban.artifact operations_log against task125, both registered during the draw: monitoring_export, the scanner's exploitable-exposure export the planner works from, which had been banned against task121 when the draw opened and left the window as task124 and task125 registered.

Axes drawn to stay off the last three, each with the honest key: forum operations_desk (executive_team task122, committee_or_panel task124 and customer_or_counterparty task125 are inside, and line_manager_or_team was inside with task121 when the draw opened); role capacity_planner (the requester plans the crews' monthly ticket capacity; compliance_or_audit would also read true and was banned against task119 when the draw opened); geography Spain rather than Portugal, which repeated task121 when the draw opened; calibration counterparty_acknowledgement, forcing event budget_or_appropriation and organisation family hospitality_or_tourism, all clear.

WARNs: none on the final check. repeat.decision (allocation_to_total against task124) fired while task124 was the last build and cleared when task125 registered; if it returns at registration, the answer is that task124 splits a capped peak among committee blocks on a forecast newcomer share (population, E) while this build splits tickets under a drain-limited realisation (objective, G1), so the answer type repeats and the mechanism does not.

Batch note: task126 and task127 are still to register before this card, so the coordinator's check at registration runs against task125 to task127. Any of these keys can collide there: business-operations-analytics x opportunity-sizing-decision, decisive G1, counterparty_acknowledgement, monitoring_export, capacity_planner, operations_desk, budget_or_appropriation, hospitality_or_tourism, shape 01 (last two), csv+pptx, number-first (last two).

Registration (coordinator, 2026-10-10, after task124 to task127 were filed): the draft card took **BLOCK** on ban.calibration counterparty_acknowledgement against task126 and ban.forcing_event budget_or_appropriation against task127, and its subdomain would have blocked task129 (service-operations-sla, drafted in parallel). Each axis was redrawn with an honest key and the decisive rung is untouched: the provider's 412 acknowledgements are closed determinations whose drain rule the solver recovers (closed_decision_corpus, the vocabulary's definition); November is the first month of the exposure-based allocation (launch_or_rollout); and the patch crews' change tickets in maintenance windows are maintenance operations (field-service-maintenance), leaving service-operations-sla to task129's page-delivery service level. WARNs answered: repeat.gate_g (binding_constraint) and repeat.decision (allocation_to_total) against task127 are this build's honest keys, and the two differ where it counts: task127 is a fund's slot split under a meter crew's weekly queue (shape 05, decisive G7 on the time gap), this is a ranked cut list under a ticket cap whose decisive move swaps the unit of value from a ticket's package to everything a rebuilt host's image fixes (shape 01, decisive G1 on the objective gap). repeat.opening is cleared by the provisional deliverable-first.

## Changes from the source note

1. Decisive rung redrawn. The note's drains per window (measured #10) are kept as the stop rung, still certified by the acknowledgements, and a new rung 3 values each colocated drain at what the rebuild removes (G1, measured #25). The note's move fails the pilot test twice: the SRE standard states the N+1 principle in a sentence the solver executes, and the acknowledgements reproduce 412 of 412 only under the true rule, a corpus that refutes the rung below it.
2. Sign. The note's ladder walks down to its answer; the new decisive rung reverses the walk, so the answer is bracketed between rung 1 and rung 2.
3. Answer. The note's answer (payments 5, checkout 6, search 71, media 102, tools 31, data pipeline 85, 4,050) becomes the stump's wrong answer; the new answer is indicative (payments 1, checkout 1, the cloud estates plus nine, roughly 5,400) and is set at stage 2.
4. The note's hygiene rung (retired CMDB records resolved through re-image links on media and the data pipeline) leaves the ladder, which becomes four rungs: re-imaging vocabulary on the cloud estates would point a solver at what a rebuild does. The CMDB device returns at stage 2 as a hazard or an ask device.
5. Domain: Product Analytics · platform security operations becomes Business & Operations Analytics · field-service-maintenance (the draw first chose service-operations-sla; registration moved it, ## Guard). The remediation planner owns an operations call on change capacity, product-analytics has no honest subdomain for it, and the pairing has never been built.
6. Operating model. Colocated hosts are provider-managed and rebuilt from the estate's platform image at every drain; the four cloud estates are patched in place, package by package, by the crews. The design stage keeps every sentence about the rebuild out of the pack and keeps every exploitable colocated exposure fixable as of the as-of date.
7. Close-out scope. The office's quarterly close-out covers only the four cloud estates, because the provider closes colocated tickets, and it names its figure ticketed exposure closed, so it is no counter-pin to the vulnerability standard's host-level definition of taken out. The cut-day EPSS rule is recovered from its cloud-estate figures.
8. World. The note's cloud platform becomes Sendalia Viajes, an online travel booking platform in Malaga (EUR), with the colocation provider Centro de Datos Guadalhorce; six personas drawn with the guard. The requester is the remediation planner (the note's office manager); the CISO keeps the one belief, and the other voices are recast at stage 2.
9. Deliverables. The note's three files (ticket_split.xlsx, exposure_removed.png, patch_plan.docx) become two: november_ticket_cut.csv and ticket_split_review.pptx. The note's asks are re-cut at stage 2: ask C as written (each rung's split) names the ladder in the prompt.
10. Shape 01 (ranked list under a cap) replaces the note's 60-criteria grid, with the arithmetic in the draw block; shape 05 was the first draw and is banned against task124.
11. Dates. As-of 2026-10-23; the split is due Friday 30 October and the crews cut on Monday 2 November.
12. Acknowledgement grain. Whether the acknowledgements list accepted host identifiers or counts only is a stage-2 decision: identifiers let a solver join accepted hosts to their rebuild dates.

## Design (stage 2)

Stage 2, 2026-10-10. Every figure below is a target the generator computes forward from the records and asserts within the band stated; none is authored into a file. The figures were priced on a scratch prototype of the world (temporal colocated hosts, ranked cloud candidates) and will move at stage 3, where the generator re-tunes and re-asserts every one by name.

### Settlements made at design (on top of "Changes from the source note")

1. **Five rungs.** The draw's four rungs become five (R0 to R4): the SRE standard's headroom clause read at each day's forecast peak becomes its own rung (R2), killed by the acknowledgements, below the window-hours reading (R3, the stop rung). Each rung names a different split.
2. **No reboot sharing, pinned by the corpus.** Each change request's hosts consume their own drains, even where two requests name one host in one window. Without this, a stop-rung solver who packs many tickets onto each drained host would approach the answer's colocated figure without the decisive move. The acknowledgements carry overlapping requests, and only per-request counting reproduces them (Calibration, below).
3. **Colocated estates are smaller.** Payments 460 hosts in service (11.5 racks of 40), checkout 582. The source note's 1,400 made the window utilisations implausible.
4. **November is the season peak.** The travel platform's November evening peak (Black Friday week, month-end settlement) is why headroom is tight now; May to October windows carried more headroom, which is why the office's past requests were almost always accepted. No outcome series steps: no colocated exposure history ships.
5. **Two provider instruments.** Colocated findings come from the provider's managed-host feed (current state only, with first-seen dates); cloud findings come from the office's own scanner (open and fixed findings over six months, the spine). No file carries fixed findings for colocated hosts, so no reproduction check touches what a past drain removed.
6. **The inventory column is neutral.** The provider's host inventory carries `in_service_since` (the date the host last entered the serving pool). Its dictionary line says exactly that and nothing about servicing.
7. **Acknowledgement grain (note item 12): host identifiers ship.** Each acknowledgement lists the hosts requested and accepted. That is the log of past interventions trap #25 needs, and a solver uses it for nothing on the way to R3 (the back-test needs counts only).
8. **The colocated ticket's package is pinned.** The vulnerability standard files one ticketing rule: a ticket names the hosts that carry the package below its fixed version, and is raised against the package whose highest-scoring open finding on those hosts scores highest. Under R4 that selects one package per colocated estate (asserted unique); under every lower rung it selects the ticket's own package.
9. **Deliverables stay two:** `november_ticket_cut.csv` and `ticket_split_review.pptx`.
10. **Forward reason.** The call commits November's 300 tickets (forward). It is a sizing built up from the addressable pool to what November can realise, not a predicted value, so the objective stays Opportunity Sizing & Decision Support.

### Gate G

**Gate G line:** binding_constraint over correct data, with method_or_model_selection support (two rules recovered by back-test); surface_read_dependency no; stumping_family analytical_non_defect; sole_data_defect no; no shipped artifact ranks the six estates on November's realisable figure.

- **Litmus, in a sentence.** No: every reported figure (the scanner's findings, the provider's feed, the capacity register, the forecast, the acknowledgements, the close-out's ticketed figure) is correct and no stakeholder conclusion about its own numbers is overturned; the difficulty is valuing a drain, a use of a binding resource, at what it actually removes from the host, which no file states and no total shows.
- **Primary mechanism:** `binding_constraint` (the provider's drains per window cap what colocated tickets realise in November), with `method_or_model_selection` for the cut-day exploitability rule and the per-window headroom rule.
- **Flags:** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
- **Deletion test.** Delete the CISO's belief, the superseded allocation memo and the drain tool configuration: the scanner, the feed and the drains still lead a competent solver to R3. No wrong number exists to delete.
- **Clean-data test, per suspect file (asserted at stage 3).** (a) The provider feed (current state only): give it six months of fixed findings and recompute; the answer and the R3 figure are unchanged, because November's value is read off the current state either way. (b) The acknowledgements (hosts listed, no servicing detail): add a servicing column and recompute; unchanged. (c) The instrument repair: an instrument that reports what each past drain removed would make the rebuild visible, but it measures the past, and the November figure still has to be built from the drains, the headroom rule and the host ranking, so the answer is constructed, not read. `answer != naive` holds under all three.
- **Lens-swap test.** The R3 read and the answer are different populations of hosts and tickets: R3 drains the hosts carrying its five densest packages on each colocated estate, the answer drains the most exposed hosts under one ticket and moves eight tickets to the cloud estates. Asserted: the overlap of the two drained host sets is under 15 per cent on each colocated estate.

### Entity, unit of value, decision

- **Entity.** Sendalia Viajes, an online travel booking platform in Malaga. Its vulnerability office splits the patch crews' 300 monthly change tickets across six production estates and is scored, from November, on exploitable host exposures taken out in the month (an exposure is one exploitable vulnerability on one host; taken out means gone from the host by month end, the standard's definition).
- **Two quantities that both read as the size of a colocated ticket:** the exposure its package carries on the hosts it reaches, and the exposure on the hosts it reaches. They rank colocated tickets differently because a drained host comes back carrying nothing the current image already fixes, so a ticket on a widely carried package lets the office choose which hosts are drained.
- **Decision.** Tickets per estate across {payments, checkout, search, media, internal tools, data pipeline}, summing to 300, with the exploitable host exposures the split takes out in November.

### Answer (targets)

| Estate | Tickets | Exposures taken out in November |
|---|---|---|
| Payments (colocated) | **1** | about 1,330 (the 96 most exposed hosts) |
| Checkout (colocated) | **1** | about 1,470 (the 120 most exposed hosts) |
| Search | **76** | about 1,370 |
| Media | **91** | about 1,680 |
| Internal tools | **49** | about 840 |
| Data pipeline | **82** | about 1,520 |
| **Total** | **300** | **about 8,210** |

Every per-estate figure and the total are graded to the nearest ten and tuned to sit at least 2.5 inside their bin (asserted). Last ticket in: a data pipeline update at 11; first ticket below the line: an internal tools update at 10 (both unique values at the boundary, asserted).

### Ladder

Splits are payments / checkout / search / media / tools / data pipeline. Figures are each rung's own reading of what the split takes out in November.

| Rung | Construction (what the solver builds) | Split | Figure | vs answer | Killed by (one shipped fact) |
|---|---|---|---|---|---|
| R0 | Rank every package update by the findings carrying the scanner's exploit-available flag on the hosts carrying it, fill 300 | 19 / 20 / 54 / 90 / 37 / 80 | about 16,630 | +103% | The Q3 close-out: the flag misses 11 of its 12 estate-month figures and its quarter total by about 14 per cent |
| R1 | Exploitable as the close-out pins it (score of at least 0.10 on the day the ticket is cut, latest score for November), every ticket assumed to complete | 19 / 19 / 73 / 88 / 22 / 79 | about 11,730 | +43% | The SRE maintenance standard: colocated work happens only by draining hosts, and the estate keeps one rack above its forecast peak while it does |
| R2 | Drains bounded by headroom one rack above each day's forecast peak (the clause's literal reading): payments 88, checkout 48; densest packages first, cap re-spent | 5 / 2 / 75 / 90 / 48 / 80 | about 5,720 | -30% | The acknowledgements: the day's peak reproduces about 340 of 412; only the peak over the window's own hours reproduces all 412 |
| R3 | **Stop rung.** Drains per window from the capacity register, the hourly forecast and the window calendar: payments 96, checkout 120; densest packages first; cap re-spent | 5 / 5 / 74 / 89 / 47 / 80 | about 5,840 | -29% | The host inventory read against the feed: no colocated host carries an open finding whose fix was published before its `in_service_since`, and every host accepted in a past window entered service on that window's date |
| R4 | **Decisive.** Each drain valued at every exploitable finding on the host it returns; one ticket per colocated estate on the package the ticketing rule selects, naming the most exposed hosts; eight freed tickets to the cloud estates (two each) | **1 / 1 / 76 / 91 / 49 / 82** | **about 8,210** | | |

**Gaps, rung by rung.** R0 to R1: gap 4, rule (G16; the close-out back-test selects cut-day scoring). R1 to R2: gap 3, objective (G8; drains bind on the colocated estates). R2 to R3: gap 4, rule (G16; the acknowledgements select window-hours headroom). R3 to R4: gap 3, objective (G1, the decisive unit-of-value swap, with G2 support: the unit a drain removes is the host, not the package).

**Why each rung is a place to stop.**
- R0: it is the office's own scanner ranked on the office's own objective, and it agrees with the CISO that the colocated estates carry the worst exposure per host.
- R1: it reproduces every close-out figure to the unit, which is the strongest evidence the pack offers about what counts as exploitable.
- R2: it executes a filed clause word for word and turns the colocated estates from the biggest destinations into small ones.
- R3: it reproduces all 412 acknowledgements, every total ties, the drains are built from three files, and the CISO's belief has been refuted on evidence.
- "A solver who does everything right up to R3 commits to 5 / 5 / 74 / 89 / 47 / 80 and about 5,840."

**The stump carrier is R3 to R4.** The seven survival properties: (1) no shipped sentence says what servicing a drained host does; the provider's schedule says hosts are drained, serviced and returned to the pool. (2) The acknowledgements are blind by construction: their counts do not depend on what a drain installs, and both readings reproduce 412 of 412 (asserted). (3) No arithmetic symptom: no shipped total measures what a colocated drain removed, because the close-out covers only the cloud estates and the feed is current state only. (4) Not a row predicate: it needs each host's latest accepted window (a group-and-max over the acknowledgements), compared with every open finding's fix publication date on that host, then a rank of hosts by whole-host count. (5) The enumeration is arithmetic (the host ranking). (6) No cutover date: every past window behaved the same way and no colocated series ships. (7) Survives deletion: nothing wrong to delete.

**Worth of each rung on the graded figure.** R0 to R1 -29.5%, R1 to R2 -51.2%, R2 to R3 +2.1% (window hours admit more drains than the day's peak), R3 to R4 +40.6%. The pre-decisive walk is down except the small R2 to R3 step, which stays 29 per cent under the answer; the decisive rung reverses it.

### Position and separation

The answer is a figure plus a split, so the separation floor binds rather than the ranking margin: the nearest wrong cell must sit at least 8 per cent from the answer's figure, and every rung's split must differ from the answer's in every estate's count. Asserted: every rung from R0 to R3 differs from the answer in all six counts; the stop rung's cloud counts each differ by 1 to 2 because the eight freed tickets are built to land two per cloud estate.

### Discriminator dominance

The stop rung's colocated drains take out about 530 (payments about 250, checkout about 280). The decisive move values the same 216 drains at about 2,800. Edge about 5.3x on the colocated figure; on the total, R4 clears R3 by 1.41x against the 1.2x floor. The richest single-package hosts carry about 5.5 exploitable findings each; the most exposed hosts carry about 13.9 (payments) and 12.2 (checkout): single-package richness and whole-host exposure are decorrelated by construction (the dense packages sit on hosts that entered service in the last five months), asserted as a correlation under 0.15 between the two on each colocated estate.

### Correction grid (four toggles; every cell priced on the prototype, re-asserted at stage 3)

Toggles: E (exploitable by flag or by cut-day score), L (no limit, day's-peak headroom, window-hours headroom), V (drain valued by package or by host), S (cap re-spent or not).

| Cell | Figure | vs answer | The shipped fact it violates |
|---|---|---|---|
| R0, R1, R2, R3 | as the ladder | +103, +43, -30, -29 | as the ladder |
| Host value, no limit | about 13,110 | +60% | the SRE standard (drains bind) |
| Host value, flag reading, window drains | about 11,270 | +37% | the close-out |
| Flag reading, window drains, package value | about 7,490 | **-8.8%** (nearest) | the close-out |
| Flag reading, day's-peak drains | about 7,290 | -11.1% | the close-out and the acknowledgements |
| Host value, day's-peak drains | about 7,260 | -11.5% | the acknowledgements |
| Rebuild found, the stop rung's five tickets kept, valued by host (partial) | about 6,280 | -23.5% | the ticketing rule (the ticket names the hosts) and the cap |
| Window drains applied as a haircut on R1's split, cap not re-spent | about 5,400 | -34.2% | the standard's objective (unused tickets) |

The nearest cell (-8.8%) costs two errors (the flag the close-out refuses, and the package valuation); stage 3 widens it toward 10 per cent and asserts every cell at least 8 per cent from the answer.

### Calibration corpora

**1. The Q3 close-out (pins R1, cloud estates only).** Twelve estate-month figures of ticketed exposure closed plus the quarter total, labelled for what they are. Rivals swept (seven): exploit flag; score at export; score at quarter end; score at cut (truth); the old CVSS band; score threshold 0.05; flag or score. Truth reproduces 12 of 12 and the total exactly; every rival misses at least 3 cells and the total by at least 4 per cent, the flag by about 14 per cent (directional, so no rival matches the total). Every in-scope finding open at export has a score outside 0.07 to 0.14 for its whole last 30 days, so the latest, 7-day and 30-day readings select identical rows for November (C1).

**2. The provider's 412 acknowledgements, May to October (pins R3).** Each lists the window, the requesting team, hosts requested and hosts accepted (identifiers), status and reason. Rule: within a window, requests are taken in submission order and accepted up to the window's concurrent drains times its cycles, less drains already accepted, counting every requested host-drain separately; concurrent drains are the whole hosts of headroom above the forecast peak over the window's own hours, less one rack of 40. Rivals swept (eight): day's peak; window average; drain tool parallelism; flat 10 per cent of hosts; distinct hosts per window (sharing); no rack reserve; two-rack reserve; truth. Truth 412 of 412; every rival misses at least 20 requests, each in both directions where the rival allows. Twin pair: two payments requests identical on hosts requested (8), team, weekday, hours (Tue 20:00 to 24:00) and month; one accepted 8, the other 4, because the second window held the month-end settlement peak; only window-hours headroom separates them. Every rule exercised: about 40 requests land in windows already holding accepted drains; about 20 windows span an hour where the forecast rises; about 25 overlapping-host requests separate per-request counting from sharing; checkout windows cross midnight so the window's hours span two dates. Blind by construction to what a drain installs: both drain valuations reproduce 412 of 412 (asserted).

### Pins and counter-pins

- **Vulnerability management standard (level 1, office):** tickets go where they take out the most exploitable host exposure in the month; an exposure is one exploitable vulnerability on one host; taken out means gone from the host by month end; a cloud ticket cut on the month's first Monday is closed by the crews within the month; the ticketing rule (settlement 8); the licensed wrong basis: the audit committee reads the plan as exposure ticketed and will see that table.
- **SRE maintenance standard (level 1, SRE):** maintenance never takes an estate below one failure domain of headroom at its forecast peak. One sentence; the corpus operationalises it.
- **Provider service schedule (level 2, provider):** windows, the 30-minute drain cycle, requests named by host, hosts drained, serviced and returned to the pool. No sentence on what servicing does.
- **Counter-pins:** none. The superseded CVSS-band memo is dated and marked superseded by the November rollout (a declared wrong-basis distractor); the drain tool configuration states a tool limit and is a declared distractor.

### Convention axes (determinism-check A.5, one line per axis)

| # | Axis | Reading chosen | Closure |
|---|---|---|---|
| 1 | Population | open findings at export on the six estates' in-service hosts, exploitable by score; cloud fixed findings excluded for November | C2 (close-out) + C1 (no in-scope score in the 0.07 to 0.14 band over the last 30 days) |
| 2 | Unit of account | host x vulnerability, per the standard | C1: no host carries one vulnerability under two packages (asserted zero), so finding rows and host-vulnerability pairs count alike |
| 3 | Attribution window | November windows for colocated; cloud tickets close in the month | filed (standard) + C1 (the calendar lists November's windows) |
| 4 | As-of dating | export 23 October, latest score 22 October | C1 |
| 5 | Version basis | one scoring model version across the history | C1 (asserted single version) |
| 6 | Denominator | none (counts) | n/a, dispositioned |
| 7 | Weighting | none | n/a, dispositioned |
| 8 | Measurement window | score at cut; November uses the latest | C2 + C1 |
| 9 | Boundary inclusivity | at least 0.10 | C1 (no score within the band) |
| 10 | Rounding path | integer counts summed, total and per-estate figures to the nearest ten at the end | C1: every graded figure at least 2.5 inside its bin, asserted |
| 11 | Tie-break | cloud cutline strict at every rung's boundary; host rank strict at 96 and 120 | C1 (unique values at R4's boundary; strict gaps asserted at R0 to R4) |
| 12 | Maturity | Q3 closed; November is forward | C1 |
| 13 | Order of operations | whole drains per window, then cycles, then summed | C1: headroom fractional parts at least 0.2 from an integer in every window, so per-window and pooled flooring agree |
| 14 | Row order | none | C1 (asserted invariant under shuffles) |
| 15 | Duplicate resolution | finding rows unique on host, package, vulnerability | C1 (asserted) |
| 16 | Identity normalisation | host identifiers identical across feed, inventory and acknowledgements | C1 (asserted; no device on these rows) |
| 17 | Netting | none | n/a, dispositioned |
| 18 | Dimensional units | forecast and per-host capacity in the same transactions-per-second unit | C1 (asserted) |
| 19 | Code semantics | acknowledgement statuses accepted, part-accepted, declined, deferred | C2 (the back-test) |
| 20 | Integerisation | whole hosts of headroom, floor | C1 (axis 13) |
| 21 | Scope of a clause | the headroom clause applies per window; requests count per host-drain | C2 (twin pair, overlapping requests) |
| 22 | Forward window contents | November windows booked to the office only (the calendar says so); no November request yet filed | filed (calendar) + C1 |

Two axes specific to the decisive rung. (a) What a November drain removes: every exploitable finding open on the host, because every such finding on a colocated host has a fix published before the export (asserted), so readings of "the image current at the window" converge (C1). (b) Which hosts: the 96 and 120 most exposed, strict at the boundary, and the ticketing rule selects one package per estate (asserted unique).

### Deliverables and criteria arithmetic (shape 01, ranked list under a cap)

1. `november_ticket_cut.csv`: one row per ticket in rank order (estate, package, hosts reached in November, exploitable exposures taken out in November). Script-generated.
2. `ticket_split_review.pptx`: the split, the total, the chart, and the estate card carrying the two device asks.

Criteria: the six ticket counts (6) and six November figures (6) and the total (1) = 13 on the call; last ticket in and first below the line, each named with its figure (4); ask A, six estates x 2 (12); ask B, four cloud estates x 2 (8); chart parts (one bar per estate on November's figure beside its open exploitable exposure today, estates in ticket order, the colocated bars annotated with their drains, the title carrying the total) (5); two files and the CSV's columns (3). About 51.

### Ask ledger (supplemental-stumping)

Main call's declared row population: open findings at export (scanner and feed), score history rows for those vulnerabilities, the provider inventory, the capacity register, the November and May to October forecast rows, the calendar, the 412 acknowledgements, the ticket log's Q3 cloud tickets and their fixed findings, the close-out. Zero device rows and zero hazard rows inside it, asserted by count at stage 3.

**Ask A: patch pace, six estates (12 figures).** For each estate, the median days from a vendor's first release of the fix to the day the ticket's last host ran it, over the office's tickets completed 1 May to 23 October, and how many of those tickets missed the standard's remediation target. Use: the CISO weighs whether each estate's tickets land, beside the split. H18 home: the other measure the deck carries for every estate. Primary devices: rollbacks in the crews' deployment log (a rolled-back deployment followed by a re-deploy; the dictionary defines the revert column; lazy reads the first time every host showed the fixed version) on the cloud estates; the provider's completion reports in UTC while checkout windows cross local midnight (lazy dates those completions a day early) on the colocated estates. Hazards: H1 vendor advisories republished with later revision dates (the standard defines the fix release as first publication; lazy takes the latest revision), moves all six estates; H2 superseded tickets in the ticket log (a later ticket on the same package carries the supersedes reference; lazy keeps both), moves four estates. Over-cleaning half: genuine retries on hosts that failed (no revert) whose completion is the retry. Path: ticket log, advisory feed, deployment log, completion reports, cloud asset register (host to estate), vulnerability standard, provider schedule (UTC note), data dictionary (8 files, 13 columns). Stops: lazy (first full deployment, latest revision, UTC) about 4 to 7 days short on the median in every estate; half-handled (rollbacks only) 2 to 4 short; over-cleaned (drop every ticket touched by a rollback) misses counts by 3 to 6; right rule on the wrong population (superseded kept) off by 1 to 3 tickets; answer. Every stop at least 2 days or 2 tickets from the golden.

**Ask B: scanner coverage, four cloud estates (8 figures).** For each cloud estate, the hosts in service on 23 October and how many of them had no authenticated scan in the 14 days before the export. Use: the CISO needs to know how much of each estate the exposure figures cover. H18 home: the trail that audits an input the call consumes. Primary device: the media estate's internal domain migration (hosts renamed mid-September; the asset register carries the instance identifier and the new name, the scanner's coverage file carries the old name for scans before the cutover); the dictionary pins the instance identifier as the key; lazy joins on hostname and counts migrated hosts as unscanned. Over-cleaning half: short hostnames reused across estates, so a join on the short name over-matches. Hazards: H3 coverage timestamps in UTC against a Madrid-local 14-day boundary (moves all four), H4 standby instances in the asset register that the standard excludes from in service (moves three). Path: cloud asset register, scanner coverage file, vulnerability standard (coverage and in-service definitions), data dictionary, the platform team's migration notice inside the planning thread, the spine's host list as referee (byte-clean, never trapped) (6 files, 11 columns; under the 8-file floor, recorded as a debt). Stops: lazy about 35 to 60 per cent over on media's unscanned count, 5 to 15 per cent elsewhere from H3 and H4; over-cleaned under on two estates; answer.

**Hazard table.** H1 (A: all six), H2 (A: four), H3 (B: four), H4 (B: three). Composed deltas for every subset outside each figure's bin, asserted at stage 3. No device or hazard family is repeated between A and B.

**Pair arithmetic.** Planning weights 38 / 7 / 55; ask criteria 24 device-carried (A and B) and 4 inheriting (last in, first below). r, the call criteria a stop-rung response keeps: about 0 (all six counts and figures differ by construction; the total differs by 29 per cent). Cracker = 45 + 55 x (4 + 24 x 0.2) / 28 = 62.3. Mirror (stop rung) = 0 + 7 + 55 x (24 x 0.2) / 28 = 16.4. Pair 39.4 at a device leakage of a fifth, at the 40 target; at a leakage of a quarter, 41.4. If no top response lands the call the pair sits near 20.

### Pack plan (names settled at stage 3 in the organisation's idiom)

Main path: the office scanner export (spine, about 210,000 rows, CSV); the provider's managed-host feed (JSON lines); the provider host inventory (XLSX); the scoring history (Parquet); the office ticket log (CSV); the Q3 close-out (PDF); the capacity register (XLSX); the hourly forecast May to November (CSV); the provider's 412 acknowledgements (XLSX); the vulnerability standard (DOCX); the SRE maintenance standard (PDF); the provider service schedule with the window calendar (PDF); the planning thread (EML); the data dictionary (MD). Ask paths: the crews' deployment log (CSV); the provider's completion reports (CSV); the vendor advisory feed (JSON); the cloud asset register (CSV); the scanner coverage file (CSV). Declared distractors: the drain tool configuration (YAML) and the superseded CVSS-band allocation memo (PDF). About 21 files, eight formats.

### Realism debts (stated)

1. Window utilisations of 90 to 93 per cent: forced by the four to six concurrent drains the ladder needs; mitigation, the season peak and fixed contractual windows, stated in the provider schedule.
2. Pack size about 21 files, above the 19 usual: the ask spans need their own files; mitigation, every file has an owner and a source system.
3. Ask B spans 6 files, under the 8-file floor.

### Stopping rule (written before any round)

One solver commits to any answer other than the golden: go to the judge. It lands the split and the figure: harden (three loops at most), first axis the host-profile route (a solver ranking colocated hosts by `in_service_since`). Still landed after three: retire.

## Harden loop 1 (2026-10-10): the ticket's reach

**The brief.** Round 1's plain solver reached the call at path step 4 by treating each drain as a rebuild and draining the 96 and 120 most exposed hosts under one glibc ticket each; it named the assumption it never tested ("the folder doesn't say which hosts the provider drains"), and the one it never noticed is that one ticket can spend a whole month of windows. Stumping Part 10, read the trace for assumptions: the solver's step still completes under the repair (the rebuild valuation and the host ranking are right, and so are the colocated figures) and still returns the wrong split.

**The new decisive rung (R5).** A colocated ticket rides one provider change request, and a request is for one window (provider schedule s.3, "A team requests a set of hosts for a window"). Each November office window drains 24 hosts, so spending payments' 96 drains takes 4 tickets and checkout's 120 takes 5, and the cloud estates keep 291 tickets, not 298. Measured trap **#4, never tests its reading against the control** (7 of 64, 5 under 0.50), with #2 behind it (the ticket as the unit when the unit that reaches hosts is the window's request). The control is the office's own record: 48 colocated tickets of May to October in `crew_deployment_log_2026.csv`, each carrying exactly one `change_request` (one of 48 requests now filed under team "Vulnerability management" in the acknowledgements), each run only on that request's window date (checkout's later hosts on the next date, past midnight), each with exactly `hosts_accepted` succeeded runs. Eight were part-accepted and never reached their declined hosts. The spanning reading predicts those eight continue in a later window; the record refutes it on 8 of 8, and no ticket carries two requests.

**Why it survives the plain solver (the bet).** No sentence links a ticket to a request: the standard defines a ticket by package and hosts, the schedule defines a request by window, the dictionary's `change_request` line says only "the provider change request the ticket was drained under". The link is in a column of a file the solver opens for the estate card (ask A), which it has no reason to read for the main call (task117's FC01 architecture). The acknowledgements reproduce 412 of 412 under both readings, and every count and total the solver checks ties under the spanning reading too, so nothing raises an alarm. The thread's "there is only so much we can drain in a month" frames the drains as a monthly budget (a belief, no figure). Risk: a solver that builds the cut list's "hosts it reaches in November" per window may file one ticket per window unprompted; a solver that opens the acknowledgements' team column sees an office team and may follow it to the crew log.

**Convergence on the ticket's host list.** Standard s.3 says a ticket "names the hosts that carry that package below its fixed version". Read as every glibc carrier or as the hosts the ticket chooses, the window takes the first 24 listed (the corpus accepts every partly accepted request's leading hosts in listed order), so both readings drain the same 96 and 120 hosts and file the same counts and figures (C1). Which 24 sit in which window is a partition that moves per-ticket rows on the cut list and nothing graded at estate level; the write-up grades the nine colocated rows together.

**Ladder as it now stands** (payments / checkout / search / media / tools / pipeline, total, against the answer):

| Rung | Construction | Split | Total | vs answer | Killed by |
|---|---|---|---|---|---|
| R0 | flag exploitability, no drain limit | 27/27/57/70/59/60 | 25,647 | +92.8% | the close-out (flag misses its cells) |
| R1 | cut-day score, no drain limit | 27/27/62/67/65/52 | 17,272 | +29.8% | the SRE standard (drains bind) |
| R2 | day's-peak drains, package valuation | 5/3/73/75/77/67 | 10,839 | -18.5% | the acknowledgements (window hours) |
| R3 | window-hours drains, package valuation | 6/6/72/75/77/64 | 11,100 | -16.6% | the feed against `in_service_since` (rebuild) |
| R4 | **stop rung**: whole-host valuation, one ticket per colocated estate spending the month | 1/1/74/77/79/68 | 13,359 | +0.4% | the crew log's one change request per ticket |
| R5 | **decisive**: one ticket per window | **4/5/72/75/77/67** | **13,302** | | |

"A solver who does everything right up to R4 commits to 1 / 1 / 74 / 77 / 79 / 68 and about 13,360."

**Position and separation.** R4 sits 0.4 per cent from the answer on the total, so the separation the stop rung needs is carried by the counts and the bins rather than the 8 per cent floor (asserted): R4 differs from the answer in all six counts (the seven tickets R4 adds are tuned round-robin over the four cloud estates: search 2, media 2, tools 2, pipeline 1), its total rounds to 13,360 against 13,300, and every cloud estate figure lands in a different ten. The lower rungs keep the 8 per cent floor (nearest R3 at 16.6 per cent). R2 and R3 now share three cloud counts with the answer (their cloud lines sit one and three tickets from the answer's), a residual a solver at those rungs collects; their colocated counts and totals differ.

**Dominance.** The decisive move does not change which hosts are drained (R4 and R5 drain the same 96 and 120, asserted), so there is no carried advantage to overturn: it changes how many tickets the drains cost, 9 against 2, and that moves seven tickets out of the cloud estates. R5 over R3 on the total is 1.20 (13,302 / 11,100); the colocated edge over the package valuation is 3,154 / 984 = 3.2x. Partial cell, one ticket per window but each drain credited with glibc only: 10,364, 22 per cent under (asserted at least 8).

**Stump sentence (loop 1).** A competent solver recovers the cut-day scoring rule, builds 96 and 120 drains from the window-hours headroom, finds that a drained host comes back on the current image and files one glibc ticket per colocated estate naming the 96 and 120 most exposed hosts, 1 / 1 / 74 / 77 / 79 / 68 for about 13,360; the step that lands it there is spending a whole month's drains under one ticket, when a ticket is one change request and a request is for one window, so the split is 4 / 5 / 72 / 75 / 77 / 67 for 13,300.

**Guard (card re-checked 2026-10-10).** The v1 architecture moved to the card's `lineage`, the new driver written; `guard.py check` returns no BLOCK. WARNs answered: driver.near 0.17 is this slot's own v1 (the stop rung it builds on); repeat.gate_g and repeat.decision against task127 as answered at registration. Nearest foreign drivers 0.08 (task108, task87 v4). The redraw rejected at the draw (task50 v4, a service order truncated by the funded window) is not this move: there the window cuts what one order reaches of a candidate's exposure, here the window sets how many requests the month's budget costs while the exposure reached is unchanged.

## Tried and rejected

- The note's own decisive rung (drains per window from the capacity register, the hourly forecast and the window calendar) as the decisive move: the SRE standard states the N+1 rule in a sentence and the acknowledgements reproduce 412 of 412 only under it, so a plain solver builds it from a stated rule plus a corpus that refutes the rung below; its driver also sits beside task106's shared-pool driver. Kept as the stop rung.
- A data-cluster maintenance cycle (each November ticket reaches only the nodes recommissioned inside the month): task50 v4's insight (a forward service order truncated by the funded window) under new nouns although text similarity read 0.06, and guard BLOCK test.same_driver_older against task87 v9 on (time, G7, binding_constraint).
- Exempting standby or idle-colour colocated hosts from the drain limit: constructible from the capacity register's serving-capacity definition and the SRE standard, and it is a class of honest records excluded from a constraint, the shape task58 v3 and v4 lost on Gate G.
- Reboot sharing among the office's own tickets on one host in one window: reads as task98 v2's driver (demand that rides on a unit already consumed), and the acknowledgements can be blind to it only if no record shows sharing, which leaves a sentence the solver executes.
- Office packages riding other teams' scheduled drains (the kernel team's rotation): provision elsewhere (task118, task36) plus a forecast of another team's rotation.
- An update pulling dependency upgrades that fix other packages: needs package-manager behaviour from outside the bundle, or a closed-ticket record that refutes the stop rung.
- Fix-availability gates (an internal mirror's soak, an extended-support entitlement, an end-of-life successor package): a status-word eligibility gate a solver executes in one join once any sentence raises it, or a correction to what the scanner reports.
- Hosts made clean as the scored unit: task87 v8's conjunctive coverage.
- Re-introduction on autoscaled estates and scan-confirmed closure: both turn on how taken out is read (a flow against a month-end state) or on the scanner as an instrument.
- Keeping counterparty_acknowledgement, budget_or_appropriation and service-operations-sla at registration: blocked against task126 and task127 (filed after this draw) and, for the subdomain, against task129 drafted in parallel; redrawn to closed_decision_corpus, launch_or_rollout and field-service-maintenance.
- The drain tool's parallelism setting as rung R2 (a filed concurrency figure between no limit and the window rule): whether it binds depends on whether two requests share a drained host, a fork the stop rung must not carry; kept as a declared distractor and a swept rival in the acknowledgement back-test, and the day's-peak reading of the headroom clause took the rung.
- Leaving reboot sharing unpinned at the stop rung: a stop-rung solver who packs many tickets onto each drained host approaches the answer's colocated figure without the decisive move; the acknowledgements now refute sharing through overlapping requests.
- The 3a colocated answer as built (one ticket per colocated estate on the package most drained hosts carry): no package was open on every top-96 or top-120 host, so under standard s.3 one ticket could not name the hosts it was credited with; replaced at 3b by an October glibc advisory on the C library every el9 host carries, the highest-scoring colocated finding.
- Acknowledgement host lists drawn at random from the drain pools (3a): accepted hosts did not share their latest window with in_service_since, which argued against the rebuild the decisive rung rests on; replaced at 3b by binding every host's in_service_since to its latest accepted window.
- Round 1 plain solver (2026-10-10) landed 1/1/76/75/77/70 for 13,362: the decisive rung (R4, drain values the whole host) was read straight off the host inventory, in the solver's words "a drained host is rebuilt from the current image. Hosts rebuilt after a CVE's disclosure don't carry it, so draining clears every finding on the host" (path step 4). Binding in_service_since to each host's latest accepted window (3b) plus no finding predating it makes the rebuild a lookup, not a construction; the silent-rung architecture failed here, harden loop 1 must break that per-host date coincidence.
- Harden loop 1 (2026-10-10), the architecture that died: R4 as a silent per-host rebuild rung with the office free to pick which hosts each colocated ticket drains. The solver's path step 4, "a drained host is rebuilt from the current image. Hosts rebuilt after a CVE's disclosure don't carry it, so draining clears every finding on the host. The best use is the 96 payments and 120 checkout hosts with the most exposures", completed in one lookup (in_service_since equal to the latest accepted window), and its own note named the assumption it never tested ("the folder doesn't say which hosts the provider drains. I assumed the hosts with the most exposures go first"). Loop 1 attacks that assumption, not the rebuild.

## Build record

Stage 3a, built 2026-10-10. Generator under `generator/` (params, cves, colo, cloud, windows,
golden, world, asks, writers_data, docs, deliver, checks, build, verify, ship). Pack in `target/`,
golden deliverables in `golden/`, `metadata.json` at the task root.

**Gate: all green.**
- Generator green: `build.py` runs `checks.run`, **104 assertions** pass (input gates; ladder
  ordering and winners; colocated (1,1) signature uniqueness; R4 over R3 1.22x and the colocated
  edge; nearest-wrong-cell 8 per cent; seven graded figures mid-bin at distance 4; decorrelation and
  the R3/R4 drained-set lens-swap overlap; the close-out and acknowledgement back-tests; November
  drains 96/120; ask answers well formed; metadata coherence).
- Independent verifier green: `verify.py` reads only `target/` and `metadata.json`, shares no code
  with the generator, and recomputes the answer split (1/1/76/75/77/70), every estate figure, the
  total (13,354), the November drains (96/120 from forecast + capacity register + window calendar),
  the close-out 12 cells, and the 412 acknowledgements. All match `metadata.json`.
- Two consecutive builds byte-identical (`ship.py`): 23 target files, 2 golden files, metadata. The
  shipped pack is byte-identical to both scratch builds. OOXML is made byte-stable by normalising
  member timestamps and every ISO datetime, including the chart's nested embedded workbook.
- Input gates asserted: 23 input files, 10 formats (csv, docx, eml, json, jsonl, md, parquet, pdf,
  xlsx, yaml), spine `vuln_findings_2026-10-23.csv` at 215,899 rows, two distractors
  (`drain_orchestrator_config.yaml`, `superseded_cvss_band_allocation_memo.pdf`) named in
  `metadata.json` and nowhere under `target/`.
- metadata clean, H1 scrub audit clean on both `target/` and `golden/` (no producer signature, no
  out-of-band timestamp); mtimes normalised to the 23 October export.

**Ladder as built** (split payments/checkout/search/media/tools/pipeline, total exposures):
R0 26/26/58/71/59/60 = 25,857 (flag, no drain limit); R1 26/26/62/67/65/54 = 17,562 (cut-day score,
no drain limit); R2 6/3/72/75/77/67 = 10,795 (day's-peak drains); R3 (stop) 7/6/72/75/76/64 = 10,963
(window-hours drains, per-package valuation); R4 (answer) 1/1/76/75/77/70 = 13,354 (whole-host
valuation, one colocated ticket per estate). The answer is the top feasible cell; R0/R1 overcount by
ignoring the drain constraint, R2/R3 undercount by crediting a drain with only the ticket package.

**Settlements made at build (design figures were targets; these are the computed values).**
1. The request corpus gets its own RNG (`Random(seed+20)`) so the mid-bin tuning of cloud ticket
   targets cannot perturb the acknowledgement back-test.
2. Cloud exploitability is rare by construction (about one exploitable CVE per package on a tuned
   number of hosts), so a cloud ticket takes out a modest count and the cutline sits at 9 to 10,
   with the two colocated tickets ranked first by a wide margin.
3. Mid-bin tuning nudges one safe cloud ticket per estate and the top drained colocated host so all
   seven graded figures sit at residue-4 (distance 4 from a multiple of ten); deterministic.

**Residual items for later stages (honest state).**
- R4 over R3 on the total is 1.22x, which clears the 1.2 discriminator floor but is thin; the
  colocated-figure edge is about 4x. A future hardening loop can widen the total margin by raising
  colocated whole-host exposure.
- Separation across rungs rests on the colocated (1,1) signature (unique to R4) and the total figure
  being at least 8 per cent from the nearest wrong cell; some cloud per-estate counts coincide
  between R2/R3 and R4, which the signature and figure separation cover.
- The ask layer ships its two asks (patch pace, scanner coverage) with their primary devices present
  (deployment rollbacks; the media domain migration keyed on instance id) and golden answers
  asserted; full hazard-stacking and the pair-ceiling simulation are a supplemental-stumping pass for
  a later stage, not part of the 3a evidence-pack gate.

### Stage 3b, write-up and ship checks (2026-10-10)

Repairs made in the generator before the goldens were frozen, each asserted in `checks.py` (114 assertions, all green; double build byte-identical; verifier green):
1. Graded figures sat at residue 4, one count from the nearest-ten flip; retuned to residue 2 (2.5 or more inside the bin, off the round value). The `bin.*` assertions now measure distance from the x5 edge.
2. The colocated ticket was not legal under standard s.3 (no package open on every drained host). glibc is now on every colocated host and carries one October advisory (published 13 October, score 0.9712), the only package open on every drained host and the highest-scoring; `ticket.*` asserts coverage 96 of 96 and 120 of 120.
3. The rebuild evidence now holds in the pack: every accepted host's `in_service_since` is its latest accepted window (new `accepted_host_ids` column, registered in the dictionary), hosts never accepted keep a pre-May build date, and every feed finding's `first_seen` follows its fix publication. `rebuild.bind`, `rebuild.identity`, `rebuild.no_future` assert zero exceptions.
4. Thirteen synthetic tuning identifiers (letters inside the CVE number) removed; colocated tuning now adds installed packages to the most exposed host, which keeps the identity.
5. The cloud cutline tied nine tickets at 9 across the line, so the split depended on a tie-break; `_tune_cutline` now leaves one ticket at the last value in (search sudo, 9) and one at the first value out (media libc6, 8), `cut.strict` asserts it.
6. Ask A counted 13 tickets completed before 1 May; filtered. Ask B's 14-day edge carried 171 scans on 9 October and 28 on 8 October; no scan now falls on either date, and standard s.6 pins in service (running) and covered (scan on or after export less 14 days). Standard s.5 pins completed as the last successful host run.
7. Dates after the as-of removed (two `in_service_since` of 26 October, base advisories clamped to 19 October).
8. Two file names renamed for leak.py sweep 1 (`cloud_q3_closed_findings.csv`, `vulnerability_management_standard.docx`); `november_window_calendar.csv` and `vendor_advisory_feed.json` registered in provenance and dictionary (H9), with `reg.*` assertions.

As built after 3b: answer 1/1/76/75/77/70 for 13,362 (13,360 to the nearest ten); estate figures 1,412 / 1,742 / 2,612 / 2,652 / 2,432 / 2,512. Stop rung R3 6/6/75/75/74/64 for 11,093; R4 over R3 1.20x on the total, the thinnest margin in the pack. Host ranks at the drain boundary tie on value (11 and 11 on payments, 12 and 12 on checkout), which moves no graded figure because the sum is the same whichever tied host is drained. `generator/golden.py` reads only `target/` and writes both deliverables; `build.py` asserts its split, figures and ask answers equal the world's. `deliver.py` retired, the ladder lives in `ladder.py`.

Residual risks for the judge and solver: the R4 over R3 margin is at the 1.2 floor; ask A's rollback device does not bite (a rolled-back run always precedes the successful re-run, so the latest-run reading lands the same median) and the advisory feed's revision dates never enter the answer because the log carries `vendor_first_release`; the chart's "ticket order" ties payments and checkout at one ticket each, ordered by their cut-list rank.

### Harden loop 1 rebuild (stage 3a gates, 2026-10-10)

Generator changes: `params.py` (office team and request counts), `windows.py` (`mark_office` relabels 48 of the 412 requests, 25 payments and 23 checkout, 8 part-accepted, one per window, on a separate generator so no capacity or acceptance changes; `nov_windows`), `asks.py` (colocated crew-log tickets built one per office request, runs on the window date and, for checkout, the next date; `change_request` column), `ladder.py` (R5 `colo_per_window`, per-window cut-list rows), `world.py` (R5 is the answer; `_tune_two_lines` makes both the answer's line at 291 and the stop rung's at 298 strict and spreads the stop rung's seven extra tickets over the four cloud estates), `docs.py` (dictionary line for `change_request`), `checks.py`, `verify.py`, `golden.py`.

**Gates: all green.**
- Generator: **247 assertions** pass, new ones covering the R4 against R5 separation in all six counts, the total's bin and every cloud figure's bin; the (4, 5) signature unique to the answer; R4 and R5 draining the same hosts; the strict lines at 291 and 298; glibc on 24 of 24 hosts for each of the nine window tickets; the crew-log identity (one change request per colocated ticket, no request carrying two tickets, every office request carrying one, runs on the window dates, succeeded runs equal to hosts accepted) and the spanning rival's 8 misses; the package-only partial cell.
- Independent verifier (`verify.py -I`, reads only `target/` and `metadata.json`): split 4/5/72/75/77/67, total 13,302, drains 96 and 120, close-out 12 cells, 412 acknowledgements, crew-log identity 48 tickets with 0 violations and 8 part-accepted. All match `metadata.json`.
- Two scratch builds byte-identical (23 target files, 2 golden files, metadata); the shipped pack byte-identical to them.
- Input gates unchanged: 23 files, 10 formats, spine 215,867 rows, the two declared distractors.
- `golden-realism`: the estate-card title is now computed from the figures (it named checkout slowest; search is, 26.0 days), a deck sentence the data contradicted was corrected (payments carries more open exposure than any cloud estate, not the worst per host; checkout's is higher), the slide-1 source line cites schedule s.3 and the crew log; chart opened and read. Container audit clean on `golden/` and `target/`.
- `leak.py`: REVIEW, the same lines answered below, nothing new beyond the dictionary's added line. `guard.py surface`: 0 pairs promoted. `guard.py heart`: WARN (answered under Harden loop 1). One `submission.md`, one `prompt.md` in the tree.

As built: answer 4/5/72/75/77/67 for 13,302 (13,300 to the nearest ten); estate figures 1,412 / 1,742 / 2,582 / 2,652 / 2,432 / 2,482, every one at residue 2. Last ticket in Data pipeline libjpeg-turbo8 at 10, first below Search libunistring2 at 9. Ask A moved with the crew log: payments 22.0 days and 4 over target, checkout 24.0 and 3, search 26.0 and 7, media 24.0 and 1, internal tools 24.0 and 3, data pipeline 23.0 and 0; the colocated sets are odd-sized (25 and 23), internal tools (30) and data pipeline (22) still even, a residual on a median. Ask B unchanged.

Thinnest margins: R4 sits 57 exposures (0.4 per cent) above the answer on the total, separated by counts and bins, not by the floor; R5 over R3 is 1.198 on the total.

### Stage 3b after harden loop 1 (2026-10-10)

- Rebuild: `ship.py` double build byte-identical (23 target files, 2 golden files, metadata), 247 assertions, verifier green; target, metadata and the cut list byte-identical to the loop-1 pack; only the deck moved (the realism pass below). `golden.py` prints the same figures before and after: 4/5/72/75/77/67, 1,412 / 1,742 / 2,582 / 2,652 / 2,432 / 2,482, 13,302; drains 96 and 120; last in Data pipeline libjpeg-turbo8 at 10, first below Search libunistring2 at 9.
- `submission.md`, rules stated as the generator applies them: step 1 now names both score sources (the parquet's latest score for cloud findings, the feed's `epss` for colocated ones; no feed CVE is in the parquet, so the old wording could not be followed on the colocated estates); step 2 states the window's hours (start hour to the hour before the end); step 5 states the host tie-break (`host_id`) and that windows take hosts in date order; step 7 says the completion filter reads the last succeeded run's date. Retrospective checks run on the pack: 632 accepted hosts with `in_service_since` equal to their latest accepted window, 0 exceptions; 0 feed findings first seen on or before their host's `in_service_since`; 48 colocated crew-log tickets, one change request each, 0 violations, 8 part-accepted; glibc the top-scoring feed package (0.9712).
- `golden-realism`: chart recoloured to the dataviz blue ramp (steps 250 and 550; the categorical validator flags the light step's chroma, relieved by direct labels on every bar), open-exposure bars now labelled with their exact counts so the deck carries the figures block 4 quotes, colocated annotations moved above their November bars off the open-bar labels; deck opened and read. Container audit clean on `golden/` and `target/`.
- `reduce-house-fixes`: clause citations resolve (standard s.2, s.3, s.5, s.6; SRE s.2; schedule s.3); one `submission.md` and one `prompt.md` in the tree; no em dashes.
- `leak.py`: REVIEW, the same nine lines answered under Leak review, no LEAK. `guard.py surface`: 0 promoted. `guard.py heart`: WARN (driver.near 0.17 against this slot's own v1, repeat.gate_g and repeat.decision against task127, each answered under Guard and Harden loop 1). Card answer, spine rows (215,867), deliverables and opening move (calendar-first) updated; `guard.py validate` 0 invalid.

## Leak review

- REVIEW sweep 3, `q3_2026_remediation_closeout.pdf`: matches the call on the estate names only; it carries Q3 cloud figures and no November figure or split.
- REVIEW sweep 3, `superseded_cvss_band_allocation_memo.pdf`: estate names and the prior percentage shares of the declared wrong-basis distractor; no ticket count or exposure figure of the answer.
- REVIEW sweep 4, `extract_provenance_2026-10-23.md`: the world's nouns (window, colocated, scanner, close-out) in file descriptions; nothing says what a drain does to a host.
- REVIEW sweep 4, `q3_2026_remediation_closeout.pdf`: states its own scope (cloud only, provider closes colocated); silent on rebuilds.
- REVIEW sweep 4, `sre_maintenance_standard.pdf`: the headroom clause the stop rung executes, by design; nothing on servicing.
- REVIEW sweep 4, `vulnerability_management_standard.docx`: the allocation, exploitability, ticketing, target and coverage rules (pins, not the move); no sentence on rebuilds.
- REVIEW sweep 4, `warehouse_data_dictionary.md`: field meanings, `in_service_since` neutral and `accepted_host_ids` as hosts accepted and drained, `change_request` as the request a colocated ticket was drained under; links neither the rebuild nor the window to the November ticket count.
- REVIEW sweep 9, `estate_transaction_forecast_2026.csv`: forward forecast through November is the input the drains are built from, forward by design.
- REVIEW sweep 9, `november_window_calendar.csv`: the November windows booked to the office, forward by design.
- Stage 3b re-run (2026-10-10): the same nine REVIEW lines and nothing new; the SRE standard's s.2 now names the window's hours, which is the stop rung's rule executed by design and says nothing about servicing or the ticket's reach.

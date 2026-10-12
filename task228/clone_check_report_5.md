# Clone check: task228 pre-flight (architecture 2, hardening loop 1) against every build, 2026-10-11

## Verdict

No reject-tier finding. There is no Exact, Same seed, Dataset or Template hit against any build. The one Track B item is the `ban.pattern` (decisive G16) against task134 that the author waived, and it is still the same ban. The card keys the new rung honestly.

## Scope and coverage

**Resolved scope.** This is a pre-flight on task228 against every build on file, with no window.
- **Build under audit.** Architecture 2 at hardening loop 1: branch `perssathya/task228-guardrail-alert-metric` at 32674c2, main merged at c53a719, `task228/target/` copied in. The branch had not moved at the end of the audit.
- **Pass.** Pass 5 for the number and the second on architecture 2. Earlier reports are untouched.
- **Draw order** (`guard.py recent`, all drawn 2026-10-11): task130, task132, task133, task134, task135, task228, task229. task230 follows on its own branch.
- **Neighbours added beyond the brief.** The brief named task130, task133 and task134 as the builds before. `guard.py` orders same-date draws by task number, so task132 and task135 also sit in that run. task135 is now the build immediately before task228: it was registered at 10:46 UTC, after task228's architecture-2 draw at 08:02, but sorts first by number. Both were adjudicated.
- **task134's position.** It is now two draws back, still inside the three-build ban window.

**Funnel.**
- **Extract.** The committed cache held no task228 entry, so it was stale. I re-extracted it in place: 129 cards.
  - 19 were fingerprinted from this checkout: task117 to task133, task228, task229 (its pack from `target.zip`).
  - 110 were carried from an earlier checkout and cannot be re-verified here.
  - The refreshed `fingerprints.json` and the guard's people cache are left uncommitted in `/home/user/orch/aud228`.
- **Screen.** `fingerprint.py screen --focus task228`: 127 builds screened (task1 and task2 have neither a prompt nor a pack), 126 pairs, **0 promoted**.
  - No hard tell: no byte-identical file, no same-seed table, no shared invented name.
  - No surface route: the top score is 0.0904, at the 88th percentile.
  - No mechanism route: no card meets task228 on more than two of gap, decisive pattern and decision type.
- **Guard.** `check` and `heart` both BLOCK only on `ban.pattern` (G16) against task134. Beyond that:
  - WARN `repeat.gate_g` against task134;
  - NOTE `driver.near` against this slot's own round-3 cut at 0.26 (differentiated on the card);
  - nearest driver from another slot: task229 at 0.07 (0.08 with task230's card in the corpus);
  - nearest heart text: 0.04 (task229's driver and stump);
  - no people or furniture finding. The persona scan's "Lucky Lake" is a station's place name, not a person.

  The loop-1 card draws exactly the BLOCK and WARN that the round-3 card (fcacbb3) draws, and fcacbb3 is the card the waiver was issued against.
- **Adjudicated: 14 pairs.**
  - Draw order, before: task130 (v3 card), task132, task133, task134, task135.
  - Draw order, after: task229 (its committed architecture-1 card, plus design 2 read from its rework branch) and task230.
  - task107 v2, the guard's earlier same-driver note.
  - Surface nearest: task131 (0.0904), task118 and task121 (0.0900), task124 (0.0891), task117 (0.0889), task123 (0.0887).

  Read by card only, from the mechanical sweep:
  - task73, task92 and the task51 v4 lineage, which meet task228 on two core axes (gap objective and `ranked_slate_under_cap`);
  - every other decisive-G16 card (task32 v2, task70, task80, task99, task104), none of which shares the gap.

  Forward, as warnings only:
  - the seeds task249 to task252;
  - task225 (seed AD48), which the seed sweep surfaced.
- **How.** All in this thread. The `Agent` tool is not available in this run, so no per-pair subagents were spawned and no server-side tool was called. I read:
  - every card named above, in full;
  - task228's prompt, design note, submission and target listing;
  - the text of task228's filed documents (NS-03, the Ninox and PLSM notes, the campaign plan, the anchor terms, the export notes), for the keying question;
  - task229's design note on this checkout, and its rework branch's note (from git, read-only);
  - task230's card and design note at `b230` cc57ac7 (from git, read-only);
  - the design-note heads of task130, task132 and task133;
  - the seeds.

  No golden file was opened, and no other build's answer key.
- **Left unread: 115 screened pairs.** None was promoted or named. Beyond the screen, three mechanical sweeps covered them:
  - the card mechanism scoring above;
  - the guard's heart sweep of task228's driver, concrete driver and stump against every card, lineage driver and ledger row (max 0.04);
  - two keyword sweeps across every card driver, concrete driver, stump, lineage driver and the shipped ledger.
    - Measurement-error language (own error, comparator, collocation, covariance, replicate, errors-in-variables, attenuation): nothing on file.
    - Shared-source language (err or fail together, shared input, parent or source, common mode, redundancy, voting): only task229 architecture 1.

**Mechanism coverage (127 screened).**
- 105 have a card (91 native, 14 back-fitted).
- 5 have a design note only (3 back-fitted).
- 17 are unavailable (all back-fitted, task36 and earlier) and were checked on Track A only.
- Outside the screen, task134, task135, task99 and task114 to task116 were compared by card through the guard, and task230 by card and design note.

**What was not checked, or was checked against something stale.**
- **task134 and task135.** No prompt, pack or design note is on this checkout; each folder holds only the seed it was redrawn from. Track B was read from their cards. Track A is limited to the cards' world, people and deliverables.
- **task130.** The folder is the spent v2 (Tenter House) while the card is v3, so the screen's Track A for task130 ran against v2.
- **task230.** Its pack is on no readable commit (`target/` is gitignored), so Track A was done by card, prompt and deliverables at cc57ac7.
- **Main still holds task228's architecture-1 card**, and so does task230's branch at cc57ac7. That card describes product-analytics, `metric-definition-measurement-science`, G13 and `population_selection`. On scratch copies:
  - against that stale card, task230's guard BLOCKs on `ban.pairing`, `ban.subdomain`, `ban.role` and `ban.artifact`;
  - against the live card, it only WARNs `repeat.gate_g`.

  Every draw made on main is guarded against the spent architecture and cannot see the loop-1 driver. The forward warnings below depend on this.
- **task229.** Its committed card is the spent architecture 1. Design 2 is unregistered; its decided points come from the rework branch's note at 702f3d5.

## In batch against earlier builds

In pre-flight the batch is task228 alone. There is no collision, on either track, with any build the ledger records as approved or delivered.
- **task107.** Its v2 row records it retired on 2026-10-04, with the portal result "not stumped".
- **No ledger row, so status unknown on the record:** task130, task131, task132, task133, task134, task135, task229, task230, task117, task118, task121, task123 and task124.
  - START_HERE lists task132, task133 and task229 as shipped, task134, task135 and task228 as in build, and task230 as open.
  - task229's rework note records architecture 1 as having failed the portal's determinism QC.
- **task73 and task92.** The world-ten and v4 rows record each build and no portal result.

## Track A findings, reviewer visible

None.
- **Surface-nearest pairs.** All six score only on folder layout and overlapping format sets. Every other axis is zero: file names, identical files, schemas, same-seed tables, ask skeleton, invented names and deliverable species. Masked prompt and write-up overlap is about 0.005 at most. This is proximity, not a finding.
- **task123** asks for the same deliverable triple (docx, csv, png) and shares nothing else. A lone shared species is not a Shape echo.
- **task134, task135 and task230, by card.** No shared invented name, persona, geography or deliverable base name. task132 is the other Canadian build (Ontario, CAD) and its card keys the same constraint-first opening, four draws back.
- **`voice-check.py task228`.**
  - Opening move: constraint-first, shared with task124 (2 of 12).
  - No carrier phrase and no unlisted repeated run.
  - 164 words, the shortest in the batch (median 248).
  - Three files, as task127 has.

## Track B findings, mechanism

### task228 against task134: the waived axis ban, re-read under the loop-1 driver

**What the axis ban is.** A Part 6.1 standing ban on the decisive pattern, enforced by the guard as a BLOCK. It is not a Template: the drivers differ.

**It is the same ban.** The same rule, the same code (G16) and the same counterpart, with no new rule firing. The waiver's precondition holds.

**Status.** Neither side has a ledger row, so status on the record is unknown. Both are in flight.

**The decisive moves, with the domain nouns stripped.**
- **task134.** A probability of an event within a horizon, when competing exits end the risk for good and follow-up is incomplete, is the cumulative incidence. The share seen so far understates it. The survival estimate that censors the competing exits overstates it, most where those exits concentrate.
- **task228.** A unit's own error is separated from two comparators by their covariances. Where both comparators draw on one shared input their errors co-vary, so the three-way separation charges the shared error to the unit. Only a fourth series independent of both separates it.

**Are they the same claim? No.**
- task134's claim is about who stays in the risk set: a competing exit is not a censored observation.
- task228's claim is about whether two comparators are independent: a shared input correlates their errors.
- A solver primed on either gains nothing toward the other's step.

**What they share beyond the pattern label.**
- A stated estimand that pins what is measured and never how.
- A bias that concentrates in one segment (the border district; the clay plains), so the allocation or the ranking moves.
- The field's standard estimator losing to a specialist extension at the top rung. This one is the G16 label itself; the first two are components.

**Loop 1 moved task228 closer to task134 in form, though not in claim.** At pass 4, task228's decisive rung set the standard validation metric against the defined estimand. Now both builds turn on an independence-type assumption of the standard estimator failing in one segment.

**Position.** Estimator choice is the decisive rung in both:
- task134: cumulative incidence over Kaplan-Meier, at the top of the ladder;
- task228: rung 4, a second station in the cell, over rung 3, plain collocation.

That is spent twice at the label level, which is why the axis ban exists. It is not spent twice at the driver level.

**The waiver's recorded grounds, against loop 1.** The waiver rests on three grounds: the drivers differ, the domains differ, and task134 was registered after this draw.
- **The drivers differ:** holds, as above.
- **The domains differ:** holds (criminology-justice against physical-environmental-sciences).
- **task134 was registered after this draw:** true of the architecture-2 draw, not of the loop-1 rung.
  - The architecture-2 draw was registered at 08:02 UTC; task134's card reached main at 08:10 UTC.
  - The loop-1 rung was keyed at 15:48 UTC, with task134's card on file and pass 4's report naming the ban.
  - A hardening that deepens the same estimator-choice step keeps G16 as a matter of course, so this is a consequence of the hardening, not a fresh choice. The waiver now rests on the first two grounds.

**Does the data survive?** No repair is asked while the waiver stands. If it were withdrawn, the axis is the decisive pattern and the data does not survive. These are all built around the collocation ladder:
- the per-season orthogonalised station errors;
- the clay cells' shared texture term;
- the sister-station geometry and gauges;
- the 387 assertions in `checks.py`.

### The card's keys against the decisive rung (asked in the brief)

**The decisive rung.** The design note's ladder (rung 4 over rung 3) and the submission's steps 3 and 4 agree on it:
- read in both products' own notes that they take soil texture from the same 1:1 million soil map, so over the clay plains their errors are not independent;
- collocate each station with the morning retrieval and a second station in its cell;
- use the model only where a station is alone, which is never on the clay.

**Each key against that rung.**
- **`pattern: none` is honest.** No A to E pattern carries the rung: no past exceedance against forward yield, no rule recovered from a corpus, no serviceable share, no two grains, no conditioned yield.
- **`generators` with G16 first is honest, and fits better than it did at pass 4.** Stumping 6.2 asks for defensible methods that disagree, with exactly one surviving a property the pack makes checkable. Here:
  - two defensible collocations disagree on the eight by three swaps: station, retrieval and model; station, retrieval and sister;
  - exactly one survives a property the pack makes checkable. The shared soil map is filed in both providers' notes. The sister's independence shows in the register's coordinates (at least 14.1 km apart) and in its own rain gauge.

  On the supporting codes:
  - G17 cannot carry the rung. It is supporting only, and keyed decisive it would BLOCK against task135 (scratch copy).
  - G13 for the current-probe lower rung is still a loose fit (G4, attribution at transition, reads closer). It carries no ban.
- **`gate_g: method_or_model_selection` is honest.** The rung is which collocation the error structure admits, with the estimand pinned by NS-03 s.2.1. `decomposition_attribution` also reads, and would only drop the WARN.
- **`stump_strategy: decomposition_attribution` is honest, and closer than at pass 4.** The decisive step is how the disagreement variance splits across three error sources when two of them overlap, which is the vocabulary's "where overlap decides the split". `causal_design` (comparison choice) is the only other family a reader might reach for. Measurement-error identification is not causal design, and neither key changes a guard verdict.
- **`gap: objective` is defensible, and it is the weakest-fitting key.**
  - **Why objective fits.** Every figure through rung 3 is a correct computation of something other than NS-03 s.2.1's estimand: first a disagreement with a reference, then a three-way figure that carries the products' shared error. That is gap 3, and the design note argues it in writing.
  - **Why population does not.** The build has no population, grain or sample-design gap: the 56 stations and their mornings are the whole filed population. Population would be a forced key.
  - **What population would cost.** On a scratch copy it raises `test.same_driver` BLOCKs against task134 (inside the batch) and against task104 and task70 v2.
  - **Time and rule** do not fit.
- **`decisive_rule_filed: true`, `official_decoy: false` and `validated_decoy: false` are honest.**
  - NS-03 states the estimand and never a method.
  - No filed text names an estimator, says the products' errors co-vary, or gives a second station a role. I checked NS-03 and the Ninox, PLSM, campaign, anchor and export notes.
  - No certified figure in the pack is reproduced by the wrong method.

**Stale text on the card (record only, not a redraw).**
- **The task107 and task134 differentiation lines** still describe the round-3 decisive step: "two independent products' errors" and "triple collocation of three independent observing systems". The loop-1 driver now calls that step the wrong rung. The task134 line is the one the waiver leans on.
- **The G16 sentence in `notes`** says "only triple collocation estimates the quantity the standard defines".
- **The waiver's parenthesis** names "triple-collocation station error" as task228's driver.
- **`pipeline.json`** still carries the round-3 `stump`, and its `duplicate_check.clone_check` still reads "no fresh pre-flight owed (driver unchanged)".

### Forward warnings (unbuilt seeds, never findings)

1. **task225, seed AD48 (Anomaly Detection, developer 2, open). It carries the loop-1 driver.**
   - **The seed's driving force.** Two-of-three voting assumes faults are independent. Sensors issued from one shipment drift together, so an agreeing drifted pair outvotes the good sensor, or the vote goes blind.
   - **Stripped of its domain nouns, that is task228's insight.** A redundancy method that isolates one measurement's error assumes the others' errors are independent. Two of the three share a source and err together, and the odd one out is charged with their shared error.
   - **The remedies differ.**
     - AD48: a shipment assignment from an oldest-first issue run, read against a book of reference checks.
     - task228: a fourth independent series.

     The step a solver has to reach is the same.
   - **The consequence.** Built as seeded and drawn after task228, task225 would carry a Template finding against task228.
   - **Why the guard will not catch it.**
     - Driver text similarity to the seed's driving force is 0.01.
     - The seed's keys (population over rule, pattern B) share no structural signature with task228's.
     - Main holds task228's architecture-1 card, so a draw on main cannot see the loop-1 driver at all.
   - **The axis, for task225 if built:** its decisive rung.
2. **task251, seed DQ24 ("both instruments noisy").**
   - **What it repeats.** Its pitfall is that the comparator carries its own error, so OLS against it attenuates, and an errors-in-variables fit with the error ratio from repeatability tests replaces it. That is the move task228's rungs 0 to 3 already spend, and it is the round-3 lineage driver an in-house solver landed.
   - **What the guard sees.** Text similarity is 0.08 to that lineage driver and 0.07 to the loop-1 driver, both under the guard's 0.12 WARN.
   - **Why it is a warning.** Decisive in task251 and low in task228 is demotion, which Part 1 allows. Against task228's lineage it repeats a driver already landed. Its replicate-ratio device also sits beside task228's rung 4.
3. **task249 to task252 (DQ22 to DQ25) all carry task228's pairing and task type:** physical-environmental-sciences / `sensor-calibration-measurement` x Data Quality Monitoring.
   - Any of them drawn within three builds of task228 BLOCKs on `ban.pairing` and `ban.subdomain`. On main that ban currently runs against the architecture-1 card, so it would not fire.
   - DQ23 (task250, a network false-alarm budget) sits near the architecture-1 lineage driver, not the new one.
   - DQ22 and DQ25 share nothing with the new driver.
4. **Near in family, not the same claim:**
   - DQ05 (task232): covariate measurement error, with replicate lag measurements;
   - DQ16 (task243): dual-system estimation, with correlation bias between two lists.

## Clean, shares components by design

Each verdict here is `clean_shares_components`, with the driver difference named.

- **task135** (immediately before; no ledger row; card only).
  - Shares:
    - the client domain, so there are two Physical & Environmental Sciences builds back to back. Part 6.1 bans the pairing, not the domain, and the objectives differ;
    - gap objective first;
    - the `field_method` Layer 2 family;
    - no calibration organ;
    - a field-standard estimator that is biased for the filed quantity, segment by segment.
  - Its driver: the back-transformed log rating curve is the conditional median, and the mean needs a retransformation correction that differs by creek.
  - Position: decisive in both, but different estimators and different assumptions.
  - A reviewer will see two water-measurement builds in a row (creek sediment in Colorado, then soil moisture with rain gauges in Saskatchewan). That is domain proximity. It is not a Shape echo: shape 14 against 01, a quantity against a ranked slate, xlsx+pdf against docx+csv+png.
  - task135 keys G17 as decisive, which 6.2 makes supporting only. That is task135's matter.
- **task133** (no ledger row).
  - Shares: the `field_method` family, a filed estimand, no calibration organ, and G16 as a supporting code.
  - Its driver: the forward probabilities of a unit part-way along a curve filed from entry are the remaining increments divided by its survival to date.
- **task132** (no ledger row).
  - Shares: Canada and CAD, the constraint-first opening key, and the `field_method` family.
  - Its driver: a failure forecast that renews each failed item at the bottom of its wear-out curve.
- **task130 v3** (no ledger row).
  - Shares: gap objective first, and a noisy-measurement theme.
  - Its driver: regression to the mean in a cohort selected on an extreme, noisy outcome, with the baseline taken from an untreated cohort selected the same way a year earlier (pattern A). task228 selects nothing on a noisy outcome.
- **task229, architecture 1** (spent per the author's record; no ledger row). This is the closest driver on file and the one real overlap in family.
  - Shared: in both, a shared upstream source makes errors move together that the textbook method treats as independent, and that step is decisive in both. The source is a comms node in task229 and a soil map in task228.
  - The claims differ:
    - task229 builds a mean's standard error over the parents through which members fail together. The decisive step is the unit of the variance (pattern D, `grain_or_unit`).
    - task228 identifies one unit's own error when two comparators are correlated, using an independent fourth series.
  - A solver primed to cluster errors does not reach the collocation step. The architecture is spent, so this is history either way.
- **task229, design 2** (paused, unregistered).
  - Its driver: accuracy over every in-scope location under selection into observation, by inverse-probability weighting per stratum.
  - Shares the objective only. No axis it has decided collides with task228's card.
- **task230** (after task229; no ledger row; read at cc57ac7).
  - Shares:
    - the objective;
    - the Gate G mechanism, so task230's guard will WARN `repeat.gate_g` against task228 once the architecture-2 card is visible;
    - the family "the default comparison set breaks the method's assumption".
  - Its driver: a staggered switch reaches heavy users first, so the not-yet-switched pool is a lighter, more seasonal mix, and the counterfactual trend comes from same-band users (G6 decisive, `causal_design`).
  - Different estimand: a counterfactual trend, against an error variance.
  - Different assumption: conditional parallel trends, against independent errors.
- **task107 v2** (retired 2026-10-04, not stumped).
  - The guard's same-driver note no longer fires, because the decisive code moved from G3 to G16.
  - Shares: covariance-ratio, IV-style algebra, which is a component.
  - Its driver: the comparison arm received the intervention through reassigned practitioners, so the effect is scaled by a two-sided receipt contrast. This is history.
- **Surface nearest:**
  - task131: interference between sub-units that share a budget;
  - task118: shares gap objective, with G16 as a supporting code; its driver is a specialist team's gain over volume the unit does not already treat;
  - task121: losses filed as newcomers belong to established accounts;
  - task124: newcomers priced from analogs held down by an intervention they cannot join;
  - task117: follow-on operations re-timed behind the operation ahead;
  - task123: a trailing total at a cut-off, scoped to contracts in force that day.

  None shares a driver.
- **task73 (world ten), task92 (v4) and the task51 v4 lineage.** They share the prompt shape (a capped ranked slate) and the gap label. Their drivers are binding-constraint slates. Unchanged from pass 4.
- **This slot's own lineage** (the round-3 cut at 0.26, and architecture 1) is not a finding. A build cannot clone its own ancestor.

## Strategy monoculture

The batch is the twelve builds in draw order ending at task228: task125, task126, task127, task128, task129, task131, task130, task132, task133, task134, task135 and task228.

- **One strategy in a third of the batch: none.**
  - The largest share is `binding_constraint`, 2 of 12 (task127, task128).
  - Every other strategy carries one build, `decomposition_attribution` (task228) included.
- **Withheld rule with an official decoy: 0 of 12** (the cap is 2). `official_decoy` is 0 of 12.
- **Certified-record decoy (`validated_decoy`): 4 of 12, over the cap of three.**
  - The builds behind it are task125, task126, task127 and task129, all drawn 2026-10-10, before the decoy retirement.
  - task228 carries none, and neither does any build drawn since.
  - In the twelve ending at task230 the count is 2 (task127, task129).
- **Decisive rule left unfiled: 5 of 12** (task125, task127, task130, task134, task135).
- **The estimator-choice label.** Decisive G16 carries 2 of 12 (task134 and task228, two apart). That is the waived axis ban above, not a monoculture by the caps.
- **The Gate G mechanism.** `method_or_model_selection` carries 4 of 12 (task126, task131, task134, task228), one under the guard's overuse WARN. The twelve ending at task230 also hold 4.

## Corpus habits

- **Pack file names.** `data_dictionary` appears in 61 builds, `export_manifest` in 34, `data_notes` in 12 and `provenance` in 12. task228 uses none of them.
- **Filed standards are named as a code with a revision suffix.** 11 builds do it, four of them since task117:
  - `fes-07_load_forecasting_standard_rev4` (task117)
  - `mp-3_measuring_offers_rev3` (task131)
  - `NS-03_reference_stations_rev2` (task228)
  - `MDS-STD-114_firmware_read_health_r3` (task229)

  An extract or export-notes file is in 8 builds, task228 among them. The filed rule is required content; the naming is habit.
- **Deliverables.**
  - `pdf+csv` leads the corpus pairings with 9 builds.
  - The last twelve hold no Code deliverable.
  - The three-file triple docx, csv and png repeats (task123, task228).
- **Openings.** voice-check classes 8 of the last 12 opening moves as "other".
- **A bias concentrated in the one segment the ranking or allocation turns on:**
  - task134: the border district;
  - task135: the flashy plains creek;
  - task228: the clay plains;
  - task229 architecture 1: a build behind few nodes;
  - task230: occasional users.

  It is the device that lets a method choice move a ranked or allocated answer. A reviewer holding the batch will see it in five neighbours.
- **The decisive step is the field's standard estimator losing on an independence-type assumption** in task134, task228, task229 architecture 1 and task230. This is the spec's Layer 2 being followed, and the strategy fields differ, so it is not counted as a monoculture.
- **Objective and Layer 2 family.**
  - Three consecutive Data Quality Monitoring draws (task228, task229, task230) come from the lane allocation, and an objective may repeat on its own.
  - `field_method` is the Layer 2 family on 4 of the 7 cards in the window that carry the field.

## What to redraw

Nothing in task228. The one Track B item is the `ban.pattern` against task134, which the author has already waived. It is the same ban, and the card keys the loop-1 rung honestly.

Not redraws, for the record:
1. **task228's card and `pipeline.json`.** Bring the task107 and task134 differentiation lines, the G16 sentence in `notes`, the waiver's parenthesis, and `pipeline.json`'s `stump` and `duplicate_check` up to the loop-1 driver.
2. **task228's architecture-2 card is not on main.** Until it lands there, every draw made on main is guarded against architecture 1. That includes task225, task249 to task252, and task230's own branch.
3. **task225 (AD48), if built as seeded:** its decisive rung is task228's loop-1 driver.

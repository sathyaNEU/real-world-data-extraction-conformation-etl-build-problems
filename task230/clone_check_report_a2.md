# Clone check: pre-flight on task230 architecture 2 against every other build, 2026-10-12

## Verdict
Shape echo (soft), Track A furniture: task230 v2's deciding forum (`committee_or_panel`) and organisation family (`professional_services`) break the three-draw bans against task446 and task445 in draw order. Nobody saw it because task230 v2 was registered after both builds but sorts before them. Track B is CLEAN: no card, lineage entry or ledger row carries task230's driver.

## Scope and coverage
- **Mode:** pre-flight on task230 architecture 2 (Tamralipta Data Services, Human Factors & Ergonomics x Data Quality Monitoring). No window applies, so task230 was compared with every build on disk and with the card-only neighbours named in the brief.
- **Repo:** /home/user/orch/aud230b at b0b36ee (main merged, task230 v2 card registered). target/ and golden/ were copied in from the build.
- **Extract:** re-run fresh because the cache predated the v2 build. It produced 133 cards, 131 of them with a prompt or target. The cache at `.claude/skills/clone-check/.cache/fingerprints.json` was refreshed.
- **Screen** (`screen --focus task230`): 131 builds, 130 pairs in scope, 1 pair promoted (task33, on the mechanism route), 0 pairs promoted on surface. The highest surface pairs were task131 and task121 at 0.095 (95th percentile), with no Track B overlap.
- **Mechanism coverage:**
  - 109 builds have a card: 95 with native labels and 14 back-fitted.
  - 5 builds have a design note only.
  - 17 builds have no mechanism layer and were screened on Track A only.
- **Adjudicated pairs (10):**
  - The promoted pair: task33.
  - The brief's pairs: task114, task182, task228 (v2 card, number paused), task229 (design-2 card from `origin/perssathya/task229-rework`), task445 and task446.
  - Three pairs I added: task131 (shape 07, `causal_design`, same Gate G, just outside the twelve), task83 (on the heart's nearest-driver list) and task230 v1 (lineage, not a finding).
- **Left unread:** none of the brief's pairs and no promoted pair.
- **How adjudication was done:** in this thread, from the cards, task230/DESIGN_NOTE.md, task230/submission.md, prompt.txt, the target listing and task446/DESIGN_NOTE.md (stump, Gate G and ladder sections).
  - There were no per-pair subagents because this run had no agent-spawning tool.
  - No answer keys were read beyond each neighbour's card and design-note ladder.
  - No server-side tools were used.
- **task229 caveat:** the task229 card in this worktree is still v1. Every guard run that involves task229 was repeated on a scratch copy of cards/ with the design-2 card swapped in (`FINGERPRINT_CARDS=/home/user/orch/auditor-scratch-230-a2/cards`). The repo's cards/ was not changed.
- **Mechanical half:**
  - `guard.py heart task230` returns WARN on `repeat.gate_g` (task228 v2 and task229 v2) and `repeat.decision` (task229 v2). It returns a NOTE on `test.same_driver_older` against task33 and task114, both differentiated on the card. The nearest driver is 0.05.
  - `voice-check.py 230` passes every rule (819 characters, question first).
  - `guard.py people task230` reports no collision.

## In batch against earlier builds
- **Only one compared build has a ledger row: task33, `approved`.** Its pair with task230 is clean (see below), so nothing reaches exclusion level.
- **Every other side's status is unknown, because none has a ledger row.** Pipeline state:
  - task445 and task446: stage 8, shipped in-house and awaiting the portal;
  - task182: stage 9;
  - task228 v2: paused;
  - task229 design 2: registered on its branch. The brief says it is now spent and an architecture 3 is being drawn, but the card does not record that yet.

## Track A findings, reviewer visible
1. **task230 v2 against task446 and task445: furniture bans broken in draw order.** Tier: Shape echo (furniture). Track A.
   - **Status:** task446 and task445 are unknown (shipped in-house, no ledger row). task230 is in flight.
   - **What is shared:**
     - task446 shares the deciding forum `committee_or_panel` (task230's service quality council against task446's credit committee). Running `guard.py check` on task446's card gives BLOCK `ban.forum` against task230 (v2).
     - task445 shares the organisation family `professional_services` (a BPO capture centre against an ownership-research firm). Running `guard.py check` on task445's card gives BLOCK `ban.org_family` against task230 (v2).
     - Both results reproduce with and without task229 v2 swapped in. task445 also BLOCKs on `people.first` and `ban.forum` against task130 and task228. Those were there before task230 v2 and are not this build's.
   - **Why nobody saw it:**
     - `draw_key` orders cards by (drawn date, task number).
     - task230 v2 was registered at 21:21 on 2026-10-11, after task446 v2 (17:36) and task445. Because it is the lower number on the same date, it sorts before both.
     - So task230's own check only met task182, task228 and task229. task445 and task446 were filed before task230 v2 existed, so their checks never met it either.
     - The guard's comment at guard.py:449 to 451 assumes later builds "met it in their own check when they were filed", which a same-day re-root under a lower number breaks.
   - **Clears it:** the axis is task230's `forum`, plus `org_family` if the author holds task230 to the ban.
     - The forum is document-level furniture: the deciding body named in the pack, never in the prompt. Changing it is a rename and the data survives.
     - The organisation family is the world itself. A BPO capture centre is professional services by nature, so clearing that one means a new world. Its cost is far above its value, so this report leaves it as the author's call.
   - **Guard bug:** a re-root registered after higher-numbered builds on the same day is invisible to both sides. This belongs in the guard, not the card.
2. **No other Track A finding.**
   - There are no shared invented names, no shared file names beyond corpus idiom, and no shared schema or seed tell.
   - The pack names its files in the organisation's idiom (`QCP-04_first_pass_quality_control.docx`, `november_operating_plan.xlsx`), with no `data_dictionary`, `export_manifest` or `provenance` file.

## Track B findings, mechanism
**None at Template tier.** No adjudicated pair turns on the same thing.

**Soft Shape echo, re-adjudicated from this side: task230 v2 against task229 design 2.** They are consecutive, both in flight, and task229 v2 is now reported spent.
- **What they share:**
  - objective (data-quality-monitoring), decision type (`designation_set`) and gap pair (time, population);
  - Gate G `method_or_model_selection`, Layer 2 family `field_method`, G13 and G17 among the generators;
  - calibration `none`, `decisive_rule_filed` true, and a question-first opening.
- **The object is one species, which the task229 report did not name:** which units clear a record-accuracy limit at a moment or under a condition the accuracy checks do not directly observe. task229's units are pick-face records counted by cycle counts; task230's are captured key fields re-keyed by a blind audit.
- **The drivers differ.** Stated with the domain nouns stripped:
  - task229: "each check resets the unit it reads, so the state at a later moment is built from each unit's accrual since its own last check";
  - task230: "the detector's hit rate is set by how rare targets are in the shared pool it works, so a forward change in the pool's mix moves every unit's residual".
  - These are different claims. One is a measurement that alters its object; the other is a performance-shaping condition set by other units. Position: neither build carries the other's device at any rung.
- **The surface differs:** domain, shape 10 against 07, html against xlsx+pptx, strategy `population_selection` against `causal_design`, world, forum, organisation family and context artifact.
- **Tier:** Shape echo, soft, not an exclusion. Once task229's architecture-3 card replaces design 2, this pair touches only a dead row and becomes history.
- **Should task230's decision type change? No.**
  - The echo is soft and the drivers differ.
  - A change would have to recast the committed call: the eleven-stream grid is where shape 07's criteria come from. task230's pack is already cut.
  - The guard WARN against task229 v2 lapses when that card is retired.
- **Forward warning only:** task229's architecture 3 sorts before task230 in draw order. Its own `guard.py check` will therefore never meet task230 v2 (the same blind spot as finding 1), so its draw should be checked against task230 v2 by hand. If architecture 3 again draws data-quality-monitoring + `designation_set` + `method_or_model_selection` on a record-accuracy object, the echo hardens into the outline a reviewer reads as one build twice.

**Card honesty: does the card describe the decisive rung that DESIGN_NOTE.md and submission.md describe?** Yes, with one label understated.
- **Layer 2 key: honest.** `field_method` / `own:pooled-queue-error-prevalence-sets-human-detection` is the decisive rung R4 of the design note and the move behind submission steps 3 to 5:
  - each queue's shift-day OCR error rate is built from every stream's audited errors;
  - the miss log-odds are fitted on the log of that rate (slope 0.63);
  - November's rates are rebuilt from the plan (day 1.9, night 5.2).
- **Strategy `causal_design`: honest.**
  - The vocabulary lists interference, and the decisive step is building a channel through which one stream's volume moves other streams' detection.
  - `forecast_method_backtest` would also be arguable: a regime the plan sets makes the natural fit wrong out of sample.
  - The card's stated reason against it ("nothing filed selects a method") is not the vocabulary's test. The better reason is that the natural fit fails because it omits a cross-unit channel, not because of time structure.
  - For the author's information, not as a recommendation: relabelling to `forecast_method_backtest` would add a `ban.strategy` BLOCK on task446 in draw order (checked on scratch).
- **Pattern A with G13, G14 and G17: true but understated.**
  - Pattern A (past exceedance against forward yield) honestly describes the frame. The streams over their limits in Q3 (N1 to N5) are not November's set, and R0 equals the Q3 exceedances.
  - But that device sits at R0 and is killed by the plan's routing. The decisive rung R4 conditions detection on a property of the shift-day pool, which is G14 conditioned yield (pattern E). The card lists G14 only as "supports".
  - `[A, E]`, or G14 written as the decisive generator, would describe R4 more exactly. On scratch, pattern E adds no BLOCK and removes the task33 same-driver NOTE.
  - This is a label fix, not a clone finding, and not a reason to relabel on its own.
- **`gate_g` method_or_model_selection by determinism form 1, `decisive_rule_filed` true, `official_decoy` false: honest.** QCP-04 4.1 to 4.3 file the estimand, the rule and the records, and name no method.
- **`validated_decoy` false: honest, with one artifact to watch.**
  - The closed quarter refutes fixed detection at the shift-day grain rather than blessing it.
  - The October second-pass list in `november_operating_plan.xlsx` reproduces R0's set for October. It is a prior-period decision, correctly labelled. Whether it reads as a shipped artifact ranking the candidates is a question for the leak reader and the judge, not this check.

## Clean, shares components by design
- **task33 (approved, ledger row 33): the promoted pair, clean.**
  - Shared: decisive gap time, pattern A and `method_or_model_selection`, which is the same-driver signature the screen promotes on. task33's labels are back-fitted.
  - task33's driver is a forward yield that stops at a filed intervention, recovered by back-testing closed actions against an acceptance bar. Pattern A carries its decisive rung.
  - task230's driver is detection moving with the target prevalence of the pool. Its pattern A device sits at R0 and is demoted.
  - Nothing is back-tested or filed, and there is no truncation. Different claims, so this is reuse rather than cloning.
- **task446 (status unknown, two after in draw order): the nearest neighbour in concept, clean.**
  - Shared: gap time and population, Gate G, and a theme of detection rates against a moving base rate.
  - task446's claim is that a screen's yield moves with the base rate while its capture and false-alarm rates hold, so it backs the base rate out through the fixed error rates.
  - task230's claim is the opposite: the detector's capture rate itself moves with prevalence.
  - A solver who carries task446's lesson into task230 (hold the detector's error rates fixed) lands on task230's default path R1. That is the clearest evidence the two drivers differ.
- **task114 (status unknown): clean.**
  - task114's demand appears only when two parties share a site, so per-site records sum short.
  - task230's records are all exact, and per-unit detection moves with the shared pool's error rate.
  - They also share `capacity_report`, `purchase_order_or_contract` and `professional_services`. task114 is far outside the three-draw window, so this is noted only.
- **task182 (status unknown, three before): clean.**
  - Shared: `designation_set`, a question-first "Which of our ..." opening, and a filed decisive rule.
  - task182's driver is a counterfactual level from each unit's own lagged response to a shared external driver. That is a different decisive move, gap and Gate G.
- **task228 v2 (paused): clean.**
  - Shared: objective, Gate G, `field_method`, G13 and G17, calibration none.
  - task228's driver is separating each sensor's own error when two references share an input. That is measurement-error decomposition, not human detection.
- **task445 (status unknown, next in draw order): clean on mechanism.**
  - Shared: `designation_set`, gap pair, Gate G and question-first, plus the `org_family` ban in Track A finding 1.
  - task445's driver is completing a censored filing period reporter by reporter (maturity censoring).
- **task131 (status unknown, outside the twelve): clean.**
  - Shared: shape 07, `causal_design` and Gate G.
  - task131's interference is spillover between sibling sub-units under randomisation, read at the parent level.
  - task230's is a prevalence-driven criterion shift in a shared human detector.
- **task83 (heart nearest, 0.05): clean.** It conditions a holdout's effect on each unit's own treatment history; task230 conditions on a pool property, not the unit's own history.
- **task230 v1 (its own lineage): not a finding.**

## Strategy monoculture
The window is the last twelve in draw order before and around task230 (task130 to task446), with task229 at design 2.

| Strategy | Builds | Share |
|---|---|---|
| maturity_censoring | task134, task181, task445 | 3/12 |
| population_selection | task132, task229 | 2/12 |
| decomposition_attribution | task182, task228 | 2/12 |
| forecast_method_backtest | task130, task446 | 2/12 |
| causal_design | task230 | 1/12 |
| stated_rule_hard_construction | task133 | 1/12 |
| other | task135 | 1/12 |

- No build in the twelve has an official decoy or a validated decoy, so both decoy caps sit at 0.
- No strategy reaches a third (4 of 12). **No cap is breached.**
- Counting task131 (`causal_design`, one build earlier) would make causal_design 2 of 14, still clear.

## Corpus habits
- **Gate G `method_or_model_selection`:** 6 of the last 12 (task134, task228, task229, task230, task445, task446), five in a row in draw order from task228. A reviewer holding the batch sees it.
- **Objective:** data-quality-monitoring on three consecutive draws (task228, task229, task230).
- **Decision type `designation_set`:** 4 of 12 (task182, task229, task230, task445).
- **Layer 2 family `field_method`:** 7 of 12.
- **Question form:** the "Which of our / the N ..." opening appears in task131, task182, task230 and task445.
- **File roles:** `data_dictionary` appears in 61 builds and `export_manifest` in 34. task230 carries neither.
- **Deliverable pairings:** pdf+csv (9) and py (8) lead corpus-wide. xlsx+pptx appears in task133 and task230 among the last twelve.

## What to redraw
1. **task230, the deciding forum:** it breaks `ban.forum` against task446 in draw order. A rename in the pack's documents clears it and the data survives.
2. **task230, the organisation family:** it breaks `ban.org_family` against task445 in draw order. Clearing it means a new world, so it is the author's call whether to hold task230 to it.
3. **guard.py, `draw_key`:** a same-day re-root registered under a lower number never meets the higher-numbered builds already filed. This is a mechanism fix, not a redraw.
4. **task230 card, `pattern`:** optional label fix. Record G14 (conditioned yield) as the decisive rung's mechanism. This is bookkeeping, not a redraw.

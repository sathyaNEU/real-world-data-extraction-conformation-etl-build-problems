# Clone check: pre-flight on task229 (architecture 2, design 2), 2026-10-11

## Verdict
Worst tier is a soft **Shape echo** between task229 v2 and task230 v2, which are consecutive and both in flight. It is not an exclusion. No Exact, Same seed, Dataset or Template finding on either track, so task229 v2 can go to the solver round.

## Scope and coverage
- **Mode:** pre-flight on task229 architecture 2. No window applies: task229 was compared with every build on disk, plus the card-only neighbours named in the brief.
- **Repo:** /home/user/orch/aud229 at bd577bc (main merged at e89a676, plus the registered task229 v2 card). target/ and golden/ were copied in from the build.
- **Extract:** re-run fresh for this check. It produced 132 cards, 130 with a prompt or target. The cache at `.claude/skills/clone-check/.cache/fingerprints.json` was refreshed. The screen saw 130 builds, put 129 pairs in scope against task229 and promoted none. The nearest pair was task127 at a surface score of 0.100 (98th percentile). It had no Track A axis evidence (file names, schema, prompt, asks, entities and write-up all at 0) and only the decisive gap `time` on Track B.
- **Mechanism coverage across the corpus:** 108 builds have a card, 5 have a note only, and 17 have no mechanism layer. Those 17 were screened on Track A only, as the screen does for them.
- **Neighbours adjudicated by hand:** 10 pairs, all named in the brief. None was promoted. They are task181, task182, task228 (paused arch 2), task230 (arch 2), task107 (v1 lineage), task132, task134, task122, task445 and task446.
  - task228, task230 and task134 have no pack on this tree, so they were compared on Track B only, from their cards.
  - task107 has no folder here, so it was compared from its card and lineage only.
  - task230's card was read from `origin/perssathya/task230-event-volume-drop` (4db6b46), as the brief asked. **The task230 card in this worktree is still architecture 1**, because b744dab is not an ancestor of bd577bc. The guard was therefore re-run against a scratch copy of cards/ with the v2 card swapped in (`FINGERPRINT_CARDS`). Nothing in the repo's cards/ was changed.
- **Left unread:** none of the brief's pairs. No other pair was promoted.
- **How adjudication was done:** in this thread, from the cards, task229/DESIGN_NOTE.md, the task229 submission and filed documents, and task132/DESIGN_NOTE.md. There were no per-pair subagents because no agent-spawning tool was available to this run. No answer keys were read beyond each neighbour's card and design-note ladder. No server-side tools were used.

## In batch against earlier builds
- **No ledger row exists** for any build compared here (task107, task122, task132, task134, task181, task182, task228, task230, task445, task446), so the approved or delivered status of every other side is **unknown**.
- Pipeline state:
  - shipped in-house, awaiting the author's portal report: task132, task445, task446 (stage 8) and task181, task182 (stage 9);
  - retired: task122;
  - card only: task228 (paused arch 2) and task230 (arch 2 in flight).
- The guard's nearest driver is task107 v1 at 0.12. That is a **retired lineage row**: its card lineage records "solved on the portal". So it is history and not a finding (see below).
- Nothing here reaches exclusion level.

## Track A findings, reviewer visible
None.
- task229's surface does not echo the corpus:
  - one deliverable, `freeze_gate_2026.html`, which is the only HTML deliverable in the last twelve;
  - pack files named in the organisation's own idiom (`extract_notes_LF_20261207.txt`, `Corderoy_CP-THN-04_perpetual_count_programme.docx`, `Thornacre_SCS-07_peak_stock_record_standard_v3.pdf`), with no `data_dictionary`, `export_manifest` or `provenance` file;
  - no shared invented names;
  - the four personas are spread across the pack, with Rhys Flynn and Stacey Sykes in the SCS-07 PDF. `guard.py people` reports no collision.
- `voice-check.py 229` passes every gate rule at 733 characters, question-first.
- The one surface note: 3 sentences averaging 41.7 words, against a batch norm of about 22. That is an economy note for the prompt owner, not a clone signal.
- The only geography shared with a recent build is United Kingdom / GBP with task446 (Halstow Bank). There is no shared name, file or schema.

## Track B findings, mechanism
None at Template tier. Each pair is set out below.

- **task229 v2 against task230 v2 (consecutive, after; both in flight). Shape echo, soft.**
  - They share the objective (data-quality-monitoring), the decision type (designation_set), the gap pair (time, population), the Gate G mechanism (method_or_model_selection) and the Layer 2 family (field_method). Both have calibration `none`, a filed decisive rule and a question-first opening.
  - The drivers differ.
    - task229: a point-in-time share of correct units cannot be read off check outcomes. Each check restores the unit it reads, and checks fall at the end of each unit's interval, so the share is built from each unit's accrual since its last check.
    - task230: a detector's hit rate falls as targets become rarer in the shared pool it works, so carrying any unit's measured hit rate forward misplaces units when the pool's composition changes.
  - The surface also differs: domain, shape 10 against 07, HTML against xlsx+pptx, and the strategy (population_selection against causal_design).
  - The echo is the outline: a third consecutive DQM build that decides a designated set by choosing a method. task230's own guard already WARNs `repeat.decision` against task229.
  - Repair: the axis is task230's decision type, since task230 is drawn after task229. Nothing in task229's data is touched.
- **task229 v2 against task132 v1 (task132 shipped in-house, status unknown). Clean, shares components** (see that section). Recorded here because it is the only build that shares the reset-on-event component at the decisive rung.
- **Card honesty.** The design note's decisive rung matches what task229.json records, and the submission bears it out:
  - Rung 3 resets at every count, fits the accrual from routine (CYC) counts only, with exposure taken from the face's last count of any kind, and builds each face's state at 06:00 on 7 December.
  - Submission steps 3 and 4 fit p by centre and class on P(MATCH) = (1 - p)^days and average (1 - p)^d over the faces.
  - So the card's fields hold: G13 as the decisive horizon mismatch (observations at count moments, the decision at one later moment), G16 for estimator selection under SCS-07 4.5, gap time first, pattern none, layer2 `field_method / own:count-corrects-the-record-it-measures`.
  - `decisive_rule_filed: true` is honest. SCS-07 4.3 to 4.5 file the estimand: what a full count at the measurement time would find, estimated as a full count would bear it out. They name no estimator, age, decay or reset.
  - `official_decoy: false` is honest. No filed document defines or reports a count-based accuracy figure. I checked the text of SCS-07 section 4 and the CP-THN-04 programme.
  - `validated_decoy: false` is honest. No closed record or back-test ships.
  - `stump_strategy: population_selection` is defensible but leans on its "exposure" clause. Rungs 0 to 2 are selection corrections. The decisive rung is a point-in-time construction, which `time_semantics` would also describe. Neither label changes a guard result or a monoculture count (see below), so it is not a finding.
  - Two card fields are stale bookkeeping: `answer_source` still says "planned set ... replaced by the golden at ship", although the cut golden confirms the same six centres, and `spine.rows` is 0 against 107,072 cut rows.

## Clean, shares components by design
- **task132 v1 (spares last-time buy; renewal of replaced modules).**
  - **Shared component:** an event restores a unit, so each unit is modelled from its age since the last such event. It sits at the decisive rung in both builds.
  - **The drivers differ.**
    - task132: a forward count of failures has to restart the hazard clock at each replacement; carrying the current item past its probable failure overcounts. The estimand is a future event total (the renewal function).
    - task229: check outcomes describe units at the end of their interval, because checks fall when due or on a symptom, while the decision needs the cross-section at one arbitrary moment. The estimand is a point-in-time share (the backward recurrence of each face since its last count).
  - **The naive routes differ.** task132's solver models per-unit age and omits renewal. task229's solver models no ages at all and reweights observation-time rates.
  - **Watch:** this reset-on-event family has now carried two decisive rungs in the last twelve draws. A third build whose decisive move is "the event restores the unit" would be a recognisable template.
- **task107 v1 (lineage, retired; the guard's 0.12).** The overlap is vocabulary only ("share", "check"). task107 v1 split check coverage by each source's delivery kind, a conditioned yield. task229 estimates a population's state at a moment from checks that reset what they observe. Since this lands on a retired row, it is history and not a redraw.
- **task228 v2 (paused arch 2, the guard's `repeat.gate_g`).**
  - Shared: the same objective, Gate G mechanism, generator set {G13, G16, G17}, field_method and calibration none.
  - Different drivers: task228 separates each unit's own error by collocation where two references share an input. task229 has no reference instrument, and its observation resets the outcome.
  - The decision, shape, deliverables and forum also differ.
- **task181 v2.**
  - Shared: gap time/population, G13 and field_method.
  - Different drivers: task181 nowcasts counts read before their records have arrived, a maturity/delay problem. task229's records are complete, and the observation corrects them.
- **task182 v1.** Shares only designation_set. task182 decides by a counterfactual driver-response decomposition.
- **task134 v1.** Shares G13 and G16 and a discrete hazard with exposure as the estimation device. task134 decides by treating competing exits as ending the risk, not as censoring. No reset or point-in-time element.
- **task122 v2 (retired).** Shares G13. task122 decides by attributing outcomes recorded after a session closes back to the exposures that produced them, a window-truncation problem. There is no reset in it.
- **task445 v1.**
  - Shared component: each unit completed from its own last observation.
  - Different drivers: task445 carries missing reporters forward at their last report, a late-arrival completion where the state persists. task229 decays each face from its last count, where the state accrues error and the observation resets it.
- **task446 v2.** Shares the UK and GBP setting and method_or_model_selection. task446 turns on a screen's yield moving with the base rate while its error rates hold. No shared driver.

## Strategy monoculture
The window is the last twelve in draw order, task130 to task446, with task230 at v2.

| Strategy | Builds | Share |
|---|---|---|
| maturity_censoring | task134, task181, task445 | 3/12 |
| population_selection | task132, task229 | 2/12 |
| decomposition_attribution | task182, task228 | 2/12 |
| forecast_method_backtest | task130, task446 | 2/12 |
| stated_rule_hard_construction | task133 | 1/12 |
| causal_design | task230 | 1/12 |
| other | task135 | 1/12 |

- No official decoy and no validated decoy anywhere in the twelve. Both decoy caps sit at 0.
- No strategy reaches a third (4/12). **No cap is breached.**
- Recoding task229 as `time_semantics` would change nothing here.

## Corpus habits
- **Gate G mechanism:** method_or_model_selection carries 6 of the last 12 (task134, task228, task229, task230, task445, task446), including four in a row from task228. This is not a strategy cap, but a reviewer holding the batch sees it.
- **Objective:** data-quality-monitoring on three consecutive draws (task228, task229, task230). Decision type designation_set on 4 of 12 (task182, task229, task230, task445).
- **Layer 2 family:** field_method on 7 of 12. Opening move question-first on 5 of 12.
- **File roles:** corpus-wide, `data_dictionary` appears in 61 builds, `export_manifest` in 34, and `data_notes` and `provenance` in 12 each. task229 carries none of them.
- **Deliverable pairings:** pdf+csv (9) and py (8) lead.
- **Aside (not a finding, outside this pair set):** task181/ carries `DESIGN_NOTE_arch1.md` and `clone_check_report_arch1.md`. CLAUDE.md bans a second design note under any name. It did not surface in any pair here.

## What to redraw
Nothing in task229.
1. task230 (the later draw), decision type: only if the author wants to clear the soft Shape echo with task229. The data survives, since this is task230's draw and not task229's pack.
2. task229 card bookkeeping (not a redraw): `answer_source` and `spine.rows` are still the pre-cut values.

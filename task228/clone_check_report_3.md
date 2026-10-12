# Clone check: pre-flight, task228 against the whole corpus (strategy axis redrawn after round 2, head 6a72d7b), 2026-10-11, pass 3

## Verdict
No reject-tier finding: there is no Exact, Same seed, Dataset or Template finding against any build, so the clone half of the stage-5 gate holds. The worst clone tier touching task228 is Idiom, a soft Track A flag that no pair carries (one stakeholder belief about the naive pick, a construction 7 of the last 12 prompts use).
- **Does the card honestly key the redrawn decisive rung?** The strategy key does, the pattern key does not.
  - **`stump_strategy: population_selection` is honest.**
    - vocab.json defines it as "who is in the denominator: survivorship, selection, attrition, exposure, scope". Rung 3 chooses the page budget's denominator, 106 of the 166 sound four-week runs, and weights nothing.
    - `composition_mix` reaches the rung only as a reweighting with a zero weight.
    - One sentence in the design note argues the opposite and should be reconciled (see Track B).
  - **`pattern: A` does not key rung 3.**
    - Rung 3 is a pooled page rate split by a per-run column (`config_rev`) and read on the one side the season occupies. That is stumping Part 2's Pattern E, conditioned yield, which is a Gap 2 pattern.
    - The card's own decisive gap is population (Gap 2). Part 2 files A under Gap 1, and all nine other cards with decisive A lead with time.
    - The design note's own DRAW names the split G14, "conditioned yield", which Part 6.2 files as "gap 2, pattern E". It lists G14 second, as "in support", behind G13. G13 is the horizon move of rung 2, the stop rung.
- **Keyed honestly, the heart check blocks.** With pattern E and G14 first, `guard.py` BLOCKs `ban.pattern` against task129, three draws back. The heart half of the stage-5 gate then fails.
  - It is a Part 6.1 guard ban, not a clone tier.
  - It falls in the same window that blocked `composition_mix` in pass 2.
  - As filed, the heart is WARN.
- **The neighbours all come out clean.**
  - In draw order, task131 is promoted on two core axes and is `clean_shares_components`. Its restriction to a subset sits on the decisive rung again, but answers interference rather than a disturbance the forward window excludes.
  - task129 is clean on the driver.
  - task130 shares no mechanism axis.
  - task229 (card only) is clean.
  - The surface neighbours task48 and task104 are close only through the flat layout and the format mix.
- **At batch level, the certified-record decoy still carries 7 of the last 12 builds** against a cap of 3. That is a Strategy monoculture finding, and task228 is not one of the seven.

## Scope and coverage
- **Mode and scope.** Pre-flight on task228 against every build on file, with no window. The run was at head 6a72d7b on `perssathya/task228-guardrail-alert-metric`. This is pass 3; `clone_check_report_task228.md` and `clone_check_report_task228_2.md` are not overwritten.
- **Why it re-ran.** Round 2, on the loop-1 cut, passed under the gate of 11 October. The parent then redrew the strategy axis inside architecture 1 (stage-5 rule: the adjudicated pre-flight re-runs when the driver changes):
  - **Retired rung.** The loop-1 decisive rung (each surface's page rate reweighted to the season's surface mix) is retired, and the app release-train physics left with it.
  - **New decisive rung.** Rung 3 now holds the budget on last year's sound four-week runs that ran unrevised (`config_rev`), because no revision ships in the change freeze.
  - **Surface reweighting is inert.** `checks.py` asserts that reweighting the surfaces by standing bookings, by every booking or equally returns the same five settings and catches. The loop-1 driver is gone from the cut.
- **Extract.**
  - The committed cache at HEAD held 125 cards (task1 to task131) and no task228. Pass 2's refresh was not kept.
  - I re-ran `fingerprint.py extract` in place at 06:41 UTC.
  - Result: 126 cards, 124 with a prompt or target. Of these, task228 was added and task130 was re-profiled from disk (13 files in the cache, 14 on disk), with nothing else changed.
  - Every input predates the extract: prompt 06:11, submission 06:17, design note 06:27, task228 card 06:28:53, task229 card 06:28:12, pack cut 06:16. They were unchanged at 06:54 and at writing.
  - The on-disk pack matches the parent's recorded rebuild hashes (`task228/.work/h_target_after.txt`).
- **Screen.** `fingerprint.py screen --focus task228` covered 124 builds and 123 pairs, and promoted 0.
  - The nearest are task131 at 0.095 (95th percentile), task48 and task104 at 0.094 (94th), task109 at 0.091 and task90 at 0.090.
  - All of that proximity comes from the flat layout and the format mix.
- **Draw order.** The guard orders by drawn date, then number. The neighbours are task129 (three draws back), task130 (two back), task131 (previous) and task229 (next, the same day).
  - Re-applying the screen's own promotion rules in that order promotes one pair: task131, on two of three core axes between back-to-back draws.
  - task130 shares no core axis, task129 shares one (the gap) and task229 shares one.
- **Builds compared: 127.**
  - 123 went through the screen. 101 were scored on both tracks with Track B read from the cards; none fell back to the ledger.
  - 22 were scored on Track A only: task3 to task10, task13 to task24, task112 and task113.
  - 4 card-only builds were scored on Track B with fingerprint.py's own `track_b`: task114, task115, task116 and task229.
  - 34 screened builds carry back-fitted labels (task36 or earlier), and 14 of them were scored on Track B.
  - Mechanism layer over the 124 screened builds: 102 have a card, 5 are note-only and 17 are unavailable.
  - Nothing comparable exists for task1 and task2, and task99 is a scratch slot that the script excludes.
- **File-level gaps.**
  - The extract profiles csv, tsv, txt and xlsx only. It never opens `target.zip`, and it covers parquet, json, docx and md by byte hash only. That includes task228's two parquet spine files.
  - 15 screened builds have no profiled target: task3, task10 and task117 to task129.
  - I profiled task117 and task119 from their zips in a scratch copy of the cache. Against task228 they score 0.085 and 0.080, with no identical file, same-seed table, column-set collision or shared name.
  - task118 and task120 to task129 have no pack on this checkout, so file-level Track A against them is unchecked.
  - task229's folder here holds only its seed, so it is compared on its card alone. /home/user/b229 was not read.
- **Supplementary runs.** All are scripts built on fingerprint.py's and guard.py's own functions, written to and read from /home/user/orch/auditor-scratch-3/ only.
  - The draw-order re-screen, and Track B for the card-only builds.
  - The zip coverage above.
  - `guard.py heart task228`, run with the people index pointed at a scratch copy so the tracked `people.json` is never rebuilt.
  - `guard.py check` what-ifs on in-memory copies of the card: pattern E; E with G14 first; A with G14 first; pattern `none` with G14 first; time first with A; `composition_mix`; `forecast_method_backtest`; E with G14 first and `composition_mix`. The card was not touched.
  - Screen what-ifs on scratch caches: E with G14, and time-first A.
  - A sweep for the new move over 799 texts: every card driver, concrete driver and stump, every lineage entry and every ledger row. It looked for a change made to a running unit, a forward freeze, a false-alarm or threshold calibration, and holding on unchanged units.
  - `voice-check.py`, run bare and on task228.
- **Pairs adjudicated.** All in this thread, with no subagents, because the invocation forbade the Agent tool.
  - No advisor or web tool was used and no golden file was opened.
  - The clone-check skill was loaded by reading its SKILL.md in full, because the Skill tool does not list it in this session.
  - The honest-keying question was judged on vocab.json, stumping Part 2 and Part 6.2, `references/proven-in-production.md` Part 3 and the fingerprint skill. The guard's verdicts are reported as consequences, not as the test.
  - **task131** (promoted in draw order): read its card, prompt, submission, target listing, and its design note's DRAW and ladder.
  - **task130** (two draws back): read its card, prompt, submission and target listing.
  - **task129** (three draws back): read its card, prompt, `pipeline.json`, and its design note's stump, decisive rung, both ladders and position table. It has no pack and no write-up.
  - **task229** (next draw): read from its card, which the parent copied from b229 into this commit.
  - **task48 and task104** (surface nearest): read from their cards; neither folder is on this checkout.
  - **What-ifs and an approved build:** task33 (approved), whose decisive pattern A the filed card now shares, and task53, which the honest key promotes on all three core axes. Both read from their cards.
- **Supplementary reads.** Card drivers were read for 32 more builds:
  - to name the difference: task35, task68, task72, task121, task11 and task12
  - as keying precedents (every card keyed `population_selection` or `composition_mix`, every card with decisive A or G13, and the conditioned-yield builds that proven-in-production S8 names): task8, task15, task20, task22, task25, task28, task43, task44, task46, task47, task56, task57, task62, task71, task76, task83, task86, task89, task95, task100, task101, task102, task107, task114, task116 and task122.
- **Unread.** 87 of the 127 builds were not read beyond the screen's numbers, because no route promoted them, no what-if surfaced them, no keying question needed them and the sweep found nothing in them.
- **Status.**
  - The ledger runs to task108. task228, task229, task131, task130 and task129 have no row, so all five are unknown on the record.
  - The ledger records eight approved builds: task25, task27, task28, task29, task30, task33, task34 and task35.
  - `pipeline.json` files claim more, but they are not the record:
    - task131: approved and delivered on 2026-10-10.
    - task130: delivered on 2026-10-11.
    - Neither pair below carries a finding, so the verdicts stand either way.

## In batch against earlier builds
Pre-flight has no batch, so this section carries the comparison the reviewer's cross-batch check runs: task228 against the builds the ledger records as approved.
- **No hit against an approved or delivered build.** None of the eight is promoted, none shows a hard tell, and none shares a driver.

| Approved build | Surface (percentile) | What it shares with task228, as filed |
|---|---|---|
| task25 | 0.020 (29th) | decision type; context-artifact type |
| task27 | 0.083 (72nd) | decision type |
| task28 | 0.080 (64th) | decision type |
| task29 | 0.078 (60th) | decision type; context-artifact type |
| task30 | 0.085 (78th), the nearest | decision type |
| task33 | 0.083 (72nd) | **decisive pattern A**; decision type; context-artifact type (two core axes) |
| task34 | 0.029 (35th) | decisive gap; calibration organ (`gold_standard_subsample`) |
| task35 | 0.073 (50th) | **decisive pattern A**; context-artifact type |

- **The A on the card creates two label collisions with approved builds.**
  - task33 and task35 share decisive pattern A with task228 on the cards. Under pass 2's card (pattern `none`, G6), they did not.
  - Both are label-only. task33's driver is a forward yield in which past elevations resolve, read by back-testing closed actions. task35's is an attachment period recovered from settled records. Neither turns on task228's move (task33 is under Clean).
  - Keyed E, task228 shares no decisive pattern with any approved build.
- **No exclusion-level exposure for task228.**

## Track A findings, reviewer visible
None at Shape echo or above.

### task131 against task228: decision shape only, unchanged since pass 2
- **Status.** No ledger row on either side. task131's `pipeline.json` records it as delivered on 2026-10-10. The two were drawn back to back (2026-10-10, then 2026-10-11).
- **The prompt is unchanged since pass 2.** There is no diff on `task228/prompt.md` between 6b19d41 and HEAD.
  - The only shared Shape echo axis is still the decision shape: one named option of N with a quantity attached.
  - The ask construction, the deliverable species (docx+png against json+xlsx+png) and the calibration organ (none against the audit) all differ.
- **The rewritten write-up shares nothing measurable with task131's.** Masked write-up overlap and step skeleton are both 0.000.
- **Mechanically**, the surface is 0.095 (95th percentile), from the format mix (0.875) and the flat layout. Masked prompt overlap and ask skeleton are 0.000, and no names are shared.

### Not findings, checked
- **Hard tells.** Across the 123 screened builds there are no byte-identical files, no same-seed tables, no identical column sets and no shared invented names. Pousalto and Vigia appear on no other card.
  - The highest masked prompt overlap is 0.004 (task51). The highest masked write-up overlap is 0.003 (task127).
  - The ask skeleton and the step skeleton score 0.000 against every build.
- **Personas.** None of task228's eight personas shares a first name or a surname with any other card. `guard.py heart` raises no people rule.
- **task104** is 28 draws back, has no ledger row, and is the corpus's other on-call threshold project.
  - Surface 0.094 (94th percentile), from the format mix only. Masked prompt overlap is 0.000.
  - The deliverables (html+svg) and the calibration organ (`other`) differ, so at most one Shape echo axis is shared.
- **task48** has surface 0.094 (94th percentile), from the format mix only. Its mechanism is under Clean.
- **task129** shares nothing reviewer-visible. It has no pack and no write-up, its prompt shares no construction (masked overlap 0.000), and its deliverables are pptx+xlsx.
  - **Pass 2's watch item is cleared.** That was the mobile release train behind both explanations. "Release train" and "batched beacons" have left task228's write-up and pack: a grep over the prompt, submission and pack text finds neither, nor "deploy" or "cache".
  - **A new echo, at design level only.** It is noted under Clean.
- **`voice-check.py`**, run bare and on task228 over task121 to task131 and task228:
  - The figures equal pass 2's, because no prompt in the window changed.
  - task228's stakes-first opening is the only one in the 12. It finds no listed carrier and no unlisted repeated run.
  - task228 runs 240 words, against a median of 253 and a flag line of 330.
  - It ships three files, at the ceiling with task123 and task127. Its JSON deliverable is the only one in the 12.

## Track B findings, mechanism
None at a clone tier. With no Template finding against any build, no rebuild is owed by the clone tiers and the data stands.
- **task228's move, with the domain nouns stripped.** A per-run false-alarm rate, set over the season a setting is live, is held only on the record's long runs that took no mid-run change. A change disturbs the per-night candidates for about a week and the cumulative one for the rest of the run, and the forward season admits none. Pooled over every long run, the threshold over-sets the candidates the changes disturb, and held on the unchanged runs, the candidate the changes hit hardest leads.
- **The mechanism screen, across the 127 builds compared, as filed.** task228 shares:
  - the decisive gap (population) with 42
  - the decisive pattern (A) with 9: task33, task35, task46, task47, task62, task89, task95, task107 and task114
  - the decisive G-code (G13) with 6: task35, task47, task89, task102, task107 and task122
  - the decision type with 20
  - the Gate G mechanism with 1 (task229)
  - the calibration organ with 5: task34, task43, task74, task93 and task111
  - the context-artifact type with 26
  - the same-driver signature with none
  - the domain and objective pairing with none.
- **Collisions and text similarity.**
  - The most core axes any pair collides on is two: task11, task12, task33, task53, task68, task72, task121 and task131.
  - The highest card-driver overlap is 0.068 (task106), against a promotion line of 0.40. task129 is at 0.058.
  - In the guard's heart text, the nearest builds sit at 0.05: task103's retired v2 row and task104's stump. In the guard's driver check, the nearest driver is this slot's own loop-1 lineage at 0.31, differentiated on the card (a NOTE).
- **The reskin route.** No text among the 799 carries two of the four families: a change made to a running unit, a forward freeze, a false-alarm or threshold calibration, and holding on unchanged units. Broadening each family leaves four incidental pairings:
  - task129: "deploy" with web "pages"
  - task42: "revision" with "budget line"
  - task48: "configuration" with "threshold"
  - task49: "deployable" with "alerts".

### Not a clone tier, but it decides the heart half of the gate: does the card key the decisive rung honestly?
**What rung 3 does.**
- Rung 2, the stop rung: the 166 sound four-week runs, pooled, give `expo_rate_gap_pp` 4.5 (12 caught) and `beacon_loss_z` 7.5 (6).
- Rung 3, the answer: split by `config_rev`, the beacon check pages 57 of the 60 revised runs at 3.0 and 4 of the 106 unrevised ones. On the 106 it holds 3.0 and leads with 22 caught against 15.
- The design note's "Written in no sentence" list:
  - **Filed:** the freeze (handbook s.6.1). The prompt also names "the 14 December change freeze".
  - **Unwritten:** "a revision disturbs a check, that last year's long runs carry revisions, or that the budget should be held on unrevised runs".
  - So the unwritten step is the conditioning: the page rate depends on a per-run property.

**`stump_strategy: population_selection` is honest.**
- **The definition reaches the rung directly.** vocab.json: "who is in the denominator: survivorship, selection, attrition, exposure, scope". Rung 3 decides which runs make up the budget's denominator (106 of 166) by the season's scope, and no weight is computed anywhere.
- **`composition_mix` also reaches it, but only as a zero-weight case.** vocab.json: "mix shift, Simpson's reversal, standardisation or reweighting changes the comparison". Here the record's revised share (60 of the 166 sound four-week runs, 36 per cent) moves to 0 per cent in the season. That is not a Simpson's reversal: the strata disagree and the pooled ranking follows one of them.
- **Corpus precedent covers both readings for a conditioned yield.**
  - task76 (E, `population_selection`) removes a zero-yield class from a forward count, and task56 (E, `population_selection`) restores a population a faithful pipeline drops.
  - task83, task43 and task44 (E or E second, `composition_mix`) transport a mixed effect to a different mix.
  - An exclusion with no weights sits with the first group. A reviewer reading "held on the 106 runs that ran unrevised" names a denominator.
- **One sentence in the design note argues the opposite and should be reconciled.**
  - "Set aside at the redraw" rejects a no-app peak because it "puts a zero weight on one surface, which is the same reweighting".
  - Holding on unrevised runs is that move on another column.
  - Either the sentence means the no-app peak kept the loop-1 stratum (surface), which is a driver point and should say so, or it holds that a zero weight is a reweighting. If it holds that, the strategy is `composition_mix` and BLOCKs against task129.
- **`forecast_method_backtest`**, the note's nearest other reading, fits the frame (a regime the record lacks) but not the construction. The note was right to set it aside.

**`pattern: A` does not honestly key rung 3. E does.**
1. **Part 2 defines A as a Gap 1 pattern.** Its markers do not describe rung 3:
   - "Some candidates are resolving and some are ongoing, and the ranking on what happened is close to the reverse of the ranking on what will happen"
   - the forward quantity built "from a property the pack supports (a fitted level shift, a decay, an ongoing versus resolved classification recoverable from the series)"
   - and its determinism note: "Pin the horizon operationally (the length of a deployment ...)".

   That last line describes rung 2, the 28-night horizon.
2. **Part 2 defines E as a Gap 2 pattern, and rung 3 matches it almost word for word:**
   - "The split is visible on a one-line group-by"
   - "The model applies the pooled success rate uniformly. The pooled rate is correct. It is just not the rate that applies to any particular candidate's pool."

   Part 6.2's G14 asks "does the observed success rate apply uniformly, or does it depend on a property of each case?". `proven-in-production.md` S8, "Conditioned yield: the pooled rate is correct and applies to nobody", quotes 83's form: "an average over a mix the decision does not face".
3. **The card's own fields point to E.**
   - Its decisive gap is population. All nine other cards with decisive A lead with time, and eight cards pair E with population first, task129 and task76 among them.
   - The design note's DRAW names the revision split "G14 conditioned yield". Part 6.2 heads G14 "gap 2, pattern E".
   - The fingerprint skill lists generators "decisive first". G14 sits second, "in support", behind "G13 horizon mismatch (looks per run)", which is the move from rung 1 to rung 2.
4. **The note's case for A rests on E's own failure clause.** Its "Pattern A, not E" paragraph argues that a split on a visible column is "a signpost". That sentence is Part 2's "Where it degrades" for Pattern E: it describes a weak conditioned yield, not another pattern.
   - The forward fact (the frozen peak holds no revision) is E's transport target. Every E transport build has one: task44's inverted mix, task83's target pool, task129's decision population.
   - That fact is filed twice, in the prompt and in handbook s.6.1.
5. **Part 2's off-chain form of A is the strongest case for A, and its own exemplar is keyed E.** The off-chain form puts "the moderator in how a period treats the unit". Its exemplar, task44 v2, is keyed E, time first, `composition_mix`, on its own card. In task228 the moderator is also recorded per run (`config_rev`) and read per run.

**Why the alternatives are not answers.**
- **Pattern `none` with G14 first passes the guard on a technicality.** Only because `decisive_mech` compares the G-code G14 with task129's letter E. G14 is Part 6.2's generator for pattern E, so this is the same key under another name, which fingerprint Part 4 calls "a card written to pass".
- **Time first with A** would make the card internally consistent, but would still describe the frame and rung 2 rather than rung 3. It also trips the guard:
  - `test.same_puzzle_older` against approved task33 and lineage rows of task41, task55 and task89
  - `test.same_driver_older` against task89's lineage.

  The screen then promotes approved task33 on all three core axes.

**What-if results.** These are in-memory runs of `guard.py check`, plus the draw-order screen on scratch caches.

| Card variant | Guard | Screen in draw order |
|---|---|---|
| As filed (population, A, G13 first, `population_selection`) | WARN (`repeat.decision` against task131) | task131 promoted |
| Pattern E, G14 first | **BLOCK `ban.pattern` against task129**; BLOCK unless differentiated, `test.same_puzzle_older` against task53 v2 (live) and the lineage rows task28 v1, task30 rounds 1 and 2, task32 v1 | task53 promoted (gap, pattern and decision all collide); task131 promoted |
| `composition_mix`, rest as filed | BLOCK `ban.strategy` against task129 | unchanged |
| Pattern `none`, G14 first | WARN | unchanged |
| Time first, A | BLOCK unless differentiated, `test.same_puzzle_older` (task33 and others) and `test.same_driver_older` (task89 lineage) | task33 (approved) promoted |
| `forecast_method_backtest` | WARN | unchanged |

**Why this is not a clone tier.**
- task129's driver differs from task228's. On the honest key they share the pattern but not the decisive insight (see Clean).
- task53's driver differs (see Clean). The lineage rows that the E variant meets are dead architectures, history and not findings.
- `population_selection` sits at 1 of the last 12.
- No approved build is involved under the honest key.

**Plainly: whether the data survives depends on the pattern key.**
- If the card is keyed E, clearing `ban.pattern` means a decisive rung that is not a conditioned yield. Rung 3, the figures and the pack would all move, so the data does not survive.
- If the author's A stands, nothing moves.
- The clone tiers require no redraw either way.
- This is the second pass in which the honestly keyed decisive rung lands in task129's three-draw window: pass 2 on the strategy, pass 3 on the pattern.

## Clean, shares components by design

### task131: previous draw, promoted in draw order (decisive gap and decision type)
- **Status.** No ledger row. Its `pipeline.json` records it as approved and delivered on 2026-10-10.
- **Shared components:** the decisive gap (population), pick one of N, a rung-0 kill by the filed standard's own definition, and again, as in round 1, the form of the decisive rung: a re-estimate on a subset fixed by a property of a group. Pass 2 recorded that form as gone; it is back.
- **Decisive moves, with the domain nouns stripped:**
  - task131: read the effect only on parent units whose sub-units all drew the same arm, because sub-units share one budget and lift moved between siblings nets to zero at full rollout.
  - task228: hold the per-run false-alarm rate only on runs that took no mid-run change, because a change disturbs the checks and the forward window admits none.
  - These are not the same claim. One is interference, a spillover between units. The other is a disturbance that only the past window carries. A solver primed on sibling spillover is not primed to look for the effect of a configuration change on a calibration.
- **Paths:**
  - task131:
    1. Net margin per card-week over the baseline and run-rate weeks.
    2. Join the allocation to the cards; cards of one membership share a household.
    3. Keep the memberships whose cards all drew one cell (decisive).
    4. Scale to the programme.
    5. The regional grid.
    6. Recommend.
  - task228:
    1. Join the exports to the audit through the bookings.
    2. Labels from the audit (rung 0 to 1).
    3. Four-week runs (rung 1 to 2, the stop rung).
    4. Split by `config_rev`.
    5. Hold the budget on the 106 unrevised runs and search the grid (rung 2 to 3, decisive).
    6. Catches in the filed window.
    7. The incumbent's record and peak coverage.
    8. Pick.
- **Position.**
  - The subset restriction is decisive in both builds. That is shared as a form; the restriction is an ordinary filter.
  - What makes it decisive (the reason the excluded units misstate the decision's condition) differs.
  - The skill's one-sentence test turns up only the population gap itself ("estimate on the units that resemble the decision's condition"), which 42 builds share. That is not a Template finding.

### task129: three draws back, `composition_mix`, pattern E
- **Status.** No ledger row. Its `pipeline.json` is at stage 2 (design), 2026-10-10, with no pack and no write-up.
- **Shared components:**
  - As filed: the decisive gap (population).
  - On the honest key, also: decisive pattern E and decisive G14.
  - The family of conditioning a quantity on a state defined by a version or configuration change, and carrying it to the decision population's state.
  - At design level only, the physics behind that state: a change that invalidates client-side cached state.
    - task129: a device's first load after a deploy against a cached reload.
    - task228's design note and `sim.py`: returning users whose cached configuration predates a revision are re-bucketed until it expires.
- **Decisive moves, with the domain nouns stripped:**
  - task129: separate two co-occurring causes by measuring each within a per-record state that no column carries, rebuilt from the order of each unit's records against version changes, and carry both to the decision population's state mix. Both separating groups sit mostly in the other state.
  - task228: as above.
  - These are not the same claim. task129's difficulty is building the hidden state, and two causes acting on opposite states so that every visible-column split ties. task228's state is a recorded column, there is a single quantity per candidate, and the target is pure.
- **Paths:**
  - task129: rung 0 crawl byte bridge; rung 1 matched URLs; rung 2 field event study at release dates; rung 3 cohort-aligned joint ramp split by the two separating groups and standardised to the phone mix through a registry column (the stop rung); rung 4 per-state effects from view order against deploys, reweighted to the base's state mix (decisive).
  - task228: as in the task131 entry.
- **Position.** A visible-column conditioning is task129's stop rung and task228's decisive rung. task129's decisive move, building the state, has no counterpart in task228. So the device is not spent twice as a decisive rung.
- **What the pair does share** on the honest key is the decisive pattern inside the three-draw window. That is the guard ban above, not a clone tier.
- **Watch item, not a finding.**
  - The cache physics is in neither build's reviewer-visible files today: task228's prompt, pack, write-up and metadata carry no cache, deploy or release-train wording, and task129 has no pack yet.
  - If task228's write-up ever explains the revision effect through cached configuration, and task129's pack ships its release-train log, a reviewer holding both would read one physical story.

### task130: two draws back, no mechanism axis shared
- **Status.** No ledger row. Its `pipeline.json` records it as delivered on 2026-10-11.
- **Decisive move:** departures from a closed group are each member's rank inside a rationed priority list against a cumulative planned supply. No rate or survival curve read off history reproduces them. Strategy `other`, quantity figure, G16 decisive.
- **Its path:**
  1. Placements.
  2. Bedroom-need reviews.
  3. The filed move-on order.
  4. Borough-wide lists.
  5. The plan worked down per size (decisive).
  6. Count those remaining.
  7. Price.
  8. Recommend.
- **Shared with task228:** only the general frame that a historical average stands in for a forward window. That frame runs through most of the corpus. Clean, with nothing to share.

### task229: next draw, built in parallel, card only
- **Status.** No ledger row. Track A is unchecked, because its prompt, write-up and pack are not in this worktree. The card was replaced in this commit: after task229's own hardening loop 1, its driver is the unit a standard error is built over.
- **Shared components:**
  - the objective (data-quality monitoring) and the Gate G mechanism `signal_vs_noise_or_hold`; these are the only two cards that carry either
  - the decisive gap (population, time second)
  - G17
  - a JSON alert configuration and a PNG among the deliverables.
- **Decisive moves, with the domain nouns stripped:**
  - task229: build the standard error of a mean over the shared parent nodes through which entities fail together. An entity-level error understates it severalfold and fires on node noise.
  - task228: hold a false-alarm rate on runs free of a change the forward window excludes.
  - These are not the same claim. They also run in opposite directions: task229's naive error understates the noise, while task228's pooled calibration overstates it for the disturbed checks.
- **Other differences:**
  - pattern D against A (or E)
  - `grain_or_unit` against `population_selection`
  - a designation set against a pick with a setting
  - shape 10 against 04
  - calibration none against the audit.
- **For task229's own pre-flight:** the pair reads as two alert builds drawn the same day.

### task48 and task104: the surface screen's nearest
- **task48** (v2; the ledger says round 1 was solved exactly and the author rejected the build; the parser mislabels it as delivered).
  - Its driver: a population invisible at the monitor's reporting grain, recovered at a two-sided pair grain once every flag has been conditioned away and the hold is the strongest wrong answer.
  - Shared with task228: the population gap and `monitoring_export`. Clean.
- **task104** (no ledger row).
  - Its driver: re-run a self-adapting scorer at settings it never ran at, because its logged scores are endogenous to the setting that produced them.
  - Shared: the frame (an on-call alert's setting for the next period, replayed against a year) and shape 04.
  - Position differs. Re-thresholding logged values is task104's stop rung and is correct at every rung of task228, whose checks do not adapt. Clean.

### task33 (approved): shares the A label as filed
- **Decisive move:** a forward yield in which a measured elevation scales with the expected forward path and stops at a filed intervention, so the largest past exceedance has already resolved.
- **Path:** back-test the closed actions against an acceptance bar, truncate at the filed interventions, scale each elevation with its expected forward path (decisive), and pick.
- **Shared with task228:** pattern A, pick one of N, `monitoring_export`, and a surveillance-alert world.
- **Not the same claim.** task33 is Part 2's canonical A, resolving against ongoing. task228's rung is not. The shared label is the filed card's, and the honest key removes it.

### task53: promoted only under the honest key (gap, pattern and decision all collide)
- **Status.** Live on the ledger (rebuilt 2026-08-28).
- **Decisive move:** where each candidate's eligible volume pools per account against an adoption scale break that a closed offer log draws and no file states. The leader's volume sits below the break.
- **Not the same claim.** task53's property is a threshold recovered from a corpus. task228's is a recorded column whose forward value a filed rule fixes. The quantities (adoption volume against a false-alarm rate) and the decisions differ.
- **A differentiation line is writable.** If the card is re-keyed, `test.same_puzzle_older` asks for one.

### task68: pass 2's promoted pair, now two distant axes
- The shared G6 has gone with the loop-1 rung.
- task68 now shares the decisive gap, pick one of N and `monitoring_export`. Its matched panel across identity successions is not task228's move.
- task72, task121, task11 and task12 share the same two axes with different drivers, as in passes 1 and 2.

### The calibration organ: a verified subsample or audit
- task34 (approved), task43, task74, task93 and task111 share it. None sits within three draws of task228.
- The audit labels sound and defective from rung 1 on, so the organ is off the decisive rung.

## Strategy monoculture
The batch is the last 12 builds in draw order ending at task228: task119, task121, task122, task124, task125, task126, task127, task128, task129, task130, task131 and task228. The counts are read from the cards.

| Measure | Count | Cap | Verdict |
|---|---|---|---|
| Withheld rule with an official decoy | 0 of 12 | 2 | under |
| Certified-record decoy (`validated_decoy`) | **7 of 12** | 3 | **over: Strategy monoculture finding** |
| Any one `stump_strategy`, task228 as filed (`population_selection`, 1 of 12) | at most 2 of 12 (decomposition_attribution, identity_resolution, causal_design and binding_constraint) | 4 (a third) | under |
| Any one `stump_strategy`, task228 keyed `composition_mix` | at most 2 of 12 | 4 | under |

- **The seven builds carrying the certified-record decoy:** task121, task122, task124, task125, task126, task127 and task129. This is unchanged since round 1.
- **Shifting the window to take in task229 and drop task119** leaves the decoy count at 7 and every strategy at 2 or fewer.
- **task228.**
  - Its decisive rule is filed (DQ-07 s.4, handbook s.6.1 and s.6.2), with no official decoy.
  - `validated_decoy: false` is honest. The pooled four-week calibration reproduces no closed, published or certified figure, because the audit labels outcomes, not settings.
  - It adds to neither capped count.
- **The forward-window frame.** As in round 1, the decisive rung turns on a condition only the forward window has (the freeze), against a record that supports the pooled method. The frame recurs across the batch. It is not counted, because no certified record blesses the wrong method here.

## Corpus habits
- **File roles.** task228 carries none of the habit names. Its dictionary is `vigia_export_fields.md` and its provenance record is `export_notes_2026-10-05.txt`.
  - `data_dictionary`: 61 builds
  - `export_manifest`: 33
  - `data_notes` and `provenance`: 12 each
  - `county_reference`: 4
  - `product_catalog`, `accounts`, `plan_catalog`, `metric_definitions`, `item_master`, `facility_register`, `site_master` and `sources_and_licences`: 3 each.
- **Deliverable pairings.** task228's json+xlsx is not among them.
  - pdf+csv: 9 builds
  - py alone: 8
  - py+pdf: 7
  - pdf+png: 6
  - py+csv, py+xlsx and pdf+xlsx: 5 each
  - docx alone: 4.
- **Ask opening.** "give me the single dollar figure we" appears in 2 builds, neither of them task228.
- **Prompt constructions in the last 12 (task121 to task131 and task228).** Recounted; no prompt in the window changed since pass 2.
  - **A stakeholder's belief about the naive pick: 7 of 12.** task121 and task124 carry it with "is sure", task125 and task131 with "expects", task128 with "wants", task129 with "blames", and task228 with "would rather".
    - task228's version is unnamed, takes one clause and uses the only "would rather" in the 12, which is the form prompt-voice.md asks for.
    - The construction itself is the habit: Idiom tier, a soft flag.
  - **The chart title stating the call: 11 of 12**, which is spec. task228 is the one prompt that puts the title first among the chart's parts.
  - **"What I need is" framing the ask: 3 of 12** (task123, task128 and task131). task228 is not among them.
  - **The pick marked on the chart: 4 of 12.** task228 is not among them.
  - **The runner-up asked for beside the pick: 2 of 12.** task228 is not among them.
- **Mechanism idiom.**
  - Population is task228's decisive gap and the most common decisive gap on file (42 of the 127 compared).
  - Data-quality monitoring exists on two cards only, task228 and task229. They were drawn the same day and both deliver a JSON alert configuration.

## What to redraw
1. **task228: the decisive pattern.**
   - Keyed by what rung 3 does (a page rate conditioned on `config_rev` and read on the stratum the frozen season occupies), it is E with G14 decisive.
   - task129 carries E three draws back, so `guard.py` BLOCKs `ban.pattern` under Part 6.1. The A and G13 on the card name rung 2 and the frame.
   - This is a guard ban, not a clone tier, and it decides the heart half of the stage-5 gate.
2. **Batch, not task228: the certified-record decoy (`validated_decoy`).** It sits at 7 of 12 against a cap of 3, carried by task121, task122, task124, task125, task126, task127 and task129.

Nothing else is owed by task228. The strategy key is honest; the one design-note sentence it contradicts (the no-app peak) is an edit, not a redraw. The Idiom is a soft flag the prompt already handles.

## Tooling notes, not findings
- **"Consecutive" uses task numbers.** fingerprint.py's `consecutive` and `adjacent` tests measure task-number distance, so task131, the previous draw, counts as 97 builds away. The guard orders by drawn date.
- **The status parser matches "delivered" anywhere in a status cell.** task48 and task72 are still labelled delivered or approved, which neither status cell says.
- **The screen never reads `stump_strategy`, and the guard compares keys only as strings.**
  - `decisive_mech` compares a pattern letter with a G-code, so a card keyed `none` with G14 passes `ban.pattern` against a card keyed E, although Part 6.2 makes G14 pattern E's generator.
  - Neither script can tell an honest key from a convenient one. Both key questions in passes 2 and 3 were found by reading.
- **The extract never opens `target.zip` and does not profile parquet.**
- **Card-only builds never enter the screen:** task114, task115, task116 and task229.
- **`pipeline.json` and the ledger disagree on status.** task131 records approved and delivered, and task130 records delivered; the ledger has no row for either. This report follows the ledger, as the agent requires.
- **The people index.** Both guard runs here used a scratch copy, so the tracked `people.json` is untouched.
- **The cache is modified and uncommitted.** `.claude/skills/clone-check/.cache/fingerprints.json` has task228 added, task130 refreshed and its `repo` field set to this worktree. Nothing was committed or pushed. No prompt, target, design note, card or ledger was modified. Scratch work is under /home/user/orch/auditor-scratch-3/.

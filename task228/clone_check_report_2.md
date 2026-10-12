# Clone check: pre-flight, task228 against the whole corpus (hardening loop 1, head 6b19d41), 2026-10-11, pass 2

## Verdict
The worst tier touching task228 is Idiom, a soft flag on Track A that no single pair carries: its one stakeholder belief about the naive pick is a construction 7 of the last 12 prompts carry. There is no Exact, Same seed, Dataset, Template or Shape echo finding against any build, so the clone condition of the stage-5 gate holds.
- **The round-1 Shape echo with task131 is cleared.** These are gone from the prompt:
  - the runner-up ask
  - "the call I need is"
  - the close on a colleague's belief followed by a bare role line
  - the marked pick.

  Only the decision shape remains (one of N with a quantity attached), and on its own it is not a finding.
- **The screen's one promotion, task68, is `clean_shares_components`.** Both cards put G6 (composition shift) on the decisive rung, but the operations run in opposite directions:
  - task68 removes a composition change from a past comparison (a matched panel of continuing units).
  - task228 puts the forward season's composition into a rate (a reweighting to the season's mix).
- **One card field decides the heart half of the stage-5 gate. It is a guard ban, not a clone tier.**
  - The card keys the stump strategy `population_selection`, which describes rung 2 (runs of the season's length).
  - The decisive rung 3 is a reweighting to the season's surface mix. vocab.json and stumping Part 2 file that under `composition_mix`.
  - Keyed that way, `guard.py` BLOCKs `ban.strategy` against task129, three draws back. As filed, heart is WARN.
- **At batch level, the certified-record decoy still carries 7 of the last 12 builds** against a cap of 3. That is a Strategy monoculture finding, and task228 is not one of the seven.

## Scope and coverage
- **Mode and scope.** Pre-flight on task228 against every build on file, with no window, at head 6b19d41 (hardening loop 1). This is pass 2. The round-1 report, `clone_check_report_task228.md`, is not overwritten.
- **Why it re-ran.** The build-pipeline stage-5 rule re-runs the adjudicated pre-flight when the driver changes, and loop 1 moved the decisive rung:
  - Round 1's decisive move was holding the page budget on runs of the forward length. It is now rung 2.
  - The new rung 3 holds the per-run false-alarm budget on the season's own mix of surfaces, taken from the peak booking queue.
  - The card's decisive generator moved from G13 to G6.
- **Extract.**
  - The committed cache (125 cards, task1 to task131) held no task228, so I re-ran `fingerprint.py extract` in place at 04:19 UTC.
  - Result: 126 cards, 124 with a prompt or target. 16 builds were fingerprinted from disk (task117 to task131, and task228); the rest were carried from the cache.
  - task130's on-disk profile (14 files) replaced the cached 13, as in round 1.
  - Every input predates the extract: prompt 04:04, submission 04:05, design note 04:10, both cards 04:10, pack 04:02.
- **Screen.** `fingerprint.py screen --focus task228` covered 124 builds and 123 pairs, and promoted 1: task68, on all three core mechanism axes.
- **Draw order.** The screen measures "consecutive" by task number, while the guard orders by drawn date, then number.
  - In draw order the neighbours are task129 (three back), task130 (two back), task131 (previous) and task229 (next, same day).
  - Re-applying the screen's own rules in that order promotes one more pair: task131, on two of three core axes between back-to-back draws.
  - task130 shares no core axis. task229 is card-only and shares one.
- **Builds compared: 127.**
  - 123 went through the screen. 101 were scored on both tracks, with Track B read from the cards (none fell back to the ledger). 22 were Track A only: task3 to task10, task13 to task24, task112 and task113.
  - 4 card-only builds were scored on Track B with fingerprint.py's own `track_b`: task114, task115, task116 and task229.
  - Nothing comparable exists for task1 and task2 (no prompt, target or mechanism) or for task99 (a scratch slot, excluded).
  - 34 screened builds carry back-fitted labels (task36 or earlier), and 14 of them were scored on Track B.
  - Mechanism layer over the 124 screened builds: 102 have a card, 5 are note-only and 17 are unavailable.
- **File-level gaps.**
  - The extract profiles csv, tsv, txt and xlsx only. It never opens `target.zip`, and it covers parquet, json, docx and md by byte hash only.
  - 15 screened builds have no profiled target: task3, task10 and task117 to task129.
  - task117 and task119 ship a zip, so I profiled them from it in a scratch copy of the cache. Against task228 they show no identical file, no same-seed table, no column-set collision and no shared name, and the screen's result does not change.
  - task118 and task120 to task129 have no pack on this checkout, so file-level Track A against them is unchecked.
  - task229's folder here holds only its seed, so it is compared on its card alone. /home/user/b229 was not read.
- **Supplementary runs.** These are scripts built on fingerprint.py's and guard.py's own functions. Scratch work was written to and read from this thread's own scratchpad only.
  - The draw-order re-screen, and Track B for the card-only builds.
  - The zip coverage above.
  - `guard.py heart task228`, run against a scratch copy of the committed people index. A live run rebuilds the tracked `people.json` from this checkout's folders and drops carried personas (round-1 tooling note).
  - A what-if `guard.py check`: task228's card with `stump_strategy` keyed `composition_mix`, held in memory only. The card is untouched.
  - Two vocabulary sweeps over every card driver, concrete driver and stump, every lineage entry and every ledger row (1,272 and 799 texts). One swept the new move (mix, composition, reweighting, under-representation, forward population). The other swept the standing frame (false-alarm budgets, repeated looks, multiplicity, release or deploy timing).
  - `voice-check.py`, run bare and on task228.
- **Pairs adjudicated.** All in this thread, with no subagents, because the invoking command forbade the Agent tool. No advisor or web tool was used and no golden file was opened. The clone-check skill was loaded by reading its SKILL.md in full, because the Skill tool does not list it in this session.
  - **task68** (screen-promoted). Read: its card, ledger rows, the cached submission's steps, critical components and recommendation, and the cached prompt profile and target listing. Its folder is not on this checkout, so its design note was not read directly; the card (mechanism source: design note) and the ledger's mechanism cell carry its ladder.
  - **task131** (promoted in draw order). Read: card, prompt, submission and target listing, plus round 1's reading of its design note.
  - **task229** (next draw, named by the invocation). Read from its card only.
  - **task129** (three draws back). The sweep surfaced it: it is the only live build that pairs the reweighting move with release-train client behaviour, and it holds `composition_mix` inside the guard's ban window. Read: card, prompt, `pipeline.json`, and its design note's draw, stump, decisive rung, both ladders, position table and correction grid. It has no pack or write-up yet.
- **Supplementary reads.** Card drivers, stumps and ledger cells were read to name the difference for 16 builds:
  - task83, the kin task228's own design note names
  - task95, task20, task43, task44, task47, task56 and task86, from the composition sweep
  - task104, the other on-call threshold build
  - task130, two draws back
  - task103, nearest in the heart run
  - task114, task116, task48, task33 and task34.
- **Unread.** 107 of the 127 builds were left unread, because neither the screen nor the draw-order rules promoted them and neither sweep surfaced them.
- **Status.** The ledger runs to task108. task228, task229, task131 and task129 have no row, so all four are unknown on the record. The ledger records eight builds as approved: task25, task27, task28, task29, task30, task33, task34 and task35.
- **Concurrency.** The parent build kept working during this run.
  - After the extract it graded round 2 on the loop-1 pack. Its `pipeline.json` records that both solvers stopped at rung 2 (mean 48.2), and it opened hardening loop 2 on the asks.
  - It then edited `DESIGN_NOTE.md` (rung-2 figures only: 8 of 166 becomes 7, and 4.8 per cent becomes 4.2), `generator/docs.py`, `extracts.py`, `sim.py` and `leak_check_report.md`, and added `generator/_search.py`.
  - None of those edits is covered here. When this report was written, the prompt, submission, card and cut pack were unchanged since the extract.
  - The round-2 brief keeps the decisive rung. Under the stage-5 rule, loop 2 therefore owes a heart re-run, and a `guard.py surface` re-screen once the pack is re-cut. It does not owe another adjudication unless the driver moves again.

## In batch against earlier builds
Pre-flight has no batch, so this section carries the comparison the reviewer's cross-batch check runs: task228 against builds the ledger records as delivered or approved.
- **No hit against an approved or delivered build.** None of the eight approved builds is promoted, none shows a hard tell, and none shares more than one of the three core mechanism axes.

| Approved build | Surface (percentile) | What it shares with task228 |
|---|---|---|
| task25 | 0.020 (29th) | decision type; context-artifact type |
| task27 | 0.083 (71st) | decision type |
| task28 | 0.080 (63rd) | decision type |
| task29 | 0.078 (59th) | decision type; context-artifact type |
| task30 | 0.085 (78th), the nearest | decision type |
| task33 | 0.083 (71st) | decision type; context-artifact type |
| task34 | 0.029 (35th) | decisive gap; calibration organ (`gold_standard_subsample`) |
| task35 | 0.073 (48th) | context-artifact type only |

- **task34.** It is far outside the three-draw window, so Part 6.1's calibration ban does not reach it. Its driver is a subpopulation that only a within-cluster fit can enumerate.
- **task33** carries G6 among seven generators, but not on its decisive rung (pattern A, `forecast_method_backtest`). Its driver is a forward yield scaled by the expected path, recovered by back-testing closed actions.
- **No exclusion-level exposure for task228.**

## Track A findings, reviewer visible
None at Shape echo or above.

### task131 against task228: the round-1 Shape echo, cleared
- **Status.** Neither build has a ledger row. task131 was drawn 2026-10-10 and task228 2026-10-11, back to back in draw order.
- **Gone from task228's prompt since round 1:**
  1. The runner-up ask ("Then the check that comes second and how many fewer defects it catches").
  2. The ask framed as "The call I need is ...".
  3. The close: a named colleague expecting the biggest mover, "since ...", then a bare role line.
     - The prompt now ends on the chart paragraph.
     - The belief sits mid-paragraph and unnamed: "The desk would rather page on events per exposed user, the check that jumps hardest when logging breaks."
     - The role is inline: "as platform lead I sign its wiring".
  4. The marked pick on the chart. The title now names the check and the setting instead.
- **What remains: the decision shape.** Both commit one named option of N with a quantity attached, asked as a single question:
  - task131: "Which of the four summer test offers goes on every member card next year, and what is it worth to the co-op in 2027?"
  - task228: "Which check, at which of the settings the alert service accepts?"

  That is one of the four Shape echo axes. The other three differ:
  - The ask construction.
  - The deliverable species: docx+png against json+xlsx+png.
  - The calibration organ: none against the replay audit.

  One axis alone is not a finding, and the design note answers the guard's `repeat.decision` WARN on it.
- **A content echo inside the belief.** Both colleagues favour the candidate that moved most:
  - task131: "because it moved more spend than any other offer in the test"
  - task228: "the check that jumps hardest when logging breaks"

  That is the corpus idiom reported under Corpus habits, not a pair finding.
- **Mechanically**, the surface is 0.095 (95th percentile), and all of it comes from the pack's format mix (0.875). Masked prompt overlap is 0.000, ask skeleton 0.000, and there are no shared names.

### Not findings, checked
- **Hard tells.** Across the 123 screened builds there are no byte-identical files, no same-seed tables, no identical column sets and no shared invented names.
  - Pousalto and Vigia appear on no other card.
  - The highest masked prompt overlap is 0.004 (task51) and the highest masked write-up overlap 0.002 (task124). The ask skeleton scores 0.000 against every build.
- **Personas.** None of task228's eight personas shares a first name, surname or full name with any card or with the committed people index.
  - The round-1 surname echo (Pires, against task121) is cleared: the on-call lead is now Salomé Nogueira.
  - "Pires" survives only in the design note's own record of the redraw. It is not in the prompt, the write-up, the pack or the generator.
- **task104** is 28 draws back with no ledger row. It sets an on-call alert's sensitivity for the next rota from a replay of its own year, and it is the corpus's only other on-call paging-threshold project.
  - Surface 0.094 (94th percentile), from the format mix only. Masked prompt overlap 0.000.
  - Its deliverables (html+svg) and calibration organ (`other`) both differ from task228's, so at most one Shape echo axis (the decision) is shared. Its mechanism is under Clean.
- **task129** shares nothing reviewer-visible today: it has no pack and no write-up, its prompt shares no construction (masked overlap 0.000), and its deliverables are pptx+xlsx.
  - One watch item: both builds' explanations turn on a mobile release train changing what clients send.
  - task129's pack is planned to ship a release-train log. task228's write-up says app tests "rode the fortnightly release train" and that "batched beacons" page sound app runs.
  - This is ordinary industry vocabulary. Noted, not a finding.
- **`voice-check.py`**, run bare and on task228 over task121 to task131 and task228:
  - task228's stakes-first opening is the only one in the 12.
  - It finds no listed carrier and no unlisted repeated run.
  - task228 runs 240 words, against a median of 253 and a flag line of 330 (round 1: 298).
  - It ships three files, at the ceiling with task123 and task127.
  - Its JSON deliverable is the only one in the 12. task229, outside this window, also commissions a JSON alert configuration.

## Track B findings, mechanism
None. With no Template finding against any build, no rebuild is owed and the data stands.
- **task228's move, with the domain nouns stripped.** A per-run false-alarm budget held over the season a setting is live is rebuilt on the forward season's own mix of a visible stratum (the surface a run sits on) that the record under-represents, because runs on that stratum page sound runs far more often across a four-week run. Held on that mix, the naive candidate has no admissible setting, and a cumulative, stratum-insensitive candidate leads.
- **The mechanism screen, across the 127 builds compared.** task228 shares:
  - the decisive gap (population) with 42
  - the decisive G-code (G6) with 1 (task68)
  - the decision type with 20
  - the Gate G mechanism with 1 (task229)
  - the calibration organ with 5 (task34, task43, task74, task93 and task111)
  - the context-artifact type with 26
  - the same-driver signature with none
  - the domain and objective pairing with none.
- **Collisions and text similarity.**
  - The most core axes any pair collides on is three (task68). Six builds collide on two: task11, task12, task53, task72, task121 and task131.
  - The highest card-driver overlap is 0.051 (task83), against a promotion line of 0.40.
  - In the guard's heart text, the nearest is 0.08: task103's retired v2 row, a funding reserve release, which is an incidental match.
- **The reskin route.**
  - No text on file combines the false-alarm frame with a mix shift or with release timing. Only task68 uses multiplicity vocabulary, in its stop rung's corrected bar.
  - Two texts pair a mix or reweighting move with release or deploy timing: task129 (in flight) and task121's never-registered v1 (history). The other matches (task49, task79 and task96) are incidental: "released address" and "release" in other senses.
- **The same strategy family, not the same driver.**
  - The sweep finds a family of builds that transport a pooled rate or effect to a target population whose mix differs: task95, task83, task129, task20, task43, task44 and task47 in their current architectures, plus the dead lineages task43 v1, task44 v2, task56 v5 and task73 v2.
  - All current ones except task47 are keyed `composition_mix`.
  - In each current one, the decisive difficulty is recovering a stratum that no column carries:
    - task95: an age class, by differencing two registers
    - task83: a unit's own treatment history, by grouping a log
    - task129: a per-view cache state, by ordering views against deploys
    - task20: a fence-against-lead-time class
    - task43 and task44: a moderator behind a join or in no column.
  - In task228 the stratum is a column (surface). The difficulty is that nothing in the pack says the rate depends on it, or that the forward mix differs.
  - That is a shared strategy with a different driver. Part 1 treats it as legitimate pair by pair and counts it at batch level, which is where Strategy monoculture reads it.

### Not a clone tier, but it decides the heart half of the gate: the stump-strategy key
- **What the card says.** `stump_strategy: population_selection` was set at the draw for round 1's decisive move (runs of the forward length) and kept through loop 1. The design note's DRAW reads: "population_selection (selection into run length, and the season's composition)".
- **What the decisive rung does.** Loop 1's decisive rung is a weighted sum of per-surface page rates, weighted by the season's standing tests on each surface (ladder rung 3, submission step 5). Every reference point files that as composition, not selection:
  - vocab.json defines `composition_mix` as "mix shift, Simpson's reversal, standardisation or reweighting changes the comparison".
  - Stumping Part 2 separates "population and selection (survivorship, attrition, exposure)" from "composition and mix (Simpson's reversal, standardisation)".
  - The card's own decisive generator is G6, composition shift.
  - The corpus keys every other forward-mix reweighting `composition_mix`: task95, task20, task83, task129, task43 and task44.
- **Which rung each key describes.** `population_selection` describes rung 2 (exposure: runs of the season's length). The fingerprint skill's rule when two keys fit is to use the one a reviewer would use, and a reviewer reading rung 3 sees a standardisation.
- **The what-if.** With the key set to `composition_mix`, `guard.py check` returns BLOCK on `ban.strategy` against task129 (`composition_mix`, drawn 2026-10-10, three draws back). That is Part 6.1's standing ban on reusing the stump strategy within the last three builds. As filed, the verdict is WARN.
- **Why it is not a clone tier.**
  - task129's driver is different (see Clean).
  - `composition_mix` would sit at 2 of the last 12, under every cap.
  - No approved build is involved.
- **Plainly: whether the data survives depends on the key.**
  - If the key moves to `composition_mix`, clearing the ban means redrawing the decisive rung's strategy, and the pack does not survive that.
  - If the author's reading of `population_selection` stands, nothing moves.
  - The clone tiers do not require the redraw either way.

## Clean, shares components by design

### task68: screen-promoted (decisive gap, decisive G-code and decision type all collide)
- **Status.** Live on the ledger: built 2026-09-04, repaired 2026-09-05, rounds held, determinism passed on the repair, nothing later recorded. Not approved or delivered on the record. task228 has no row. Severity: status unknown on one side, not exclusion level.
- **Shared components:**
  - the decisive gap (population)
  - G6 on the decisive rung
  - pick one of N
  - the context-artifact type `monitoring_export`: task68's July movement screen and task228's Vigia export, both correct and ranking nothing
  - a multiplicity frame below the decisive rung: task68's corrected screen bar at its stop rung, and task228's repeated looks at rungs 1 and 2.
- **Decisive moves, with the domain nouns stripped:**
  - task68: measure the change on a fixed panel of units present in both windows, linked across identity successions, because entrant inflow and a price offset hold every aggregate flat, on the basis and bar that a closed corpus of dispositions certifies.
  - task228: hold a per-run false-alarm rate on the forward population's own mix of a stratum the record under-represents, because runs on that stratum page sound runs more often, which leaves the naive candidate no admissible setting.
  - These are not the same claim. G6 runs in opposite directions: task68 takes a composition change out of a past comparison, like for like, while task228 puts a forward composition into a rate.
  - task68 also needs its basis recovered from a corpus (pattern B). task228 recovers nothing.
- **Paths:**
  - task68:
    1. Build the record: latest versions, procedure filter, conversions, contingency rows.
    2. Replicate the movement screen.
    3. Set dairy aside as price.
    4. Set fruit aside as season timing.
    5. The value basis files a nil return (the stop rung).
    6. Back-test bases against 17 dispositions. Only the matched, succession-walked quantity basis reproduces 17 of 17 (decisive).
    7. Apply that basis: chapter 22 at -18.1 per cent.
    8. Check it against the register's history.
    9. Recommend.
  - task228:
    1. Join the exports to the audit through the bookings.
    2. Take the labels from the audit, not the tracker (rung 0 to 1).
    3. Hold the budget on runs of the season's length (rung 1 to 2).
    4. Take the season's surface mix from the queue and split the sound four-week runs by surface (rung 2 to 3, decisive).
    5. Grid-search each check's most sensitive setting within the season-weighted budget.
    6. Count catches in the window over all 78 defects.
    7. Pick.
- **Position of the shared moves.**
  - Explaining loud movers away is task68's steps 3 and 4. In task228 the loud mover is rung 1's pick (the events check), which drops out at rung 2, once the budget is held on runs of the season's length.
  - The composition move is decisive in both under one label, but it is a different operation in each.
  - task68's deciding corpus rule has no counterpart in task228.
- **The card's differentiation line**, written for `test.same_puzzle_older`, is accurate.

### task131: previous draw, two core axes
- **Status.** No ledger row, so unknown on the record.
- **Shared components:** the decisive gap (population), pick one of N, and a subset fixed by a group property.
- **Driver difference.**
  - task131: read each option only on parent units whose sub-units all drew the same arm, because sub-units share one budget and lift moved between siblings nets to zero at full rollout. That is interference.
  - task228: put the forward season's stratum mix into a per-run rate. That is transport.
- **Position.** The subset restriction that decides task131 (memberships whose cards all drew one cell) has its counterpart at task228's rung 2 (four-week runs), the stop rung, so it is demoted there. Round 1's "shared form of the final rung" no longer holds, because task228's final rung is now a reweighting.
- **Ladder furniture.** Both still kill rung 0 with the filed standard's own definition.

### task229: next draw, built in parallel, card only
- **Status.** No ledger row. Track A unchecked, because its prompt, write-up and pack are not in this worktree.
- **Shared components:**
  - The objective (data-quality monitoring). These are the only two cards that carry it.
  - The decisive gap (population), with time second.
  - The Gate G mechanism `signal_vs_noise_or_hold`, again the only two cards.
  - G17 as a non-decisive generator.
  - A JSON alert configuration and a PNG among the deliverables.
- **No longer shared: the context-artifact type.** task229's card moved from `monitoring_export` to `filed_standard` in loop 1, which was round 1's first redraw item. It is done.
- **Driver difference.**
  - task229 scores each group as the average of its member units' shares over the units present the whole window, with a between-unit error, instead of a record-pooled ratio with a record-count error that high-volume units dominate (pattern D, `grain_or_unit`).
  - task228 puts the forward season's stratum mix into a per-run rate.
  - Both decisive rungs replace a naive pooled rate's weights, and a reviewer holding the pair may notice that. But the weights answer different questions: the unit of analysis and its error in task229, the target population's composition in task228. A solver primed on one is not primed for the other.
- **Position.** The noise term sits inside task229's decisive rung, because the between-unit error decides which builds breach. In task228 the noise budget is the frame from rung 1.
- **Other differences:**
  - the decision: a designation set against one pick with a setting
  - the shape: 10 against 04
  - the calibration organ: none against the audit
  - the strategy: `grain_or_unit` against either of task228's keys.

### task129: three draws back, surfaced by the sweep, holds `composition_mix`
- **Status.** No ledger row. Its pipeline is at stage 2 (design), dated 2026-10-10, with no pack and no write-up.
- **Shared components:**
  - the decisive gap (population)
  - the strategy family: reweighting a stratum-conditioned quantity to the population the decision acts on
  - a mobile release train as the physical reason the stratum matters: first loads after each deploy in task129, and app runs that span a release and send batched beacons in task228.
- **Decisive moves, with the domain nouns stripped:**
  - task129: measure each of two co-occurring causes separately in a hidden per-record state rebuilt from the order of each unit's records against version changes, and carry it to the decision population's state mix, because the separating groups sit mostly in the other state and every standardisation on a visible column ties.
  - task228: as above.
  - These are not the same claim. task129's decisive difficulty is building a state no column carries (G14, pattern E), and the reweighting is only its transport (D). task228's stratum is a column.
- **Position, which is what clears the pair.**
  - task129 puts a visible-column composition standardisation (the phone mix, through the device registry) at its stop rung, rung 3, one below its decisive rung 4. Its note calls it "a composition correction a reviewer expects".
  - task228's decisive rung is a visible-column composition standardisation (the surface mix, through the booking queue).
  - The shared device is the stop rung in one build and the decisive rung in the other, so it is not spent twice as a decisive rung.
- **Not a Template finding.** What the pair does share, the strategy, is the `ban.strategy` question under Track B.

### task83: the kin task228's design note names
- **Status.** Live on the ledger: re-root 2.1, with no stump result recorded.
- **Shared components:** the decisive gap (population), the strategy family, `monitoring_export`, and an experimentation world.
- **Driver difference.**
  - task83 conditions a randomised effect on each unit's own treatment history, a stratum no column carries, rebuilt by grouping the treatment log per unit. It then fills a capped allocation cell by cell (G14, pattern E, `binding_constraint`).
  - task228's stratum is a column, its quantity is a false-alarm rate, and its decision is a check and a setting.
- **Card-driver overlap** is 0.051, the highest against task228 but far under the 0.40 promotion line.

### task95 and task20: forward class-weight transport, keyed `composition_mix`
- **task95** (no ledger row). A conversion rate that reproduces every closed period is a weighted average over two classes, and the forward class weight has moved outside the record. The class sits in no column and is recovered by differencing two dated events across two registers. The decision is a quantity forecast.
  - It is the nearest kin on the transport step.
  - It differs on the hidden class (decisive there) against a visible column, on the quantity (a yield, not a false-alarm rate), and on the decision.
- **task20** (no ledger row). A forward rate depends on an unfiled per-unit classification (commitment fence against lead time) after two large units moved. The decision is a quantity.

### task104: the other on-call threshold build
- **Status.** No ledger row. Drawn 2026-10-03, 28 draws back.
- **Shared components:**
  - the frame: an on-call alert's setting for the next period, replayed against the past year
  - shape 04
  - a pass in the naive path that re-thresholds at each allowed setting.
- **Driver difference.**
  - task104 re-runs a self-adapting scorer at settings it never ran at, because the logged scores are endogenous to the setting that produced them (`forecast_method_backtest`).
  - task228 transports a per-run false-alarm rate to the forward season's mix.
- The frame is the shape-04 component both builds use. The drivers differ.

### The calibration organ: a verified subsample or audit
- The builds that share it are task34 (approved), task43, task74 and task93 (live), and task111 (unknown).
- None sits within three draws of task228.
- In task228 the audit labels sound and defective from rung 1 on, so the organ is off the decisive rung.

## Strategy monoculture
The batch is the last 12 builds in draw order ending at task228: task119, task121, task122, task124, task125, task126, task127, task128, task129, task130, task131 and task228. The counts are read from the cards.

| Measure | Count | Cap | Verdict |
|---|---|---|---|
| Withheld rule with an official decoy | 0 of 12 | 2 | under |
| Certified-record decoy (`validated_decoy`) | **7 of 12** | 3 | **over: Strategy monoculture finding** |
| Any one `stump_strategy`, task228 as filed | at most 2 of 12 (decomposition_attribution, identity_resolution, causal_design and binding_constraint) | 4 (a third) | under |
| Any one `stump_strategy`, task228 keyed `composition_mix` | at most 2 of 12 (composition_mix joins the four at 2) | 4 (a third) | under |

- **The seven builds carrying the certified-record decoy:** task121, task122, task124, task125, task126, task127 and task129. This is unchanged since round 1. Shifting the window to take in task229 and drop task119 leaves every count the same.
- **task228.**
  - Its decisive rule is filed, with no official decoy and no validated decoy.
  - The design note agrees: the audit labels outcomes, and rung 2 reproduces no closed, published or certified figure.
  - Under either key it adds to neither capped count.
- **Where task228's strategy question bites.** Not here, under the twelve-build caps, but under the three-build ban covered in the Track B section.

## Corpus habits
- **File roles.** task228 carries none of the habit names. Its dictionary role is `vigia_export_fields.md` and its provenance role is `export_notes_2026-10-05.txt`.
  - `data_dictionary`: 61 builds
  - `export_manifest`: 33
  - `data_notes` and `provenance`: 12 each
  - `county_reference`: 4
  - `product_catalog`, `accounts`, `plan_catalog`, `metric_definitions`, `item_master`, `facility_register`, `site_master` and `sources_and_licences`: 3 each
- **Deliverable pairings.** task228's json+xlsx is not among them.
  - pdf+csv: 9 builds
  - py alone: 8
  - py+pdf: 7
  - pdf+png: 6
  - py+csv, py+xlsx and pdf+xlsx: 5 each
  - docx alone: 4
- **Ask opening.** "give me the single dollar figure we" appears in 2 builds, neither of them task228.
- **Prompt constructions in the last 12 (task121 to task131 and task228)**, recounted on the loop-1 prompt:
  - **A stakeholder's belief about the naive pick: 7 of 12.**
    - task121 and task124 carry it with "is sure", task125 and task131 with "expects", task128 with "wants", task129 with "blames", and task228 with "would rather".
    - Round 1 counted six, without task129's "blames".
    - task228's belief is unnamed, takes one clause and uses the only "would rather" carrier in the 12. That is what prompt-voice.md asks for ("At most one stakeholder belief, as one clause", carrier varied). The construction itself is the habit: Idiom tier, a soft flag.
    - In task131 and task228 the belief names the candidate that moves most. In task124 and task128 it names where the largest risk or exposure sits.
  - **The chart title stating the call:** required in 11 of 12, which is spec. task228 is now the one prompt that puts the title first among the chart's parts. Three still close the list with "and a title that ..." or "and a title naming ...": task124, task129 and task130.
  - **"What I need is ..." framing the ask:** 3 of 12 (task123, task128 and task131). task228 has dropped out.
  - **The pick marked on the chart:** 4 of 12 (task121, task122, task129 and task131). task228 has dropped out.
  - **The runner-up asked for beside the pick:** 2 of 12 (task129 and task131). task228 has dropped out.
  - **A prompt ending on a bare role line:** task131, plus task122 with a clause after the role. task228 has dropped out. Corpus-wide, round 1 found four such prompts on file, task228 among them, so it is now three.
- **Mechanism idiom.**
  - Population is task228's decisive gap and the most common decisive gap on file, shared with 42 of the 127 builds compared.
  - Transport to a forward mix is a recurring strategy family (see Track B).
  - Data-quality monitoring exists on two cards only, task228 and task229. They were drawn the same day, both decide an alert's wiring, and both deliver a JSON alert configuration, so a reviewer holding both will read them as a pair. The later draw, task229, carries that in its own pre-flight.

## What to redraw
1. **task228: the decisive rung's stump strategy.**
   - Keyed by what rung 3 does, a reweighting to the season's surface mix, it is `composition_mix`.
   - task129 holds `composition_mix` three draws back, so `guard.py` BLOCKs `ban.strategy` under Part 6.1. The `population_selection` on the card names rung 2.
   - This is a guard ban, not a clone tier, and it decides the heart half of the stage-5 gate.
2. **Batch, not task228: the certified-record decoy (`validated_decoy`).** It sits at 7 of 12 against a cap of 3, carried by task121, task122, task124, task125, task126, task127 and task129.

Nothing else is owed by task228. Round 1's Shape echo, the shared surname and the stale card fields are cleared, and the Idiom is a soft flag that task228's own prompt already handles the way prompt-voice.md asks.

## Tooling notes, not findings
- **"Consecutive" uses task numbers.** fingerprint.py's `consecutive` and `adjacent` tests measure task-number distance. task131, the previous draw, therefore counts as 97 builds away, and task129 (three draws back) as 99.
- **The status parser matches "delivered" anywhere in a status cell.** task48 ("one group-by delivered the conclusion") and task72 ("service delivered under a grantee's agreements") are still labelled delivered or approved. Neither is delivered on the record.
- **The screen never reads `stump_strategy`.** It is not among fingerprint.py's `FP_FIELDS`, so a strategy repeat inside the three-build window never promotes a pair. Only `guard.py`'s `ban.strategy` sees one, and only on the key the card carries. The key question above was found by reading, not by either script.
- **The extract never opens `target.zip` and does not profile parquet.** On this checkout, 13 screened builds have no file-level fingerprint.
- **Card-only builds never enter the screen:** task114, task115, task116 and task229.
- **The people index.**
  - Any live `guard.py` run (heart, check or surface) rebuilds the tracked `people.json` when a task folder is newer than it, from this checkout's folders only, and drops carried personas. This run used a scratch copy, so `people.json` is untouched.
  - The committed copy indexes no personas for task120, task121, task122 or task128. The card scan here covered them.
- **The cache is modified and uncommitted.** `.claude/skills/clone-check/.cache/fingerprints.json` now has task228 added and task130 refreshed. Nothing was committed or pushed, and no prompt, target, design note, card or ledger was modified.

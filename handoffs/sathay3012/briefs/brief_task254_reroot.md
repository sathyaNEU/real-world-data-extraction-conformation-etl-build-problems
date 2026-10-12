# Brief: task254 re-root, architecture 2 (stage 1 draw, then stage 2 design)

Worktree: /tmp/claude-0/-home-user-real-world-data-extraction-conformation-etl-build-problems/0a4d0be2-5538-5acb-b824-9d9be7c9c38c/scratchpad/wt254
(branch `sathay3012/task254-fire-planning-bands`, checked out, up to date with `71a9346`). Work only
there: run every script by its path inside the worktree, never touch the main checkout or the sibling
worktree `wt253` (task253 is in design there, in parallel). The branch name stays as it is even if the
new draw leaves wildfire; the author's rule is never to rename a branch.

Commits: on this branch only, pushed with `git push -u origin sathay3012/task254-fire-planning-bands`
(retry 2s/4s/8s/16s on network failure). Every message ends with:
```
Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_0142Jt4Mt622iBfGoK24ivCU
```
Revert `.claude/skills/fingerprint/.cache/people.json` before each commit (guard.py rewrites it). No em
dashes anywhere. No backup or versioned files.

## Why you are here

Architecture 1 (burned area apportioned to protection zones by footprint, not by point of origin)
failed the stage 2 gate: a precise estimand, "acres burned on state-protected land", names the method,
and once footprints are tabulated in a form a pandas analyst can join, the strongest solvers walk
straight to the golden, so the stump would rest on Layer 1 mess. Read `task254/DESIGN_NOTE.md` in full
first (`## Stage 2 verdict` and `## Tried and rejected`): every rung it lists as dead stays dead.

**The lesson to build on:** the new draw needs an estimand that says precisely WHAT to measure and is
silent on HOW, with a wrong "how" that a strong solver still takes after cleaning the data and reading
every field, code, unit, definition and rule correctly. If stating the estimand precisely names the
method, the draw is dead; test that before you register, not after.

## Stage 1: the re-root draw

Read `CLAUDE.md` and `.claude/authors/sathay3012.md`. Invoke `build-pipeline` (Retirement, re-root),
`fingerprint`, `guide-to-prompt`, `stumping`, `determinism-check`. Then:

1. `guard.py recent`, `coverage`, `suggest`. Same objective (Descriptive & Distribution Analysis,
   `descriptive-distribution`), same task number; the domain, niche and Layer 2 pitfall are new. The
   draw must be bespoke: its pitfall comes from its own data's analytic structure (the data-native
   sentence), from `stumping/references/client/layer2-rigor-patterns.md` learned, never copied, or
   `own:`. One idea the v1 designer surfaced, unchecked by the guard and yours to take or leave: daily
   concurrent large fires, where classifying a fire as large on a given day by its eventual final size
   is a look-ahead error. Weigh it against fresher territory from `coverage`; it keeps the wildfire
   domain, which the guard may or may not like.
2. Before filing, write in the design note the **strongest-solver test**: the cleanest, most careful
   path a top solver takes after reading the prompt (as you would write it) and every file, and show in
   two or three sentences why that path still files the wrong answer. If you cannot write it, redraw.
3. Re-root the card per `fingerprint` Part 2 step 3: move architecture 1's identity into `lineage` with
   its fate ("spent at stage 2: the precise estimand names the overlay, no stump power"), write the new
   draw into the main fields with every required field (`stump_class: analytical`, `analyst_test`,
   `domain_test`, `stump_strategy`, `decisive_rule_filed`, `official_decoy: false`,
   `validated_decoy: false`, `client_domain`, `layer2_family`, `layer2_pattern`, `layer1`, `forum`,
   `forcing_event`, `org_family`, personas via `guard.py names --geo <geo> --seed 254`), then
   `guard.py check` until PASS or WARN answered, and `guard.py register`.
4. Design note: add a `## Architecture 2` part with DRAW (ten lines), Gate G line, stump sentence,
   data-native sentence, the two layers, the three rules, the strongest-solver test, shape and criteria
   arithmetic; one line in `## Tried and rejected` for architecture 1 (the reason above).
5. `pipeline.json`: `architecture` 2, `loops` 0, stage 1, `stump` the new sentence, `domain` the new key,
   `updated` 2026-10-11. Commit and push. This commit must land before stage 2 starts.

## Stage 2: design, in the same run

Then carry out stage 2 exactly as
`/tmp/claude-0/-home-user-real-world-data-extraction-conformation-etl-build-problems/0a4d0be2-5538-5acb-b824-9d9be7c9c38c/scratchpad/brief_stage2.md`
sets it out (ladder, 22-axis closure table, ask sheet with pair arithmetic, deliverables, prompt under
1,000 characters through voice-check, the client's pre-ship check on paper, the stage 3 file plan),
with two standing constraints from architecture 1:
- the rigorous method must be computable with Python, pandas and numpy only (no shapely, geopandas,
  pyproj or GDAL in the solver's sandbox), so no stump is a tool barrier;
- no filed standard may state the decisive method; a stated standard may pin conventions, never the
  step the stump rests on.

If architecture 2 also fails the stage 2 gate, write why in `## Tried and rejected`, update the card's
lineage, set `pipeline.json` accordingly, commit, push, and return; do not draw architecture 3 yourself.

## Return

Under 30 lines: the draw in ten lines (pairing, niche, stump sentence, shape and criteria count,
deliverables, nearest exemplar and its measured mean, guard verdict), the strongest-solver test in two
sentences, then the stage 2 return block from `brief_stage2.md` (ladder, prompt text with character
count and voice-check verdict, asks, deliverables, gate counts, open items, commit hashes).

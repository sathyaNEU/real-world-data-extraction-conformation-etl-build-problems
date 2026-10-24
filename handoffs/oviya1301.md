# Pickup: oviya1301, ETL lane (paused 2026-10-12)

Everything was stopped on the author's instruction. No agent is running, and each build's work in
progress is committed and pushed on its own branch. This file says where each build stands and what
the next session does first. Delete it once the work has resumed and it stops being true.

## Resume in this order

1. Read `CLAUDE.md`, `.claude/authors/oviya1301.md`, then this file.
2. The author has new instructions. Take those first; nothing below runs until the author says so.
3. When told to resume, give each build its own worktree from a fresh clone:
   `git worktree add ../wt-task445 oviya1301/task445-hardening` and
   `git worktree add ../wt-task447 oviya1301/task447-organic-deposit-growth`.
   Each build then reads its `DESIGN_NOTE.md` (`## Tried and rejected` first), `pipeline.json` and
   `solver_rounds/`. The old container's worktrees, `/home/user/scratch-hold` briefs and
   `/home/user/results` round folders are gone with it; everything they held that matters is committed
   or written below.

## Lane state

| Task | Status on main | Branch, head | Stopped at | Next |
|---|---|---|---|---|
| task446 | reshipped 2026-10-15 | main | the client returned it on the 10/10 rule-application rule (CRM-07 5.2 filed the model and the leave-one-cohort-out selection); repaired by perssathya at the author's request: 5.2 files the estimand only, the data forces the basis, prompt.txt, pairing to Forecasting; caseload 133 and every figure unchanged; judge DETERMINISTIC, APPROVE | wait for the author's portal re-test |
| task445 | in build | `oviya1301/task445-hardening`, b7981df (WIP on the loop 2 design 647a2c5) | stage 3, loop 2 builder stopped mid-build | finish the build, leak reader, round 4, judge, ship |
| task447 | in build | `oviya1301/task447-organic-deposit-growth`, d59cc9c (WIP on the built pack 19c3127) | stage 2, ask-layer designer stopped early | finish the ask design, build, leak reader and clone pre-flight, round 1, judge, ship |
| task448, task449 | open | none | not started | the author's rule starts the next lane task when one ships; on hold until the author says |

PR #49: https://github.com/sathyaNEU/real-world-data-extraction-conformation-etl-build-problems/pull/49.
Status artifact (`builds` collection): https://claude.ai/artifact/U4syUnRUycHUsWwhonBYoQ, not updated for
the pause.

## task445: 13F institutional ownership flags (Quantitative Finance)

How it got here:

- Portal round 1 (2026-10-11): average 52, determinism failed (answer_contradicts_files: OM-4 s.2's
  "managers that file", read literally, flagged only WHII and JEMS, and 128 against 125 managers to
  carry was unpinned).
- Fix in the pack: OM-4 s.2 files the estimand literally (every manager with a holdings or combination
  report for the period, plus every prior-period filer with no 13F notice for this one, holdings not
  yet filed estimated) and a selection criterion (the basis that, run on the previous period with only
  the reports filed by the same lag, comes closest on everything since filed; closeness is the largest
  difference in points across the flag file's securities). s.3 leaves put and call lines out; s.8 names
  layout v4.
- Loop 1 (type-change completion): round 2 missed on a flat carry; round 3 landed on the type-pooled
  ratio (proxy 52.3) while the asks held (18 per cent of ask weight, 0 of 4 items). Logs:
  `task445/solver_rounds/round-1.md` to `round-3.md`.
- Ask layer (a78cb74): Ask A, September ownership per name (primary device DV-1, same-day amendments
  whose numbers run against file order); Ask B, the September bridge chart (primary device DV-2, header
  period June against cover page September, Selwood 0000950123-22-001007); hazard DV-3, the January
  option-only amendment.
- Loop 2 design (647a2c5, written up in `DESIGN_NOTE.md`): index sponsors hold a fixed slice of each
  company, so their shares follow each name's own share count (OTF's October follow-on, +4.6 per cent).
  Golden: each sponsor still due is grown by its filed peers' change in that name, every other type flat,
  which flags WHII, GLI, OTF, JEMS and SAF. Stump: the type-pooled change (round 3's basis) flags WHII,
  GLI, JEMS and SAF, with OTF about 79.2. precut exit 0, pair ceiling 35.0. The guard's `ban.forum`
  BLOCK against task228 v2 was forced (a registration-order artifact, noted in `pipeline.json`).

Where the builder stopped (b7981df):

- Done: sim.py share-count tracking and the late passive filers; world.py `GROW = 1.055`; golden.py
  `STAKE_BASES` and `window()`; checks.py's literal-reading block, with the rival margin measured
  against the golden basis; verify.py's estimate; the make.py and maincall.py figures;
  `generator/main_call_ref.json` re-snapshotted for loop 2.
- The snapshot matches the design: December ownership WHII 88.60, GLI 84.42, OTF 80.40, JEMS 84.80 and
  SAF 91.40 flagged, FENN 79.59 not; the sponsors-pooled rung puts OTF at 79.16.
- Red: `make.py` stops in checks.py (line 347), the DV separation assert, `September W04 0.034 under
  ('cover', 'latest', 'all', 'correct', 'correct', 'correct', 'correct', 'oct')`, which needs at least
  0.06 points and another rounding bin. The builder was about to grid-search `DV1_T` and `DV2_O` (per
  issue, in sim.py) so that every non-golden device combination stays 0.06 points or more off the golden
  on the touched names while the stop rows S1 to S4 stay in range. The search script lived in the
  scratchpad and is lost; write it again.
- Check while there: the golden's September figure for HAMR moved from 49.1 to 52.5 under the WIP sim.
  Confirm it is the intended share-count move, not a bug.
- Not done: submission.md and figures.json, `figures_check.py`, golden-realism on
  `sep_quarter_bridge.png`, `verify.py`, the byte-identical rebuild, `leak.py`, `guard.py surface`,
  `precut.py`, target.zip, and the loop 2 build record in `pipeline.json`.

Next, in order:

1. A fresh builder (Opus, medium) from b7981df finishes the loop 2 build to those gates. The main call
   must reproduce `main_call_ref.json`. Commit and push.
2. The leak reader (Sonnet, medium) on the rebuilt pack, alongside `guard.py heart`. Fix leak-level
   findings only and defer the rest.
3. Solver round 4 (`/solve`, sandbox under `/sbx/`). `grade.py` exit 0 passes. Exit 2 means hardening
   loop 3, the last this architecture gets. Exit 3 means the ask layer is rebuilt.
4. The judge rehearsal, in the background (determinism-check, "Running the judge rehearsal").
5. Ship: a PR to main, commit `SHIPPED (task445): <call>`, then the next lane task.

## task447: APCD notice review (Healthcare Delivery & Health Economics)

- Call: notice N25-014 (Ledgestone Health buying Brightwater Medical Group) goes on to a cost and market
  impact review. The 2026 commercial spending increase is about $2.2M against the $2.0M threshold.
- Stump: solvers measure referral capture on Ledgestone's earlier purchases (pooled, by carrier or by
  product; Bayfield Value Tier patients never moved), project about $1.6M and close the review. In fact
  capture follows each patient's tier for the acquirer (Norbridge's 2024 re-tiering of Wolf River moved
  its Tiered EPO patients), and Bayfield places Ledgestone in its first tier from 2025, which gives
  $2.2M. The records force the method (no filed back-test, so this build does not repeat task445's organ).
- Built at 19c3127 (stage 3 gates green, `leak.py` REVIEW with no LEAK). precut fails two rows: the pair
  ceiling (72 against 40) and the cracker sheet. The old asks split the committed increase, follow the
  main calculation, and filed appendix rules A2, A4 and A5 settle them.
- WIP d59cc9c: prompt.txt asks for the call and the 2026 increase in `N25-014_preliminary_review.pdf`
  with the review's two market exhibits:
  - the 2024 commercial imaging, endoscopy and arthroscopy services that Manitowoc and Kewaunee
    residents received, by county and line (12 cells), with the share Brightwater's physicians referred;
  - the shares of the two counties' 2024 commercial office visits billed by Brightwater and by
    Ledgestone in primary care, gastroenterology, orthopaedics and cardiology (8 cells).

  The design note's Shape row says the same. Not done: the cracker sheet, the devices, the ask sheet,
  the hazards, the referee, the pair ceiling, the builder's instructions, voice-check and precut. The
  pack, the golden and the submission still carry the old asks.

Next, in order:

1. A fresh ask-layer designer (Opus, max) from d59cc9c, on the brief below. precut exit 0, then commit
   and push.
2. A builder (Opus, medium) for the new ask layer, with the main call asserted byte-identical.
3. The leak reader with `guard.py heart` and the clone pre-flight, solver round 1, the judge, ship.

The ask designer's brief, in short:

- Read the full supplemental-stumping skill, determinism-check §1 and §2, and the design note
  (`## Tried and rejected` first).
- Keep fixed: the main call, the ladder, the filed estimand, the method the records force, and the main
  call's rows and figures (asserted byte-identical).
- Design:
  - The cracker sheet first: the response that lands the call, runs the hygiene battery and executes
    every filed rule must miss every ask figure, outside its bin.
  - Asks decoupled from the call. No split of the committed increase, no after-cells that follow the
    main calculation, no chart ordered or titled on the decision quantity.
  - One silent primary device per ask, forced by the records and adjudicated by no filed sentence.
    Remove or neutralise appendix rules A2, A4 and A5, or move those devices to hazards.
  - No marker and one referee per ask; eight files and ten to fifteen columns per ask; three to five
    asserted stops per ask; pair ceiling at or under 40 on paper.
  - No ask golden that a filed sentence, read literally, contradicts.
- Deliver: the note updated in place, with one `## Tried and rejected` line for the old ask layer;
  prompt.txt through voice-check; `pipeline.json` at stage 2; precut green. Then commit and push.
- Don't run: data cuts, leak readers, solvers, the clone check or the judge.

## Operating notes for this lane

- Builders work only in their own worktree. They invoke skills as the routing table in `CLAUDE.md`
  says, hold the stage gates in `build-pipeline`, never run a reader, solver, clone check or judge,
  commit and push before stopping, and report in under 300 words.
- voice-check inside a worktree:
  `python3 .claude/skills/guide-to-prompt/references/voice-check.py --file task445/prompt.txt --task task445`.
  The bare task-number mode matches `wt-task445` in the path and maps every folder to 445.
- Revert the tracked caches before any commit (`.claude/skills/clone-check/.cache/fingerprints.json`,
  `.claude/skills/fingerprint/.cache/people.json`), and take main's side when they conflict in a merge.
- The determinism-judge agent has no Agent tool in this runtime. The main session writes the judge
  brief (the judge prompt verbatim, the submission's grounded blocks, a fresh unzip under
  `/tmp/determinism-check-*`) and spawns one general-purpose thread itself, with the literal reading
  first.
- Solver sandboxes go under `/sbx/`, never the scratchpad, which builders fill with their own scripts.
- Leak readers have twice claimed that task445's CUSIP 359Y60106 fails its check digit. It passes.

## task482

At stage 4 of architecture 12 (drawn 2026-10-24): the Quillmere Lake basin's 2026 peak-season populations for the 2027 Seasonal Communities Aid, each city's population present in its busiest month read through its plant's influent BOD load per person, calibrated on January to April 2026. precut.py exit 0 (51 checks), checks 82 of 82, verify 26 of 26, two byte-identical rebuilds (zip be45d7b75ea5cc24). Resume from `task482/pipeline.json` (stage 4: readers and judge).

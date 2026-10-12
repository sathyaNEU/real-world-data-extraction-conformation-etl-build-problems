# Clone check: pre-flight, task445 (hardening loop 1) against every other build, 2026-10-11

## Verdict
CLEAN of Template, Dataset, Same seed and Exact. task445 against task181 is clean and shares components. The one open item is a Part 6.1 consecutive ban on `stump_strategy` (forecast_method_backtest) between task445 and task446, both in flight. It is a strategy repeat, not a repeated driver.

## Scope and coverage
- Mode: pre-flight on task445 against every other build, window ignored (`screen --focus task445 --all`). Worktree /home/user/wt-task445 at f5ca187.
- Extract: `fingerprint.py extract` was written to a scratch file, not the tracked cache. It found 20 builds on disk with a prompt or target (task117 to task133, task181, task229, task445). All 20 had a fingerprint card.
- Screen: 19 pairs in scope, **0 promoted**. Nearest neighbours were task181 (surface pct 85, gap 1.00, pattern 0.00), task130, task131, task132, task229 (decision family yes) and task117 (gap 1.00, pattern 1.00). None crossed a promotion route, and none had a hard tell.
- Mechanism layer beyond the screen: `guard.py heart` and `nearest` were run on task445 against all 136 cards on file, their lineage rows and the ledger rows. Of those cards, 126 have a design-note mechanism, 5 are ledger-seeded (back-fitted) and 5 are submission_only (Track A only). Builds task1 to task116 have cards but no folders in this worktree, so they were checked on Track B through their cards and **not on Track A**.
- In-flight siblings: the task446 and task447 cards were read from /home/user/wt-task446 and /home/user/wt-task447, read-only, and run through `guard.py check` against this corpus. Their prompts were read by hand. Their packs were not fingerprinted, because neither is in this worktree and task447 has no target yet. **task445 against task446 and task447 is therefore Track A by reading only, not by screen.**
- Adjudicated: no pair was promoted. On the caller's instruction, five pairs were read directly from cards and design notes: task181, task107 v4, task446, task447, and task130 v1 (dead row). **No adjudicator subagents were spawned**, because this run had no Agent tool. The reading was done in this thread from cards, prompts and design-note ladders, and no answer keys or golden figures were read beyond the ladder tables.
- Left unread: none of the promoted pairs (there were none).

## In batch against earlier builds
- **task181** (another author's build). The ledger has no row for task181, so its delivery status is **unknown on the ledger**. Its card records judge APPROVE (pass 2), and the caller reports it shipped, so it is weighted here at exclusion level. Verdict: clean, shares components (see below). No Track A hit: the screen surface sits at pct 85, there are no shared names, files, schemas or deliverable species, the decisions differ (pick one of N against a designation set) and the opening moves differ.
- **task107 v4** (ledger: the author reports the main call stumped and determinism passed; delivery not recorded). Verdict: clean, shares components (see below).
- **task130 v1** (failed on the portal, retired; a dead row). Its lineage driver built holdings at a future date forward from a past snapshot of filed returns. It touches only a retired row and is not the same claim, so it is recorded as history and nobody is sent to redraw it.

## Track A findings, reviewer visible
None. The screen promoted nothing. The prompt is 986 characters with a question-first opening, and the voice check flags nothing against the 12-build batch. task445 (csv + png, a 13F flag file and a waterfall) shares no file name, schema, invented name or person with task181, task446 or task447. The people.last WARN for Henderson against task117 (older) was already answered in the design note.

## Track B findings, mechanism
1. **task445 against task446: Part 6.1 consecutive ban on stump_strategy.** Tier: standing-ban hit, not Template, because the drivers differ (see Clean below). Both builds are in flight, neither is approved, and both were drawn on 2026-10-11.
   - The shared item is the strategy: a filed estimand plus a filed back-test criterion that selects an estimation basis without naming it, with the natural basis losing that back-test.
   - Position in each path: in task445 the back-test selects between R4 (flat carry) and R5 (per-type drift). In task446 it selects between the pooled yield and the error-rate basis. In both builds the strategy carries the decisive rung.
   - Timing: task446 v2 registered forecast_method_backtest at 17:36. task445 adopted it at 19:58 in hardening loop 1 (card commit fc92bea). It had been maturity_censoring before. task446 then took on the same filed-estimand-and-selection-test repair in its own loop 1, citing task445's portal failure.
   - Where the BLOCK lands: run here, `guard.py check` on the task446 card BLOCKs `ban.strategy` against task445, because same-day draws sort by task number. Neither card was on main when the other drew.
   - Axis to redraw: stump_strategy on one of the pair.
   - Data: if task445 is the one redrawn, the data does not survive, because the back-test table and the September-window calibration are the strategy.
2. task445's own `ban.forum` BLOCK against task228 v2 is a registration-order artifact. It is already answered on the card with `register --force` (task445 at 15:47, task228 v2 at 16:21). It is recorded here and is not a new finding.

## Clean, shares components by design
- **task445 against task181 (the caller's question).**
  - task181's decisive move, domain nouns stripped: a count read before its records have all arrived is completed with each unit's own arrival-delay distribution, so how much of the period is still missing comes from each class's own route.
  - task445's decisive move: the reporters still missing are known exactly. Their last report is a stale value for the class whose holdings drift at a common rate every period, so each missing reporter is moved by the drift its own class shows among peers that have reported. A filed back-test selects that basis over flat carry.
  - The two are different claims. One is completeness (how much has not arrived). The other is the value of a known missing unit (what it holds now).
  - Ordered paths. task181: arrived count, protocol excess on arrivals, ratio, pooled-delay nowcast, route-specific nowcast (answer). task445: reports on file (R0), last quarter (R1), aggregate completion shares (R2, R3), per-reporter completion from own last report (R4, the stump filed), one pooled rate (R4b), per-type drift (R5, answer).
  - The move that was task181's answer, completing unit by unit rather than by one pooled share, is also task445's original driver. It now sits at R4, the wrong answer the solver files. That is a demotion, so it is reuse.
  - Shared component that remains: the final step in both builds is to stratify a correction by class instead of pooling it (task181 R3 to R4, task445 R4b to R5). In task445 that step is the second half of the decisive move, not what the stump rides on: the solver stops at flat carry because it wins the back-test against every aggregate basis.
  - Minor exposure to note: the tail of task445's card driver ("any single rate for every missing reporter misplaces...") echoes task181's ("not on an arrival speed pooled across units"). This is a component echo and not a finding.
- **task445 against task107 v4.** Both stump on a per-unit carry-forward that a subgroup's change makes stale.
  - task107's driver is a dated, discrete step: an entry rate lifts at a service anniversary that falls just before the window. The decisive question is when, and every carry route reproduces every closed period, so no back-test separates them.
  - task445's driver is a continuous drift at a common rate, measured on filed peers in the same open period, and a filed back-test does separate the bases.
  - Shared component: the case against carry-forward. Different driver: the timing of an event against a forward window, versus the class-specific drift of a reporter that is known to be missing.
- **task445 against task446.** Different drivers. task446: a screen's yield does not travel across a moved base rate, while its error rates do. task445: last reports go stale for a drifting class. They share the strategy (Track B item 1), objective etl, gate_g method_or_model_selection, gaps time and population, and a data-plus-chart deliverable pair (csv + png against xlsx + svg). That is several outline features in common, which makes it a soft Shape echo. It is not a Template.
- **task445 against task447.** Both carry G14, a rate conditioned on a class rather than pooled, chosen by a filed criterion that names no model.
  - task447's driver is the conditioning variable being reset for the forward period, so the history has to be transported across a new mix.
  - task445's driver is the staleness of a last observation for a drifting class inside an open period.
  - Shared component, different driver.

## Strategy monoculture
- Last 12 by draw order ending at task445 (task129 to task445): no strategy appears more than twice. forecast_method_backtest is 2 of 12 (task130 v3, task445), maturity_censoring 2 of 12 (task134, task181), causal_design 2 of 12 (task131, task230). Official decoy: 0. validated_decoy: 1 (task129). All are under the caps.
- Window of 12 ending at task447 (with task446 and task447 in flight): forecast_method_backtest is 3 of 12 (task130, task445, task446), under the cap of a third (4). Read by construction rather than label, the filed estimand plus a filed basis-selection criterion that names no basis is carried by task445, task446 and task447 back to back (task447 is labelled composition_mix but its decisive_rule_filed note describes the same organ). That is 4 of 12 with task130 v3, one short of the cap, and all three of the latest builds in a row.

## Corpus habits
- The deliverable pair xlsx + docx appears in 2 of the 20 builds on disk (screen). There is no Code deliverable anywhere in the voice-check batch.
- The last three builds in flight (task445, task446, task447) are all objective etl with gate_g method_or_model_selection. The guard reports Gate G mechanism overuse at 5 of the last 12.
- 10 of the 12 prompts in the voice-check batch are at or over the 1,000-character ceiling. task445 (986) and task181 (849) are under it.

## What to redraw
1. task445 / task446, stump_strategy: the forecast_method_backtest consecutive ban (the guard BLOCK lands on task446). Settle it before either build ships.

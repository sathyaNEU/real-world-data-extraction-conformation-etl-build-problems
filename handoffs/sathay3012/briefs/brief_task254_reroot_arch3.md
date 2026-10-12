# Brief: task254 re-root, architecture 3 of 3 (stage 1 draw, then stage 2 design to precut.py exit 0)

You are the designer (Opus, max effort). Worktree:
/home/user/real-world-data-extraction-conformation-etl-build-problems/.work/wt254 (branch
`sathay3012/task254-fire-planning-bands`, main merged in, at f847d14). Work only there; scratch under
`/home/user/real-world-data-extraction-conformation-etl-build-problems/.work/notes/agent-scratch/task254-arch3/`,
never under /tmp. Commit and push on this branch only (retry 2s/4s/8s/16s), every message ending with:
```
Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_0142Jt4Mt622iBfGoK24ivCU
```
Revert `.claude/skills/fingerprint/.cache/people.json` before each commit. No em dashes. The branch keeps its
old slug. You never cut data. **This is the last architecture this task number gets**: if it cannot pass the
gate honestly, the number is retired, so spend the effort on the draw, not on the paperwork.

## Why architectures 1 and 2 are spent (read the design note's `## Tried and rejected` first)

1. Architecture 1, fire planning bands on burned area apportioned by footprint: the precise estimand ("acres
   burned on state-protected land") names the overlay, so a strong solver walks to the golden.
2. Architecture 2, Lyrevo RMP monitoring windows from a right-truncated post-marketing case series: under
   main's literal-determinism rule the filed estimand, executed word for word, gave the stump's month (16), so
   the stump was a reading of the population term (a fork); refiled to include reactions not yet begun, every
   correction a solver reaches for (mature cohorts from 480 days, reweighting, the product-limit estimator)
   files the golden (20), so no stump is left; and its asks failed the cracker (pair ceiling 70.1).

The sibling build task253 has had the same experience (its voucher architecture collided with task230, and its
crossing-criticality redraw had no stump once the assignment rule was filed); its architecture 2 is being
drawn now on `sathay3012/task253-rent-relief-closeout`, and its card is registered there before you start.

## Lessons that bind this draw (main's current spec: `CLAUDE.md`, `stumping`, `determinism-check`, `supplemental-stumping`)

- **Literal determinism.** The estimand (population including members not yet observed at the as-of date,
  outcome, window, unit, comparison) is filed so its literal execution is the golden; no filed rule gives
  another answer read literally; the stump lives in how the stated quantity is computed. A precise estimand
  that a careful reader computes correctly by reflex has no stump; neither does a quantity that is a mechanical
  procedure once filed. The decisive step must be a computation a competent analyst gets wrong while executing
  the literal estimand in good faith, with the pack's own structure letting an expert get it right.
- **Test before you register**: write the literal estimand, execute it step by step as a strong model would
  (the default path, ending on a named figure that is not the golden), then the strongest-solver test (the
  most careful path, including the reflex corrections a strong model reaches for, and why it still misses). If
  the reflex correction lands the golden, the draw is dead: that is exactly how architecture 2 died.
- **Dead or banned families for this slot or the batch**: footprint apportionment (this slot's v1); right
  truncation and maturity censoring of time to event (this slot's v2, task134); stand-in pools reweighted or
  matched within the class driving selection and outcome (task230, task253 v1); grain or unit of count
  (task229); population selection (task228); a base rate backed out of a screen's error rates and a filed
  back-test organ (task446, never in consecutive builds); a model or formula re-run (task253's redraw); and
  whatever task253's architecture 2 card and the pooled guard block.
- **Learn from what shipped under the new spec**, as method only: read the design notes of the builds main
  carries that passed `precut.py` after the rule change (for example task446 and task445; check
  `git log origin/main` for others), to see how their estimand was filed, how their default path ended on a
  wrong figure and how their asks beat the cracker. Never copy a driver, a device, a dataset structure or a
  wording: the clone check reads the driver, and a repeated driver is a Template.
- **The pooled guard is mandatory**: export every in-flight card on other branches read-only (task253's from
  its own branch) into a temporary folder with main's cards, point `FINGERPRINT_CARDS` at it for `recent`,
  `coverage`, `check` and `heart`, run `register` without it, delete the folder.
- **The ask layer is designed against the cracker**: the response that landed the call, ran the hygiene
  battery and executed every filed rule misses every ask figure; no device adjudicated by a filed rule, a
  marker or a referee that ties only under the golden; pair ceiling at or under 40; the ask gate fails a round
  where a solver that missed the call still keeps 35 per cent of the ask weight.
- **`prompt.txt`**: one paragraph, question first, under 1,000 characters, the ten rules; `voice-check.py`
  exit 0.
- Same objective (Descriptive & Distribution Analysis), same number; the domain is free (prefer fresh
  territory from `coverage`). Bespoke: the pitfall comes from the data's own analytic structure. The current
  pack (Lyrevo) is dead; reuse nothing unless the new design genuinely needs a piece of it.

## Stage 1 (draw) and stage 2 (design), in this run

Invoke `build-pipeline` (Retirement, re-root; stage 1 and 2 rows; Models and effort), `fingerprint`,
`guide-to-prompt`, `stumping`, `determinism-check`, `supplemental-stumping`. Then:

1. Draw, pooled guard, the literal estimand, the default path and the strongest-solver test written and
   tested, then re-root the card (architecture 2 into `lineage` with its fate beside architecture 1; the new
   draw in the main fields; every required field; personas from `guard.py names --geo <geo> --seed 254`
   checked against the pooled corpus), `check` until PASS or WARN answered, `register`. Commit and push.
2. Rewrite `task254/DESIGN_NOTE.md` for architecture 3 in the H2 sections `precut.py` reads (Draw, Default
   path, Stump sentence, Three rules, Readability screen, Semantic fork table, Ladder of 3 to 5 rungs,
   Closure table with all 22 axes, Literal reader, Oracles, Ask sheet with `Pair ceiling:` and the cracker
   sheet, Tried and rejected append-only with the earlier architectures' lines kept), plus `## Builder brief`
   written so a fresh builder replaces the dead generator and pack without you. If precut checks SF ids
   against the dead `generator/checks.py`, say so in the builder brief rather than editing the dead generator.
3. Write `task254/prompt.txt` and delete `task254/prompt.md`.
4. `python3 .claude/skills/stumping/precut.py 254` exit 0 (WARNs answered in the note).
5. `pipeline.json`: architecture 3, loops 0, stage 2, stage_name "design (re-root, architecture 3)", `stump`,
   `domain`, `updated` 2026-10-11. Commit and push.

If architecture 3 cannot pass the gate honestly, write why in `## Tried and rejected`, update the card lineage
and `pipeline.json` (stage `retired` is the main session's call, so leave it at stage 2 with the reason),
commit, push and return.

## Return

Under 30 lines: the draw in ten lines (pairing, niche, literal estimand, default path's last step and figure,
golden, stump sentence, shape and criteria count, deliverables, nearest exemplar and measured mean, pooled
guard and heart verdicts), the strongest-solver test in two sentences, the ladder, the ask sheet with the
cracker's result and the pair ceiling, the prompt.txt text with character count and voice-check exit,
precut's final line, the builder brief in five lines, and the commit hashes.

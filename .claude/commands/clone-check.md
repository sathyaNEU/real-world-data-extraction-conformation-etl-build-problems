---
description: Run a clone/template/duplicate check across the shipped task corpus, or one build against it as a pre-flight. Fingerprints every build, screens every pair, adjudicates the promoted ones, and writes clone_check_report.md.
argument-hint: <nothing for the last 15 builds, or taskNN for a pre-flight, or "last 8" / "through task47" / "all">
---

# /clone-check

Run **exactly one** clone check over the builds named in `$ARGUMENTS`.

Resolve the argument first. **Empty means the default batch, which is the last 15 builds ending at
the newest one**, so a run made while task50 is current covers task36 through task50. A bare number
or `taskN` means pre-flight mode on that build against every other, ignoring the window. A count
(`last 8`) resizes the window, `through taskNN` moves its end point, and `all` drops it. The agent
reports the range it resolved to. Do not guess a scope from recent context.

Then spawn the `clone-auditor` agent with a single `Agent` tool call:

- `subagent_type: clone-auditor`
- The prompt must state plainly that **this is the `/clone-check` slash command invoking it**, must
  give the repo root, and must give the resolved scope and mode.
- If a report already exists for that scope, say so and give the pass number, so the agent writes a
  numbered report rather than overwriting the earlier one.

Spawn one agent and only one. The funnel (mechanical fingerprinting, the corpus baseline screen,
per pair adjudication), the window semantics, the two tracks, the tier ladder, the exclusions and the
report structure all live in `.claude/agents/clone-auditor.md`. Do not restate any of it here and do not improvise around
it.

When the agent returns, relay its verdict line, the finding counts by track, and the report path. Do
not apply a redraw, do not edit the shipped ledger, and do not soften a tier.

**This command is author triggered only.** Never invoke it on your own initiative, including right
after finishing a build that looks like it wants checking. It reads the whole corpus and spends real
adjudication tokens, so the author decides when that happens.

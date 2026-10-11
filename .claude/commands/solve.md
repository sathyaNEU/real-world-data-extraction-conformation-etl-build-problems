---
description: Run an in-house solver round on a built task before the judge and the portal (stage 6 of /build, or on its own). One isolated solver works the task in a sandbox holding only the prompt and the bundle, returns its committed call and every ask figure, and grade.py scores it against submission.md. The round passes when the solver does not commit to the main call.
argument-hint: taskNN [--label "..."]
---

# /solve

Run one solver round on the task named in `$ARGUMENTS`. Resolve a bare number or `taskN` to
`taskN/` at the repository root (the folder holding `CLAUDE.md`); if nothing is named, ask and stop.
The round number `k` is one more than the rounds already recorded in `<task>/pipeline.json`.

1. **Invoke the `solver-round` skill.** The solver, the decision rule and the isolation rules come
   from it; do not restate them from memory.
2. **Refuse an unfinished build.** `submission.md` must exist with a block 4, and every file the
   prompt names must be in `<task>/` or `<task>/golden/`. If `leak_check_report.md` reads LEAK, say
   so and stop, because a solver reading a leak measures nothing.
3. **Make the sandbox** with Bash: `S=<scratchpad>/solve-<task>-<k>`; copy `prompt.md` to
   `$S/prompt.md`; unzip `target.zip` (or copy `target/` when there is no zip) so the bundle sits at
   `$S/target/`; a zip that extracts flat has its files moved under `target/`. Create `$S/work/` for
   the solver's scripts. Nothing else goes under the scratchpad: no earlier round's copy, no result
   file, no design or grading notes (results and notes live outside it).
4. **Spawn one isolated `Agent`** of type `Explore` (it carries no repository instructions) with
   `model: opus` and `effort: high` (high, not max), with the spawn prompt below, `S` and the
   deliverable file names filled in. Pass the model explicitly, because an `Explore` agent otherwise
   runs on its own default model. One agent needs no Workflow script.
5. **Write the solver's JSON** to a results folder outside the scratchpad and grade it:
   `python3 .claude/skills/solver-round/grade.py <task> <results>/solver.json --label "round k"`.
6. **Read the main-call sentence yourself** in `solver_rounds/<label>.md`. Where the token match
   says LANDED for a wrong set, or missed for a right one phrased differently, re-run `grade.py` with
   `--landed no|yes`.
7. **Report**: the proxy score, landed or missed, the asks cracked, and the path step at which the
   solver left the ladder (read the path against the design note's rungs; this is the one place the
   main thread opens the design note in this command). Then the decision: **pass** when the solver
   did not commit to the main call, **harden** (with the hardening brief in one sentence) when it
   did, or re-root when the architecture is spent; and the round's row in `pipeline.json`
   `solver_rounds`.

Run on its own, this command reports and stops; the hardening is the pipeline's next stage-2 pass.
Inside `/build` the pipeline carries on from the decision. Do not run the determinism judge or the
clone check from here.

## Spawn prompt

```text
You are the analyst this request was sent to. The request is at S/prompt.md and the folder it
refers to is S/target/. Those are the only locations you may read; do not open anything else on
this machine, do not use web tools, and do not spawn agents. The files are the universe: a fact
absent from the folder does not exist for this work. Read the request, do the analysis with Python
(pandas is available; write scratch scripts under S/work/), reconcile against whatever the folder
lets you reconcile against, and commit to one answer for the main request and one value for every
figure each deliverable asks for, in the unit and rounding the request states. You are not
producing the files themselves; return the figures they would carry. Deliverables requested:
<file names>. End your reply with one JSON object matching the schema below, and nothing after it.
```

Schema, appended to the prompt:

```json
{"type": "object",
 "properties": {
   "main_call": {"type": "string", "description": "the committed recommendation in one sentence, naming every entity and figure it rests on"},
   "deliverables": {"type": "array", "items": {"type": "object", "properties": {
     "file": {"type": "string"},
     "answers": {"type": "array", "items": {"type": "object", "properties": {
       "ask": {"type": "string", "description": "the ask, in a few words"},
       "value": {"type": "string", "description": "every figure the ask owes, each with its name, unit and the rounding the prompt asked for"}},
       "required": ["ask", "value"]}}},
     "required": ["file", "answers"]}},
   "path": {"type": "array", "items": {"type": "string"}, "description": "the ordered steps actually taken, each naming the files, joins, filters and rules used and the intermediate figure it produced"},
   "confidence": {"type": "string"},
   "notes": {"type": "string", "description": "anything the files left open, in one or two sentences"}},
 "required": ["main_call", "deliverables", "path", "confidence"]}
```

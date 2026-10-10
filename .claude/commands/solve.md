---
description: Run an in-house solver round on a built task before the portal. One plain solver by default; "2" runs plain and skeptic together. Each solver sees only the prompt and the bundle, returns its committed call and every ask figure, and grade.py scores it against submission.md.
argument-hint: taskNN [1|2] [--label "..."]
---

# /solve

Run one solver round on the task named in `$ARGUMENTS`. Resolve a bare number or `taskN` to
`taskN/` at the repository root (the folder holding `CLAUDE.md`); if nothing is named, ask and stop. The second
argument is the number of solvers: `1` (default) runs the plain lens, `2` runs plain and skeptic
together. The round number `k` is one more than the rounds already recorded in `<task>/pipeline.json`.

1. **Invoke the `solver-round` skill.** The lenses, the decision rule and the isolation rules come
   from it; do not restate them from memory.
2. **Refuse an unfinished build.** `submission.md` must exist with a block 4, and every file the
   prompt names must be in `<task>/` or `<task>/golden/`. If `leak_check_report.md` reads LEAK, say
   so and stop, because a solver reading a leak measures nothing.
3. **Make the fresh scratch copy** with Bash: `S=<scratchpad>/solve-<task>-<k>`; copy `prompt.md`
   to `$S/prompt.md`; unzip `target.zip` (or copy `target/` when there is no zip) so the bundle
   sits at `$S/target/`; a zip that extracts flat has its files moved under `target/`. Create
   `$S/work/` for the solver's scripts.
4. **Run the solvers through the Workflow tool** with the script below, filling `SCRATCH`, `N` and
   the file names the prompt asks for. This command is the author's opt-in to the workflow. The
   plain lens uses `agentType: 'Explore'`, which carries no repository instructions; the skeptic
   uses the default agent type.
5. **Write each solver's structured result** to `$S/<lens>.json` and grade it:
   `python3 .claude/skills/solver-round/grade.py <task> $S/<lens>.json --label "round k, <lens>"`.
6. **Read both main-call sentences yourself** in each `solver_rounds/<label>.md`. Where the token
   match says LANDED for a wrong set, or missed for a right one phrased differently, re-run
   `grade.py` with `--landed no|yes`.
7. **Report**: per solver, the proxy score, landed or missed, asks cracked, and the path step at
   which it left the ladder (read the path against the design note's rungs; this is the one place
   the main thread opens the design note in this command). Then the decision under the skill's
   rule: pass, harden (with the hardening brief in one sentence), or re-root.

Do not harden in this command. Do not run the determinism judge or the clone check from here.

## Workflow script

```javascript
export const meta = {
  name: 'solver-round',
  description: 'Independent in-house solve of one built task, plain and optionally skeptic lens',
  phases: [{ title: 'Solve' }],
}
const S = args.scratch          // absolute path holding prompt.md and target/
const N = args.n || 1
const files = args.deliverables  // the file names the prompt asks for, e.g. ["x.xlsx", "y.png"]
const SCHEMA = {
  type: 'object',
  properties: {
    main_call: { type: 'string', description: 'the committed recommendation in one sentence, naming every entity and figure it rests on' },
    deliverables: { type: 'array', items: { type: 'object', properties: {
      file: { type: 'string' },
      answers: { type: 'array', items: { type: 'object', properties: {
        ask: { type: 'string', description: 'the ask, in a few words' },
        value: { type: 'string', description: 'every figure the ask owes, each with its name, unit and the rounding the prompt asked for' },
      }, required: ['ask', 'value'] } },
    }, required: ['file', 'answers'] } },
    path: { type: 'array', items: { type: 'string' }, description: 'the ordered steps actually taken, each naming the files, joins, filters and rules used and the intermediate figure it produced' },
    confidence: { type: 'string' },
    notes: { type: 'string', description: 'anything the files left open, in one or two sentences' },
  },
  required: ['main_call', 'deliverables', 'path', 'confidence'],
}
const base = `You are the analyst this request was sent to. The request is at ${S}/prompt.md and the folder it refers to is ${S}/target/. Those are the only locations you may read; do not open anything else on this machine, do not use web tools, and do not spawn agents. The files are the universe: a fact absent from the folder does not exist for this work. Read the request, do the analysis with Python (pandas is available; write scratch scripts under ${S}/work/), reconcile against whatever the folder lets you reconcile against, and commit to one answer for the main request and one value for every figure each deliverable asks for, in the unit and rounding the request states. You are not producing the files themselves; return the figures they would carry. Deliverables requested: ${files.join(', ')}. Return your result as the structured output; put nothing else in your final text.`
const lenses = [
  { lens: 'plain', agentType: 'Explore', prompt: base },
  { lens: 'skeptic', prompt: base + ` One working rule: where the folder publishes prior figures produced by the same process (last year's table, certified cells, settled cases), treat reproducing every one of them exactly as the test of your method, and do not report on a method that misses any of them.` },
].slice(0, N)
phase('Solve')
const results = await parallel(lenses.map(l => () =>
  agent(l.prompt, { label: `solve:${l.lens}`, phase: 'Solve', schema: SCHEMA, effort: 'high', agentType: l.agentType })
    .then(r => ({ lens: l.lens, result: r }))))
return results.filter(Boolean)
```

Pass `args` as a JSON object: `{"scratch": "<S>", "n": 1, "deliverables": ["..."]}`.

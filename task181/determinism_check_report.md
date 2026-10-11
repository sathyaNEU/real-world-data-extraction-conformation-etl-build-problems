# determinism-check report, task181, 2026-10-11

## Verdict
NO VERDICT. Pass 1 did not run. Its one judge thread could not be spawned, so nothing was judged.
**Disposition:** NONE. This is not APPROVE, FIX_NOW or SEND_BACK. Re-invoke the pass.
**Stumping type:** mechanism: not classified, stumping_family: not classified, surface_read_dependency: not classified, sole_data_defect: not classified
**Three rules:** domain: not classified, layers: not classified, decisive_step: not classified

## Why
The orchestrator ran as a general-purpose subagent, and that configuration does not include the Agent tool. `ToolSearch` found no match for `Agent`, `Task`, `Workflow` or `ListAgents`, and no other local tool spawns a subagent. So step 5 of the interaction pattern (spawn exactly one judge thread, `subagent_type: general-purpose`) could not run. The guardrail covers a thread that does not produce a completed `verdict.md`, and it applies here: the pass stops, with no stand-in judge, no retry inside the pass and no verdict. The error class is harness tool provisioning: a subagent cannot spawn another subagent. It is not an API error and not a finding about task181.

## How far the pass got
| Step | Status |
|---|---|
| 1. Inputs present: `prompt.md`, `target/` (11 files; no `target.zip`, which is cut at ship), `submission.md` | done |
| 2. Judge blocks extracted from `submission.md`: FINAL_RECOMMENDATION, SUPPLEMENTARY_ANSWERS (`response_team_brief.pptx`: asks 1 and 2, `pertussis_cases_by_lga.csv`: ask 1), CRITICAL_COMPONENTS, SOLUTION_STEPS. Tags excluded, KEY_ASSUMPTIONS empty | done |
| 3. Fresh bundle copy (`cp -a`) into the pass scratch dir. sha256 identical to `task181/target/` on all 11 files | done |
| 4. `guidelines/determinism_judge_system_prompt.md` read in full (266 lines, 59,520 bytes, sha256 `05b08c24b95b4eb8eeeeed802db3d752a5e1b7efce1219a41a6d27ab049408ad`) | done |
| 5. Spawn exactly one judge thread | BLOCKED: no Agent tool in this session |
| 6. Read `verdict.md` | not run |
| 7. Spec gates; Gate G and Gate H reconciliation | not run |

No intent file was opened. Reading `DESIGN_NOTE.md`, `metadata.json` and the fingerprint card `task181.json` waits on the thread having returned. The generator, goldens, solver rounds and `pipeline.json` were never touched. The materials below were prepared before any of those were read, so they are clean.

Prepared for the re-run. Both sit in the session scratchpad `/tmp/claude-0/-home-user-data-extraction-and-standardization/5ec7cb86-793f-5895-a00b-808e36976e12/scratchpad/`, outside the repo:
- `determinism-check-task181-p1.spawn_prompt.md` (390 lines) is the complete judge spawn prompt, to be inlined unedited. It contains:
  - the allow-list, which permits only `determinism-check-task181-p1/`, and every forbidden path named;
  - the no-server-tools rule and the no-spawn rule;
  - the instruction to recompute every value and record it in the ledger;
  - the instruction to write `verdict.md` in the judge's OUTPUT FORMAT, including the Three rules line;
  - the full system prompt between markers, sha256-checked against the source;
  - `prompt.md` verbatim, sha256-checked;
  - the blocks under the judge's labels.
- `determinism-check-task181-p1/target/` is a bundle copy that no thread has opened.

## Recomputation ledger
Not run: no judge thread.

## Competing answers that survived
Not assessed: no judge thread.

## Spec gates
Not run. The agent file runs them only after the thread returns, and the invocation allows `metadata.json` (the declared distractors) to be read only at that point.

## Gate G reconciliation
Not run. There is no thread classification to compare with the design note and the card (`stump_class`, `analyst_test`, `domain_test`, `gate_g`, `layer`).

## Stump power (Gate F)
Not assessed: no judge thread.

## Findings, ranked
1. Process, blocking. This is not a task181 finding. Stage 7 asks a general-purpose subagent to spawn the judge, and general-purpose subagents in this harness get no Agent tool, so the orchestrator invoked this way can never reach step 5. The fix belongs in the pipeline, not the task: spawn the judge thread from a context that has the Agent tool.

## Next action for the author
Have the main thread make the one judge spawn itself, as pass 2:
1. Refresh the bundle copy (`rm -rf` the `determinism-check-task181-p1/target/` dir, then `cp -a task181/target` into it).
2. Make one Agent call, `subagent_type: general-purpose`, whose prompt is the full text of `determinism-check-task181-p1.spawn_prompt.md`, unedited.
3. Once `verdict.md` exists, run steps 6 to 8 of the determinism-judge agent file. A fresh orchestrator subagent can do this, since those steps need no spawn.
4. File the result as `determinism_check_report_pass2.md`.

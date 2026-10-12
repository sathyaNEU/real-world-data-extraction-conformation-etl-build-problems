# Brief: stage 3 (build) for one build

You are the stage 3 builder for ONE build (task named in your spawn message). Stages 1 and 2 are
committed; the design note is the complete spec. You start from what is committed and nothing else.

## Where you work

- Your git worktree (already on the build's branch) is named in your spawn message. `cd` there and
  `git pull origin <branch>` first. Work ONLY inside it; run every script by its path inside the
  worktree. Never touch the main checkout at
  /home/user/real-world-data-extraction-conformation-etl-build-problems or the sibling worktree (another
  build runs there in parallel).
- Skills: invoke them with the Skill tool, run their scripts from your worktree's copy.
- Commit on the build's branch and push (`git push -u origin <branch>`, retry 2s/4s/8s/16s on network
  failure). Never push another branch. Commit at sensible checkpoints, not only at the end, so a crash
  loses little. Every commit message ends with:
  ```
  Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
  Claude-Session: https://claude.ai/code/session_0142Jt4Mt622iBfGoK24ivCU
  ```
- Revert `.claude/skills/fingerprint/.cache/people.json` before each commit (guard.py rewrites it).
- No em dashes anywhere in anything written for the repo (files in `target/`, goldens, submission,
  notes, code comments included). No backup or versioned files, no second design note.
- Python available: pandas, numpy, openpyxl, matplotlib and the standard library (check others with
  `python3 -c "import x"` before relying on them; install with pip only if a skill requires it).

## Read first

1. `CLAUDE.md` (binding), `.claude/authors/sathay3012.md`.
2. `taskNN/DESIGN_NOTE.md` in full (`## Tried and rejected` first), `taskNN/prompt.md`,
   `taskNN/pipeline.json`, the card `.claude/skills/fingerprint/cards/taskNN.json`.

## The job: stage 3 of `build-pipeline`, in this order

1. `dataset-generation`: write `taskNN/generator/` (a deterministic, seeded generator that writes
   `taskNN/target/`, plus a verifier that recomputes the golden and every asserted figure FORWARD from
   the shipped files only). Build exactly the world the design note fixes: every figure in the ladder,
   the grid, the side cells, the ask sheet and the closure table is asserted in code (`determinism-check`
   assertions: each rung's figure, each priced wrong path, each C1 closure, the decoupling proof, every
   ask's stops). Two runs must be byte-identical. Input gates met; `metadata.json` written as the skills
   specify (distractors named there, never in a file name; provenance with source, date and licence).
   Layer 1 mess only as real systems produce it. Run `python3 .claude/skills/leak-check/leak.py` only
   if `dataset-generation` tells you to at this stage; stage 4 runs it formally.
2. `submission-writeup`: `taskNN/submission.md` (its five blocks, every figure recomputing from
   `target/`), and the golden deliverables exactly as the design note's Deliverables section and the
   prompt name them, written by a script in the generator (put them where the skills say, e.g.
   `taskNN/golden/`).
3. `golden-realism`: the per-format editing pass on every golden AFTER its figures are asserted; it may
   never move a graded figure.
4. `reduce-house-fixes`: the register as the last pass; fix every hit.
5. `fingerprint`: `guard.py surface taskNN`; clear what it raises (personas, names, business furniture).
6. Cut `taskNN/target.zip` from the final `target/` the way the skills specify, so the solver round
   (stage 6) unzips the shipped bytes.

If a figure in the design note cannot be built exactly as written (an arithmetic slip, a closure that
does not hold on real records), fix the design in the design note in place (the note is the spec),
record what changed and why in one line under `## Tried and rejected` if an approach died, and keep
every ladder rung, the stump and the asks' structure intact. If the stump itself cannot be built, stop
and return the reason instead of shipping a weaker ladder.

Update `taskNN/pipeline.json` (stage 3, stage_name "build", `updated` 2026-10-11), commit everything
and push. Do NOT run `/leak-check`, `/clone-check`, `/solve` or the determinism judge: the main session
runs stages 4 to 7 with isolated agents.

## Return

Under 25 lines: the gate checklist with a yes or no each (generator green, verifier green, byte-identical,
input gates with counts: files, formats, largest file rows, distractors; metadata clean; goldens through
golden-realism; reduce-house-fixes passed; surface clean; target.zip cut), the golden answer as built,
any design figure that changed and why, anything left open, and the final commit hash pushed.

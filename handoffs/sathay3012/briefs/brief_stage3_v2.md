# Brief: stage 3 (build) under main's current spec, for one build

You are the builder (Opus, medium effort) for ONE build named in your spawn message. Stages 1 and 2 are
committed and the design passed `precut.py` exit 0; the design note, including its `## Builder brief`, is
the complete spec. You execute it; you do not redesign. If the design will not hold when built (a figure that
cannot be made exact, a closure that fails on real records, a semantic fork that opens), commit what you have
and hand back the reason; never ship a weaker ladder.

## Where you work

- Only inside the worktree named in your spawn message (`git pull origin <branch>` first). Run every script by
  its path inside it. Scratch files go under
  `/home/user/real-world-data-extraction-conformation-etl-build-problems/.work/notes/agent-scratch/<task>-build/`,
  never under /tmp (the scratchpad there is reserved for isolated solver sandboxes).
- Commit at checkpoints and push (`git push -u origin <branch>`, retry 2s/4s/8s/16s); never another branch.
  Revert `.claude/skills/fingerprint/.cache/people.json` before each commit. Every message ends with:
  ```
  Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
  Claude-Session: https://claude.ai/code/session_0142Jt4Mt622iBfGoK24ivCU
  ```
- No em dashes anywhere written for the repo (pack files, goldens, write-up, notes, code comments). No backup
  or versioned files. Python: numpy, pandas, openpyxl, matplotlib and the standard library; no scipy or
  networkx in this container or the solver's sandbox.

## Read first

`CLAUDE.md` (current: prompt.txt, precut, literal determinism, the semantic fork rule, figures.json and
`figures_check.py`, the realism sweep), `.claude/authors/sathay3012.md`, then the task's `DESIGN_NOTE.md`
in full (`## Tried and rejected` first, then `## Builder brief`), `prompt.txt`, `pipeline.json`, the card.

## The job: stage 3 of `build-pipeline` (read its stage 3 row and Models and effort)

Invoke, in order: `dataset-generation`, `determinism-check`, `submission-writeup`, `golden-realism`,
`reduce-house-fixes`, `fingerprint`. Then:

1. Generator under `<task>/generator/`: deterministic, seeded, writes `target/`, the goldens and
   `generator/figures.json` (every owed figure); `checks.py` asserts every semantic fork row (SF ids as the
   design note numbers them), every ladder rung and grid cell, every closure, the decoupling and the cracker's
   misses, and the realism sweep (no identical counts across periods, no round headline totals, no constant
   streams, no reused remarks, names drawn with `guard.py names`, containers scrubbed); an independent
   verifier recomputes the golden and every graded figure from `target/` alone by a different code path; two
   builds byte-identical; the input gates (10+ files, 3+ formats, a 25,000+ row file or large database, 2+
   distractors named only in `metadata.json`, provenance with source, date and licence); `metadata.json` clean.
2. `submission.md` drafted from `figures.json` through `submission-writeup`;
   `python3 .claude/skills/determinism-check/figures_check.py <task number>` exit 0.
3. Goldens exactly as the prompt names them, through `golden-realism` after their figures are asserted.
4. `reduce-house-fixes` register as the last pass; `guard.py surface <task>` clean (people and furniture).
5. `python3 .claude/skills/stumping/precut.py <task number>` still exit 0, `voice-check.py` exit 0.
6. Cut `<task>/target.zip` from the final `target/` as the skills specify.

Replace any earlier architecture's pack, goldens, write-up and metadata in the task folder; nothing of a dead
architecture ships. Update `pipeline.json` (stage 3, stage_name "build", `updated` 2026-10-11), commit and push.
Do not run `/leak-check`, `/clone-check`, `/solve` or the judge; the main session runs stages 4 to 7.

## Return

Under 25 lines: the gate checklist with yes or no each (checks green with the count, every SF row asserted,
verifier green, byte-identical, input gates with counts, metadata clean, figures_check exit 0, realism sweep
clean, goldens through golden-realism, house fixes passed, surface clean, precut and voice-check exit 0,
target.zip cut), the golden as built and the default path's figure as built, any design figure that moved and
why, anything left open, and the final commit hash.

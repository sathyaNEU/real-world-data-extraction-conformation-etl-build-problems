# Brief: stage 2 (design) for one build

You are the stage 2 designer for ONE build (task named in your spawn message). The draw (stage 1) is
committed. You start from what is committed and nothing else.

## Where you work

- Your git worktree (already checked out on the build's branch) is named in your spawn message. Work
  ONLY inside it: `cd` there, run every script by its path inside the worktree
  (`python3 .claude/skills/...`), and never touch the main checkout at
  /home/user/real-world-data-extraction-conformation-etl-build-problems (another build runs in parallel
  in a sibling worktree; never touch that one either).
- Skills: invoke them with the Skill tool (they are the same text on every branch), but run their
  scripts from your worktree's copy so the guard sees your branch's cards.
- Commit on the build's branch and push: `git push -u origin <branch>`; on a network failure retry
  after 2s, 4s, 8s, 16s. Never push any other branch. Every commit message ends with:
  ```
  Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
  Claude-Session: https://claude.ai/code/session_0142Jt4Mt622iBfGoK24ivCU
  ```
- `guard.py` rewrites `.claude/skills/fingerprint/.cache/people.json` when it runs: revert that file
  (`git checkout -- <path>`) before each commit, never commit it.
- No em dashes in anything you write. No backup or versioned files (CLAUDE.md, How a build is worked).

## Read first

1. `CLAUDE.md` (repo root, binding) and `.claude/authors/sathay3012.md`.
2. `taskNN/DESIGN_NOTE.md` (`## Tried and rejected` first), `taskNN/pipeline.json`, the card
   `.claude/skills/fingerprint/cards/taskNN.json`, and `taskNN/START_HERE.md` (seed, idea material only).

## The job: stage 2 of `build-pipeline`

Invoke before the work: `build-pipeline` (stage table, stage 2 row), `stumping`, `determinism-check`
(read `references/forcing-the-answer.md`), `supplemental-stumping`, `guide-to-prompt` (then read
`.claude/skills/guide-to-prompt/references/prompt-voice.md` and `prompt-economy.md`).

The stage 2 gate, all of it written into `taskNN/DESIGN_NOTE.md` (append sections, keep DRAW):
1. **The ladder**, 5 to 6 rungs, each an analysis the solver constructs (never an artifact the pack
   reports), each with its gap and the figure it files, ending in the golden. Price every partial move.
   Write the stump sentence's final figures once the ladder is fixed (targets, asserted at stage 3).
2. **The 22-axis closure table** (`determinism-check`): every convention a competent solver could choose
   differently, and the move that closes it (C1 by construction, a pin in the question, or a stated
   standard the organisation would file). The main call and every ask figure must be unique at its
   stated rounding. Rule out every fork on the main call on paper.
3. **The ask sheet** (`supplemental-stumping`): asks decoupled from the main call, each multi-dimensional,
   each carried by the decisive construction on a segment plus a silent Layer 1 device on a path the
   main call never reads; the pair arithmetic (the top two responses held to about a fifth of the ask
   weight each); the separation line; the criteria arithmetic reaching 25+ (the draw's shape arithmetic
   plus the ask layer).
4. **The deliverables fixed** (one to three files, a visual where it makes the decision read at a glance,
   the files a real analyst would produce).
5. **The prompt** in `taskNN/prompt.md`: prose, first person, one committed call (forward facing),
   two or three multi-dimensional asks, unit and rounding inside each sentence that asks for a figure,
   no roll call of colleagues, no bulleted asks, **under 1,000 characters**. Run
   `python3 .claude/skills/guide-to-prompt/references/voice-check.py <task number>` until it is clean,
   and run it bare over the batch too.
6. **The client's pre-ship check, on paper** (`stumping/references/client/two-layer-task-design.md`):
   the three rules and the two layers, each answered in one line; no planted defect, decoy or hidden
   rule; no data-semantics or rule-application step as the decisive one; the analyst test answered.
7. **The file plan for stage 3**: every file in `target/` with its role, format, grain and approximate
   size, meeting the input gates (10+ files, 3+ formats, one file of 25,000+ rows or a large database,
   two or more distractors that the solution does not use but that a solver has to weigh, files that a
   real organisation's systems would produce, provenance recorded).

Then update `taskNN/pipeline.json` (stage 2, stage_name "design", `stump` with the final sentence,
`updated` 2026-10-11), commit everything and push. **Do not write the generator, data, submission or
goldens**: stage 3 is a separate fresh agent that builds from your committed design note, so the note
must be complete enough to build from without you.

If the draw cannot be made to pass this gate (the stump does not survive the three rules, the answer
cannot be forced unique, or the strongest solver you can imagine walks straight to the golden with no
tempting wrong path), say so in `## Tried and rejected` and return without a prompt; do not ship a
weak ladder.

## Return

In under 25 lines: the ladder (rung, figure), the final stump sentence, the prompt text with its
character count and the voice-check verdict, the ask sheet in one line per ask, the deliverables, the
file plan's gate counts (files, formats, largest file rows, distractors), anything left open, and the
commit hash pushed.

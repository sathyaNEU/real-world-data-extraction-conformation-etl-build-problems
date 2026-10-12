# Brief: bring a build's design up to main's current spec (designer, stage 2 redo)

You are the designer for ONE build (named in your spawn message, with its worktree and branch). While the
build was in flight, main changed the spec; main has now been merged into the build's branch, so the
skills in your worktree are the current spec. Your job is the paper half: bring the design to the new
stage 2 gate, `precut.py` exit 0, and write down exactly what the builder must change. You never cut data.

## Where you work

- Only inside your worktree. Run every script by its path inside it. Scratch files go under
  `/home/user/real-world-data-extraction-conformation-etl-build-problems/.work/notes/agent-scratch/<task>-design/`,
  never under /tmp (the scratchpad there is reserved for isolated solver sandboxes) and never in another
  worktree.
- Commit on the build's branch and push (`git push -u origin <branch>`, retry 2s/4s/8s/16s). Never push
  another branch. Revert `.claude/skills/fingerprint/.cache/people.json` before each commit. Every commit
  message ends with:
  ```
  Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
  Claude-Session: https://claude.ai/code/session_0142Jt4Mt622iBfGoK24ivCU
  ```
- No em dashes. No backup or versioned files, no second design note.

## Read first, in the merged worktree

`CLAUDE.md` (it changed: prompt.txt, precut, literal determinism, the semantic fork rule, the cracker
sheet, models and effort), `.claude/authors/sathay3012.md`, then the task's `DESIGN_NOTE.md`
(`## Tried and rejected` first), `pipeline.json`, the card, the prompt, and (if it exists)
`leak_check_report.md`, `clone_check_report_<task>.md` at the worktree root, and `submission.md`.

Invoke, before the work: `build-pipeline` (stage 2 row, Models and effort), `stumping` (Part 1, the default
path; Part 2, the readability screen and the semantic fork table; Part 5, what precut checks),
`determinism-check` (§1 and §2: determinism is literal; the literal-reader line; the closure table),
`supplemental-stumping` (Part 1, the cracker sheet; the ask sheet and the pair ceiling), and
`guide-to-prompt` (then `references/prompt-voice.md`, the ten rules for `prompt.txt`).

## The gate

`python3 .claude/skills/stumping/precut.py <task number>` exit 0, every FAIL fixed by real design work,
never by filling a template. Today it fails on the missing sections (Default path with numbered steps, an
`Ends on:` line and a `Golden:` line; Three rules with Domain test, Analyst test, Layer 1, Layer 2;
Readability screen table; Semantic fork table with SFn rows; Ladder of 3 to 5 rungs; Closure table with
all 22 axes; Literal reader; Oracles; Ask sheet with a `Pair ceiling:` figure at or under 40 and a cracker
sheet table) and on the prompt gate (no `prompt.txt`).

Restructure `DESIGN_NOTE.md` so the current design sits in the H2 sections precut reads; older material
(earlier architectures, superseded drafts) is condensed into `## Tried and rejected` lines, which stays
append-only. The note states the current design only.

## What has to be argued, not formatted

1. **The default path**: the pipeline a competent analyst builds without thinking, step by step from the
   files, ending on a named figure that is not the golden. If the honest default path ends on the golden,
   the build has no stump: say so and stop (see the stop rule below).
2. **Literal determinism**: the estimand (population, including any members not yet observed at the as-of
   date, outcome, window, unit, comparison) must be filed so that its literal execution is the golden's
   quantity, and no filed rule, basis or formula may give another answer when read literally. If filing the
   estimand literally makes the call easy, the stump was a fork, and the decisive step has to be redesigned
   so the difficulty lives in how the stated quantity is computed.
3. **The semantic fork table**: every term in the main ask and every convention the main computation
   depends on, each with the golden reading, each plausible alternative, the call under it, and the
   sentence of the prompt or a shipped document that rules it out, or `same call`. The stump is never one of
   the readings.
4. **The readability screen**: the decisive rung stays silent in the pack and the prompt.
5. **The ask layer against the cracker**: the cracker sheet is the response that landed the call, ran the
   hygiene battery and executed every filed rule; it must miss every ask figure. No device may be
   adjudicated by a filed rule, a marker or a referee that ties only under the golden, and no ask is keyed
   to the call. Pair ceiling at or under 40. Redesign any ask that fails this.
6. **`prompt.txt`**: plain text, one paragraph, led by the question, under 1,000 characters, the ten rules
   of `prompt-voice.md` (no persona, title, meeting or reader; no "Then" or "Last"; rounding stated once at
   the end; ask, do not specify; keep every surviving ask's file names, columns, periods, units and rounding
   exactly). `voice-check.py <task number>` exit 0. Delete `prompt.md` once `prompt.txt` replaces it.
7. If the card's draw changes (pattern, gap, Gate G, driver), re-run `guard.py check` and `heart` against
   main's cards plus every in-flight card on other branches (export them read-only into a temporary folder
   under `.work/notes/agent-scratch/`, point `FINGERPRINT_CARDS` at it for the checks, run `register`
   without it, delete the folder), and update the card in place.

## The builder list

Write `## Builder brief` at the end of the design note: every change the builder must make to the generator,
the pack, the documents, the goldens, `submission.md` (now drafted from `generator/figures.json` and gated by
`figures_check.py`), the checks (every semantic fork row asserted, the realism sweep asserted), with each
figure that moves. Keep it concrete enough that a fresh builder can execute it without you.

## Stop rule

If the design cannot pass the gate honestly (the default path ends on the golden, the literal estimand
leaves no stump, or no ask layer survives the cracker), write why in `## Tried and rejected`, set
`pipeline.json` (stage 2, a note), commit, push and return the reason. Do not redraw the architecture
yourself.

Update `pipeline.json` (stage 2, stage_name "design (spec update)", `stump`, `updated` 2026-10-11), commit and
push. Return, under 30 lines: precut's final line, the default path's last step and the figure it ends on,
the golden, the literal-reader line, the semantic fork rows that needed real closure, the ladder (rung,
figure), the ask sheet (one line per ask, the cracker's result, the pair ceiling), the prompt.txt text with
its character count and voice-check exit, the builder brief in five lines, and the commit hash.

# Project Mark guidelines (canonical)

This folder is the client-facing spec for Project Mark.

**There are no per-task `task<n>/guidelines/` mirrors.** A stale spec sitting next to a task is worse than no spec. Task folders are not self-contained: if you zip one for hand-off, add `guidelines/` from the repo root alongside it.

## Files

- `introduction.md`, what Project Mark is and how tasks flow. **Carries the operative 2026-09-05 bar block at the top: a task passes when the model responses average under 70 percent against the generated rubric AND at least one response is genuinely stumped, the two conditions conjunctive.**
- `rubric.md`, the generated rubric: you no longer write or edit it, it must reach 25 or more criteria, the weighting (**30 to 40% recommendation, 5 to 10% instruction-following, ~55% asks** as of 2026-09-05), what a good criterion evaluates, and how a prompt gets past 25. **The route to 25 changed on 2026-09-05: the criteria come from the prompt shape, the structure of the answer, never from stacking simple asks.**
- `scope_of_project.md`, Axis 0 (domain), Axis 1 (analytical objective), Axis 2 (reasoning phase). **Six accepted domains as of 2026-08-27 (Biology was dropped from the roster), and Axis 1 carries exactly six objectives** (Forecasting, Root-Cause, Anomaly Detection, Experiment & Causal, Descriptive & Distribution, ETL). Use the canonical labels unchanged. Carries the boundary rules that decide close calls.
- `prompt_guide.md`, how to write the prompt. **Carries the operative 2026-09-05 format block at the top: the prompt is prose and first person, one to three named deliverables with three as the ceiling, no format family assigned, a visual prioritized wherever it makes the call read at a glance, and uncapped multi-dimensional asks feeding a generated rubric that reaches 25 or more criteria through the prompt shape.** Also carries the client's "Updated Announcement" at the foot of the file, the ask-shape steer toward a prospective or predictive committed call, propagated into `../.claude/skills/guide-to-prompt/SKILL.md` as the 2026-08-22 block. The per-deliverable asks replaced the standalone numbered-questions block, and the single `.py` deliverable rule is retired.
- `guide_to_submission_writeup.md`, how to write the submission. Carries the operative 2026-09-05 block at the top: the rubric is generated and no longer edited, **the golden is one to three files with three as the ceiling**, block 5 states every figure a multi-dimensional ask owes rather than summarising it, and the golden must satisfy every positive criterion of the generated rubric. Submission is `submission.md`, the golden is every deliverable the prompt named, and block 5 is Deliverable Answers grouped by file.
- `techniques.md`, the trap catalog (Families A to F). **Carries two operative blocks: the 2026-09-05 bar, which puts one genuine stump back as a pass condition and makes these mechanisms load-bearing again, and the standing judge v3 ban on surface-read rejection as the primary strategy at any depth, which retires the loud artifact and the compound correction chain along with the planted-defect flip.** Read `.claude/skills/stumping/SKILL.md` Parts 1 and 2 before using any family here.
- `determinism_judge_system_prompt.md`, **v3 (2026-08-18).** System prompt for the judge that scores determinism. Gate G now bans surface-read rejection as the primary strategy regardless of depth, which reverses v2's protection of the compound chain and the wrong-methodology artifact. Holds every committed answer to the main recommendation's bar, accepts a Key Assumptions block as reviewer context only, and requires a disposition of APPROVE, FIX_NOW or SEND_BACK. This is the file `/determinism-check` hands to its judge thread verbatim.
- `reviewer_workflow.md`, the reviewer checklist: the four quality checks, the prelim and final verdicts, and what usable review feedback looks like.

## Where the working standard lives

These files are the client-facing spec. The skills under `../.claude/skills/` are the working standard and
are kept ahead of them, so where the two disagree the skill wins:

- `../.claude/skills/guide-to-prompt/` for the pairing, the ask and the prompt format, plus
  `../.claude/skills/guide-to-prompt/references/shapes/` for the eighteen 2026-09-05 prompt shapes
  and the 72 worked prompts, which is the live example library
- `../.claude/skills/stumping/` for the trap architecture, plus
  `../.claude/skills/stumping/references/shipped-ledger.md` for what has already been drawn
- `../.claude/skills/supplemental-stumping/` for the ask layer and the field arithmetic behind the
  under-70 bar
- `../.claude/skills/dataset-generation/` for the pack
- `../.claude/skills/determinism-check/` for the gates, plus `/determinism-check` for the rehearsal
- `../.claude/skills/submission-writeup/` for the write-up and the goldens

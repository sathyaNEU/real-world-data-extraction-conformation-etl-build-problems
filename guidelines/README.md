# Project Mark guidelines

The client's dated spec, kept to the three pages a build still reads. The working standard is the skills under
`../.claude/skills/`, which are kept ahead of these pages; where the two disagree the skill wins (`../CLAUDE.md`,
Standing rules). There are no per-task `task<n>/guidelines/` mirrors.

## Files

- `introduction.md`: what Project Mark is and how a task flows. The top block is the client's update of
  2026-10-10, the three rules every task is built and reviewed against (the task really uses its domain, two
  layers, and no planted defect, data semantics or rule application as the decisive step); below it the
  2026-09-05 bar (the top two responses average under 70 per cent against the generated rubric and at least one
  is genuinely stumped, conjunctive). `stumping` 1.1 is how a design note answers the three rules.
- `rubric.md`: the generated rubric, 25 or more criteria supplied by the prompt shape, and its weights (30 to 40
  per cent recommendation and critical components, 5 to 10 instruction-following, 55 to 60 asks).
  `supplemental-stumping` Part 0 is the pair arithmetic built on it.
- `determinism_judge_system_prompt.md`: the determinism judge's system prompt, v3 with Gate H (the three rules),
  handed verbatim to the `determinism-judge` agent.

## Where the working standard lives

- `../.claude/skills/guide-to-prompt/` for the pairing, the prompt shape and `prompt.txt`, with the shape catalogue
  and worked prompts under its `references/`
- `../.claude/skills/stumping/` for the main call's stump, with the measured record in `references/evidence.md`
  and the ledger in `references/shipped-ledger.md`
- `../.claude/skills/supplemental-stumping/` for the ask layer
- `../.claude/skills/dataset-generation/` for the pack
- `../.claude/skills/determinism-check/` for the gates and the judge
- `../.claude/skills/submission-writeup/` and `golden-realism/` for the write-up and the goldens
- `../.claude/skills/leak-check/`, `fingerprint/` and `clone-check/` for the ship gates
- `../.claude/skills/build-pipeline/` for the stage machine

The client's prompt guide, trap catalogue, scope page, reviewer checklist, submission guide and example library
were retired on 2026-10-30: everything in them a build needs is in the skills, and what is not was behind the
10/10 rules.

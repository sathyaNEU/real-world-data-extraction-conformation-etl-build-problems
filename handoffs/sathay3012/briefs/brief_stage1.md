# Brief: stage 1 (draw) for task253, then task254

Repo: /home/user/real-world-data-extraction-conformation-etl-build-problems. Author: sathay3012
(read `.claude/authors/sathay3012.md` and `CLAUDE.md`, both binding). Lane: Descriptive & Distribution
Analysis (vocab key `descriptive-distribution`).

Branches (already cut from main, each with `taskNN/pipeline.json` at stage 0):
- task253 on `sathay3012/task253-rent-relief-closeout` (seed DA03, `task253/START_HERE.md`)
- task254 on `sathay3012/task254-fire-planning-bands` (seed DA04, `task254/START_HERE.md`)
Never push to any other branch. Commit messages end with:
```
Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_0142Jt4Mt622iBfGoK24ivCU
```

## The job: stage 1 of `build-pipeline`, for each task in order (253 first, then 254)

Invoke, via the Skill tool, before the work: `build-pipeline` (read the stage table only), `fingerprint`,
`guide-to-prompt`, `stumping`, `determinism-check` (forcing the answer while the draw is fixed). Run
`guard.py recent` and `guard.py coverage` first.

For each task:
1. Read its START_HERE.md seed. The seed is idea material written to the banned withheld-rule-with-decoy
   architecture: re-root its stump as a Layer 2 **analytical** pitfall (stumping Part 1/2, the three rules
   in CLAUDE.md). No official decoy, no certified record that blesses the wrong method, no withheld
   decisive rule. A strong analyst who cleaned the data and read every rule correctly must still be able
   to get it wrong by doing the analysis the easy way. Give the house domain its client domain.
   If the seed cannot be made analytical, redraw inside the same objective and keep the number.
2. Pick the prompt shape (guide-to-prompt shapes/ picker) with criteria arithmetic worked to 25+; read the
   two nearest exemplars as idea seeds only.
3. Fill the card (`guard.py new taskNN`), every required field including `stump_class: analytical`,
   `analyst_test`, `domain_test`, `stump_strategy`, `decisive_rule_filed`, `official_decoy: false`,
   `validated_decoy: false`, `client_domain`, `layer2_family`, `layer2_pattern`, `layer1`, `forum`,
   `forcing_event`, `org_family`, personas drawn with `guard.py names --geo <geo> --seed <N>`.
   `guard.py check` until PASS (or WARN answered), then `guard.py register`. task254's card must be
   checked AFTER task253's card is registered, so the bans see it (copy task253's card file into the
   task254 branch's cards/ dir too, so the guard on that branch sees it).
4. Start `taskNN/DESIGN_NOTE.md` with: DRAW (the ten-line summary below), Gate G line, the stump
   sentence (the wrong committed answer a competent solver files and the step that lands them there,
   with rough target figures), the data-native sentence, the two layers named, the prompt shape and
   criteria arithmetic, and an empty `## Tried and rejected` section (record any rejected draw there,
   one line each with the reason).
5. Update `taskNN/pipeline.json`: domain key, objective `descriptive-distribution`, stage 1, stage_name
   "draw", `stump`, `updated` 2026-10-11. Commit the card, design note and pipeline.json on the task's
   branch and push (`git push -u origin <branch>`, retry on network failure 2s/4s/8s/16s).

Do NOT write data, the prompt, the submission or goldens. That is stage 2/3, done by a later agent.

## Return

For each task, ten lines: pairing (client domain, task type, objective), niche, stump sentence, prompt
shape with criteria count, deliverables, nearest exemplar and its measured mean, guard verdict, and the
commit hash pushed. Plus anything you could not resolve.

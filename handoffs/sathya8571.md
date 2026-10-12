# Where to pick up (sathya8571, saved 2026-10-12)

Everything is stopped. No agents are running.

## Shipped or closed
- task132: shipped.
- task133: re-shipped after portal round 1, PR #41 on main. The prompt is prompt.txt, 840 characters.
  - Waiting on the author's portal result.

## In flight (two builds, both architecture 2, both at stage 3, build)

### task134
- Branch `sathya8571/task134-reentry-returns`, head `2126d34` (a WIP commit).
- Worktree `/home/user/wt134` (recreate it from the branch if the container is new).
- The world: Strathallan HSCP. The question is how many council-funded long-stay care home residents at 30 Jun, 30 Sep and 31 Dec 2027 and 31 Mar 2028.
  - Golden about 800 at 31 Mar 2028: a self-funder conversion hazard by months since admission, with deaths competing.
  - Default path about 750: conversions taken at their run rate.
  - Residents to the nearest 10.
- Paper design committed at 3952b38. precut.py passes 37 checks with 0 FAIL, and voice-check passes.
- The builder was stopped mid-build. The generator is committed as WIP, and the pack, goldens and submission are not finished.
- Next:
  1. A fresh builder runs from the design note's Build record, with the brief pattern in this file's "Brief" section.
  2. Stage 3 gates.
  3. Leak reader and clone pre-flight in parallel.
  4. Solver round at high effort.
  5. Judge.
  6. Ship.

### task135
- Branch `sathya8571/task135-forebay-sediment` (the name is legacy; the task is no longer forebay), head `ae2ee69` (a WIP commit).
- Worktree `/home/user/wt135`.
- The world: The Wrexford Trust. The question is the largest growth share, in 10-point steps, inside a 10% volatility cap for 2027.
  - Golden 60%: non-synchronous pricing (noon fund valuation against the London close) handled by weekly returns, lead-lag or Newey-West.
  - Default path 70%: a daily covariance scaled by the square root of 252.
  - Two decoupled asks: income and capital release at nine steps, plus an SVG chart.
- Paper design committed at da4697e. precut.py passes 37 checks with 0 FAIL, and voice-check passes.
- The builder was stopped mid-build; the generator is WIP.
- The builder still owes two things:
  - resize the ask hazards so that no mishandling combination lands within £600 of a golden figure;
  - meet ask A's 8-file span floor, or record the reason.
- Next: the same steps as task134.

## Rules in force (main, PR #43)
- precut gate.
- prompt.txt only, under the author's ten rules.
- Semantic fork table on the main call.
- Ask gate: grade.py exits 3.
- Returned tasks: design, build, commit, ship, with no reader, solver round or judge.
- Solver at high effort.

## Open with the author
- The wording of the portal's P2 and P6 prompt checks has not been provided yet.
- task130: removed from the status tracker at the author's request. The repo removal is unanswered: which of the folder, the card and the START_HERE row should go.

## Status tracker
https://claude.ai/artifact/1nSdDVZwd9p449nYQ9V3o9, collection `builds`.

## Brief
- The builder brief pattern: copy the stage 3 brief in the build-pipeline skill.
- Spawn a fresh builder agent (Opus, medium effort) that reads the design note's Build record, executes it without redesigning, passes every stage 3 gate, commits and pushes.

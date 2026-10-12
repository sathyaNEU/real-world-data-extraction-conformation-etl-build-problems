# Pickup point (oviya13ya, Anomaly Detection lane), stopped 2026-10-12 00:25 UTC on the author's instruction

Repo: sathyaNEU/real-world-data-extraction-conformation-etl-build-problems. Board artifact:
https://claude.ai/artifact/W6PdTkfmbBvbD19W4ECZLY. Briefs and scratch: /home/user/oviya-notes/ (brief-*.md).
Nothing is running.

## Author's standing rules (also in PR #48, `.claude/authors/oviya13ya.md`)
- No retiring, ever: repair or re-root until it ships. Paused builds go back to Status `open`.
- No in-house solver round. Pipeline: draw, design (Opus max), build (Opus medium), leak + duplicate checks
  together, determinism judge (Sonnet medium), ship, then start the next open task at once.
- Every stump unique. Branches `oviya13ya/...`, merged by PR; the author merges (the session cannot merge its own).
- Commit trailers: `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` and
  `Claude-Session: https://claude.ai/code/session_017NMcBvUc2Vu9DKDdwmhqo4`. No model names in commits.
- "Complete" means shipped. Ship commit: `SHIPPED (taskNN): <the call>`, Status shipped on main via PR.

## Open PRs (author to merge)
- #48 `oviya13ya/status-no-retiring`: author rules file, task180 card on main, statuses (180 open, 181/183 in build).
- #50 `oviya13ya/skills-lean`: no solver round, skills slimmed (1.76 MB to 0.42 MB markdown), strategies.md,
  organized ledger, prompt examples. After it merges, merge main into the task branches.

## task183 (8 underground feeders, cable failure recurrence; golden Quarry Hill 21)
Branch `oviya13ya/task183-surge-trigger`, worktree /home/user/wt-183, head 45b42f5.
- Done: design (precut exit 0, prompt.txt 829 chars), build green at 40c47f7 (233 checks, verify, byte-identical),
  leak reader pass 1 (no leak; findings in oviya-notes/t183/leak_reader_pass1.md), clone pre-flight CLEAN (5294cdd).
- In flight when stopped: stage 4 repair of the reader's 5 realism tells (brief oviya-notes/brief-task183-stage4-repair.md).
  45b42f5 is its WIP generator edits, NOT rebuilt or verified.
- Next: finish the repair (rebuild, all gates, append reader pass 1 to leak_check_report.md), leak reader pass 2 (Sonnet),
  determinism judge (determinism-judge agent, Sonnet medium), ship + PR.

## task181 (re-root to architecture 4, author's choice)
Branch `oviya13ya/task181-arch4`, worktree /home/user/wt-181, head c156a01 (task183 card brought in). Nothing designed yet.
- History: arch 1 spent; arch 2 pertussis (portal: determinism fail; the fix designed at 7cc9f49 works but no stump
  survives a filed method); arch 3 criminology (closure infeasible on honest data, branch oviya13ya/task181-arch3).
- Next: fresh designer (Opus max) on oviya-notes/brief-task181-reroot-a4.md, then builder, checks, judge, ship.

## Others
- task182: shipped (PR #40), waiting on the author's portal test.
- task180: open (three architectures in-house; resume later by re-root; branch oviya13ya/task180-revenue-protection).
- Known tooling bug: fingerprint/business.py build_index drops cached persona names for a task folder present on disk
  without its pack; restore `.cache/people.json` before committing.

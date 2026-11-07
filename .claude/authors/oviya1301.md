# Author: oviya1301

Account email: not yet recorded; until it is, the author names the handle at the start of the session. A backlog list, not a territory: no task belongs to anybody, and any build in here can be worked by whoever the user asks.

- **Backlog: Batch 5 (the author's queue, 2026-10-31).** 36 tasks in six objectives, in five priority groups, from the
  author's `Batch_5_Claude_Code.csv`. It replaces every earlier wave in this file. The waves below are the batch's
  queue order cut into fours.
- **Four at a time, one chat (the author, 2026-11-01 and 2026-11-03).** Four tasks are in flight at once; the moment one
  finishes, the next task in queue order starts. The author works in a single chat: parallel builds run as background
  agents or threads inside that one session, never as separate chat sessions (no `create_session`). Each build works in
  its own git worktree, pulls the batch branch with `--rebase` before every guard check and every push, and registers a
  card the moment a draw is fixed, so concurrent draws guard each other.
- **A shipped task here is not done.** Its note names the work it still owes: a rebuild from stage 2 after the portal
  landed its call, a determinism or prompt repair, a resume of a paused draw, or a re-check under the new gates
  (precut anatomy lines, the voice-check count rule, leak.py sweeps 12 and 13, the guard.py heart shell), which reships
  only on a failing gate or a portal result. `status.py next` skips SHIPPED numbers, so the queue is read from this
  table.
- **No retirement (the author's rule, 2026-10-20).** No task number is ever retired: a spent architecture is re-rooted
  with a fresh design, however many architectures it takes, until one ships. This replaces the build-pipeline cap for
  this backlog.
- **Status board:** https://claude.ai/artifact/U4syUnRUycHUsWwhonBYoQ (Batch 5 Build Queue: one row per task in queue
  order, its work item and where it stands, the call, links to the prompt, submission and `target.zip` on `main`),
  updated as each task moves.
- **Resume:** each task's `pipeline.json` and its design note's `## Tried and rejected`.

## Backlog

Work the waves in order, four tasks in flight. The note says what the task owes: rebuild from 2 (the portal landed
the call), determinism fix, prompt repair, re-check (the new gates), resume (a paused or open draw).

| Wave | Tasks, in order |
|---|---|
| 1 | task157 (rebuild from 2: the call landed, new world) · task446 (re-check) · task144 (prompt repair) · task168 (determinism fix: confirm the 10-28 repair) |
| 2 | task187 (re-check) · task261 (re-check) · task188 (re-check) · task230 (re-check) |
| 3 | task472 (re-check) · task140 (re-check) · task265 (re-check) · task267 (re-check) |
| 4 | task166 (rebuild from 2: the call landed, new world) · task229 (determinism fix) · task479 (re-check) · task249 (re-check) |
| 5 | task308 (re-check) · task465 (re-check) · task455 (re-check) · task476 (re-check) |
| 6 | task152 (re-check) · task153 (re-check) · task192 (re-check) · task193 (re-check) |
| 7 | task240 (re-check) · task241 (re-check) · task260 (re-check) · task307 (re-check) |
| 8 | task461 (re-check) · task462 (re-check) · task487 (re-check) · task488 (re-check) |
| 9 | task173 (resume: new draw) · task194 (resume: new draw) · task200 (resume: new draw) · task276 (resume: new draw) |
| 10 | task313 (new) · task398 (new) · task210 (new) · task285 (new) |
| 11 | task489 (new) · task314 (new) · task399 (new) · task211 (new) |
| 12 | task286 (new) · task490 (new) · task315 (new) · task400 (new) |
| 13 | task212 (new) · task287 (new) · task491 (new) · task316 (new) |

Wave 10 onward are new numbers, cut once Batch 5's own re-roots are in flight. Forecasting's range (task132 to task179) is full, so each wave takes the next open number in each objective that has one, so no objective repeats inside a wave (`status.py wave "<objective>"`).

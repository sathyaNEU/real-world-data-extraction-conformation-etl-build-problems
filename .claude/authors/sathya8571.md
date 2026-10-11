# Author: sathya8571

Applies only to sessions run for this author (account email sathya8571@gmail.com). A session run
for anyone else ignores this file and keeps its own branch rules.

## Branches

- Every build goes on its own branch under the `sathya8571/` prefix:
  `sathya8571/taskNN-<short-slug>`, for example `sathya8571/task132-reserving-triangles`.
- This is the author's standing permission to push build work to that branch instead of the
  session's designated `claude/...` branch. Skill and rule edits that are not part of one build go
  on `sathya8571/skills-<short-slug>`.
- Create the branch from the latest `main` at stage 0 (intake), push it at every stage boundary,
  and open the pull request to `main` when the build ships.
- Never push to a branch with another prefix, and never rebase, rename or delete one: those belong
  to other sessions.
- If the author names a different branch in the session itself, that instruction wins.

## Lane

- One Axis 1 objective at a time, two builds in parallel inside it. The current lane is
  **Forecasting & Predictive Modeling**, builds task132 and task133 (`.claude/reservations.md`).
- Each build keeps its own branch (`sathya8571/task132-...`, `sathya8571/task133-...`) and its own
  fingerprint card, registered as soon as its draw is fixed so the other build's guard check sees it.

# Author: oviya13ya

Applies only to sessions run for this author (account email ovi13ya@gmail.com), the developer who works
the Anomaly Detection block under the `oviya13ya` branch prefix. A session run for anyone else ignores
this file and keeps its own branch rules.

## No retiring

- **There is no retiring in this author's builds.** This overrides `build-pipeline`'s Retirement section
  and the three-architecture cap for this author's sessions.
- A build that cannot be made to work is never retired, whatever stopped it: the hardening cap, a
  SEND_BACK, a clone finding, or a design that fails the literal-determinism test. It is repaired or
  re-rooted until it ships.
- A determinism finding from the portal is fixed as the portal requires. If the fix makes the main call
  easy, design a new strategy to stump; the build is never given up.
- Never set Status `retired` in the root `START_HERE.md`, never write a `## Retired` section, never set
  `pipeline.json` to `retired`, and never offer retirement as an option. A build the author pauses
  goes back to Status `open`.

## Branches

- Every build goes on its own branch under the `oviya13ya/` prefix, `oviya13ya/taskNN-<short-slug>`,
  cut from the latest `main` and merged back by a pull request. Status-only and rule changes go on
  `oviya13ya/status-<slug>` or `oviya13ya/skills-<slug>`.
- This is the author's standing permission to push build work to those branches instead of the
  session's designated `claude/...` branch.
- The author merges pull requests. The permission check stops a session merging its own, so a session
  opens the pull request and says so.
- Never push to a branch with another prefix, and never rebase, rename or delete one: those belong to
  other sessions.

## Lane

- The **Anomaly Detection & Diagnostics** block, task180 to task227 in the root `START_HERE.md`, two
  builds in flight at a time. When one ships, pull `main` and start the next open number.
- When a build starts, set its Status to `in build` (Owner `oviya13ya`) on `main`; set `shipped` when it
  ships.
- A shipped build's commit is `SHIPPED (taskNN): <the committed call>`, with the other details in the
  body.
- Keep the author's status board current at every stage: task, prompt, submission and bundle links, and
  SHIPPED or IN PROGRESS.

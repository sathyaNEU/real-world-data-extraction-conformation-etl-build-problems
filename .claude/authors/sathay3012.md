# Author: sathay3012

Applies only to sessions run for this author, the developer who works under the `sathay3012` branch
prefix (account email: add it here so a session matches this file on its own; until then the author
names the handle at the start of the session). A session run for anyone else ignores this file and
keeps its own branch rules.

## Branches

- Every build goes on its own branch under the `sathay3012/` prefix:
  `sathay3012/taskNN-<short-slug>`, for example `sathay3012/task253-rent-relief-closeout`.
- This is the author's standing permission to push build work to that branch instead of the
  session's designated `claude/...` branch. Skill and rule edits that are not part of one build go
  on `sathay3012/skills-<short-slug>`.
- Create the branch from the latest `main` at stage 0 (intake), push it at every stage boundary,
  and when the build ships open the pull request to `main` and merge it.
- Never push to a branch with another prefix, and never rebase, rename or delete one: those belong
  to other sessions.
- If the author names a different branch in the session itself, that instruction wins.

## Lane

- One Axis 1 objective at a time, two builds in parallel inside it. The lane is **Descriptive &
  Distribution Analysis**, the block task253 to task300 in the root `START_HERE.md`, taken two at a
  time from the lowest open numbers (task253 and task254 first).
- When a task starts, set its Status to `in build` (Owner `sathay3012`) in the root `START_HERE.md`
  on `main`; set `shipped` when it ships and `retired` if it dies.
- Each build keeps its own branch and its own fingerprint card, registered as soon as its draw is
  fixed so the other build's guard check sees it.

## The work, and how a build ships

- Every build is high quality, bespoke and stumping, never templated: it runs through `/build` under
  `CLAUDE.md`'s current spec. That means the three rules (the domain swap test, the two layers, and
  no planted, data-semantics or rule-application stump as the decisive step), the bar of the top two
  responses averaging under 50 and built to 40, asks decoupled from the main call, and a prompt under
  1,000 characters.
- When a build ships, its final commit is `SHIPPED (taskNN): <the committed call in one line>`, the
  pull request is merged to `main`, and the session pulls `main` before the next build starts.
- Bookkeeping comes after delivery (`CLAUDE.md`, How a build is worked).

## Status artifact

- Keep one status artifact: a published Artifact page with a shared database collection `builds`,
  one row per task, updated at every stage boundary. Each row carries:
  - the task id and the committed call;
  - the stage and the status (IN PROGRESS, SHIPPED, ON HOLD, RETIRED);
  - links to the prompt, the submission and `target.zip` (GitHub links on the build's branch, or on
    `main` once shipped);
  - a short note of where the build stands, and the date.

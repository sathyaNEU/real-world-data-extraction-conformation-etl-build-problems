# Handoffs

Where each paused build stopped, written by the session that paused it. Read the note naming your task, then
the task's `pipeline.json` and its design note's `## Tried and rejected`.

Every branch these notes name was folded into `main` when the repo moved to one branch: the task folder on
`main` holds that branch's tip, and the branch itself is gone. A step that names a solver round, a scored
reader, a probe, a `/solve` sandbox, a clone pre-flight, a branch, a pull request or a fresh designer or builder agent is superseded by `CLAUDE.md` and
`build-pipeline`: skip it and carry on in the current workflow. A returned build goes to `/fix-determinism`
or `/fix-rubric` as its portal result says.

Every build these notes describe is now `FAILED_TO_STUMP` and sits in its owner's backlog wave (`.claude/authors/`),
with the wave note saying where it restarts. When a build resumes and ships, delete its paragraph here in the
`SHIPPED` commit.

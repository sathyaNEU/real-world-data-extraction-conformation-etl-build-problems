---
description: Check a built task for anything that hands the solver the answer or the author's intent. Runs leak.py's eleven mechanical sweeps, then one isolated solver's-eye read of the prompt and bundle, and writes leak_check_report.md.
argument-hint: taskNN [--asof YYYY-MM-DD]
---

# /leak-check

Run the leak check over the one task named in `$ARGUMENTS`. A bare number or `taskN` means
`taskN/` at the repository root (the folder holding `CLAUDE.md`). If no task is named, ask which one and stop.

1. **Invoke the `leak-check` skill** so the sweeps and the four questions come from the current file.
2. **Resolve `--asof`.** If the argument does not carry it, read the fiction's as-of date from the
   design note's DRAW block (`as-of`, `as of`, `cut-off` or the decision date) and pass it. If the
   note has none, run without it and say so.
3. **Run the mechanical half** with Bash:
   `python3 .claude/skills/leak-check/leak.py <task> --asof <date> --quiet`
   and read `<task>/leak_check_report.md`.
4. **Run the reader's half** with a single `Agent` call, `subagent_type: general-purpose`:
   - First, with Bash, make a fresh scratch copy: `<scratchpad>/leak-<task>/prompt.md` and
     `<scratchpad>/leak-<task>/target/` (unzip `target.zip` if `target/` is absent).
   - The prompt tells the agent it is an analyst who has just been handed this folder, gives the
     scratch path as the **only** readable location, forbids reading anything else on the machine
     (name the task folder, the design note, the generator, the submission and the report as
     forbidden), forbids `Agent`, `WebSearch`, `WebFetch` and every server-side tool, and asks the
     four questions from the skill, each answered with a quotation or the word "none".
   - Then give it the REVIEW lines from the mechanical report, verbatim, and ask for one line per
     item: harmless, with the reason, or a leak, with what it gives away.
5. **Append** the agent's answers to `<task>/leak_check_report.md` under `## Solver's-eye read`.
6. **Report** to the author: the mechanical verdict, the four answers in one line each, and the
   list of items to fix. Do not fix anything in this command; the fix is the author's and it goes
   in the generator.

Spawn one agent and only one. Do not run the determinism judge, the clone check or a solver from
here.

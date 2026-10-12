# Brief: task253 stage 7 FIX_NOW repair (builder, Opus, medium effort)

Worktree: /home/user/real-world-data-extraction-conformation-etl-build-problems/.work/wt253 (branch
`sathay3012/task253-rent-relief-closeout`, at 55b8736). Work only there; scratch under
`/home/user/real-world-data-extraction-conformation-etl-build-problems/.work/notes/agent-scratch/task253-fixnow1/`,
never under /tmp. Commit and push on this branch only (retry 2s/4s/8s/16s), every message ending with:
```
Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_0142Jt4Mt622iBfGoK24ivCU
```
Revert `.claude/skills/fingerprint/.cache/people.json` before each commit. No em dashes.

## The finding (read `task253/determinism_check_report.md`)

The judge found the build DETERMINISTIC; the spec gate set FIX_NOW on one item. The students figures (by region
and by hub, 7,072 in all) take 2027 Years 3 to 6 as the August 2026 census Years 2 to 5, and no shipped file says
that a year level in the census is the 2026 school-year level and that a cohort moves up one level at the start of
the next school year. A literal reader who stops at the census Years 3 to 6 files 6,946.

## The repair, and only this

1. In the generator (never by hand in `target/`), add the fact to `data_team_notes.txt` beside the census entry,
   in the data team's own voice: the census records each student's year level in the 2026 school year, and students
   move up one year level at the start of each school year. A fact about the census and the school year, not an
   instruction to roll the census forward, and no figure.
2. Rewrite the A1 stop-assertions in `checks.py` that assumed the roll-forward was unfiled; assert that the literal
   reading of the notes plus the census gives the golden students figures, and that the un-rolled reading violates
   the new sentence. Update the semantic fork table row for it in the design note (the ruling sentence is now the
   notes' fact) and the ask sheet's pair arithmetic (the census device no longer holds against a solver who lands the
   call; re-state the pair ceiling honestly).
3. Rebuild and run every gate: checks green, verifier green, two builds byte-identical, `figures_check.py`,
   `precut.py`, `voice-check.py`, `leak.py` (no LEAK; answer any new REVIEW line in the design note),
   `guard.py surface`; assert the golden (42; 41.95), the default path (28) and every ask figure unchanged. Cut
   `target.zip` from the final rebuild.
4. One line in the design note's `## Tried and rejected` (the unfiled census bridge as an ask device, and why it went),
   `pipeline.json` (stage 7, stage_name "FIX_NOW repaired; round 2 and re-judge next", `updated` 2026-10-12), commit
   and push.

If the repair moves any graded figure or rung, stop and return the reason.

## Return

Under 12 lines: the sentence added (quoted), the gates (checks count, verifier, byte-identical, figures_check, precut,
voice-check, leak.py verdict, surface), the golden, default path and ask figures as rebuilt, the new pair ceiling, and
the final commit hash.

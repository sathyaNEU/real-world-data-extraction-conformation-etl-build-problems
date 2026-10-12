# Brief: task253 stage 6b, the post-round repair (builder, Opus, medium effort)

Worktree: /home/user/real-world-data-extraction-conformation-etl-build-problems/.work/wt253 (branch
`sathay3012/task253-rent-relief-closeout`, at 7e10162). Work only there; scratch under
`/home/user/real-world-data-extraction-conformation-etl-build-problems/.work/notes/agent-scratch/task253-6b/`,
never under /tmp. Commit and push on this branch only (retry 2s/4s/8s/16s), every message ending with:
```
Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_0142Jt4Mt622iBfGoK24ivCU
```
Revert `.claude/skills/fingerprint/.cache/people.json` before each commit. No em dashes.

## State

Architecture 2 passed round 1: the solver missed the call at the decisive step (28 places against 42) and kept
no ask figure (`task253/solver_rounds/round-1.md`, the main thread's reading at its end). Stage 6b is one repair
of what the leak reader deferred, and nothing else.

## Read first

`CLAUDE.md`, the design note (`## Tried and rejected`, `## Leak check (stage 4)`, `## Builder brief`,
`## Stage 3 build record`), `task253/leak_check_report.md` (`## Solver's-eye read` and the dispositions),
`clone_check_report_task253_pass2.md` (its people note), `pipeline.json`. Invoke `build-pipeline` (stage 6b row),
`dataset-generation`, `golden-realism`, `reduce-house-fixes`, `determinism-check`.

## The repair: the reader's deferred realism tells, fixed in the generator

1. `data_team_notes.txt`: the field-by-field row counts that read like a generated manifest, and the CC BY 4.0
   licence line placed inside an internal cover note (keep provenance in `metadata.json`, where it belongs).
2. `LT-AS-04_analysing_school_results.pdf`: the truncated document-history row and the page break that leaves a
   near-empty page 2.
3. `hub_visit_plan_2027.xlsx`: spelling variants spread uniformly across all five sheets (real coordinator lists
   are lumpy: one coordinator abbreviates, another does not).
4. School names: many repeated saint names across localities read as generated; vary them the way a real
   Catholic system's register reads (parish names, a few colleges, some duplicated saints, not a template), and
   re-check every invented place and school name against real Australian ones (H21).
5. `hub_school_road_distances.csv`: a full 264 x 5 matrix no routing service would export; ship what a real
   travel analysis would (for example each school's distance to the hubs that could serve it), as long as every
   golden and every graded figure stays computable and unchanged.
6. `literacy_specialist_rates_2027.xlsx`: one vehicle allowance for every role.
7. `reading_partnership_2027_guidelines.docx` and other containers: python-docx template parts
   (`stylesWithEffects.xml`, `customXml`, a blank thumbnail); scrub them through the reduce-house-fixes H1 audit.
8. The pass 2 clone note: a persona surname (Williams) shared with task446's card; redraw it with
   `guard.py names` if it is cheap.

## The rule for this stage

Realism is presentation: **no graded figure, rung, ladder cell, semantic fork row or the default path may move.**
Re-run the generator's checks, the verifier, two builds byte-identical, `figures_check.py`, `precut.py`,
`voice-check.py`, `leak.py` (no LEAK; answer any new REVIEW line in the design note), `guard.py surface`, and
assert the golden (42; 41.95), the default path (28) and every ask figure unchanged. Cut `target.zip` from the
final rebuild. If a fix would move a graded figure, do not make it: record it in `## Tried and rejected`.

Record the repair in the design note (one short `## Stage 6b repair` section: what changed, what was declined
and why), update `pipeline.json` (stage 6b, `updated` 2026-10-11), commit and push.

## Return

Under 15 lines: each of the eight items fixed or declined (with the reason), the gate results (checks count,
verifier, byte-identical, figures_check, precut, voice-check, leak.py verdict, surface), the golden and default
path as rebuilt, whether any document under `target/` changed (the main session then runs a second leak read),
and the final commit hash.

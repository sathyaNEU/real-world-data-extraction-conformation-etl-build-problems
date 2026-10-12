# Handoff: sathay3012, task253 and task254 (paused 2026-10-12 at the author's request)

Lane: Descriptive & Distribution Analysis (block task253 to task300). Both tasks are `in build` (Owner sathay3012)
in the root `START_HERE.md` on main. No agent is running; nothing is half-written. Every build change is committed
and pushed on the build branches below. This folder (on branch `claude/exciting-tesla-84medc`) holds this note, the
session's agent briefs, task254 architecture 3's prototype scripts and task253's round 1 and judge evidence; all of
it was local scratch before.

Status board (Artifact, shared database `builds`, one row per task):
https://claude.ai/artifact/Ht1rZ4FAUWxn91Ma75XRzC (titled "Distribution Analysis Board"; both rows set ON HOLD).

## Where each build stands

### task253, branch `sathay3012/task253-rent-relief-closeout`, head `ac60466`

- **Architecture 2 of 3** (Education & Learning Sciences, student growth and value-added modelling): the 2027
  Reading Partnership, how many of 264 primary schools have an underlying Year 5 reading average below 480 on the
  NAPLAN scale, from the 2024 to 2026 sittings (year groups of 4 to 160 students).
- **Golden: 42 places** (the sum of the schools' probabilities of an underlying average below 480 under the filed
  LT-AS-04 model at its fitted values, 41.95). **Default path: 28** (count the schools whose model average, the
  shrunken prediction, is below 480). Raw three-year averages give 56.
- **Passed**: precut (before the FIX_NOW), build (749 then 744 checks, independent REML verifier, byte-identical,
  figures_check), leak check (leak.py REVIEW only; two Sonnet reads, no decisive-step sentence, no answer file, no
  main-call fork), clone pre-flight pass 2 CLEAN (`clone_check_report_task253_pass2.md` at the repo root of the
  branch), **solver round 1 PASSED** (`task253/solver_rounds/round-1.md`: the Opus solver read everything correctly,
  fitted the filed model and committed to 28; it kept 0 of 25 ask figures; grade.py's token match had to be
  overridden twice, see the round file's "Main thread's reading"), stage 6b realism repair done.
- **Judge pass 1** (`task253/determinism_check_report.md`): DETERMINISTIC; the thread approved, the spec gate set
  **FIX_NOW** on one unfiled inference (2027 Years 3 to 6 taken as the August 2026 census Years 2 to 5). Repaired in
  `ac60466`: one fact filed in `data_team_notes.txt` ("The year level is the student's year level in the 2026 school
  year; students move up one year level at the start of each school year."). No graded figure moved.
- **Open, blocking**: `precut.py` now exits 1: **pair ceiling 44.5 against 40**, because with the census bridge filed
  a solver who lands the call also keeps Ask A (students served by region); only the hub device (B1, the February
  2026 directory against the 2027 visit plan) still holds. 44.5 is under the 50 bar but over the 40 target, and the
  gate blocks.
- **Next, in order**: (1) a designer (Opus, max effort) re-cuts Ask A with a silent device that no filed rule
  adjudicates and that survives the hygiene battery, on the ask's own path, keeping the main ladder untouched, until
  precut exits 0 with the pair ceiling at or under 40; (2) a builder (Opus, medium) rebuilds and runs the stage 3
  gates and `leak.py`; (3) one Sonnet leak read (a document changed); (4) solver round 2 (Explore, Opus, high
  effort) in a clean sandbox; (5) the single re-judge (determinism-judge prepares, the main session spawns the
  thread from its `judge_brief.md`, a fresh determinism-judge writes the report); (6) ship.

### task254, branch `sathay3012/task254-fire-planning-bands`, head `2039b02`

- **Architecture 3 of 3, the last** (Urban & Regional Science, network analysis): a hospital's transportation
  planning team sets the 2027 morning departure of a staff shuttle from a remote park-and-ride lot to the downtown
  campus while the staff garage is demolished: the latest five-minute slot whose trips would have reached the campus
  stop by 8:00 a.m. on at least 90 per cent of the weekdays of the twelve months to September 2026, read from a probe
  vendor's segment travel times by five-minute period. Stump on the card: summing every segment at the departure
  period files 7:15 (on time on 235 of 250 weekdays) against 7:05, because each later segment must be read at the
  period the shuttle reaches it (delay builds during its own passage). Strategy `time_semantics`, shape 04.
- **Done**: the draw, registered with the guard (`70f729d`, card `.claude/skills/fingerprint/cards/task254.json`).
  `pipeline.json` set to architecture 3, stage 1.
- **Not done**: the pooled heart check was mid-run when the designer was stopped; the design note still describes
  architecture 2 (everything from architecture 1 and 2 is in its `## Tried and rejected`); no prompt.txt; no data.
- **Next**: a designer (Opus, max) re-runs the pooled guard and heart (main's cards plus every in-flight card from its
  own branch; `task254-arch3-prototype/tools/build_pool.py` here builds the pool), then writes stage 2 for
  architecture 3 to `precut.py` exit 0 (literal estimand, default path ending on 7:15, the strongest-solver test,
  semantic fork table, readability screen, ladder, closure table, literal reader, oracles, ask sheet with the cracker
  sheet and a pair ceiling at or under 40, prompt.txt, builder brief), using the prototype here as a start
  (`walk_proto*.py`, `ladder10.py`, `asks8.py`, `freeze7.py`, `search*.py`). Then build, leak and duplicate checks,
  round, judge, ship. If architecture 3 fails, the number is retired.

## Architecture history (all in each design note's `## Tried and rejected` and each card's `lineage`)

- task253 v1, nonresponse adjusted within registry licence class (rent-relief vouchers): built, then the stage 5
  clone pre-flight found a TEMPLATE against task230 (another author's in-flight build). Its one redraw, crossing
  criticality by re-solved traffic equilibrium: under main's literal-determinism rule the filed assignment makes the
  closure estimand a mechanical re-run, so no stump. Architecture 1 spent.
- task254 v1, fire planning bands on burned area by footprint: the precise estimand names the overlay. v2, Lyrevo RMP
  monitoring windows from a right-truncated case series: read literally the filed estimand gave the stump's month (a
  fork); refiled, every reflex correction gives the golden; asks failed the cracker. Both spent.

## Process notes that cost time this session (read before resuming)

1. **Merge main first.** Main changed the spec mid-build on 2026-10-11 (prompt.txt, `precut.py`, literal determinism,
   the semantic fork table, the cracker sheet, `figures_check.py`, the ask gate, models per role). Both branches have
   main merged as of 2026-10-11/12; merge `origin/main` again before resuming, and re-run `precut.py`.
2. **Keep the main checkout on current main**: the Skill tool loads skills from it.
3. **Pool the guard.** `guard.py` only sees its own branch's cards; point `FINGERPRINT_CARDS` at a folder with main's
   cards plus every in-flight card taken from its own branch for `check` and `heart`, and run `register` without it.
   task253 v1's collision with task230 was invisible without this.
4. **Worktrees and scratch.** Work each build in its own git worktree outside the scratchpad (this session used
   `.work/wt253` and `.work/wt254` in the repo, excluded by `.git/info/exclude`); keep agents' scratch out of the
   scratchpad, which must hold nothing but the isolated sandbox while a solver, reader or judge runs.
5. **Roles** (build-pipeline, Models and effort): designer Opus max; builder Opus medium; leak reader Sonnet medium;
   clone auditor Opus medium; solver `Explore` Opus high; judge Sonnet medium. A repair is always a fresh agent with a
   short brief on committed state (the `briefs/` here are the ones used).
6. **grade.py** matches tokens: a wrong call can be read as LANDED on shared words, and region or hub names inflate the
   ask share. Read both and adjudicate by figures; record the reading in the round file and the pipeline row.
7. **The determinism-judge agent has no Agent tool** in this runtime: it prepares `judge_brief.md` and stops; the main
   session spawns one isolated Sonnet thread from it, then a fresh determinism-judge writes the report from
   `verdict.md`. "Our judge is the floor": a fork the thread settles by the natural reading is a FIX_NOW.

## Files in this folder

- `briefs/`: every agent brief used this session (stage 1 to 3, spec update, re-roots, 6b, FIX_NOW).
- `task254-arch3-prototype/`: the architecture 3 designer's prototype and pool builder.
- `task253-evidence/`: round 1's solver output and the judge thread's pass 1 verdict.

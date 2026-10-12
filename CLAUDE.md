# Project Mark task builds

Every `taskNN/` folder is one deterministic analytical task: `prompt.txt`, the bundle under `target/`,
the golden deliverables and `submission.md`.

## Skill routing (binding)

Invoke the skill before the work, whatever the request's wording; if two apply, both, in pipeline order.

| Doing this | Invoke first |
|---|---|
| Starting or re-rooting a build, or asking whether a build repeats an earlier one | `fingerprint` |
| The domain and objective pairing, the prompt shape (the 25 criteria), the Main Recommendation Ask, `prompt.txt` | `guide-to-prompt` |
| The pitfall, the default path, the stump sentence, the ladder, hardening, re-rooting | `stumping` |
| The supplemental asks and the devices that carry them | `supplemental-stumping` |
| Forcing a unique answer while designing, or checking a build against the judge's gates | `determinism-check` |
| Building or repairing the bundle under `target/` | `dataset-generation` |
| Writing or editing `submission.md` or any golden deliverable | `submission-writeup` |
| Making a golden read as a real work product (after its figures are asserted) | `golden-realism` |
| Declaring a bundle ready, or recording a fix that came back from submission | `reduce-house-fixes` |
| Checking a cut pack for anything that hands over the answer or the author's intent | `leak-check` |
| Checking a build or a batch for cloning, templating or duplication | `clone-check` |
| Taking a task to ship, or resuming a build in flight | `build-pipeline` |

**Four slash commands, all author-triggered:** `/build` (the pipeline), `/approve` (heart check and
sign-off), `/leak-check` (sweeps plus one reader), `/clone-check` (adjudicated corpus comparison).
No isolated thread runs on the model's own initiative; `/build` licenses the threads it sequences
(the leak reader, the clone pre-flight, the judge).

## The workflow

```
0 INTAKE    taskNN from the root START_HERE.md, Status in build on main, the branch, pipeline.json
1 DRAW      fingerprint recent + coverage, the pairing and prompt shape, the card through guard.py
            (check, then register): the stump is unique, no repeated driver, pattern or strategy
2 DESIGN    designer, Opus max: default path ending on a wrong answer, stump sentence, ladder,
            semantic fork table, closure, the asks, prompt.txt          gate: precut.py exit 0
3 BUILD     builder, Opus medium: generator, pack, goldens, submission.md
            gate: generator checks, verify, two byte-identical rebuilds, figures_check.py,
            the realism sweep, golden-realism, reduce-house-fixes, guard.py surface
4 LEAK + DUPLICATE, together: leak.py + one leak reader (Sonnet medium);
            guard.py heart + the clone pre-flight (clone-auditor, Opus medium);
            every finding fixed in the generator before the judge
5 JUDGE     determinism-judge (Sonnet medium). APPROVE ships; FIX_NOW fixed, re-judged once;
            SEND_BACK re-roots or retires
6 SHIP      target.zip from the final build, commit "SHIPPED (taskNN): <the call>", Status shipped
            on main, ledger row delivered. Then start the next open task at once.
7 PORTAL    the author's result goes into the ledger row. A return takes the fast path: designer
            (if the call or determinism failed), builder, the free mechanical gates, re-ship.
            No reader, clone check or judge.
```

There is no in-house solver round. Stump power is argued on paper (`precut.py`), checked by the leak
reader and the judge's Gate F, and measured by the portal, the only stump evidence the ledger records.
Every repair (a leak fix, a FIX_NOW, a returned task) runs in a fresh agent from the committed state
named in a short brief; a finished agent is never resumed. At most two builds in flight per author.
Gates, models, `pipeline.json`, re-rooting and retirement: `build-pipeline`.

**The fingerprint guard is mandatory and free.** The card is registered the moment the draw is fixed,
so builds in flight guard each other. Personas are drawn with `guard.py names --geo <geo> --seed <task
number>`, never typed; `forum`, `forcing_event` and `org_family` are banned against the last three
builds. The adjudicated `/clone-check` runs only when the author asks or `/build` reaches stage 4.
Reusing a proven device is legitimate; a repeated driver or a strategy monoculture is not.

**Determinism is a construction, not an inspection**: invoke `determinism-check` while the ladder and the
generator are written. Its judge thread is spawned only when the author asks or `/build` reaches stage 5.

## Per-author rules

Authors keep standing rules (branch prefixes, lanes) in `.claude/authors/<handle>.md`. At session start
read the file matching the session user's email and follow it; ignore every other author's file. Task
numbers come from the root `START_HERE.md`; a session builds the number it was handed and sets its
Status on main, so no two sessions draw the same `taskNN`.

## How a build is worked

1. **Deliver before bookkeeping.** Finish and hand over what was asked; only then the ledger row, skill
   lessons, house fixes or memory. This defers filing, never design or a skill. The ledger row is
   rewritten whenever a build's status changes (drawn, built, shipped, re-rooted, retired) and takes the
   portal result the day the author reports it (`stumping/references/shipped-ledger.md`).
2. **One design note per build, with an append-only `## Tried and rejected` section** (that exact
   heading). When an approach dies, add one line: what was tried and why it died, written at the moment
   it is abandoned. Every iteration reads it first.
3. **No backups, snapshots or versioned design docs.** Banned in a task folder: `DESIGN_V2.md` and
   later, `_v*_snapshot.zip`, `.bak`, dated copies of the prompt or golden, a second design note. Allowed
   beside the note: `START_HERE.md` (never edited once the build starts), `pipeline.json` (state only),
   `generator/figures.json`, and the leak, clone and determinism reports (evidence). Older folders may
   also hold `solver_rounds/`, kept as history. A build that cannot be rebuilt from its generator has a
   broken generator.

## Standing rules

- No em dashes anywhere in the repo. Use a comma, or parentheses for an aside.
- Every figure in `submission.md` recomputes from `target/`, and a figure shared by two deliverables
  agrees in both to the same rounding.
- Skills state the current spec only: rules rewritten in place, no changelogs, no dated blocks, no
  "as of", no retired rules. Build IDs and measured numbers stay only where a rule stands on them.
- `guidelines/` is the client's dated spec and is behind the skills; where they disagree the skill wins.
  It still says top two under 70, built to 60; the bar is 50 and the target is 40.

## Current spec

**The three rules** (a break sends the task back even when it is deterministic):

1. **The task really uses its domain.** The deciding quantity is one the field would estimate, model or
   test. Swap test: with another field's nouns the task must stop making sense (`guide-to-prompt`).
2. **Two layers.** Layer 1 is realistic mess across several files (grains, versions, calendars, IDs,
   partial extracts, superseded documents), always something the organisation's systems would produce,
   never what the stump rests on (`dataset-generation`). Layer 2 is the analytical pitfall: the shortcut
   a capable analyst takes and an expert rejects, with the rigorous method the only defensible one. It
   carries the stump (`stumping`).
3. **Banned as the decisive step:** a planted defect, decoy or hidden rule; data semantics (reading a
   field, code, unit or definition right); rule application (executing stated rules). Test: could a
   strong analyst who cleaned the data and read every rule still get it wrong by doing the analysis the
   easy way? Choosing the estimand or unit of analysis counts as analysis.

Cards carry `stump_class` (only `analytical` passes), `analyst_test` and `domain_test`. The guard blocks
an official decoy, a certified record built to bless the wrong method, and a decisive rule left unstated
against a stated one. File the rules a real organisation writes down; the answer turns on a step they
leave open.

**Determinism is literal.** The judge executes the shipped text word for word. The estimand
(population, including members not yet observed, outcome, window, unit, comparison) is filed so its
literal execution is the golden; the method stays open only where the design, a standard's general
method or a filed selection criterion forces it, with the data separating the candidates (a filed
back-test is a recognisable organ, never in consecutive builds; `determinism-check` §1). **No semantic fork on the main recommendation**: every term and
convention has a row in the design note's fork table, closed by a sentence or `same call`, asserted in
`checks.py`; `precut.py` refuses an open one. A reading difference is never the stump.

**Every stump is bespoke and unique.** Never replicate an approved task's trap, method, questions or
strategy onto new data. The pitfall comes from the dataset's own structure and the design note says why
in one data-native sentence. Client libraries and the `analytical_tasks/` seeds are idea seeds: keep
the world, decision and quantity, re-find the pitfall from the data. Calibration corpora,
twin pairs and colleague voices are organs, never furniture or decoys.

**Deliverables:** one to three, three the ceiling. No format family is required; pick what a real
analyst would produce, and prefer a visual wherever it makes the decision read at a glance.

**Asks:** uncapped, each multi-dimensional and hard (many rows, periods or cuts resolving to one
answer), unit and rounding inside the asking sentence, every figure separately gradable and
determinate. Asks are decoupled from the call and free of its rules: an ask may turn on semantics or
rule application, and each carries its own silent device against the careful solver's path
(`supplemental-stumping` Part 2.1).

**Prompt:** `prompt.txt`, one plain paragraph, question first, under 1,000 characters, no persona,
roll call or bullets, gated by `voice-check.py` (`guide-to-prompt`).

**Rubric:** generated, 25 or more criteria, supplied by the prompt shape (every candidate, period, cell
or reconciling item graded), never by stacking simple asks. Weights: 30 to 40 percent recommendation and
critical components, 5 to 10 percent instruction-following, 55 to 60 percent asks.

**The bar:** the top two responses average under 50 percent with at least one genuinely stumped; build
to 40. A response on the main call banks about 45 before any ask, so the ladder keeps all but one
response off the call and the asks hold each of the top two to about a fifth of the ask weight. The
ten points are margin for the portal's regrade. The flip-the-wrong-number trap is banned.

**Goldens look business-realistic**; an LLM first draft is sent back (`golden-realism`).

**Domains:** the client's 21 domains in seven groups (`guide-to-prompt/references/domains/`). One
domain, one task type, one objective; a new draw in a house domain names its client domain.

**Eight objectives, nothing else is a valid tag:** Forecasting & Predictive Modeling (most wanted);
Root-Cause Analysis; Anomaly Detection & Diagnostics; Experiment & Causal Analysis; Descriptive &
Distribution Analysis; Data Extraction & Conformation (ETL); Opportunity Sizing & Decision Support (the
headline is a sized opportunity, pool to realisable, that drives the call); Data Quality Monitoring &
Alerting (the object is the health of the data or pipeline, the call is a monitoring decision). Either of
the last two fails if the prompt could be retagged without changing a word.

**Gate G:** no shipped artifact ranks the candidates on the decision question and gets it wrong, at any
depth. The one exception is a declared wrong-basis distractor named in `metadata.json`, ruled out by a
shipped fact and never the stump. The difficulty survives deleting every wrong number from the pack.

**The call is forward facing by default**: a quantity about a window not yet closed. A retrospective
call is legal with its reason in the design note; never retag as Forecasting because the window is open.

**Input gates:** 10 or more files, 3 or more formats, one file of 25,000 or more rows (or a large
database file), two or more distractors (relevant enough to weigh, unused by the solution, named in
`metadata.json`, never in a file name), every file license-clean with source, date and license recorded,
nothing that reads as LLM generated.

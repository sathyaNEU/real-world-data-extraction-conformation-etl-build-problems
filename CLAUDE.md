# Project Mark task builds

Every `taskNN/` folder is one deterministic analytical task: `prompt.txt`, the bundle under `target/`,
the golden deliverables and `submission.md`. The goal is one thing: high-quality, unique, submission-ready
tasks, shipped one after another. Everything below serves that and nothing else.

## STOP: no solver, no scored reader, no probe, on any build

**Binding on every session and every developer, read before anything else.** The solver flow is retired and is
never run under any name: no scored readers, no `score_reader.py` (deleted), no call-only or draw probes, no "cold"
or "blind" reader that solves the prompt and hands back figures, no isolated thread that answers the task. Stump power
is argued on paper (`precut.py`, the design note's ladder and `## Three rules`) and measured by the portal alone.

**Every returned task is fixed and reshipped on the regular checks only.** A portal send-back of any kind (a
FAILED_TO_STUMP, a determinism block, a rubric block, a duplicate finding) is fixed in the generator and reshipped once
these pass: the free gates (generator checks, `verify`, two byte-identical builds, `figures_check.py`, `precut.py`,
`voice-check.py`), the determinism judge, the leak check (`leak.py` and the one isolated leak reader, which reads the
pack for leaks and never solves it) and the clone check (`guard.py heart` and `surface`). Nothing waits on a solver's
score. A skill, note or author file that still describes a reader round, a probe or a scored read describes the retired
practice: do not run it, and remove it where you find it.

## The 10/10 rules come first

The client's update of 2026-10-10 sends back more tasks than anything else in this file. Every draw, every
rework of a `FAILED_TO_STUMP` build and every fix answers it before any other work, and a build that fails it
is neither resumed nor shipped: it is redesigned. The client's own text is the top block of
`guidelines/introduction.md`; `stumping` Part 1.1 is how a design note answers it.

1. **The task really uses its domain.** The quantity that decides the call is one the field would estimate,
   model or test, worked the way one of the domain's task types works it. Swap test: put another field's
   nouns in ("hospital" for "school", "megawatt-hours" for "visits"); if the task still reads the same, the
   domain is a backdrop. A stated score, an eligibility check, a sort or a filter deciding the call is a
   backdrop at any depth (`guide-to-prompt`).
2. **Every task has two layers.** Layer 1 is realistic mess that the organisation's own systems produce:
   layouts changing across years, tables inside PDFs, imperfect keys across sources, a preliminary and a
   revised release overlapping, fiscal against calendar years, local time against UTC, thousands against
   units. It complicates the work, is never planted, and never carries the stump (`dataset-generation`).
   Layer 2 is the analytical rigor that decides the answer: the method an expert in the field recognises,
   where a capable analyst's easy route files a wrong answer (the right comparison group, the data's real
   structure such as censoring, the evidence judged with its uncertainty, a forecast validated out of
   sample). It carries the stump (`stumping`).
3. **Three kinds of stump are banned as the decisive step.** They may appear; none may decide the call:
   - a planted defect, decoy or hidden rule (a block of readings secretly copied, a memo arguing the wrong
     answer, a rule deliberately left unstated);
   - data semantics (the answer flips only on reading a field, code, unit or definition correctly);
   - rule application (the answer comes from executing stated rules, however many steps there are).

**The test, answered in writing for the main call:** could a strong analyst who cleaned the data and read
every rule correctly still get the answer wrong by doing the analysis the easy way? Yes is analytical and
valid. No is semantics or rule application, and the build is redesigned. Choosing the right estimand or unit
of analysis counts as analysis. Rule 3 binds the main call's decisive step; the asks are free of it.

**Where builds slip past it, and what catches each:**
- **A determinism repair that files the method.** Filing HOW the figure is computed turns the decisive step
  into rule application. File the WHAT (population, window, unit, comparison), never the HOW
  (`/fix-determinism`, `determinism-check` §1).
- **A rework resumed from an old design.** Before resuming a `FAILED_TO_STUMP` build, its card carries
  `stump_class: analytical`, `analyst_test` and `domain_test` and its note a passing `## Three rules`; a
  stump that is a decoy, a withheld rule, a field reading or an executed procedure is re-rooted, never
  resumed. `status.py next` flags a rework that has not been re-checked.
- **A seed copied as a design.** The seeds in `analytical_tasks/` were written to the withheld-rule-with-decoy
  architecture the client bans. Take the world, the decision and the quantity only; `status.py taskNN`
  prints nothing else.
- **Mess carrying the stump.** If cleaning the data makes the call easy, the stump was Layer 1: move it into
  the analysis.
- **The domain as backdrop.** If the deciding number is a stated score or a list check, nothing the field
  estimates decides the call.

**The gates.** The card's `stump_class` (only `analytical` passes), `analyst_test` and `domain_test`:
`guard.py` blocks a draw without them, and blocks an official decoy, a certified record built to bless the
wrong method, a decisive rule left unstated against a stated one, and a task type that does not serve the
objective. The note's `## Three rules`, one labelled line per point of the client's check, `No decoy:`,
`Not semantics:` and `Not rule application:` each on its own line: `precut.py` refuses a missing or one-word
line. `checks.py` executes the analyst test on the generator's clean truth (`dataset-generation` §7.1). At
stage 4 the leak reader's question 6 and the judge's Gate H read the three rules from outside the design.

## A stuck build is unblocked, never parked

No build waits in `PAUSED` for a blocker to clear. The session that meets the blocker removes it at once and
carries the build on to ship:

- **A guard ban the draw cannot clear** (an axis the last three builds hold, a strategy the window bans, a seed
  whose own furniture is barred): redraw the axis, and when the seed's world cannot carry an honest unbanned
  draw, move the build to another client domain, world and dataset under the same objective and number. Never
  wait for the window to move and never relabel a card to pass it.
- **A dead design** (`precut.py` fails, the readability screen fires, the judge sends it back, a FIX_NOW fails
  twice, the portal returns it unstumped): re-root at once with a new draw, a new dataset and a new generator,
  in another domain when the old one is spent. A re-root past a slot's third architecture needs no checkpoint.
- **Anything else** (a generator that will not go green, a failing gate, a missing input): fix it in the
  generator and rebuild.

`PAUSED` means one thing: the session itself is ending with work mid-stage. Its `resume` line names the next
action, and the next session takes that build before any new number (`status.py next` names it first).
Retirement and a ban waiver stay the author's call, and neither is a reason to stop: a redraw in another
domain is always available.

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
| Taking a task to ship, resuming a build, or repairing a returned one | `build-pipeline` |

## Commands and effort

Each command sets its own effort in its frontmatter, so a session gets the right depth without being told; the three build commands also run on Opus (`model: opus`).

| Command | What it does | Effort |
|---|---|---|
| `/build taskNN` | draw, design, build, leak read and judge, ship; resumes from `pipeline.json` | max |
| `/fix-determinism taskNN <portal finding>` | closes the determinism block's finding; the main call, the stump and every graded figure stay frozen | max |
| `/fix-rubric taskNN <portal finding>` | reworks the supplemental asks until the top two sit under 70, built to 60; the main recommendation side stays frozen | max |
| `/approve taskNN` | the mechanical sign-off (heart, surface, precut, leak verdict) | medium |
| `/leak-check taskNN` | `leak.py` plus one isolated reader | medium |
| `/clone-check [scope]` | the adjudicated corpus comparison, **author-triggered only** | medium |

Every spawned agent (the leak reader, the determinism judge, the clone auditor) runs at medium effort, set in
`.claude/agents/` or on the `Agent` call. There is **no solver round**, no scored reader and no probe, and none is
rebuilt under another name (the STOP block at the top).
No isolated thread runs on the model's own initiative; the commands above license the ones they name.

## The workflow

```
0 INTAKE    status.py next <handle>: the next task in your backlog wave (a rework resumes from its own
            pipeline.json; a new number reads only the seed's header and Situation, status.py taskNN)
1 DRAW      guard.py recent, coverage and mechanisms --objective <o>; the pairing and shape; the card through
            guard.py check, then register.                                    COMMIT "DRAWN (taskNN)"
2 DESIGN    default path ending on a wrong answer, stump sentence, ladder, fork table, closure, the asks,
            prompt.txt                                                        gate: precut.py exit 0
3 BUILD     generator, pack, goldens, submission.md
            gate: generator checks, verify, two byte-identical rebuilds, figures_check.py, realism sweep,
            golden-realism, reduce-house-fixes, leak.py, guard.py surface and heart
4 CHECK     the leak reader and the determinism judge spawned together in the background (both medium);
            the card and the pre-ship check proceed meanwhile; every finding fixed in the generator in one
            pass; a FIX_NOW is re-judged once
5 SHIP      target.zip from the final rebuild, ledger row, card current       COMMIT "SHIPPED (taskNN): <call>"
            then the next open number at once
6 PORTAL    the author's list: APPROVED is SHIPPED_APPROVED, PENDING_REVIEW stays SHIPPED, a shipped build
            left off it is FAILED_TO_STUMP and joins its lane owner's backlog wave; a determinism finding goes
            to /fix-determinism, a rubric at or over 70 with the call held to /fix-rubric
```

One session runs the whole build in its main thread at max effort: design and build are the same hand, and
a repair is done where the context already is, never handed to a fresh agent that rereads every skill. Stump
power is argued on paper (`precut.py`), checked by the leak reader and the judge's Gate F, and measured by the
portal, the only stump evidence the ledger records. The adjudicated `/clone-check` is not a stage: the free
`guard.py heart` and `surface` gate every build, and the author asks for the adjudicated read when they want it.

**The fingerprint guard is mandatory and free.** The card is registered the moment the draw is fixed and
committed with it, so builds in flight guard each other. `guard.py mechanisms` reads every spent driver on the
objective in one screen before drawing; personas come from `guard.py names --geo <geo> --seed <task number>`,
never typed; `forum`, `forcing_event` and `org_family` are banned against the last three builds. Reusing a
proven device is legitimate; a repeated driver or a strategy monoculture is not.

**Determinism is a construction, not an inspection**: invoke `determinism-check` while the ladder and the
generator are written. Its judge thread is spawned at stage 4, by `/fix-determinism`, or when the author asks.

## Git: one branch, commits at status changes only

There is one branch, `main`. No build, skill or status branch is created, and no pull request is opened.

- **Commit only at a status change**, never at a stage boundary: `DRAWN (taskNN)` (the card, `pipeline.json`
  and the design note, so other builds' guard sees the draw), `SHIPPED (taskNN): <the call>`, `RESHIPPED
  (taskNN): <what the repair moved>` after a fix command, `PAUSED (taskNN)` with the resume step in
  `pipeline.json` (only when the session ends mid-stage, never for a blocker: the section above),
  `RETIRED (taskNN)`. A skill change is its own commit, `SKILLS: <the rule>`.
- **Each commit carries every artifact that status touches:** the task folder, its card, its ledger row, and at
  ship `target.zip` and the `golden/` files added with `git add -f`. Stage paths by name; never `git add -A`.
- **Before every push:** `git pull --rebase origin main`, then push. Task folders and cards are one file per
  build, so they never collide; on a ledger conflict keep both rows. Never force-push, never rewrite history,
  never commit `.cache/` or anything `.gitignore` names.
- Status lives in each build's `pipeline.json` (`DRAWING`, `DESIGN`, `BUILD`, `SHIPPED`, `SHIPPED_APPROVED`,
  `RETURNED`, `FAILED_TO_STUMP`, `PAUSED`, `RETIRED`) and `status.py` prints the board. The author's portal list
  goes into the ledger's portal record in one `STATUS: portal results` commit.

## Lanes, authors and handoffs

Task numbers come from the root `START_HERE.md`, numbered by objective; each lane has one owner. At session
start read `.claude/authors/<handle>.md` for the session user's email and ignore the others: it holds the lane,
the status board link and the **backlog**, waves of six tasks to ship worked in order (reworks first). `status.py
next <handle>` names the next task, `status.py` shows every wave; at most two builds in flight per author.
A paused build is resumed before any new number: read `handoffs/<handle>.md` if it names the task, then
`pipeline.json` and the design note's `## Tried and rejected`.

## How a build is worked

1. **Deliver before bookkeeping.** Finish and hand over what was asked; only then the ledger row, skill
   lessons, house fixes or memory. This defers filing, never design or a skill. The ledger row is written
   at ship (or retirement) and takes the portal result the day the author reports it
   (`stumping/references/shipped-ledger.md`).
2. **One design note per build, with an append-only `## Tried and rejected` section** (that exact
   heading). When an approach dies, add one line: what was tried and why it died, written at the moment
   it is abandoned. Every iteration reads it first.
3. **No backups, snapshots or versioned design docs.** Banned in a task folder: `DESIGN_V2.md` and
   later, `_v*_snapshot.zip`, `.bak`, dated copies of the prompt or golden, a second design note. Allowed
   beside the note: `pipeline.json` (state only), `generator/figures.json`, and the leak, clone and
   determinism reports (evidence). Older folders may also hold `START_HERE.md` (the seed they were numbered
   from) and `solver_rounds/`, kept as history. A build that cannot be rebuilt from its generator has a
   broken generator.

## Standing rules

- No em dashes anywhere in the repo. Use a comma, or parentheses for an aside.
- **No dollar sign before a digit in a skill body.** The skill loader reads `$0` to `$9` as its own
  argument placeholders, so an agent invoking the skill with arguments is served the argument string
  where the figure belongs: a rule standing on a measured number loses the number silently, and on disk
  the file still looks right. Write the unit in words (`USD 38M`, `34 cents a day`, `exactly zero`).
- Every figure in `submission.md` recomputes from `target/`, and a figure shared by two deliverables
  agrees in both to the same rounding.
- Skills state the current spec only: rules rewritten in place, no changelogs, no dated blocks, no
  "as of", no retired rules. Build IDs and measured numbers stay only where a rule stands on them.
- `guidelines/` is the client's dated spec and is behind the skills; where they disagree the skill wins.
  Its bar and this file's agree, top two under 70 built to 60; a page there that says 50 is behind.

## Current spec

**The three rules** are the first section of this file, and everything below assumes them.

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

**The bar:** the top two responses average under 70 percent with at least one of them genuinely stumped
on the main call; build to 60. A response on the main call banks about 45 before any ask and a response
off it about 12, so the ladder keeps at least one of the top two off the call, and the asks are built hard
regardless: each of the top two keeps under two fifths of the ask weight, which puts the pair near 51. If
both land the call the pair reaches 60 only with each held to about a quarter of the ask weight, so a
design whose ladder, argued on paper, leaves both responses on the call is redesigned, not shipped. The ten points are margin for
the portal's regrade. The flip-the-wrong-number trap is banned.

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

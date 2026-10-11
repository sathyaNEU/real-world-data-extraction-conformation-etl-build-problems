# Project Mark task builds

Every `taskNN/` folder in this repo is one deterministic analytical task: a prompt, a
shipped evidence bundle under `target/`, the golden deliverables the prompt named, and the
write-up in `submission.md`. Sessions usually run with the cwd set to a task folder, and
this file applies to all of them.

## Skill routing (binding)

**Before writing or editing any `submission.md`, invoke the `submission-writeup` skill.**
This is not optional and it is not conditional on the request wording. It applies when the
ask is to draft a submission, rewrite one, fill in a block, fix a block a review called
thin, or produce any of the golden deliverables that ship with it. The skill carries the
block list, so writing one from memory or by copying an older task ships the wrong format.

The rest of the pipeline routes the same way:

| Doing this | Invoke first |
|---|---|
| Writing or editing `submission.md`, or any golden deliverable | `submission-writeup` |
| Making a golden deliverable look like a real work product rather than an LLM draft | `golden-realism` |
| **Starting a new build or re-rooting one** (before the pairing is chosen, and again when the draw is fixed), or asking whether a build repeats an earlier one | `fingerprint` |
| Choosing the domain and objective pairing, **picking the prompt shape that supplies the 25 criteria**, shaping the Main Recommendation Ask, writing or editing `prompt.txt` | `guide-to-prompt` |
| Finding the analytical pitfall, writing the default path and the stump sentence, screening the rungs, designing or hardening the ladder, re-rooting a spent architecture | `stumping` |
| Designing or hardening the supplemental asks, or the data-quality devices that carry them | `supplemental-stumping` |
| Building or repairing the evidence bundle under `target/` | `dataset-generation` |
| Checking a finished build against the judge's gates, or **forcing an answer to be unique while the build is still being designed** | `determinism-check` |
| Rewriting long-form prose into the user's voice | `humanizer` |
| Checking a build, or a batch, for cloning, templating or duplication | `clone-check` |
| Declaring a bundle ready to ship, or recording a fix that came back from submission | `reduce-house-fixes` |
| Checking a cut pack for anything that hands the solver the answer or the author's intent | `leak-check` |
| Running the in-house solver round on a finished build (stage 6 of `/build`, or `/solve`) | `solver-round` |
| Taking a domain and an objective to a delivered task, or resuming a build in flight | `build-pipeline` |

If two apply, invoke both, in pipeline order.

**Five slash commands, all author-triggered:** `/build` (the pipeline), `/approve` (the heart
check and sign-off), `/leak-check` (the leak sweeps plus a reader's pass), `/clone-check` (the
adjudicated corpus comparison) and `/solve` (a solver round: one isolated solver in a sandbox, graded).
Each spends tokens in isolated threads except `/approve`, so none runs on the model's own
initiative; `/build` is the author's licence for every stage it sequences: the leak reader, the
adjudicated duplicate check, every solver round its loop needs, and the determinism judge.

**The workflow is design (gated by `precut.py`), build (gated by the generator's checks,
`figures_check.py` and the realism sweep), leak check and duplicate check together, solver round,
determinism check, ship, and it loops.** Nothing with a token cost runs on a pack the free mechanical
gates have not passed. One isolated solver works every finished build cold, in a sandbox holding only
`prompt.txt` and the bundle. A round where it commits to the main call sends the build back to design
with a hardening brief, the default path rewritten first; it is hardened, rebuilt, leak-checked and
solved again, three loops per architecture, then re-rooted in the same objective and number, three
architectures, then retired. A round where the solver misses the call but still keeps 35 per cent of
the ask weight, or cracks any ask, sends the ask layer back (`grade.py` ASKS LEAK) without touching the
ladder. A round that passes both gates gets one repair of whatever the leak reader deferred and goes on
to the determinism judge, run in the background, whose FIX_NOW is fixed and re-judged once. No session
runs a solve in the main thread, which has read the design. Each role runs on its own model and effort
(`build-pipeline`, Models and effort): the designer on Opus at max effort; the solver on Opus at high;
the builder and the duplicate-check auditor on Opus at medium; the leak reader and the judge on Sonnet
at medium.

**Returned tasks skip the heavy stages.** A shipped task the author brings back with portal feedback is
repaired design, build, commit, ship (`build-pipeline`, Returned tasks): a designer when the call
landed, a builder when it held and the asks scored, with the free mechanical gates only (the
generator's checks, `verify`, byte-identical rebuilds, `leak.py`, `guard.py`, `voice-check.py`,
`figures_check.py`, `precut.py`). No leak reader, solver round, judge or clone check runs for it. New
builds keep the full workflow.

**Solver first, polish after.** The leak reader runs once per build, on Sonnet, after the realism sweep
and in parallel with the clone pre-flight, before the round. Only
what hands the solver the answer (a sentence naming the decisive step, a file that ranks the
candidates or states the asked figures, a file that exists only to help) and any fork on the main call
are fixed before the solver sees the pack. The reader's realism tells and its forks on ask figures wait
for a round the solver misses, or ride in the hardening brief when it lands, so no repair is spent on a
pack that is about to be rebuilt. A second read runs only when a fix changed a document or the prompt.
An author keeps at most two builds in flight, a re-rooted architecture included. Every repair after a
round (a hardening rebuild, an ask-layer rebuild, the deferred findings, a judge's FIX_NOW, a returned-task repair) runs in a fresh agent that starts
from the committed state: the round's log in `solver_rounds/`, `pipeline.json` and the design note,
named in a short brief. A finished agent is never resumed, so no repair pays for the transcript behind
it (`build-pipeline`, Running the stages).

## Per-author rules

Some authors keep standing working rules (branch prefixes, for one) in `.claude/authors/<handle>.md`.
At the start of a session, read the file whose account email matches the session's user and follow
it; ignore every other author's file. A rule there binds only that author's sessions.

Task numbers are given out from the root `START_HERE.md`: every unbuilt seed in `analytical_tasks/`
has a numbered folder, objective by objective, and each `taskNN/START_HERE.md` carries its seed and the
rules. A session builds the number it was handed and sets its Status there on main, so parallel
developers never draw the same `taskNN`.

## The build loop

```
fingerprint recent + coverage   (what the last builds spent, and what has never been drawn)
   ->  guide-to-prompt  (pairing, then the PROMPT SHAPE, with its criteria arithmetic worked to 25+)
       + the two nearest exemplars (guide-to-prompt/references/exemplars/, the client's measured tasks)
   ->  stumping: the draw (the card checked and registered), the pitfall from the dataset and the
       domain's rigor patterns, the DEFAULT PATH written and ending on a wrong answer, the stump sentence
   ->  DESIGN: the readability screen (the decisive rung silent), the semantic fork table (no fork on
       the main call), the ladder (3 to 5 rungs), determinism-check (literal reader, 22 axes closed),
       supplemental-stumping (the cracker sheet, the ask sheet, pair ceiling at or under 40),
       guide-to-prompt (prompt.txt through voice-check.py)
              gate: precut.py exit 0, or nothing is cut
   ->  BUILD: dataset-generation (the realism sweep asserted)  ->  submission-writeup (blocks from
       figures.json, figures_check.py exit 0)  ->  golden-realism  ->  reduce-house-fixes
              ->  fingerprint surface
   ->  LEAK CHECK and DUPLICATE CHECK together: leak.py and one /leak-check reader pass on Sonnet;
       guard.py heart and the /clone-check pre-flight (leak-level findings and main-call forks fixed in
       the generator now; realism tells and ask-level forks deferred to after the round; a reject-tier
       clone finding redraws the colliding axis once, or retires)
              meanwhile: the next number's draw, if a slot is free
   ->  SOLVER ROUND: /solve, one isolated solver in a sandbox, graded at the rubric's weights
              grade.py exit 0: the solver does not commit to the main call and the asks hold
              exit 2, landed: back to design with the brief and the deferred findings (default path
              rewritten, harden, rebuild, leak check, solve again); 3 loops per architecture, then
              re-root; 3 architectures, then retire
              exit 3, asks leak: the ask layer rebuilt against the cracker sheet, a fresh round
              pass: one repair of the deferred findings (a new read only if a document or the prompt
              changed, a new round only if the prompt, a rung or the decisive path changed)
   ->  DETERMINISM CHECK: the judge rehearsal, in the background. APPROVE ships; FIX_NOW is fixed and
              re-judged once (a fresh solver round first only if the fix moved a figure, a rung or a
              document); SEND_BACK re-roots or retires
   ->  SHIP to the author
   ->  the author tests on the official portal and reports back
              RETURNED: design (if the call landed), build, commit, ship, with the free mechanical gates
              only; no leak reader, round, judge or clone check (`build-pipeline`, Returned tasks)
   ->  only then: ledger row, lessons folded into the skills, house fixes, memory
```

`/build taskNN` (or `/build <domain> <objective>`) runs that loop as a stage machine with `pipeline.json` as its state
(`build-pipeline`), without stopping for the author.

The judge rehearsal runs once the solver round has passed, in the background: keep working the
stages that do not move a graded figure (the card, the pre-ship check, the design note) while it
runs. The portal's own Determinism QC also runs in the background now and no longer
blocks submission, so a build is not held waiting on it; the in-house judge still gates the ship.

The prompt shape is picked **before** the ladder, not after a thin rubric comes back, because it
decides where the criteria come from and it is the cheapest thing in the build to change. The
eighteen shapes and the picker are at `.claude/skills/guide-to-prompt/references/shapes/`.

**The fingerprint guard is mandatory, mechanical and free.** Every build has a fingerprint card in
`.claude/skills/fingerprint/cards/`, and `guard.py` checks a new draw against all of them: the
`stumping` Part 6 standing bans against the last three builds, the same-puzzle test against the last twelve,
the driver sentence against every driver on file including retired architectures, and the legality
gates. A draw with a BLOCK does not get a ladder. The card is filed with `guard.py register` the
moment the draw is fixed, so a build in flight is visible to the next one, which the shipped ledger
cannot do because it only gets a row when the portal result comes back. A card records identity
only and never an outcome. It spawns nothing and costs nothing, so it is run on every build without
being asked; only the adjudicated `/clone-check` is author-triggered.

**People and business furniture are checked too**, because the same first names and the same
deciding boards otherwise recur across builds. Every persona in a build is drawn with
`guard.py names --geo <the build's geography> --seed <task number>` and listed on the card, never
typed from memory; and each card declares its deciding `forum`, its `forcing_event` and its
`org_family`, which are banned against the last three builds like every other axis. Name pack files
in the organisation's own idiom: the dictionary and the provenance record are required content,
`data_dictionary.md`, `export_manifest.csv` and `provenance.md` are habits.

`golden-realism` runs **after** the golden's figures are correct and asserted, never before, because
it edits presentation and a figure that moves afterwards invalidates the pass. It owns what a
deliverable looks like when a human opens it; `reduce-house-fixes` owns the container and the
write-up prose, and the two are run together as the last block before the bundle is called ready.

**The portal is the stump oracle; the solver round is the filter in front of it.** The author tests
the build on the official portal and reports the result, and that report is the only stump evidence
the ledger records. The in-house round decides what is worth sending: a build its solvers crack is
hardened, not shipped, and a build they miss still has to face the portal. Solves run only in
isolated threads on fresh scratch copies, never in the main thread (a solve that has read the design
note measures nothing). Stump power is argued on paper first: **name the stump in the design note**
before the pack is cut: first the default path, the pipeline a competent analyst builds without
thinking, step by step, ending on a named figure that is not the golden; then the stump sentence, the
wrong answer that default path files and the step that lands it there. A design whose default path ends
on the golden has no stump (task134 landed 33 navigators in four minutes that way), and a ladder whose
author cannot write the sentence is not built; `precut.py` refuses both, and the round then tests the
sentence. A hardening deepens the analysis and never plants a decoy.

**`/clone-check` is author-triggered only**: never invoke it on your own initiative, including right
after applying a patch that seems to want validation, because it spends real tokens in an isolated
thread. The cheap mechanical half of the same question (`guard.py heart`) runs inside the build
stage, so a template or duplicate is caught before the adjudicated check is paid for; inside
`/build` the adjudicated pre-flight on that one build is stage 5, and `/approve` runs the mechanical
half on request.

`/clone-check` also runs on a plain request, so a chat asking for a clone check, a template
check or a duplicate check invokes it. It compares a build, or the whole batch, against every
other build, the way the final_verdict reviewer does, and it separates what a reviewer can see
(prompt wording, file names, schemas, the data itself) from what only the design notes show
(the gap, the pattern, the decisive rung). Reusing a proven trap device is legitimate and the
check says so out loud. What it hunts is a repeated driver, meaning the same insight carrying
the stump twice, which is a clone however far apart the two surfaces sit, and a strategy
monoculture, one stumping strategy carrying a large share of the batch across different drivers. Run it in pre-flight
on a build whose draw is fixed and whose data is not yet cut, because a mechanism finding caught
then costs a redraw and the same finding caught later costs the build.

**Determinism is a skill, not a command, and it is a construction, not an inspection.** Invoke
`determinism-check` **while the ladder is being designed and while the generator is being written**,
not only at the end; its `references/forcing-the-answer.md` carries what made 44 shipped builds'
answers unique. Invoking it costs nothing and spawns nothing. The one thing it can spawn, an isolated
judge thread over the shipped bundle, is governed by **Running the judge rehearsal** in that skill:
the author asks in their own words, and nothing else licenses it. Never spawn it because a build just
finished or a patch seems to want validation.

## How a build is worked

Three rules about the working method rather than the product.

**1. Deliver before you do bookkeeping.** Finish what the author asked for, say it is done, and hand
it over. Only then touch the ledger, fold a lesson into the skill it belongs to, add a
`reduce-house-fixes` entry or write memory. None of that is part of the deliverable and none of it is
urgent, and a session that spends its last stretch updating skills has made the author wait for
filing. If the session ends before the bookkeeping happens, nothing is lost that the design note
does not already hold.

This defers **bookkeeping**, not design. The routing table above stays binding: `submission-writeup`
is invoked before a `submission.md` is touched, `guide-to-prompt` runs before a prompt is written,
the ladder is designed before data is cut. Speed comes from not writing files nobody reads and from
recording a dead end once. It never comes from a thinner ladder or a skipped skill.

**2. One design note per build, with an append-only `## Tried and rejected` section.** When an
approach dies, add one line to that section: what was tried, and the reason it died, in enough
detail that the next iteration does not rediscover it. Then move on and build something else. That
section is the entire memory of what did not work, and reading it is the first thing an iteration
does.

Use that exact heading so it can be grepped. Write the line when you abandon the approach, not in a
tidy-up pass at the end, because the reason is what matters and the reason is what gets forgotten.

**3. No backups, no snapshots, no versioned design docs.** The generator rebuilds the pack, so there
is nothing to preserve. Banned inside a task folder: `DESIGN_V2.md` and every later number,
`_v*_snapshot.zip`, `.bak` files, dated copies of the prompt or the golden, and a second design note
under any name. If a scratch copy is genuinely needed while an edit is in flight, it goes in the
scratchpad and is deleted when the edit lands. What a task folder may carry beside the design note:
`START_HERE.md` (the seed it was numbered from, never edited once the build starts), `pipeline.json` (state, never reasoning), `solver_rounds/` (the graded rounds), `generator/figures.json` (the
owed figures the write-up is drafted from) and the `leak_check_report.md` and
`determinism_check_report*.md` reports, which are evidence rather than design.

A build that cannot be rebuilt from its generator has a broken generator, and the fix is the
generator, never a zip.

## Standing rules

- No em dashes in anything written for this repo. Use a comma, or parentheses for an
  aside. Em dashes are named as a rejection cause in the review.
- Every figure quoted in `submission.md` has to recompute from the files under `target/`.
  A number that cannot be recomputed does not exist, and every figure shared between two
  deliverables has to agree in both, to the same rounding.
- **Skills state the current spec only.** When a rule changes, rewrite it in place in the skill
  that owns it: no changelogs, no dated update blocks, no "as of" framing, no retired rules kept for
  reference. A lesson from a portal result goes into the skill body as a present-tense rule. Build
  evidence (build IDs, measured numbers, what died and why) is not history and stays where it
  supports a rule; the shipped ledger and the fingerprint cards are records, not spec.
- `guidelines/` holds the client's spec as dated format updates, stacked newest first. The skills
  under `.claude/skills/` are the working standard and are kept ahead of `guidelines/`; where they
  disagree, the skill wins. In particular `guidelines/` still states the pass bar as the top two
  under 70 and building to 60 under its OPERATIVE banners; the bar is 50 and the target is 40.

## Voice and structure

**Every prompt is `prompt.txt`**: plain text, one continuous paragraph, led by the question, under
1,000 characters. It sounds like a person asking for help with their task, not a backstory about them,
and it mentions only what the task needs. The ten rules (`guide-to-prompt/references/prompt-voice.md`):
lead with the question; cut who and why (no names, titles, sign-offs, meetings or readers); test every
fact before cutting it (a date or a stop rule the answer depends on stays); keep every ask exactly (file
names, columns, periods, units and rounding word for word); do not change meaning while smoothing; one
continuous paragraph, with no "Then" and "Last"; merge and shorten, each rounding rule stated once at the
end; ask, do not specify; drop claims made only to be rejected; and run the 10/10 check last. The client's
note names the shape to avoid: *"I'm a X working at Y. Here's some context. Give me this main
recommendation and here are the two deliverables that I need from me."*

**The gate is mechanical.** `python3 .claude/skills/guide-to-prompt/references/voice-check.py <task
number>` exits non-zero per rule: the file is `prompt.txt`, no markdown character, one paragraph, a
question mark in the first two sentences, under 1,000 characters, no em dash, no persona or job title
(the card's `world.people` and a title lexicon), no sequencing words, no LLM tells, no roll call,
rounding as a closing clause, one to three deliverables named. `leak.py` runs the same gate as its sweep
11, `precut.py` runs it before any data is cut, and every reader of the prompt (`/solve`, `/leak-check`,
the judge, the guard, the clone check) reads `prompt.txt` first and falls back to `prompt.md` only on a
build shipped before the rule. Run it bare over the batch before submission: variety now lives in the
question's form, the sentences and the files, and the batch report measures it. Self-report does not
catch a calcified voice; `grep` does.

## Current spec

**Every task is built and reviewed against three rules**, and a task that breaks one is sent back even
when it is deterministic and correct. Tasks are training data, and a task is useful only if getting it
right teaches a model something real.

1. **The task really uses its domain.** It does the kind of analysis its domain is about, close to one of
   the domain's task types, and the quantity that decides the call is one the field would estimate,
   model or test. The swap test: put another field's nouns in ("hospital" for "school", "megawatt-hours"
   for "visits"); if the task reads exactly the same, the domain is only a backdrop (`guide-to-prompt`
   Step 1).
2. **Every task has two layers.**
   - **Layer 1, data messiness.** Realistic, hard-to-parse data spread across several files: the grains,
     versions, calendars, identifiers, partial extracts and superseded documents a real export carries.
     A model may trip here, and that is fine, but the stump never rests on mess and never on an
     unrealistic planted defect. Every piece of mess has to be something the organisation's real
     systems would produce (`dataset-generation` §7).
   - **Layer 2, the analytical or methodological pitfall.** The shortcut a capable analyst is tempted to
     take and an expert in the field would recognise as wrong, with the task set up so the rigorous
     method is the only defensible one. This layer carries the stump (`stumping` Part 1).
3. **Three kinds of stump are banned as the decisive step**: a planted defect, decoy or hidden rule;
   data semantics (the answer flips only on reading a field, code, unit or definition correctly); and
   rule application (the answer comes from applying stated rules correctly, however many steps there
   are). All three may appear in a task, never as what decides it. **The test:** could a strong analyst
   who cleaned the data and read every rule correctly still get the answer wrong by doing the analysis
   the easy way? If yes, the stump is analytical and valid; if no, it is semantics or rule application.
   Choosing the right estimand or unit of analysis counts as analysis (`stumping` Part 1).

Every card drawn from 2026-10-10 carries `stump_class` (only `analytical` passes), `analyst_test` and
`domain_test`, and the fingerprint guard blocks the draw without them. The guard also blocks on the draw:
a filed rule, basis or metric planted to give the wrong answer (an official decoy); a closed or certified
record built to bless the wrong method until a forward condition breaks it; and a decisive rule
deliberately left unstated with a conflicting stated rule as the trap. File the rules a real
organisation would have in writing; what decides the answer is an analytical step those rules leave to
the analyst, never the rules themselves.

**Determinism is literal.** The portal's judge executes the shipped text word for word and infers
nothing. So the estimand (population, including any members not yet observed at the as-of date, outcome,
window, unit, comparison) is filed so that its literal execution is the golden's quantity; the method may
stay open only behind a filed criterion that selects it, with the data separating the candidates under it;
and no filed rule, basis or formula may give another answer when read literally. The stump lives in how
the stated quantity is computed, never in what is meant: if a literal estimand makes the call easy, the
stump was a fork and the decisive step is redesigned (`determinism-check` §1 and §2).

The client's libraries are the working material: `stumping/references/client/two-layer-task-design.md`
(the three rules, the two layers and the pre-ship check), `stumping/references/client/layer2-rigor-patterns.md`
(300 rigor patterns by domain and task type: the pitfall, the tempting shortcut, what pins the rigorous
method) and `dataset-generation/references/layer1-messiness.md` (the universal Layer 1 techniques and
eight per domain). A pattern is learned, never copied: the build makes its own version on its own data,
and the same pattern on the same data structure is a duplicate the guard blocks. The answer is pinned by
the question and a stated standard (the estimand defined precisely: population, outcome, window, unit,
comparison; the design implying the method; alternatives ruled out by the data's own structure), never
by a hidden method recovered from certified or published figures, which the client caps at review.

**Every build is bespoke, never templated.** Replicating an approved task's traps, solution method,
questions or stumping strategy onto another dataset teaches the model nothing and is sent back. Each
build picks the pitfall its own dataset's analytic structure produces, and its design note says why
in one line (the data-native sentence, `stumping` Part 1.7). The client's examples and the strategy
libraries are idea seeds: learn the fundamentals from them, never copy one.

A calibration corpus, a twin pair and colleague voices are organs a strategy may need, never
furniture every build ships, and none of them may act as a decoy. The 300 notes under
`analytical_tasks/01` to `06` were all written to the withheld-rule-with-decoy architecture, so they
are idea seeds and never build plans (`README.md`): a seed supplies a world, a decision and a quantity,
its withheld rule is filed, its decoy is cut, and the pitfall is re-found from the data (`stumping`, the
references table).

**No semantic fork on the main recommendation.** Every term in the main ask and every convention the
main computation depends on has a row in the design note's semantic fork table: the golden reading, each
plausible alternative, the call under it, and the sentence of the prompt or a shipped document that rules
it out, or `same call` where the records converge. `checks.py` asserts every row and `precut.py` refuses a
note with an unresolved one. The stump is never one of the readings: a reading difference is a fork and
data semantics at once, and six builds in one window built or defended one as their difficulty
(`stumping` Part 2.2, `determinism-check` §2).

**One to three deliverables, and three is the ceiling**, so a four-file build is a spec failure.
**No format family is assigned.** The four families (Data: CSV, TSV, JSON, XLSX, Parquet · Visual:
PPTX, PNG, SVG, HTML, JPG · Text: PDF, DOCX · Code: PY, IPYNB, SQL, R) describe what a file is for,
but nothing requires the set to span two of them. Pick the files a real analyst would actually
produce for the decision and be honest about it, because `analysis_report.pdf` is not the
best-suited deliverable for every task. **Prioritize a visual wherever it makes the decision read at
a glance.** A table can live inside a memo, a workbook, or a script's output rather than taking a
slot of its own.

**The asks are uncapped and untargeted, and each has to be multi-dimensional and hard.** One ask can
span many rows, periods or cuts and still resolve to one defensible answer, and that is the ask you
want, because a wrong analytical path fails it everywhere at once. Unit and rounding are stated
inside the sentence that asks for the figure, and every figure inside an ask is separately gradable
and separately determinate. One deterministic recommendation anchors everything. An ask is free of the
main call's rules: it needs no filed rule to pin its handling, its golden may go against the procedure,
and its device may turn on data semantics or rule application, which rule 3 bans only as the main call's
decisive step (`supplemental-stumping` Parts 2 and 6). Every ask is designed against the careful solver's
path: the cracker sheet (the response that landed the call, ran the hygiene battery and executed every
filed rule) misses every ask figure, so no device is adjudicated by a filed rule, a marker or a referee
that ties only under the golden, and no ask is keyed to the call (`supplemental-stumping` Part 1).

**The prompt is `prompt.txt`: plain text, one paragraph, question first, under 1,000 characters**
(Voice and structure above). No persona, title, meeting or reader; no bracketed blocks, headers or
bulleted asks; no roll call of colleagues' opinions, which is a design defect rather than a style one,
because each named opinion hands the solver a rung to refute. One committed call and two or three asks,
each multi-dimensional and hard, never a list of small ones (`guide-to-prompt`, and `voice-check.py`
fails a draft at 1,000 characters or more).

**The rubric is generated and must reach 25 or more criteria.** A one-to-three file prompt is a small
surface, so the criteria come from the **prompt shape**, the structure of the answer: a ranked list
under a cap grades every candidate, a forecast across many periods grades every period, a grid
grades every cell, a bridge grades every reconciling item. Eighteen shapes with 72 worked prompts
live in `.claude/skills/guide-to-prompt/references/shapes/`, and the picker there carries the
criteria arithmetic. **Never stack simple asks to reach 25.** Weights: 30 to 40 percent
recommendation and critical components, 5 to 10 percent instruction-following, about 55 to 60
percent asks. Full spec: `guidelines/rubric.md` (its bar wording is behind the skills, see Standing
rules).

**The bar is the top two responses averaging under 50 percent, with at least one response genuinely
stumped, and you build to 40.** Both conditions must hold, and because the bar averages the top two,
a build has to hold against the strongest solvers rather than the field. A response that lands the
main call banks about 45 (recommendation plus instruction-following) before it answers an ask, so
two responses on the call anywhere in the field take both top slots and the build fails: the main
ladder has to keep every response but one off the call, and the asks have to hold both top responses
to about a fifth of the ask weight each (`supplemental-stumping` Part 0). The ten points under the
bar are margin: the on-platform verifiers are not perfectly accurate and the task is **regraded more
accurately after submission**, so a build measuring 48 can regrade past 50 after work has stopped.
Difficulty comes from the honest-data shapes (forecasting, method selection, a binding constraint, a
decomposition, a confirm-the-number, a hold); the flip-the-wrong-number trap is banned.

**The golden deliverables must look business-realistic.** A golden that reads as overly
LLM-generated is sent back even when every figure recomputes. Using an LLM to draft is fine,
shipping its first draft is not, so every golden gets an editing pass. The `golden-realism` skill
carries the per-format passes and the tells a reviewer reads.

**The domains are the client's taxonomy**: seven groups and twenty-one domains, each with its own
task types (`guide-to-prompt/references/domains/README.md`, the `client_domains` block of
`fingerprint/vocab.json`). Product Analytics; Marketing & Consumer Research; Quantitative Finance;
Banking, Credit & Financial Risk; Actuarial Science & Insurance; General Statistics & Data Science;
Biomedical & Clinical Research; Epidemiology & Public Health; Pharmacology, Pharmacoepidemiology &
Safety; Healthcare Delivery & Health Economics; Economics & Econometrics; Political Science & Public
Policy; Sociology & Demography; Psychology & Behavioral Science; Criminology & Justice; Physical &
Environmental Sciences; Energy Systems & Utilities; Human Factors & Ergonomics; Survey Research &
Official Statistics; Urban & Regional Science; Education & Learning Sciences. A build picks one domain,
one task type in it and one objective that task type serves. The nine house domains of the earlier
spec stay valid for every card on file, and a new draw in one of them names the client domain it sits
in.

**Eight Axis 1 objectives.** Forecasting & Predictive Modeling (most wanted), Root-Cause Analysis,
Anomaly Detection & Diagnostics, Experiment & Causal Analysis, Descriptive & Distribution Analysis,
Data Extraction & Conformation (ETL), Opportunity Sizing & Decision Support, and Data Quality
Monitoring & Alerting. The last two are objectives, never domains. Opportunity Sizing earns its tag
when the headline figure is a sized opportunity built up from the addressable pool to what can
actually be realised and that sizing drives the call; Data Quality Monitoring earns it when the
object under analysis is the health of the data or of the pipeline that delivers it and the call is
a monitoring or alerting decision. Either fails its tag if the prompt could be retagged Forecasting,
Descriptive or Anomaly Detection without changing a word (`guide-to-prompt` carries the full
definitions). Nothing else is a valid tag, "Comparative analysis and explanation" included, and a
task tagged outside the eight is rejected on the tag alone.

**Gate G (determinism judge v3) bans surface-read rejection at any depth.** Ship no artifact that
ranks the candidates on the decision question and gets it wrong, however many rungs sit above it.
The one exception is a declared wrong-basis distractor: wrong on a basis a shipped fact rules out, named in
`metadata.json`, and never the stump. Depth is not a defence. The difficulty has to survive deleting every wrong number from the pack.
`.claude/skills/stumping/SKILL.md` Part 1.4 carries the four gaps and the patterns with a measured
record, and Part 2 the readability screen every rung passes before data is cut.

**The committed call is forward facing by default.** The Main Recommendation Ask commits to a
quantity about a window that has not closed. A retrospective ask is legal and needs its reason
written into the design note. This is an ask-shape rule and not a tag rule, so a build keeps its own
objective, and retagging as Forecasting because the window is open is itself a rejection risk.

**Input gates:** 10 or more files, 3 or more distinct formats, either a file of 25,000 or more
rows in any format or a large database file, two or more distractors (files the solution does not use
that look relevant enough that the solver has to weigh them; a completely unrelated file does not
count; named in `metadata.json` and never in a file name), files real and license-clean with source, date and license recorded, nothing that reads as
LLM generated.

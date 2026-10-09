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
| Choosing the domain and objective pairing, **picking the prompt shape that supplies the 25 criteria**, shaping the Main Recommendation Ask, writing the prompt | `guide-to-prompt` |
| Designing, hardening or repairing the trap architecture | `stumping` |
| Designing or hardening the supplemental asks, or the data-quality devices that carry them | `supplemental-stumping` |
| Building or repairing the evidence bundle under `target/` | `dataset-generation` |
| Checking a finished build against the judge's gates, or **forcing an answer to be unique while the build is still being designed** | `determinism-check` |
| Rewriting long-form prose into the user's voice | `humanizer` |
| Checking a build, or a batch, for cloning, templating or duplication | `clone-check` |
| Declaring a bundle ready to ship, or recording a fix that came back from submission | `reduce-house-fixes` |
| Checking a cut pack for anything that hands the solver the answer or the author's intent | `leak-check` |
| Running an in-house solve of a finished build and reading its path against the ladder | `solver-round` |
| Taking a domain and an objective to a delivered task, or resuming a build in flight | `build-pipeline` |

If two apply, invoke both, in pipeline order.

**Five slash commands, all author-triggered:** `/build` (the pipeline), `/approve` (the heart
check and sign-off), `/solve` (a solver round), `/leak-check` (the leak sweeps plus a reader's
pass) and `/clone-check` (the adjudicated corpus comparison). Each spends tokens in isolated
threads except `/approve`, so none runs on the model's own initiative; `/build` is the author's
licence for the stages it sequences.

## The build loop

```
fingerprint recent + coverage   (what the last builds spent, and what has never been drawn)
   ->  guide-to-prompt  (pairing, then the PROMPT SHAPE, with its criteria arithmetic worked to 25+)
       + the two nearest exemplars (guide-to-prompt/references/exemplars/, the client's measured tasks)
   ->  stumping: the draw, decisive rung from traps/_measured.md  ->  fingerprint check + register
   ->  CHECKPOINT A: the author reads the draw and the stump sentence
   ->  the ladder (5 to 6 rungs)  ->  determinism-check (22 axes closed)  ->  supplemental-stumping
   ->  /clone-check   (pre-flight, only when the author asks)
   ->  dataset-generation  ->  build  ->  submission-writeup  ->  golden-realism  ->  reduce-house-fixes
   ->  leak-check (leak.py)  ->  fingerprint surface
   ->  CHECKPOINT B: /approve   (guard.py heart: the stump against every card and ledger row)
   ->  solver round 1 (one plain solver)  ->  harden or pass  ->  solver round 2 (plain + skeptic)
   ->  determinism-check judge rehearsal  ->  /leak-check reader pass  ->  DELIVER to the author
   ->  the author tests on the official portal and reports back
   ->  only then: ledger row, lessons folded into the skills, house fixes, memory
```

`/build <domain> <objective>` runs that loop as a stage machine with `pipeline.json` as its state
(`build-pipeline`), stopping only at the two checkpoints.

The prompt shape is picked **before** the ladder, not after a thin rubric comes back, because it
decides where the criteria come from and it is the cheapest thing in the build to change. The
eighteen shapes and the picker are at `.claude/skills/guide-to-prompt/references/shapes/`.

**The fingerprint guard is mandatory, mechanical and free.** Every build has a fingerprint card in
`.claude/skills/fingerprint/cards/`, and `guard.py` checks a new draw against all of them: the
Part 6.1 standing bans against the last three builds, the same-puzzle test against the last twelve,
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

**The portal is the stump oracle; the solver rounds are the filter in front of it.** The author
tests the build on the official portal and reports the result, and that report is the only stump
evidence the ledger records. Before it, a finished build goes through two in-house solver rounds
(`solver-round`): one plain solver that sees only the prompt and the bundle, then plain and skeptic
together. A build a plain solver cracks never goes to the portal; a build no solver cracks still has
to. Rounds run only through `/solve` or the `/build` pipeline, never as an ad hoc "quick sanity
solve" in the main thread, because a solve that has read the design note measures nothing. The
written test of stump power stays: **name the stump in the design note** before the pack is cut, the
wrong committed answer a competent solver files and the step that lands them there. A ladder whose
author cannot write that sentence has no stump in it, and no round is run on it.

**`/clone-check` is author-triggered only**: never invoke it on your own initiative, including right
after applying a patch that seems to want validation, because it spends real tokens in an isolated
thread. `/approve` runs the cheap mechanical half of the same question (`guard.py heart`) and is
where a template or duplicate is caught before any solver is paid for.

`/clone-check` also runs on a plain request, so a chat asking for a clone check, a template
check or a duplicate check invokes it. It compares a build, or the whole batch, against every
other build, the way the final_verdict reviewer does, and it separates what a reviewer can see
(prompt wording, file names, schemas, the data itself) from what only the design notes show
(the gap, the pattern, the decisive rung). Reusing a proven trap device is legitimate and the
check says so out loud. What it hunts is a repeated driver, meaning the same insight carrying
the stump twice, which is a clone however far apart the two surfaces sit. Run it in pre-flight
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
`pipeline.json` (state, never reasoning), `solver_rounds/` and the `leak_check_report.md` and
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

The client's requirement is that every prompt feel different. Their note names the shape to avoid:
*"I'm a X working at Y. Here's some context. Give me this main recommendation and here are the two
deliverables that I need from me."* Prose, first person, one committed call, one to three
deliverables, unit and rounding inside the sentence and 25 or more criteria off the prompt shape all
hold; what is banned is a fixed skeleton, context in two or three sentences and then one paragraph
per deliverable in the same order every time.

**Before writing or editing any prompt, read
`.claude/skills/guide-to-prompt/references/prompt-voice.md`.** It carries the twelve opening moves
derived from the client's own 72 worked prompts, the table that separates spec-mandated wording
from wording that is merely our habit, and the structural axes (length, file count, format mix)
that rewriting an opening does not fix. Then run
`python3 .claude/skills/guide-to-prompt/references/voice-check.py <task number>` on the draft, and
bare over the batch before submission. Self-report does not catch a calcified voice; `grep` does.

## Current spec

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
and separately determinate. One deterministic recommendation anchors everything.

**The prompt is prose, first person, the way you would write to a colleague.** No bracketed blocks,
no `file.ext (Family)` headers, no bulleted asks. What costs you is a **roll call** of colleagues'
opinions, which is a design defect rather than a style one, because each named opinion hands the
solver a rung to refute.

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

**Nine accepted domains.** Product Analytics, Supply Chain & Logistics, Economics, Policy &
Education, Demographic & Social Science, Nonprofit & Grant-making, Marketing & Consumer Research,
Business & Operations Analytics, and Accounting, Audit & Forensic Analytics. Biology, Biostatistics,
Epidemiology & Bioinformatics is not an accepted domain, so do not start a build there.

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
`.claude/skills/stumping/SKILL.md` Parts 1 and 2 carry the four gaps and the five patterns that
pass.

**The committed call is forward facing by default.** The Main Recommendation Ask commits to a
quantity about a window that has not closed. A retrospective ask is legal and needs its reason
written into the design note. This is an ask-shape rule and not a tag rule, so a build keeps its own
objective, and retagging as Forecasting because the window is open is itself a rejection risk.

**Input gates:** 10 or more files, 3 or more distinct formats, either a file of 25,000 or more
rows in any format or a large database file, two or more distractors (files the solution does not use
that look relevant enough that the solver has to weigh them; a completely unrelated file does not
count; named in `metadata.json` and never in a file name), files real and license-clean with source, date and license recorded, nothing that reads as
LLM generated.

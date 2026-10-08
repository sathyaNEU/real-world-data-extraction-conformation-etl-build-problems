---
name: guide-to-prompt
description: Decide what to ask before writing a word of the prompt. Pick one Axis 0 domain and one Axis 1 analytical objective from the canonical taxonomy, shape a forward-facing Main Recommendation Ask, pick the prompt shape that supplies the generated rubric's 25 or more criteria, then write the prompt as prose, first person, one committed call, and one to three named deliverables with uncapped multi-dimensional asks that cover unit and rounding. Every prompt has to read differently, so references/prompt-voice.md carries the twelve opening moves, the requirement-against-carrier wording table and the structural axes, references/voice-check.py measures the batch, and no prompt follows a fixed "I run X at Y, here is the context, here are the two deliverables" skeleton. The prompt is also concise, with no yapping and no narrated context, and references/prompt-economy.md carries the measurement against 25 paid-out prompts (227 words and 21.6 per sentence against our 404 and 31.4, with their 334-word maximum below our median), the four places our words actually go, the seven compression moves that keep every requirement, and the budget the script's ECONOMY block checks as a target plus a flag. The references/shapes/ library holds the client's eighteen prompt shapes with 72 worked prompts, and the per-objective files carry each objective's definition and the shapes that carry it. Every worked prompt is an idea seed that is never copied into a build, and every draw is checked by the fingerprint guard before the ladder is written. Use at the start of every task build, before the stumping skill designs the ladder, and when an existing draft needs its pairing checked or its ask reshaped.
---

# Choosing What To Ask

> ## The prompt is concise
>
> **The prompt has to be concise.** No yapping, nothing lengthy, nothing that reads as LLM
> generated, and not too much context about the work. Straightforward.
>
> That is not a style note layered on the spec. It is the one difference that shows up on every
> axis at once when 25 prompts the client paid out on are measured against the current window:
> **227 words against 404, 21.6 words per sentence against 31.4, 1.5 commas per sentence against
> 2.1, and 0.8 subordinating connectors per hundred words against 1.5.** We are 78 per cent longer
> and our individual sentences are 45 per cent longer, which means the extra words are not one
> deletable section. They are in every sentence, and the paid-out maximum of 334 words sits below
> our median.
>
> **The context paragraph is not the prize, and this is the one that misleads.** Ours runs 95 words
> against their 53 and is **the same share of the prompt** (22.8 per cent against 22.4). It is 22
> per cent of a prompt that is 78 per cent too long. Cutting the organisation bio and the pack
> inventory is right because they grade nothing, but it does not reach the budget on its own.
>
> **Concise never means asking for less.** The paid-out set carries the
> full repeated structural unit, the runner-up, the gap, the flip condition, the chart's parts and
> the rounding coverage, in a quarter fewer words, because it compresses per sentence rather than
> asking for less. Reading "shorter" as "ask for less" trades a realism finding for a Gate E or a
> 25-criteria finding, which is the worse trade in both directions.
>
> **Read `references/prompt-economy.md` before drafting, next to `references/prompt-voice.md`.**
> It carries the measurement with its spread, the four places the words actually are (the sentence
> that will not end, the reason clause hung on every ask, the rounding tag repeated per figure, and
> the narration in the context paragraph, in that order because that is the order the measurement
> supports), the seven compression moves that keep every requirement, and the budget as a target
> plus a flag. `voice-check.py` prints an **ECONOMY** block that measures all of it, because a rule
> here bites only when the script counts it: asking for shorter prompts in prose brought the median
> down from 575 words to 404 while words per sentence went **up**.
>
> **Draft at whatever length the ideas arrive in, then compress**, then run both halves of the
> gradability check: walk the figure list, and re-count the criteria off the shape's arithmetic.
> Writing short from the first keystroke is how requirements go missing.

> ## Every prompt reads differently
>
> The client's note: *"Right now the majority of prompts are following the same exact voice and
> structure. 'I'm a X working at Y. Here's some context. Give me this main recommendation and here
> are the two deliverables that I need from me.' Let's try to switch it up and make every prompt
> feel different."*
>
> **The contract is fixed and the surface varies.** Prose, first person, one committed call, one to
> three deliverables, uncapped multi-dimensional asks, unit and rounding inside the sentence, 25
> or more criteria off the prompt shape. The **surface** is a review-visible property of the
> batch, and a batch that collapses to one template is sent back.
>
> The evidence is measured, not asserted. Across task66 to task83, the eighteen builds drafted
> under the prose spec: **17 of 18 open in first person with a role verb in clause one**, **12 of
> 18 open with the literal words "I run"**, **18 of 18 ship a PDF**, **16 of 18 ship three files**
> when three is the ceiling and two is the library norm, and ten live formats have never been used
> once. Ten of eighteen close their chart ask with "and a title that states".
>
> **Three things follow.**
>
> - **Read `references/prompt-voice.md` before drafting any prompt.** It carries the twelve
> opening moves derived from the client's own 72 worked prompts, the requirement-against-carrier
> table that separates what is spec from what is merely our habit, and the structural axes (length,
> file count, format mix) that a rewritten opening does not fix.
> - **Run `references/voice-check.py`**, once with the draft's task number and once bare over the
> batch before submission. Eighteen builds passed a self-reported checklist here. They would not
> have passed `grep`, which is why the check is a script.
> - **There is no prescribed skeleton**, here, in the shape files or in `../stumping/SKILL.md`
> Part 7. If you are working from a memory of "context, two or three sentences, first person,
> ending on the decision", drop it.
>
> Everything the note does **not** license is in `references/prompt-voice.md` section 9. The short
> version: first person survives, the asks keep their units and their rounding, and an opening move
> that misrepresents the decision to look novel is worse than a familiar one.

> ## The spec in brief
>
> Every step below carries these.
>
> - **One to three deliverables, three the ceiling, and no format family is assigned.** A
> four-file set is a spec failure on the count alone. Pick the one to three files a real analyst
> would actually produce for this decision, and **prioritize a visual** wherever it makes the call
> read at a glance. A table can live inside a memo rather than taking a slot of its own.
> - **The asks are uncapped and untargeted, and each one has to be multi-dimensional and hard.**
> There is no per-file floor. One ask can span many rows, periods or cuts and still resolve to one
> defensible answer, and that is the ask you want. Unit and rounding are stated inside the
> sentence that asks for the figure.
> - **The prompt is prose, first person, the way you would write to a colleague**, never a block of
> `file.ext (Family)` headers with bulleted asks underneath. What costs you is the roll call of
> colleagues' opinions, because it hands the solver the ladder as a refutation checklist.
> - **The rubric has to reach 25 or more criteria, and it gets there through the prompt shape.** A
> one-to-three file prompt is a small surface, so the criteria come from the structure of the
> answer: a ranked list under a cap, a bridge between two totals, a grid of cells, a forecast
> across many periods. Eighteen shapes with 72 worked prompts are in `references/shapes/`, and the
> picker there carries the criteria arithmetic. Never stack simple asks to reach 25.
> - **The bar is the top two responses averaging under 50 percent, with at least one model
> genuinely stumped.** The two conditions are conjunctive. **Build to 40, not to 50**: the
> on-platform verifiers are not perfectly accurate and the task is regraded more accurately after
> submission, so a build measuring 48 can regrade past the bar after work has stopped. A response
> that lands the main call banks about 45 before any ask (the recommendation block plus
> instruction following, at the planning weights), so two responses landing the call anywhere in
> the field take both top slots and fail the build. At most one response may land it, which puts
> the ladder on the critical path of the average as well as of the stump condition.
> - **The rubric weights:** 30 to 40 percent on the recommendation and its critical components, 5
> to 10 percent on instruction-following, about 55 to 60 percent on the asks.
> - **The roster and the input gates:** six domains, eight objectives, 10 or more files, 3 or more
> formats, a file of 25,000 or more rows in any format, or a large database file, at least one
> distractor named in `metadata.json`, real and license-clean with source, date and license
> recorded, nothing that reads as LLM generated.
>
> The eight objectives include **Opportunity Sizing & Decision Support**, which the client's
> example page also uses as a filter, and **Data Quality Monitoring & Alerting**; both are
> objectives, never domains. The page also tags two examples "Comparative analysis and
> explanation", and **that is not a valid Axis 1 tag here**: a task tagged outside the eight is
> rejected on the tag alone.

> ## The committed call faces forward
>
> The client's announcement (carried in full at `guidelines/prompt_guide.md`, section "Updated
> Announcement") says the strong models are hard to stump with current techniques, and its steer
> is about the **shape of the committed call**, not about the taxonomy: ask for a **prospective
> or predictive** recommendation rather than a retrospective one, so the analyst has to commit to
> a quantity
> about a window that has not closed, and keep the ask landing on a business recommendation
> rather than on a bare number.
>
> **What it means.**
>
> - **Default the Main Recommendation Ask to a forward-facing commitment.** The canonical form
> is "the one figure we file, book, obligate, order or staff for the period that has not closed
> yet", or "the one option we commit the coming cycle to", not "what happened last quarter".
> A retrospective ask is legal and needs its reason in the design note.
> - **It does not change the Axis 1 tag, and retagging on this basis is a rejection risk.**
> The objective is a claim about what the analyst has to *produce*. A Data Extraction &
> Conformation build whose committed figure is an accrual, a
> certification or an obligation for an open period is still ETL, because the work is
> reconciling multi-source inputs into a contract-conforming dataset. A Descriptive build whose
> figure sets next cycle's threshold is still Descriptive. Only retag as Forecasting when the
> answer is genuinely **a predicted value the supplied history pins down**, which is the test in
> step 2.
> - **Forecasting & Predictive Modeling is the most wanted objective and the tiebreak.**
> - **Where the forward window is not a forecast, say so in one clause of the design note**, so
> the review reads the classification instead of guessing it, exactly as Gate G's flags work.
>
> **What it does not license.** It does not license a prompt clause that fixes the horizon, the
> basis or the population, because the prompt still outranks every shipped file. The forcing
> event can carry the period ("this cycle", "the close on Thursday", "before the coming award
> year opens"), and the convention that decides how the period is
> measured still lives in a shipped file or in the calibration corpus.
>
> The announcement's example questions are in `guidelines/prompt_guide.md`. Read them as
> **shapes** and instantiate them, they are not asks to lift, and several of them sit in domains
> outside the six.


> Every task carries **one domain** and **one Axis 1 analytical objective**, chosen before you write a word of the prompt. Work the four steps in order, save the pairing, and the rest of the build carries it.

Labels come straight from the canonical taxonomy. Do not rename them and do not invent new ones. This skill decides *what the decision is*. The `stumping` skill decides *why it is hard*, and `dataset-generation` builds the evidence that makes it deterministic. Run them in that order.

---

## The reference files, and the rule that governs every example in them

| You are working | Load | Contains |
|---|---|---|
| **Fixing the draw, before the prompt or the ladder** | **`references/exemplars/index.md`, then the two nearest entries in the domain's file** | **The client's own 49 accepted tasks with the current model's measured mean: prompt verbatim, deliverables, inputs, solution, the model's miss. The voice and the architecture the client pays for, measured rather than argued.** |
| Choosing or checking a domain | `references/domains/<domain>.md` | The domain's typical decisions and data, its enumerated subdomains, and its boundary rules. It carries no examples. |
| **Choosing where the 25 criteria come from** | **`references/shapes/README.md`, then the one shape file** | **The eighteen prompt shapes: what each is, where its criteria come from, how to size it past 25, what makes it hard rather than long, and four worked prompts each. Load the picker, then exactly one shape.** |
| **Writing the prompt, once the shape is picked** | **`references/prompt-voice.md`, and `references/voice-check.py` over the batch** | **The twelve opening moves and what each one needs to be true, where the role sits, the requirement-against-carrier table, the structural axes (length, file count, format mix), and the per-build and per-batch checks. Required reading, because the worked prompts in the shape files are where a single voice gets picked up.** |
| Shaping the ask for a fixed objective | `references/objectives/<objective>.md` | The objective's canonical definition and the shapes that carry it natively. Its worked prompts live in `references/shapes/` |
| Designing the trap, once the pairing is fixed | `../stumping/references/traps/<objective>.md` | Model failure modes on that objective, stated as how the model fails. Read `_cross-objective.md` alongside it |

**The examples are idea seeds, never material.** This is a standing rule and it is
rejection-level, because a lifted scenario is a clone and the review reads it as one. Read a
few examples to see what a task in the objective can be about and how a finished prompt
reads, then draw a fresh domain, subdomain, entity, metric and decision of your own through
the fingerprint guard (`../fingerprint/SKILL.md`) and the anti-clone draw in
`../stumping/SKILL.md` Part 6.1. Nothing transfers from an example into
a build: not the scenario, not the entity, not the metric, not a file name, not the wording
of an ask. What transfers is the **shape**, and only the shape.

**The example library is `references/shapes/`.** It organizes the client's 72 worked prompts by
prompt shape rather than by objective, because the shape is what supplies the 25 criteria. The
per-objective files carry each objective's definition and its shapes.

**Domains** (`references/domains/`): `product-analytics` · `supply-chain-logistics` · `economics` · `policy-education` · `demographic-social-science` · `nonprofit-grant-making` (Biology, Biostatistics, Epidemiology & Bioinformatics is not an accepted domain)

**Objectives** (`references/objectives/`), eight and only eight: `forecasting-predictive-modeling` · `root-cause-analysis` · `anomaly-detection-diagnostics` · `experiment-causal-analysis` · `descriptive-distribution-analysis` · `data-extraction-conformation-etl` · `opportunity-sizing-decision-support` · and Data Quality Monitoring & Alerting, which has no reference file: its definition and test are in Step 2 below

---

## Step 1. Choose one domain

Six accepted domains. Pick the one whose **decision-maker would actually own the call**, which is a better test than which sector the data came from, because a census extract can sit under Demographic & Social Science or under Policy & Education depending on who is deciding.

1. Product Analytics
2. Supply Chain & Logistics
3. Economics
4. Policy & Education
5. Demographic & Social Science
6. Nonprofit & Grant-making

Anything outside these six does not qualify, however good the data is, and that includes Biology, Biostatistics, Epidemiology & Bioinformatics. Open the domain file, pick one **enumerated subdomain**, and if your trap needs a subdomain that is not listed, change the trap rather than stretching the scope.

## Step 2. Choose one Axis 1 objective

**Eight objectives, and exactly one per task**, in every domain. Open the objective file and read
its definition and a few worked prompts from the shapes it points to before you decide, because
the objective is a claim about *what the analyst has to produce*, not about the subject matter.

| Objective | The decision turns on |
|---|---|
| **Forecasting & Predictive Modeling** | A future value or predicted outcome that the supplied history can pin down |
| Root-Cause Analysis | Naming the driver of a move, with rival explanations ruled out on evidence |
| Anomaly Detection & Diagnostics | Separating a real event from an artifact |
| Experiment & Causal Analysis | A causal claim, from a designed test or from observational data with confounders |
| Descriptive & Distribution Analysis | How a population is composed or how a metric is distributed, not on why it moved |
| Data Extraction & Conformation (ETL / Pipeline Build) | Reconciling messy multi-source inputs into one analysis-ready, contract-conforming dataset |
| Opportunity Sizing & Decision Support | A sized opportunity (addressable volume, value at stake, headroom or recoverable value), built up from the addressable pool to what can actually be realised, that drives a committed decision |
| Data Quality Monitoring & Alerting | The health of the data or of the pipeline that delivers it, not a business metric, with a monitoring or alerting decision as the committed call |

**Nothing outside the eight is a valid tag**, and a task tagged outside them is rejected on the tag
alone, so check this before anything else. In particular, the client's example page tags two
examples **"Comparative analysis and explanation"**, and that is not an Axis 1 label here.

**The two newest objectives each carry a discriminating test**, because each sits next to older ones
it is easily confused with. Both tests are here, and `references/objectives/opportunity-sizing-decision-support.md` carries the first in full. **Opportunity Sizing & Decision
Support** earns the tag only when the headline figure is a sized opportunity built up from the
addressable pool to what can actually be realised and that sizing drives the committed decision: if
the prompt could be retagged Forecasting or Descriptive without changing a word, it does not earn
the tag. **Data Quality Monitoring & Alerting** earns it only when the object under analysis is the
health of the data or of the pipeline that delivers it (freshness, volume, completeness, schema,
contract or SLA breach, check coverage, alert routing) and the committed call is a monitoring or
alerting decision: if the prompt could be retagged Anomaly Detection or Forecasting without changing
a word, it does not earn the tag. Both are objectives, never domains, so the build still draws its
domain from the six.

The eight cover more than their names suggest. A like-for-like comparison, a binding constraint, a
sizing exercise and a monitoring rule can each be the substance of a task; they just sit under one
of the eight labels. A comparison that names a driver is Root-Cause Analysis, one that separates an
event from an artifact is Anomaly Detection, a sizing exercise whose answer is a projected quantity
is Forecasting, one that builds a sized opportunity up to what can be realised and commits on it is
Opportunity Sizing & Decision Support, and a monitoring rule over the data or its pipeline rather
than over a business metric is Data Quality Monitoring & Alerting.

**Forecasting & Predictive Modeling is an objective, not a domain.** Any accepted domain
can carry it when the supplied evidence pins the answer down, and it is the objective the client
most wants, so it is the right tiebreak whenever the evidence can pin a future value.

If two objectives fit equally well, the decision is probably not deterministic yet, so sharpen the
ask until one of them clearly owns it.

## Step 3. Settle the close calls

Two boundaries decide most disputes, and both are canonical.

**Demographic & Social Science or Biology?** Biology is not an accepted domain, so this boundary matters in one direction only: population characteristics or social conditions read from census, survey, or administrative data belong in Demographic & Social Science, and a study centred on biological mechanisms, biomedical study data, epidemiology, genetics or bioinformatics has no valid domain, so redraw it rather than stretching Demographic & Social Science to hold it.

**What counts as Economics?** In scope: macro, labor, trade, and fiscal reads. Out of scope: corporate finance, markets trading, and lending underwriting.

One more that comes up in practice: a platform selling into a sector is Product Analytics with that sector's data as its addressable market (see `dataset-generation` section 1).

## Step 4. Save the pairing, then check it against what you have already built

Write the domain, the subdomain, and the objective into `DATASET_NOTES.md` before generating anything, and carry the same pairing into the submission tags and Axis 2.

Then run the anti-clone check while it is still cheap, because the pairing is the cheapest thing to change. A pairing you have shipped before is not banned, but the domain, the stakeholder role, the artifact type, the calibration form and the decisive mechanism must not all repeat. The check is mechanical and free: `python3 .claude/skills/fingerprint/guard.py recent` and `coverage` before you choose, then `guard.py check` on the draw card once the ladder's draw is fixed in `stumping` Part 6.1 (`../fingerprint/SKILL.md` carries the whole procedure). The cards cover every build on disk, including builds finished but not yet reported on the portal, which the shipped ledger cannot see because it only gets a row once the author reports the result. The adjudicated `/clone-check` is author-triggered and is not part of this step.

**Axis 2 applies.** Tag the reasoning phases: Explore/Discover, Hypothesize, Analyze/Validate, Synthesize, Recommend/Communicate. Ideally all five, and a task that only exercises the last two is a memorization test.

---

## The prompt shape

The prompt is **prose**, written the way you would write to a colleague, not a bulleted spec.
Everything below says what the prose has to **contain and do**. It deliberately does not give you
an order to put it in, because a fixed order is what makes a batch read as one template.

| The prose has to | Which means |
|---|---|
| Put a real person behind the request | First person, with the role somewhere in the context. Not necessarily in the first clause, and the client's library puts it mid-paragraph and last as often as first |
| Say what forces the call now | The meeting, the filing, the deadline, the cycle that opens. One clause, wherever it lands |
| Carry the standard the call runs on | Only where the pack does not carry it, and never in a form that fixes the basis, the window or the population |
| Commission one to three named files | In whatever order the reader would actually meet them, which is not always memo, then chart, then workbook |
| Ask for figures that are gradable | Every figure's unit and rounding covered, the convention stated once for a block and pinned per figure only where the figure's type does not already fix it |
| Say it in about 227 words | The paid-out median. Every requirement above survives compression; the narration between them does not |

**Then read `references/prompt-voice.md` and pick the opening move, the ordering and the carrier
wording deliberately.** That file carries the twelve opening moves derived from the client's 72
worked prompts, the requirement-against-carrier table that says which phrases are spec and which
are ours, and `voice-check.py`, which measures the batch. Skipping it is how eighteen consecutive
builds opened with "I run".

**Then read `references/prompt-economy.md` and compress.** Voice and economy are different
defects and the script measures them separately: a prompt can open on a move nobody has used,
ship an unused format, and still run at 480 words with 31-word sentences, which is where every
build in the current window sits.

There is no bracketed block of `file.ext (Family)` headers with bulleted asks underneath, and
nothing about what has to be **gradable** is relaxed for it. Every figure names its unit and its
rounding inside the sentence that asks for it, the way a person writing to a colleague would: "their gap on <metric> in <that metric's own unit>", "one bar per
<component> labelled in whole <units>", "as a percentage to one decimal place".

| Part | Requirement |
|---|---|
| **Context** | First person, with the role somewhere in it, the forcing event, and the standard the call runs on where the pack does not carry it. Short. There is no prescribed length, no prescribed opening and no prescribed order, and `references/prompt-voice.md` carries the moves to choose between. |
| **Main Recommendation Ask** | Exactly one committed call, and a reader has to be able to **quote it as one whole sentence**. It may close the context or open the first deliverable paragraph, but it may not be carried by a colon-appositive, by an anaphor ("the figure goes first"), or by a sentence whose subject is who owns the figure. Run the hierarchy read below before you call the draft done. This is what `stumping` operates on, it anchors 30 to 40 percent of the generated rubric, and it is what the client's own prompt review checks first. |
| **Deliverables** | **One to three named files.** No format family is assigned. Prioritize a visual wherever it makes the decision read at a glance. |
| **Asks** | Uncapped and untargeted. Each one multi-dimensional and hard: a single ask can span many rows, periods or cuts and still resolve to one defensible answer. |
| **Golden Solution** | Every file the prompt asks for, in the requested format, each answering its own requests correctly and consistently with the others. Not an LLM-looking artifact. It must satisfy every positive criterion of the generated rubric. |

### First person, yes. The same first sentence eighteen times, no.

**First person is the contract.** What the client sends back is narrower and it is ours, not
theirs: the role verb in sentence one, clause one, which opened 17 of 18 consecutive builds, with
"I run" literally opening 12 of them. The client's own library states the role in the opening clause, mid-paragraph after the
decision is already on the table, as a short sentence of its own ("I own monetization."), and as
the last line of the context ("I own supply resilience."), and it opens as often on the rule, the
constraint, the deliverable, the question or the number as on the person asking.

So: **first person, role present, position deliberate.** `references/prompt-voice.md` carries the
twelve opening moves with the condition each one needs, and the rule that the move is taken from
what actually forces this decision and then checked against the last three builds.

What costs you is the **roll call**: a parade of colleagues' opinions staged in the context
("my deputy wants A, our finance manager wants B, the western regional manager blames C"). That
is not a voice problem, it is a design problem. Each named opinion is a rung handed to the solver
as a checklist of things to refute, so the ladder arrives pre-framed and the work of finding the
candidates disappears.

**One stakeholder belief, as one clause, is fine and is often useful.** "The growth lead reads it
as a stickier product" is a licensed decoy belief that adds pressure the solver has to overcome
with evidence. One belief, stated as a belief, never a computed ranking, and never a survey of the
whole room. The full advocate structure, when a build needs one, lives in the pack's social layer.

### The hierarchy read, and the rejection it prevents

**The client's prompt review checks, before it looks at anything else, that the prompt resolves to
one deterministic recommendation.** A prompt that fails it is rejected on the prompt alone, with
the analysis never examined. This is the single most repeated finding against this repo's builds,
and it has never once been a finding about the analysis.

**It fails on hierarchy, not on inventory.** The spec puts about fifty-five to sixty per cent of
the score on the asks, so a compliant prompt is one committed call plus a large supporting layer, and nearly
all the words are in the supporting layer. Written straight down the page, the call ends up
structurally indistinguishable from the outputs that exist to hold it up, and a reviewer reading
at speed sees a reporting pack. The call is usually right there in the prose. It is just not
findable in one read.

**The three reads.** None of them involves a figure, and a prompt failing any one of them reads as
a list of outputs however well the call itself is worded.

**They test findability, not position.** The call may close the context or open the first
deliverable paragraph, and no order is prescribed, so what fails read 1 is a call a reader has to
assemble, never a call in the wrong slot. Applying it as "every context ends on the call" would
make the ending a structural fact of every build, which is the monoculture the voice rule exists
to prevent.

1. **The call is a whole sentence at the seam between the context and the first deliverable**,
   carrying its unit and rounding, on whichever side of the seam you put it. Not the basis, not who
   owns the figure, not what the meeting is for.
2. **The clause saying what the committing file leads with names exactly one quantity.** A comma
   series there reads as several recommendations rather than one with its detail underneath.
3. **Every paragraph after the first opens by tying back to that quantity**, not on a bare
   commissioning verb. "Build me the deck" starts a new output. "That number goes to the board on
   slides, so build me the deck" continues the one you already have.

**A fourth read, and grammar cannot fix this one.** The three above are about how the prompt
reads. Ask separately whether each supporting ask's **answer** is a component of the committed
call, a direct qualifier of it (its sensitivity, its flip condition, its reconciliation to another
total), or the trail that audits it. An ask a person could act on with the committed call still
unmade, a figure for another period, another population's exposure, a call about a different
action, is a second decision sharing a deck, and it draws the same rejection for a reason no
reordering touches. Run it on the ask's answer, never on the sentence that introduces it, because
that sentence is exactly what hides it. This is `../reduce-house-fixes/SKILL.md` H18, the repair is
to retire the ask and win the criteria back inside the decision (a second measure on each candidate
that the call does not turn on, an audit trail, a reconciliation), and it is cheap before the data
is cut and expensive after, which is why it belongs here rather
than only at ship time. The ask layer is also decoupled from the main call by default
(`../supplemental-stumping/SKILL.md`, Decoupled asks), which is independence of difficulty
and passes this read: draw the asks from the case's other measures, its audit trails and its
reconciliations, computed off the main trap's path, and treat sensitivities, flip conditions and
denser splits of the committed figure as coupled, because a solver who cracks the trap gets them free.

`references/voice-check.py <task number>` prints the inputs to the first three reads under
HIERARCHY READ and flags a bare commissioning opener. It does not judge reads 1 and 2, because whether a sentence is
the call is not something a regex can decide, so read them yourself off what it prints.

**The specimen, because the defect is invisible until it is set beside its repair.** Both of these
commission the same two files and ask for the same figures to the same rounding.

> *Fails.* ... so the figure that sizes the slate is mine to put in front of them: the most the May
> docket can commit, in whole dollars. ... I want the figure our budget policy supports.
>
> The board runs the meeting from slides, so build me `x.pptx`. The figure goes first, with the
> priority area that has the least room left against its allocation and that room in whole dollars.

The call is hanging off a colon inside a sentence about who owns it, the context then closes on the
basis, "the figure" arrives as an anaphor with no antecedent naming it as the recommendation, and
the second paragraph opens on a commissioning verb.

> *Passes.* ... so the figure that sizes the slate is mine to put in front of them, and the board
> votes the slate against it, so it has to be one number I can defend line by line, not a range.
> ... The one thing I need from you is the most the May docket can commit, in whole dollars.
>
> That number goes in front of the board on slides, so build me `x.pptx`. It opens on the figure,
> and everything behind it is there to defend it, starting with the priority area that has the
> least room left against its allocation and that room in whole dollars.

Not one ask changed, not one unit moved, and the repair is grammar and paragraph order.

**Take the move, never the sentence.** "Everything behind it is there to defend it" is one carrier
for the bridge and the carrier table already logs a near neighbour of it at 3 of 18. Written into
the next eighteen builds it stops being a repair and becomes the template, which `voice-check.py`
will flag and a batch reviewer will read as one prompt. Say who asks for each piece and why, or
name what the deck has to survive, or let the asks stand on their own order.

**The remedy the review proposes is not the repair, and following it fails the build a different
way.** The finding usually arrives suggesting you cut to a single output. Do not. The supporting
layer carries the score, the criteria come from its structure, and dropping a deliverable or
softening an ask into background prose takes the rubric under its 25-criteria floor, which is a
worse failure than the one being answered. Reviews have been seen passing the deliverable count on
one check and demanding a single file on another in the same pass, which is the tell that the
finding was about legibility all along. Fix the hierarchy and keep the files.

**Where the line falls.** This is about the prompt's grammar, never about what the pack pins. The
repair moves sentences that carry stated grain, ordering, basis and precision, so re-read every
clause it touches: a blanket convention that governed all the asks has to stay above all of them,
and sharpening the call must not name the basis, the window or the population, which would trade a
shape finding for a determinism finding. `../reduce-house-fixes/SKILL.md` H13 carries the same
defect as a ship-time entry.

### The deliverable spec

**Count. One to three.** Three is a **ceiling**, not a floor, and a four-file set is a spec
failure on the count alone. One file is legal and two is the observed norm across the client's
library.

**No format family is assigned to you.** The families exist as a way of thinking about variety
and about what a stakeholder actually reads, but nothing requires the set to span two of them and
nothing assigns you a pair.

| Family | Formats (examples, not a fixed menu) | What it is for |
|---|---|---|
| Data | CSV, TSV, JSON, XLSX, Parquet | Tables and records somebody keys off or audits |
| Visual | PPTX, PNG, SVG, HTML, JPG | Charts, decks and rendered pages a stakeholder reads first |
| Text | PDF, DOCX | The memo, brief or determination that commits to the call |
| Code | PY, IPYNB, SQL, R | A script or notebook that runs and prints the answer |

**Pick the files a real analyst would actually produce for this decision, and be honest about
it.** `analysis_report.pdf` is not the best-suited deliverable for every task. A forecast may call
for a runnable script, a certification for a CSV, a board decision for a short memo. Match the
format to the work rather than reaching for the same pair every build, which is also what the
clone check reads.

**Prioritize a visual where it genuinely helps.** A visual is not mandatory. It is what a
stakeholder reads first, so reach for one wherever it makes the decision read at a glance: a
chart, a waterfall, a matrix, a heatmap, a tree, or a table. A criteria-dense visual is also one
of the cheapest honest routes to a wide rubric, because naming its parts (the chart type, each
series, the ordering, a labelled threshold line at its value, an annotation on the key point, and
a title that states the finding) is worth five to seven criteria where "include a chart" is worth
one. **Name all of them in one sentence, in that order, with no reason attached to any of them.**
The paid-out set carries the same parts and spends a sentence on them where we spend a paragraph;
the parts earn the criteria and the narration between them earns nothing.

**A table does not have to be a separate file.** It can live inside the memo, inside a workbook,
or be printed by a script. Do not spend a deliverable slot on a table that the memo should have
carried; with a ceiling of three, slots are scarce.

**A `.py` is welcome and is the cleanest way to make a figure recomputable**, because
a script prints the graded numbers rather than transcribing them and a reviewer can rerun it.
Where a text deliverable needs a chart, the chart is produced by code, never described in
words. Name each file after the decision, not after the analysis.

### Reaching 25 criteria, through the shape

The rubric is generated, and it has to reach **25 or more criteria** before the task advances. A
one-to-three file prompt with a handful of asks is a small surface, so the criteria come from
**the structure of the answer**.

That structure has a name, and the name is the **prompt shape**. A ranked list under a cap grades
every candidate's score. A forecast across many periods grades every period. A grid grades every
cell. A bridge grades every reconciling item. The criteria are already in the shape of the answer,
and the prompt's job is to ask for them.

> **Load `references/shapes/README.md`, pick the shape whose structure your data and decision
> already have, then load that one shape file.** Eighteen shapes are documented, each with where
> its criteria come from, how to size it past 25, what makes it hard rather than merely long, and
> four worked prompts. They are ideas rather than a fixed menu: a different structure that earns
> the criteria honestly is fine, and the arithmetic in the picker is the discipline.

Size the shape on paper, before a file is generated. The arithmetic is always the same: **one
repeated structural unit, times the number of times it repeats, plus the decision furniture.**
Ten to twenty units, optionally doubled by a second figure on each unit, plus the committed call,
the runner-up, the gap, the flip threshold, the named chart parts, and the files themselves. If it
lands under 25, the fix is a **denser structure**, more units or a second figure per unit, and
never more asks bolted on the side. Over 25 is fine and uncapped.

**The shape is not the mechanism.** It decides where the criteria come from; `../stumping/SKILL.md`
decides why the task is hard, and the bar requires at least one model genuinely stumped.
Each shape file carries a "what makes it hard rather than long" section, and that section is the
seam where the shape meets the ladder. Work the shape without it and you get a wide, easy task the
whole field answers, which fails the average bar from the other direction.

### The same contract, three surfaces

**One decision, shown three ways**, to make the point that the contract is fixed and the surface
is not. A single worked example becomes a template: the calcified-carrier counts in
`references/prompt-voice.md` trace an eighteen-build monoculture almost sentence for sentence to
one example's wording.

Three is not a menu of three. It is a demonstration that the same requirements survive any
ordering, and the move you use comes from what forces your decision, not from this page.

**A. Rule-first, chart commissioned before the memo, role in the second sentence.**

> The cut rule has not changed: the category that goes is the one whose removal gives the
> strongest defensible improvement in continuing-portfolio economics, not the one with the
> weakest quarter. I run category planning, and Q3 came in under plan, so exactly one category
> comes out of the next buying cycle.
>
> Put the picture in front of the board first, `category_cut_margins.png`: one bar per category on continuing-portfolio
> margin, best cut to worst, before and after the removal, the cut category and the runner-up
> labelled, the flip threshold as a line at its value, titled with the call in words.
>
> The report behind it, `category_cut_decision.pdf`, opens on the category we cut, the strongest one it beats, and what
> the removal does to continuing-portfolio margin in percentage points to one decimal place. Then
> every category in that same order with revenue in whole USD and both margins as percentages to
> one decimal place, tying to the portfolio figure, and close on the threshold that flips it and
> the one evidence-backed change that would put the runner-up first.

**B. Deliverable-first imperative, one file, role last.**

> One file, `q4_category_cut.pdf`, and it does all the work. It has to open on
> the category we are cutting from the next buying cycle, the strongest category it beats, and the
> continuing-portfolio margin change the removal produces, in percentage points to one decimal
> place. Under that, every category ranked best cut to worst, its revenue in whole USD and its
> direct and continuing-portfolio margins as percentages to one decimal place, tying to the
> portfolio total. A chart on the same page, one bar per category in that order, before and after,
> the cut and the runner-up labelled, the flip threshold drawn at its value. Close on that
> threshold and the single evidence-backed change that would reverse the call.
>
> Q3 profitability came in under plan and the standard for the cut is settled, so what I need is
> the name and the arithmetic behind it, not options. I run category planning.

**C. Question-first, short, a workbook the buyers key off and a deck the board sees.**

> Which category comes out of the next buying cycle, and what does taking it out do to the margin
> we keep? Those are the two things I have to put in front of the board, and Q3 under plan is why
> I am asking now.
>
> The buying team keys off `category_margins.xlsx`, so give me every category ranked best cut to worst with its
> revenue in whole USD, its direct margin and its continuing-portfolio margin as percentages to one
> decimal place, and a total that reconciles to the portfolio.
>
> The board sees `category_cut_review.pptx`. One slide: the categories on continuing-portfolio margin in that order,
> before and after the cut, the category we take out and the one closest behind it labelled, the
> level at which the call would flip drawn at its value, and the call itself in the title. I run
> category planning.

**What is identical in all three, and is the actual contract.** First person with the role present.
One committed call. One to three files, each named after the decision. Every figure carrying its
unit and its rounding inside the sentence that asks for it. One ask spanning every category on
three measures at once, which is where the criteria live. A chart with its parts named rather than
described. The flip condition as a numeric threshold. No file name, no method hint, no trap word,
and nothing fixing the basis, the window or the population.

**What differs, and is yours to choose.** The opening move. Where the role sits. Which deliverable
is commissioned first. Whether the table takes a slot or lives inside another file. The verbs.
The length. The file count.

### The task-ready contract, read off the client's library

Seventy-two published prompts agree on a working shape, and a prompt that reads like them is what
"task ready" means. What transfers is the contract, never the content.

**The files play roles, and with a ceiling of three you pick the two or three roles the decision
actually needs.** A **text file that commits** (opens with the call, names the runner-up and why
it loses, closes with the flip condition), a **visual that reads at a glance** (the deciding
metric by option, ordered, threshold marked, title stating the finding), a **data file that
audits** (the breakdown at a named grain, a rank column, a total row that reconciles), and a
**code file that reproduces** (prints the graded figures and the validity check). The library's
most common pairing is commit plus read-at-a-glance, with the audit table folded into the memo.

**The asks are built from a small set of devices, and each device is worth criteria because a
wrong path gets it wrong:**

- the committed value, in its unit and rounding, with the interval or range on the same basis
- the runner-up named, with the gap on the deciding metric in that metric's own unit
- the flip condition, stated as a numeric threshold on the deciding metric
- the repeated structural unit, stated for every instance ("every shortlisted district ranked most
  unmet first, its tonnage, and whether its facility can take the route"), which is where the bulk
  of the criteria live
- a second figure on that same unit, which doubles the count for free
- a rank or ordering, as a whole number or as a stated sort
- a total row that reconciles across files, so the audit trail ties out
- a validity check: a backtest against a naive baseline, a placebo, a pre-period check, a
  sensitivity, or a cross-file reconciliation
- a second decision axis: the cost against the effect, the capacity against the forecast, netted
  to one figure the recommendation is judged on
- a chart with its parts named: each series, the ordering, the labelled threshold line at its
  value, the annotation on the key point, and a title that states the finding in words
- a code file that **prints** the figures, never one that merely computes them

**The prompt hygiene rules in this repo sit on top of the library.** Several client examples
state the decision basis, thresholds or capacity constants in the prompt's own voice; in a build
those constants live in the shipped files, because a prompt sentence outranks every file and closes
the fork the data was supposed to close. Copy the library's contract, not its habit of narrating
the furniture.

### Writing the asks

**There is no cap on the number of asks, no target number to hit and no per-file floor.** The
demand is quality: **each ask should be multi-dimensional and carry real difficulty.**

**What multi-dimensional means.** One ask spans many rows, periods or cuts and still resolves to
one defensible answer. "Lay out every shortlisted district ranked most unmet first, its tonnage,
and whether its facility can take the route" is one ask, one sentence, and thirty criteria. "Give
me the tonnage for District 4" is a lookup and belongs nowhere. The test is whether a wrong
analytical path gets the ask wrong, and a multi-dimensional ask fails **everywhere at once** under
a wrong path, which is exactly what makes it discriminating.

**Every figure's unit and rounding has to be covered**, and where the carrier goes matters. A
figure whose precision is not settled is a Gate E finding, because two correct
solvers format differently and only one matches the golden. What is **not** required is a tag on
every clause: 21 of the 25 paid-out prompts carry no rounding tag at all and none carries more than
two, while one of our recent builds carries thirteen, which is `../reduce-house-fixes/SKILL.md`
**H12** shipping unrepaired. H12 draws the line and it is the one to follow. **State the convention
once in the requester's own voice, then pin rounding explicitly only where the figure's type does
not already fix it:** a count of discrete things in the shipped data is a whole number by nature and
opens no fork untagged, while a derived quantity (a share, an average, a rate, a ratio, a
counterfactual, a difference in points) keeps its own explicit statement. After dropping a tag,
confirm the figure it covered is integer by construction in the shipped data, and re-enumerate the
surviving pins against the full figure list, because the failure mode of this repair is dropping
one pin too many. The rule is that **every figure inside an ask is separately gradable and
separately determinate**, so an ask spanning ten rows on three measures owes thirty determinate
answers.

**Do not stack simple asks to reach 25.** That is the failure the spec is aimed at.
Three or four hard, multi-dimensional asks over the right shape beat a dozen shallow ones, and the
generated rubric counts a median, a p90 and a top-tier share as **one** finding restated, not
three.

### Every ask has to be an ask a real person would make

**The 25-criteria floor creates direct pressure to ask for things because they generate criteria,
rather than because anyone acts on the answer.** That pressure is structural, and it
produces exactly the artifact the client is trying to kill: a request that reads as a spec written
against a scoring sheet. Run six tests over the ask set, and run them before the wording is
polished, because the repair is usually a re-cut rather than an edit.

1. **Use.** Name who acts on the answer and what they do differently once they have it. An ask
   whose answer changes nobody's next move is a rubric artifact, and it reads as one.
2. **Provenance.** Delete the rubric from your head and reread the request. Would this ask still be
   in it? An ask that exists only to reach 25 is visible to a reviewer for the same reason a
   padded paragraph is.
3. **Genre.** Does this ask belong in **this** document? A determination memo carries the standard
   and the finding. A reconciliation carries the bridge. A per-row audit table belongs in the
   workbook, or inside the memo as a table, not as a request bolted onto a one-page brief. This is
   the same discipline `../golden-realism/SKILL.md` applies to the output, applied here to the
   request.
4. **Vocabulary.** A stakeholder asks in their own domain's words, not in analyst words. "The
   aggregate at the facility grain" is a spec; "how many free shifts that facility has left" is a
   request. This test doubles as an anti-leak check, because analyst vocabulary is precisely where
   method hints and the banned trap words live.
5. **Asymmetry.** Real requests are lopsided. One thing is needed urgently and named to the
   decimal, another is mentioned in passing. An ask set where every ask carries identical
   specificity and identical weight reads as generated, for the same reason evenly sized sections
   do in a document.
6. **Already-known.** Do not ask an organisation for a figure it would already have on hand. Its
   own headcount, its own budget line, its own site list. Ask for what the analysis produces, not
   for what the requester could read off a wall.

**When an ask fails a test, the repair is almost never deletion**, because deletion costs criteria
you still need. Two better moves, in order:

- **Find the decision it actually serves and re-cut it to that.** An ask that failed the use test
  usually had a real use one step away: not the raw figure but the figure against its threshold,
  not the count but the count relative to what the constraint allows.
- **Fold it into the adjacent multi-dimensional ask** as one more measure on the same repeated
  unit. Three orphan asks that each read as filler become one ask that reads as a decision table,
  and the criteria count is unchanged or better.

**The use test and the difficulty test pull the same way**, which is the reason this is worth doing
rather than a tax on top of the design. An ask with a real use turns on the structure of the
decision, and an ask that turns on the structure is an ask a wrong analytical path gets wrong. An
ask invented to be graded usually has no structure behind it, which is exactly why it is easy, and
easy asks are a rejection cause in their own right.

**Use more than one kind of evidence across the set:**

- **Supporting or justification.** A metric or finding that backs the recommendation.
- **Comparison.** How the winner sits against the runner-up, on the deciding metric, in its unit.
- **Context or flip.** A related conclusion, or the evidence-backed change that would move the
  runner-up into first place, stated as a numeric threshold.

**Where the same figure appears in two files, make the second appearance a reconciliation** ("a
total row that ties out to the memo's figure") rather than a repeat, so it earns its criterion as a
cross-file check instead of being counted once and discarded.

**An ask that names an entity and asks for an aggregate has to say which grain it wants, and you
find out by computing both.** "Name the county of the provider that carried the most households"
reads two ways: the county aggregate, and the county of the single busiest provider. Where the two
readings land on different answers, the wording has to name the grain and the sourcing route in the
same breath: *"Name the county that carried the most households in the certified figure, counting
each household to the county its provider sits in."*

The check is mechanical and belongs in the generator, not in a proofread. **For every ask that
resolves an argmax through a join, compute every reading the wording admits and assert that they
differ, then confirm the wording selects the one the golden answers.** If two readings agree you
have nothing to fix; if they disagree and the ask does not pin the grain, the review will find it.
Emit both readings into the golden so the next person can see which one the wording chose.

**They must not enumerate the methodology, name the trap, identify the decisive file, or walk
through the answer path.** Asking for every obvious intermediate hands over the ladder. This is the
sharpest tension in the format: the asks want to be specific enough to grade and general enough not
to leak, so write them from the golden's outputs rather than from its steps.

**Each one is graded at the main recommendation's bar.** The judge treats every supplementary
answer as a committed answer: it must reproduce from the shipped files and be uniquely forced.

**Prefer asks a script satisfies.** A chart the deliverable script renders, a table it writes, a
control total it prints: all of them recompute, none of them can read as LLM-generated prose, and
the reviewer can rerun them.

Write all of them **after** the golden exists, never before.

## What the prompt may say, and what it may never say

**Licensed**, because a fair prompt has to carry the decision's own furniture:

- Naming the **belief a stakeholder already holds**, as one clause, stated as a belief. That is
  the decoy advocate, and it adds social pressure the solver has to overcome with evidence.
- Naming the **generic threat to validity in the open** ("participation was voluntary", "traffic
  mix swings a lot between weekdays and weekends"). This states that a confound exists without
  saying which way it resolves or which file settles it.
- Naming the **operational constraint the decision runs into** ("the mandate requires a 12
  percent reduction", "the provider can run fewer engagements than there are acceptances"),
  because a constraint that is not in the ask cannot be checked.
- Naming the **candidate set** when the decision is one-of-N.

**Banned, every one of them:**

- **Any sentence that fixes the decision basis, the measurement window, the scoring convention,
  or the population.** The prompt outranks every shipped file, so such a sentence is the most
  load-bearing sentence in the task and it answers the question before a file is opened
  (`stumping`, the pin and the authority hierarchy).
- Naming the metric that decides it, the eligibility rule, or the fee schedule. Bury these in
  the data.
- Naming any input file, or any governing standard by acronym.
- Method hints ("compare A against B", "cross-reference the extracts") or trap words (*clean,
  unduplicated, reconcile, attribution, mix, standardise, grain*).
- Signposting that a metric might mislead.
- More than one candidate metric named as valid, which invites hedging.

The working test: you may say **that** the analyst faces a confound, never **which** evidence
defeats it. "The treatment cohort skews toward users who signed up later" is the tension. "Drop
the first two weeks and the lift goes flat" is the answer.

### When the answer is hold

**"Not enough information to make a decision" is an acceptable final answer.** If your task lands there, the ask needs one extra clause and nothing else: the non-pick goes in as one option alongside the candidates, on the same footing.

> Name the single intervention to scale, **or state that none should be scaled this cycle**.

That is a licence. These are not, and each hands the answer over:

> ~~Tell me whether there is enough evidence to decide.~~ The question is the answer.
> ~~Assess the strength of the evidence before recommending.~~ Method hint plus signpost.
> ~~Recommend one, or hold if the data is inconclusive.~~ "Inconclusive" names the finish line.

The commit demand stays exactly as strict, because hold is one of the committed calls rather than permission to hedge. Everything that makes a hold gradable is built in the data, not the prompt: `stumping` Part 6.4 carries the build requirements, the most important being that the hold is forced by a computed quantity that reproduces from the files.

---

## Handoff

1. Pairing saved, subdomain enumerated, anti-clone draw done.
2. **Prompt shape picked**, from `references/shapes/README.md`, with the criteria arithmetic worked
   on paper and written into `DATASET_NOTES.md`. If it does not reach 25, fix the structure now,
   because every later step is more expensive.
3. Load `stumping`, answer the litmus, pick a mechanism off the Gate G pass list, and read your objective's trap catalog plus `_cross-objective.md` before opening a data file. The Main Recommendation Ask is what has to stump, so the ladder is designed against that one question. Two tests it has to clear before you build anything: **the clean-data test** (with perfectly clean and correct data, the task must still be hard and the answer still non-obvious) and **the litmus** (the reported figures in the pack must be correct, so the difficulty is not catching that a read is wrong).
4. Load `dataset-generation` and build the pack, with the domain, subdomain, and objective at the top of `DATASET_NOTES.md`.
5. Write the prompt last. Read `references/prompt-voice.md` first and pick the opening move, the ordering and the file set deliberately, then read every clause back asking whether it fixes a choice the data was supposed to fix, and run `references/voice-check.py <task number>` before you call it done, and read its HIERARCHY READ against the three reads above, because that is what the client's prompt review checks first.
6. **Compress it, against `references/prompt-economy.md`.** Draft at whatever length the ideas arrived in, then cut toward the paid-out median: about 250 words at about 24 words per sentence, with the ECONOMY block in `voice-check.py` clean. That block flags at the paid-out set's own p90 or maximum (330 words, 33 words per sentence, a 180-word paragraph, a context paragraph over 46 per cent of the prompt), so a flag means the draft sits outside anything that has been paid out. Then run both halves of the gradability check: walk the figure list, and re-count the criteria off the shape's arithmetic, because compression is what silently drops an element from the repeated structural unit.
7. Invoke `determinism-check`, which costs nothing and spawns nothing; its judge rehearsal runs only when the author asks or when `/build` reaches stage 6. The solver rounds (`solver-round`) run on the finished build through `/solve` or `/build`, and the portal remains the oracle.
8. Write the submission with the `submission-writeup` skill, as `submission.md`, then the `golden-realism` pass, then hand the build to the author.

## Checklist

- [ ] Exactly one domain, from the **six** accepted, and it is the one whose decision-maker owns the call
- [ ] Exactly one enumerated subdomain, written into `DATASET_NOTES.md`
- [ ] Exactly one Axis 1 objective, one of the **eight** live labels, unchanged, and for Opportunity Sizing & Decision Support or Data Quality Monitoring & Alerting its discriminating test passed. "Comparative analysis and explanation" appears on the client's example page and is **not** a valid tag here
- [ ] The objective's reference file read before drafting, and the evidence pack can actually support the ask
- [ ] **A prompt shape picked from `references/shapes/`**, with its criteria arithmetic worked on paper and landing at **25 or more** before any file is generated
- [ ] The shape's "what makes it hard rather than long" section read, and the ladder built against it
- [ ] No scenario, entity, metric, file name or ask wording lifted from any reference example, including the shape library
- [ ] Axis 2 phases tagged, ideally all five
- [ ] The boundary rules checked if the task sits near one
- [ ] Main Recommendation Ask is a single question resolving to one committed call, forward-facing by default, and it is the part the trap is designed against
- [ ] **The committed call can be quoted as one whole sentence**, carrying its unit and rounding, and it is not assembled from a colon-appositive, an anaphor or a sentence about who owns the figure
- [ ] **The hierarchy read passes all three**: the context's last sentence before the first deliverable is the call stated bare, the clause naming what the committing file leads with names exactly one quantity, and every later paragraph opens by tying back to that quantity rather than on a bare commissioning verb
- [ ] **Every supporting ask's answer is a component of the committed call, a qualifier of it, or its audit trail**, and none of them is a figure for another period or another decision riding in the same file; by default each is also decoupled in computation from the main trap (`supplemental-stumping`, Decoupled asks)
- [ ] The deliverable set was **not** cut to answer a hierarchy finding, because the asks carry the score and the criteria floor
- [ ] Context is first person with the role present, short, no roll call of colleagues' opinions, at most one stakeholder belief carried as one clause
- [ ] **`references/prompt-voice.md` read, and the opening move chosen from what forces this decision**, not inherited. The role does not have to be in the first clause and on most builds should not be
- [ ] **`voice-check.py` run with this build's number.** Its opening move differs from the last three builds, no carrier phrase in it comes back flagged as calcified, and the file count and format mix are not both the batch mode
- [ ] The deliverable set is not a PDF plus a chart plus a workbook by default. One file is legal, two is the library norm, and DOCX, PPTX, HTML, CSV, JSON and the rest are live formats this batch has under-used
- [ ] **One to three named deliverables**, three being the ceiling, each named after the decision and each one a file a real analyst would produce for this decision
- [ ] **A visual included wherever it makes the decision read at a glance**, with its parts named: chart type, series, ordering, labelled threshold line at its value, annotation, and a title that states the finding
- [ ] No slot spent on a table that could have lived inside the memo, the workbook or a script's output
- [ ] The asks are **multi-dimensional and hard**, none of them a lookup, and none of them stacked simply to raise the count
- [ ] Every ask passes the six realism tests: a named **use**, **provenance** independent of the criteria count, the right **genre** for the file it sits in, the stakeholder's **vocabulary** rather than the analyst's, **asymmetry** across the set, and nothing the organisation would **already know**
- [ ] Asks that failed a test were re-cut to the decision they serve or folded into an adjacent multi-dimensional ask, not deleted and not left in
- [ ] Every figure inside every ask has its unit and its rounding covered: the convention stated once in the requester's voice, and an explicit pin on every derived quantity (a share, an average, a rate, a ratio, a counterfactual, a difference in points). No tag on a figure whose type already fixes it, and no unit phrase repeating more than about twice across the prompt (H12)
- [ ] **`references/prompt-economy.md` read and a compression pass run on the draft**, aiming at the paid-out median of about 250 words at about 24 words per sentence, with the ECONOMY block from `voice-check.py` clean. It flags at the paid-out p90 or maximum: over 330 words, over 33 words per sentence, a paragraph over 180 words, a context paragraph over 46 per cent of the prompt, more than three rounding tags with no convention sentence, two or more "because" clauses, or no sentence under eight words
- [ ] **After compressing, both halves of the gradability check run again**: every graded figure still named, still carrying its unit, still covered on rounding, **and** the criteria re-counted off the shape's arithmetic, since the colon-list and purpose-clause moves are what drop an element from the repeated structural unit. These are the only two ways the compression pass fails
- [ ] No pack inventory, no organisation bio, no business-model clause, and no reason clause hung on an ask that does not need a motive
- [ ] The files cover the decision between them: one commits, and the others read at a glance, audit or reproduce. Cross-file figures appear as reconciliations rather than repeats
- [ ] The prompt reads as prose a busy person would actually write, not as a bulleted spec
- [ ] If the answer is a hold, the non-pick is licensed as one option among the candidates, and no clause asks whether the evidence suffices
- [ ] Nothing in the prompt fixes the basis, window, convention, or population
- [ ] No input file name, standard acronym, method hint, or trap word anywhere in the prompt
- [ ] The task would still be hard on perfectly clean data, and the reported figures in the pack are correct, so it is neither a planted-defect flip nor a surface-read rejection
- [ ] Anti-clone draw shows no repeat of domain plus role plus artifact type, **and no repeat of the prompt shape's driver**, which is the insight that carries the stump rather than the shape itself

---
name: dataset-generation
description: Build the evidence pack that carries a designed trap. Covers the input gates (10+ files, 3+ formats, one file of 25,000 or more rows in any format, or a large database file), the ten file roles, the calibration file that makes the answer deterministic, authentic mess that cannot change the answer, and the provenance discipline that keeps the bundle compliant. Use after the refusal ladder is designed via the stumping skill, when repairing a pack whose trap does not bite, or when a determinism review says a number does not reproduce. Never build data before the ladder exists.
---

# Building the Evidence Pack

> The prompt names the decision. The pack *is* the task. Every rung of the ladder must reproduce to zero drift from files in this bundle, and every rival must die to a fact that is also in this bundle. If a number in your golden cannot be recomputed from the pack, it does not exist.

**Prerequisites, in order.** The pairing is fixed via `guide-to-prompt` (one domain, one enumerated subdomain, one Axis 1 objective), the build's fingerprint card is filed and clear of BLOCK (`../fingerprint/SKILL.md`, which also bans a spine whose entity and grain or source dataset repeats a recent build), the refusal ladder is designed and written down per the `stumping` skill (Part 13, the design note), and the ask sheet and device ledger are fixed per the `supplemental-stumping` skill, because the eight-file spans that skill floors are schema decisions this pack has to honour. Do not open a data file before the design note states everything Part 13 and the ask ledger require. Building data before the ladder produces a pack that either leaks the answer or carries no trap, and building it before the pairing produces a pack that carries evidence for an objective nobody tagged.

**Navigation.** §1 scope rule · §2 sourcing doctrine · §3 the ten roles · §4 the calibration file, fittability and the twin pair · §5 the context artifact · §6 rung exactness, position table, discriminator dominance · §7 authentic mess and the realism gate · §8 governing documents · §9 provenance and hygiene · §10 build order · §11 verification, the assertion regime, the independent verifier · §12 repair directions · §13 anti-clone · §14 checklist

---

## 1. The scope rule (non-negotiable)

Every task sits in **exactly one** of the nine accepted domains (Biology, Biostatistics, Epidemiology & Bioinformatics is not one of them), with a subdomain enumerated in `guidelines/scope_of_project.md`. Subdomains outside the enumerated lists are out of scope, not a browsing suggestion.

1. Product Analytics
2. Supply Chain & Logistics
3. Economics
4. Policy & Education
5. Demographic & Social Science
6. Nonprofit & Grant-making
7. Marketing & Consumer Research
8. Business & Operations Analytics
9. Accounting, Audit & Forensic Analytics

Write the domain, the subdomain **and the Axis 1 objective** at the top of `DATASET_NOTES.md` before generating anything. If your trap needs a subdomain that is not listed, change the trap rather than drifting. The domain files in `guide-to-prompt/references/domains/` carry the enumerated subdomains and the two boundary rules, one file per domain.

### The evidence must support the objective you tagged

A pack that carries the wrong kind of evidence fails on the objective even when the ladder is sound, because the reviewer checks the tags against the files. One objective per task, from the **eight** objective labels, and the pack has to make *that* objective the natural reading. A pack tagged outside the eight is rejected on the tag alone.

| Objective | The pack must ship | Cheapest way to fail it |
|---|---|---|
| Descriptive & Distribution Analysis | Row-level records at the decision grain, enough volume for the shape to be real, and a published summary statistic that the distribution contradicts | Shipping only pre-aggregated summaries, so no distribution can be recovered |
| Anomaly Detection & Diagnostics | Enough baseline history to establish normal variation, the seasonal or day-of-week structure, and the operational log that separates artifact from event | A spike with no baseline, which makes the call a matter of taste |
| Root-Cause Analysis | Two or more rival drivers that each correlate with the move at the aggregate level, and the evidence that separates them | One candidate driver, which makes the answer the only story available |
| Opportunity Sizing & Decision Support | The addressable pool at row level, the shipped evidence that takes it down to what can actually be realised (eligibility, capacity, uptake or recovery), and the decision the sizing drives | A sizing that is one published number, or one a solver could retag as a forecast or a descriptive total without changing a word |
| Data Quality Monitoring & Alerting | The pipeline's own records (deliveries, arrival times, row counts, schema versions, check results, the incident register, alert routing) beside what was published, so the health of the data is measured rather than asserted | A business metric dressed as a data-quality question, which retags as Anomaly Detection or Forecasting without changing a word |
| Experiment & Causal Analysis | Assignment records, the outcome at the pinned horizon, and the confounder as a real column rather than a claim in a memo | Arm-level summaries only, so no reanalysis is possible |
| **Forecasting & Predictive Modeling** | History long enough to fit and to hold out, the regime break or shifting seasonality as an actual feature of the series, and a calibration corpus of already-settled outcomes | A series so short or clean that every method agrees, or a horizon the history cannot pin down |
| Data Extraction & Conformation (ETL) | Three or more genuinely disagreeing sources plus the crosswalks, id maps and dated FX or unit tables that make reconciliation possible | Sources that differ cosmetically, so conformation is string cleaning |

**Forecasting & Predictive Modeling is actively wanted and any domain can carry it**, but only when the supplied evidence pins the future value down. If the history leaves the horizon genuinely open, the task is not deterministic and no amount of trap work fixes that.

### The framing rule that makes any domain work

When the brief demands a specific framing (for example, "product analytics at a tech company") but your subject matter sits elsewhere, resolve it the same way every time:

> **The entity is a platform. The public dataset is the market it sells into.**

A platform that sells into education, logistics, grants administration, or public health is a tech company doing product analytics; the sector dataset is its addressable market, not its product telemetry. This keeps the framing honest while giving you access to every rich public dataset.

**Cross-domain leakage** is still a failure: if a pack starts pulling evidence from a second sector to make the trap work, the trap is wrong. Restart.

---

## 2. Sourcing doctrine

### The preference order

1. **Real public dataset as the spine**, strongly preferred. Carries authenticity, volume, genuine mess, and clean licensing.
2. **Real publisher documentation** alongside it, the survey form, API data-elements guide, universe documentation, program handbook. Long, genuine, and often the natural home for a decisive definition.
3. **Constructed operating layer** on top, the entity's own extracts, ledgers, configs, memos. This is where the trap physically lives.

A **fully constructed pack with no public spine can pass**, and does. The real bar is not "contains public data." It is:

> **Provenance plus plausibility.** Every derived file is declared for what it is, and every file behaves like a real system export.

### Compliance, treat as blocking

- **Never fabricate, corrupt, pad, or truncate to manufacture difficulty.** Complexity must be authentic.
- **Never ship a long generated document.** Machine-written PDFs, DOCX and PPTX are recognisable in seconds, thin content, oceans of white space, suspiciously clean tables. Long documents in the pack must be genuine publications.
- **Keep constructed documents short and functional.** A memo, a thread, a config, a runbook extract, a terms clause. Two to four pages of real operational content, not a report.
- **Ship explicit provenance.** A `DATA_NOTES.md` or `export_manifest.csv` stating what each derived file is and how it was produced. This is the mechanism that makes a constructed operating layer legitimate.
- AI may locate data and write transformation scripts. It may not create the empirical source evidence.

### Choosing a spine

Pick a dataset whose **subject is the market the entity sells into**, at a scale that gives you 10³–10⁶ rows and real missingness. Rotate spines between builds (see §13).

Properties to check before committing:
- Does it have a **natural entity key** you can join on?
- Does it have **published documentation** you can ship?
- Does it contain **genuine mess**, non-response, code changes across vintages, hierarchical records, revisions?
- Does it have a **dimension you can make the decision grain differ from**? If every row is already one clean entity, half the generators in the stumping skill are unavailable to you.

---

## 3. The ten roles

The `stumping` skill Part 8 lists these. Here is how to actually build each one.

| # | Role | Count | Build notes |
|---|---|---|---|
| 1 | **Spine dataset** | 1–4 | Ship close to raw. Split by period or entity class if it exceeds size limits, a natural split is also a realistic one. |
| 2 | **Publisher documentation** | 0–1 | Genuine PDF. If it is not decisive, disclaim it in the governing document (§8). |
| 3 | **Operating extracts** | 2–4 | The entity's telemetry. **The trap lives here.** Give each a plausible export cadence and a `pull_date`-style column. |
| 4 | **Context artifact** | 1–2 | §5. Correct numbers, about a question that is not the decision question |
| 5 | **Calibration file** | 1 | §4, build this first |
| 6 | **Governing document** | 1–2 | §8, carries the pin and the licensed wrong basis |
| 7 | **Social layer** | 1 | Thread or notes; named people holding wrong beliefs, never quoting a computed ranking |
| 8 | **Dimension / lookup tables** | 3–6 | Small, boring, essential. They force joins and make the warehouse look real. |
| 9 | **Data dictionary / codebook** | 1 | §6.5, where grain statements live |
| 10 | **Provenance note** | 1 | §9 |

### The input gates, and they are pass/fail

These are spec, not targets. A pack that misses one is rejected before anyone reads the analysis, so
assert all five in the generator.

| Gate | Requirement |
|---|---|
| File count | **10 or more** |
| Formats | **3 or more distinct**, four is the working target, across {csv, xlsx, json, parquet, sqlite/db, pdf, md, docx, txt, png} |
| Volume | **either a file of 25,000 or more rows in any format, or a large database file** (a SQLite or DuckDB `.db`, for example). One or the other is enough, and a pack that carries neither fails |
| Distractor | **two or more distractor files**: files the solution does not use that look relevant enough that a solver has to weigh them, named in the task's `metadata.json` and never in a file name or anywhere under `target/` (§8.3). A file unrelated to the question does not count |
| Authorship | nothing that reads as LLM generated. Obvious artifacts get the task rejected outright |

**Targets on top of the gates:** 10 to 19 files, median around 13. Each file under the platform's
per-file limit, the bundle under the total limit.

The volume gate is usually the spine's job, so check it when you pick the spine (§2) rather than
discovering at the end that the interesting dataset is 4,000 rows and the bulk one is padding. The
25,000 rows can sit in any format (CSV, Parquet, XLSX, JSON, a database table), and the point of
leaving the format open is variety: do not default the big file to CSV build after build, pick the
format the source system would actually export. A database file meets the gate by being the place
the bulk records actually live, with real tables a solver has to query, never as an empty or
one-table wrapper added to tick the box.

**Every file must do work.** A file that could be deleted without changing the answer or the difficulty is padding, and padding is checkable. A distractor (§8.3) earns its place by making the solver weigh a relevant-looking file and set it aside, and a disclaimed background document (§8.3) by carrying authenticity.

### Naming

Name files the way a real export would be named: `implementation_roster.csv`, `settlement_extract_fy24.csv`, `fee_schedule.csv`, `platform_runbook.pdf`, `q3_planning_thread.md`.

Never name a file after the trap. `data_quality_notes.md`, `known_issues.txt`, `reconciliation_needed.csv`, `THE_REAL_TRUTH.csv`, all disqualifying. If the trap needs a note, it belongs inside a natural business artifact as a clause.

---

## 4. The calibration file, build this first

This is the hardest artifact to make convincing and the one that decides whether your task is deterministic. Everything else is easier, so build it while you still have freedom.

**What it is:** a record of **outcomes the decision does not cover but the method must explain.** The solver computes each candidate basis, then checks which basis reproduces these known outcomes. The right one fits; the rivals do not.

### Forms that work

- a ledger of already-settled transactions
- an acknowledgement or confirmation file from a counterparty system
- a pilot log carrying filed decisions
- the book of existing customers/accounts/markets with actuals
- a prior-period operating summary for units already served
- a retry/revision log showing which attempts succeeded and which returned nothing

### How to engineer it

1. **Decide the test before the data.** Write the sentence you want the solver to be able to say: *"Basis X reproduces these outcomes at ___; the rivals reach only ___."*
2. **Build the underlying records first, then compute the outcome column from them.** The summary row is an *output* of the pack, never an input. See §4.1, this is the rule that gets broken most often and it is fatal.
3. **Generate the outcomes from the correct basis**, with realistic noise. The fit must be tight but not suspicious, a perfect R² of 1.000 reads as synthetic.
4. **Verify the rivals fail hard.** Compute each rival basis against the same outcomes. If a rival gets close, the test does not discriminate and you must change the mechanism, not the tolerance.
5. **Control the confounders by construction.** If the calibration is a success/failure split, make the failing and succeeding cases share operators, sites, and timing so the *only* thing separating them is the property you are testing. This is what makes the finding unarguable.
6. **Check who the file nominates.** Run the lookup-transfer shortcut yourself: match each candidate to the calibration case it most resembles on the columns a solver can see, carry that case's rate across, and see who wins. **It must be the decoy.** If the shortcut lands on your answer, the calibration file is solving the task and every rung above it is decoration.

### 4.1 Fittability, build both halves

A calibration outcome that **no rule in the pack reproduces** fails review as a fabricated intermediate (`stumping` Part 11 Failure C), and it also fails as a trap: solvers who cannot fit a case declare it unexplainable and fall back to using the file **ordinally**, which lands them on the decoy without ever measuring anything.

So a calibration case is always two artifacts:

| Half | What it is | How it is built |
|---|---|---|
| The row | the shipped summary line, projected, booked, outcome | **computed by script** from the records below |
| The records | the register / ledger / claim / attempt rows behind it | generated first, with the mechanism that produces the outcome |

Never add a row to the calibration file in a patch without building the records that reproduce it in the same edit.

### 4.2 The twin pair, the highest-value single artifact in the pack

The most common solver shortcut is **lookup transfer**: match each candidate to a reference case on a few columns, transfer that case's rate, skip the measurement. Everything you built above it goes untouched.

Kill it in the data: ship **two calibration cases identical on every column a lookup can see, whose outcomes are a factor of ~2 apart.**

Build recipe:

1. Pick the two cases and make them **byte-identical on every lookup-visible field**, flags, design attributes, category codes, tier labels, and on the corresponding entry in every document that describes them. One distinguishing prose line anywhere and the shortcut survives.
2. Drive the outcome difference entirely through the **mechanism the decisive rung measures** (timing, clawbacks, conditioning, whatever the rung turns on), inside the records.
3. Compute both outcome rows from those records.
4. **Back-test the whole family**: the correct rule reproduces N of N cases within *x*%; every rival rule in the swept family misses at least one case by ≥ *y*%. Assert both numbers, and state the count of rules you actually swept.

After this, no rate transferred by resemblance can reproduce the file, so the solver has to measure, and the twin pair also destroys the ordinal escape, because two cases a lookup cannot tell apart, converting 2× apart, have no defensible ranking story.

### 4.3 A decision window that runs past the data pull

When the window the decision prices extends past the pull, the driver for the uncovered span ships as a file, never as an assumption, or every back-test in the pack is blind to how a solver treats it (task47: 12.5 per cent of the filed figure came from sales after the volume freeze). The file is an operating artifact rather than a method sentence: a plan for the driver (a daily volume plan by category, say) covering the same horizon in every season, published before each season's freeze, never restated, and generated forward from the underlying process rather than from the realised book, so plan against actual is a real accuracy record a solver can compute from the shipped history. Keep it silent the way the rest of §4 asks: field semantics in the dictionary, one operational mention in the social layer, no clause anywhere saying what to do with it. Assert three things: the plan's error on every horizon it can be scored on, the share of the graded figure the post-cutoff span carries, and that dropping the span lands the figure in a different rounding bin with clearance.

### Gap targets

| Test form | Do not ship | Ship |
|---|---|---|
| Predictive fit | R² 0.88 vs 0.84 | **0.92 vs 0.59** |
| Reconciliation | 2% vs 5% error | **0.000% vs no match** |
| Success split | 70% vs 50% | **all of one group vs none of the other** |
| Prediction error | $400 vs $900 | **single dollars vs tens of thousands** |
| Cross-unit stability | 1.4× vs 1.9× spread | **1.26× vs 5.30× spread** |
| Rule reproduction | "mostly matches" | **every filed decision reproduced** |

If the gap is marginal, "it's a judgment call" survives and you do not have determinism.

### Prefer threshold-free tests

The strongest calibration needs no cutoff you invented:

- **Definitional:** a record either was or was not on the governing list on that date.
- **Empirically self-drawing:** every attempt with property P succeeded; every attempt without it returned nothing. The data draws the line, not you.

A test that requires you to pick a threshold is a fork you left open.

**Give a threshold-free rule a floor in the data, so every threshold rival converges to it.** Solvers still reach for a de minimis, and each threshold is a separate cell in the fork grid. Close it in the generator rather than in the corpus: build the records so no observation sits between zero and a floor above any plausible de minimis, so every threshold below the floor selects exactly the same set and files the same figure (task44: a face-empty event takes a block of lines, so nothing in the pack sits between zero and 13 per cent off face, and every de minimis up to 15 per cent files one figure). Assert the floor on the observed share directly. What is left above the floor is arbitrary, and the calibration corpus refuses it case by case.

### Keep it quiet, and never label the convention

Name it naturally. Do not mention it in the prompt. Do not make it the largest or most prominent file. Solvers routinely open the calibration file, use it for something incidental, and miss the decisive check inside it, that is the trap working correctly.

**Do not ship the decisive convention as a column.** A field called `..._measurement_basis` or `projection_convention` reading "cash booked within 24 months of the certification date" is a **louder** signpost than any prose line, because it turns the decisive rung into a two-column lookup. But do not simply delete the parameter either, an unpinned parameter with no anchor is a determinism defect, and solvers each fit their own and split on the figure.

**Pin it empirically instead:** build the records so the parameter is recoverable as the *unique* value that reproduces every calibration outcome, and pin it nowhere else. The data does the pinning, and the solver still has to do the fit.

---

## 5. The context artifact

**Never build a file that computes the naive answer to the decision question.** An in-pack artifact
that ranks the candidates on the decision basis and gets the ranking wrong is
`surface_read_dependency: yes` by construction, and Gate G sends the task back regardless of how many
rungs sit above it. It is the leading cause of rejection and it is easy to build out of habit.
The one exception is the declared distractor (§8.3), which is never the stump and is named in
`metadata.json`.

**Rung 0 is not a file.** It is the answer the most natural correct pipeline produces when a
competent solver opens the pack and does the obvious thing. You engineer the data so it comes out
that way and you assert it in the generator, but you never write it into an artifact. See `stumping`
Part 3.

### What you build instead

A **context artifact**: a file whose numbers are correct and which answers a question that is not
the decision question.

| Ship | Do not ship |
|---|---|
| A monitoring or detector export reporting a past quantity it measures correctly | Anything that ranks the candidates on the decision basis and gets the ranking wrong |
| An operations log, a register, a published series | A scorecard, workbook, filed model or prior-review memo that answers the decision question wrongly |
| A capacity report, which is not a ranking | A method-notes line stating a wrong method for the decision |
| A prior-period close-out, which is not a forecast | An advocate quoting a computed ranking of the candidates |

### Requirements

- **Reproduces to the last digit** from the spine and operating extracts. Reviewers recompute it.
- **Internally flawless.** No cell errors, no broken formulas, no bad joins.
- **Labelled in-file for the question it does answer**, in one line. *"Alert scores are computed on
 the trailing four weeks and describe the breach, not the forward burden."* / *"Capacity as of the
 cycle open; does not net committed volume."* This is what keeps it fair: the solver can see what
 the file is a statement about, and the difficulty is noticing that the decision asks for something
 else.

### Build procedure

1. Build the spine and operating extracts first.
2. Compute the artifact's figures **from those files**, by script.
3. Write the resulting numbers into the artifact. Never author numbers by hand and then make data
 match them, which is how drift and fabricated intermediates enter.
4. Re-run the script against the shipped files and diff. Zero tolerance.

### Make it credible

Give it the trappings of a real internal artifact: a version tag, a refresh date, an owner, a
distribution list. Authenticity is still worth having. What you do not get to do is make it
authoritative *about the decision*.

---

## 6. Rung exactness

**Every rung of the ladder must reproduce to zero drift.** Not just the answer, the wrong rungs too, because they anchor the rubric and because reviewers recompute them.

### 6.1 Compute forward, never backward

Build the data, then compute each rung's number from it by script. Record the outputs. Never decide a number first and reverse-engineer data to hit it, that path produces figures that recompute to something slightly different and fail Gate A.

Keep a regeneration script that emits every rung's figure from the shipped files. Re-run it after any data change.

### 6.2 Rung separation, and the position table

Each rung must land on a **different named candidate**. After computing all rungs, print the ranking under each basis and confirm the winners differ. If two rungs share a winner, one rung is doing no work, redesign the data so it separates, or drop the rung.

**Re-run this after every parameter change, not once at the end.** A parameter tuned to strengthen a lower rung, enlarging an anchor record, widening a decoy's lead, routinely hands the *final* rung to the same candidate as the rung beneath it. The rung still computes; it just stops naming a different candidate, and nothing in house will tell you the last two rungs agree, so you find out from a portal result or never. Assert per-rung winners **by name** so the collision fails the generator run at the moment the parameter moves.

Also print, and assert, the *shape* (`stumping` Part 3):

| Check | Requirement |
|---|---|
| Answer's rank on the natural pipeline (rung 0) | **4th or 5th** |
| Answer's rank on every intermediate rung | never 1st |
| Rungs where the answer sits 2nd | at most one, and there by ≥1.20× |
| Any rung margin | never under 1.15× |
| Final margin on the correct basis | ≥1.2×, target 1.5–2× |

### 6.3 Discriminator dominance, check the arithmetic before you build

The decoy reaches the final rung carrying an advantage from the rung below (more exposure, more volume, a bigger book). The final rung can only flip the ranking if the winner's edge on the decisive axis clears that carried advantage:

```
edge(winner, decisive axis) ≥ 1.2 × advantage(decoy, carried axis)
```

Compute both ratios from the data as built and assert the product. If the decisive axis is worth a few percent and the carried axis is worth tens of percent, the rung cannot fire, and no amount of extra documentation, findability or prose rescues it. Fix it in the data: widen the decisive spread between the two candidates, or shrink the decoy's carried advantage.

### 6.4 Construct the disagreement, it does not emerge from independent draws

If a rung turns on **two axes disagreeing** (measured by date versus by period label, per-record versus per-entity, gross versus net, cohort versus calendar), the generator must build the correlation that makes them disagree, per candidate.

Draw the driver columns independently and every candidate ends up with the same profile on both axes: the mechanism is documented, findable and inert. Concretely, if the design says "the winner looks slow on the period-label view and fast on the date view, the decoy is fast on both", then the generator must correlate the timing driver (certification month, cohort entry, signing quarter) with the outcome timing per candidate, and **assert the resulting split for each candidate in both directions**.

### 6.5 Pin grain statements in the dictionary

The data dictionary is authoritative for **field semantics**, and several generators depend on it:

- *"Recipients are distinct within [entity], [program] and [period]"*, makes a cross-dimension sum provably not an entity count.
- *"An annual term is invoiced once for a twelve-month period"*, makes a survival property derivable.
- *"[Field A] is the billing entity; [field B] is the entity for the site"*, makes a grain recoverable.
- *"[Status field] is account-level and survives a lapsed subscription"*, warns off a wrong proxy without naming the right one.

Write these as flat field definitions. Never as advice.

---

## 7. Authentic mess, and the realism gate

### Realism is a rejection criterion, not a nicety

The pack has to read like an export from a system that has been running for years, not like a
generated fixture. Two specific failures get tasks rejected on sight:

- **Placeholder identities.** No John Doe, no Jane Smith, no Acme Corp, no Lorem Ipsum, no Company A
 and Company B, no obviously sequential fake names. Invent names the way a real registry would
 carry them, with the inconsistency real registries have.
- **Anything that reads as LLM generated.** Long documents with thin content, uniformly tidy prose,
 suspiciously balanced bullet lists, every file written in the same voice.

What buys realism cheaply: **real published vocabularies** (NAICS, SOC, HS, ISO, FIPS, agency series
codes, CUSIP-shaped identifiers), real geography, real institution and program naming conventions,
real release calendars, and real revision and vintage behaviour. A code column whose values are
genuine published codes reads as an export in a way nothing else does.

And the strongest single defence, which belongs to the deliverables rather than the pack: **prefer
artifacts a script produces**. A chart rendered by a plotting library and a workbook written by code
cannot read as generated prose, because they are not prose.

Ship the data close to raw. Clean, self-consistent inputs produce tasks any model solves.

### The governing rule

> **You must know exactly which complication you preserved, and confirm it does not change the correct recommendation, it only makes reaching it harder.**
>
> **If a messy choice could flip the answer, cut it.**

"The answer" there means the main recommendation and every ask a complication does not serve. A **ledgered ask device** from `supplemental-stumping` is the one licensed exception: it may move exactly the ask answers its ledger row names, by the stated deltas, and nothing else, and it has zero rows inside the main call's declared row population, asserted by count in the generator rather than argued. Undesigned mess stays answer-neutral everywhere.

The rule carries extra weight because the **planted-defect flip is banned**, and Gate G bans surface-read rejection as the primary strategy at any depth (`stumping` Part 1). A complication that flips the answer is not merely a determinism risk: it is a banned shape, and the task gets redesigned rather than patched.

**Apply the clean-data test to the pack before you ship it:** if every file were perfectly clean and correct, would the task still be hard and the answer still non-obvious? It has to be, because Gate G bans surface-read rejection as the primary strategy at any depth: a chain of defect corrections fails exactly as a single one does, and depth is no defence. Mess supplies authenticity and length, and the difficulty comes from analysis that clean data would not rescue.

**The inverse pack is a first-class build.** Under G18 the headline figure is genuinely correct and the pack ships three or four *legitimate* things that look like defects: real repeat events that resemble duplicates, a documented decommissioning that resembles a coverage gap, an honest eligibility widening that resembles denominator drift. Each needs its own shipped document establishing it as legitimate, or a solver who corrects it is right and your golden is wrong, and the reconciling artifact must balance **only** when the figure is left as reported. Sweep every combination of adjustments and assert that the unadjusted figure is the sole reconciling one.

Test this explicitly: for every complication, compute the answer with it handled and with it ignored. Both must give the same winner unless the complication is a designed rung of the main ladder or a ledgered ask device, and a ledgered device gets the scoped assertion in §11.6 instead of a pass.

### Good mess (real, and safe)

- **Re-pulls:** the same business key exported again with a later `pull_date`. Row counts overstate activity until collapsed.
- **Catch-up transfers:** a batch that replays part of a local buffer, so record counts run ahead of the periods actually at stake.
- **Aborted / null-measurement records** that carry no value and must be dropped rather than read as zero.
- **Genuine non-response:** whole jurisdictions, periods, or reporting groups that never filed a field. Structure it in blocks, that block structure is what makes it discoverable as non-response rather than measured zero.
- **Mixed date formats** across sources that were built by different teams.
- **Schema drift** in a live feed: a column added mid-period, a code list revised on a dated effective date.
- **Hierarchical records:** parent rows carrying the value and unpriced child rows carrying labels.
- **Duplicate placeholder identifiers** and unconfirmed sentinel values, left visible.
- **Casing and whitespace inconsistency** in join keys, at a realistic rate.

### Bad mess (rejected)

- Random corruption or deliberately unparseable files
- Truncated, password-protected or broken files
- Repeated filler to pad length
- One simple table artificially split to inflate file count
- Decorative documents that carry nothing
- Any complication that could flip the answer

### The reconciling artifact

When you plant structured non-response, ship a rollup that **reconciles only when blanks are left blank**. That rollup is the proof, and it is what lets a solver distinguish "no record" from "record of zero" without being told.

---

## 8. Governing documents

### 8.1 The pin

One sentence, in the highest-authority document in the pack, fixing the decision metric or the scope rule.

- Stated once. Never repeated, never explained, never justified.
- Written as a filed fact: *"Success is measured as [X] at [horizon]. That is the number on the scorecard."*
- Buried in operational noise, logistics, names, dates, distribution list, a "do not forward" footer.

**Before shipping, grep the pack for counter-pins *and for restatements*.** Any file stating the opposite convention at or above the pin's authority level kills the task, and any file *repeating* the pin turns it into a signpost, cleared in one step and quoted back at you. State each load-bearing fact exactly once, in the highest-authority file that carries it. Where a rung must be discoverable without any single file being sufficient, split it instead: one file carries the rule, a second carries the layout fact the rule operates on, and neither alone gets you there.

Authority order, highest first: **the prompt** (which is why no pin may live there, it outranks everything you ship and hands the basis over for free) > governing standard > charter/SOW/terms > decision memo > data dictionary (field semantics only) > workbook method-notes > thread.

### 8.2 The licensed wrong basis

The same document also licenses the wrong path, and it licenses a **basis**, never a ranking. Give the wrong basis a named advocate, a table of constants it operates on, and an explicit
endorsement:

> *"[Named executive] has been working from [wrong basis]. [They] will present it at the review and
> it is what the room will have in front of it."*

> *"A [unit] whose [measure] sits further from its [constant] is a larger [build] on that read. The
> constants are planning facts for it."*

This is what makes the task fair and brutal at once: the wrong path was legitimately available in
writing, and the evidence still refutes it.

**The line, and it is the one that decides Gate G.** The document may say *what basis* the executive
works from. It may not say *which candidate that basis picks*, and no file in the pack may compute
that ranking. A basis is context. A ranking on the decision question is the banned artifact wearing a memo.

### 8.3 The distractors

**Every pack ships two or more distractors.** A distractor is a file the solution never reads that
**looks relevant**: a solver who opens the pack has to consider it and decide for themselves whether
it bears on the question. That act of weighing is the whole point. Solvers rarely fail because they
cannot compute; they fail because they use whatever looks usable and never ask whether it belongs.

A file counts as a distractor only while both of these hold:

- **The solution does not use it.** No step of the correct path reads it, no graded figure depends on
  it, and deleting it changes neither the answer nor any ask. Assert this in the generator by
  recomputing the golden with the file removed.
- **It looks like it might be useful.** It sits in the same world as the decision: the same
  organisation, entities, keys, system or period, a measure adjacent to the one asked for, a topic a
  careful analyst would expect to matter. Good forms: an extract of a neighbouring measure keyed the
  same way, a prior cycle's working file, a report on a related programme, a register for a scope the
  question turns out not to cover, a planning note on an option that was never on the slate.

**A completely unrelated file is not a distractor.** Another department's data with no tie to the
question, a different topic, a file a solver dismisses from its name alone: none of these makes the
solver weigh anything, they read as padding, and they do not count toward the two. The test is
whether a competent analyst would open the file and have to think before setting it aside.

**Named in the task's metadata, never in the pack.** Every distractor is identified in
`metadata.json` in the task folder, beside `prompt.md` and outside `target/`, with its path as it
appears in the shipped bundle (use the portal's key names where its template gives them):

```json
{"distractor_files": ["exports/ops_kpi_dashboard_q4.xlsx", "planning/fleet_refresh_options_2024.docx"]}
```

No file name, sheet name, header or line in the pack calls a file a distractor, and no distractor
carries an in-file warning that it is out of scope. `leak.py` fails the word "distractor" anywhere
under `target/` and in any file name.

**The wrong-basis distractor (optional, stronger).** A distractor may go further and offer a clean
wrong answer: it looks authoritative (official, internal, already done, or recent), its arithmetic
reproduces from its own inputs, and its basis is wrong (an outdated year or business unit, a rule
since amended or superseded, a changed definition), never a planted arithmetic error, which is the
banned flip-the-wrong-number shape. A shipped file rules it out by a fact a careful analyst can
quote (a clause, an effective date, a definition, a control total), and the design note names that
file and line. The ruling-out file may name the distractor outright, because an amendment notice
that names the version it replaces is exactly what makes the fact quotable.

**The Gate G line.** Any distractor that answers the decision question, or a graded quantity, on a
wrong basis is the one such file the pack may ship, and it is licensed only while all four hold:

1. **It is never the stump.** Delete it and the build still stumps a strong solver; the primary
   difficulty lives in the ladder, and ruling it out takes one quotable fact.
2. **Its wrongness is a matter of record** (a date, a scope, a supersession), not an error in its
   numbers, so the clean-data test is untouched.
3. **It is declared in `metadata.json`**, so the reviewer reads it as a deliberate distractor rather
   than as the surface read the task turns on.
4. **Its answer is one the ladder does not need.** It is neither the correct answer nor the decoy
   rung 0 lands on (`stumping` Part 3): matching the decoy would tell a solver who rules it out that
   the decoy is wrong, and matching the answer would confirm the answer. Assert both inequalities in
   the generator, and assert that its figure sits outside the correct answer's bin.

A distractor that answers nothing on the decision question needs none of this; it only has to be
unused and look relevant.

**Not the context artifact, not a background document.** The context artifact (§5) is used by the
solution, so it is never a distractor. A large genuine document shipped for authenticity is
disclaimed in the governing document, *"[Document] is in the folder as background on [topic]; it is
not one of our documents and it does not speak to this decision"*, and because the disclaimer tells
the solver it does not apply, nothing is left to weigh and it never counts as a distractor either.

### 8.4 The social layer

A thread or notes file. Two to four named people. Two hold wrong positions. The owner of the correct answer **argues against it**:

> *"[Correct option] I would not reopen. The detail has us mid-table and it isn't the story the board will recognise. We can cover it through the existing book."*

**They hold beliefs, they do not quote figures.** A voice may say it has always ranked these on
throughput and would not change now. A voice may not quote a computed ranking of the candidates on
the decision question, because that is the banned artifact in dialogue form. Useful side effect: the
burden of making every figure a character quotes recompute mostly disappears, since they are not
quoting figures.

Write it as real correspondence: timestamps, timezones, reply chains, someone slightly annoyed, an
internal-only footer.

### 8.5 Document tone

Write every constructed document as the person would actually write it: a busy operator's tone, concrete logistics, named people, dates that reconcile with the data. Never a data-generation script's voice. Never a summary of the task.

---

## 9. Provenance and hygiene

### Provenance (blocking)

Ship `DATA_NOTES.md` or `export_manifest.csv` stating, per derived file: what it is, what it covers, what it does not cover, and how it was produced. This is what makes a constructed operating layer legitimate under the sourcing rules.

The manifest is also a legitimate place for a real caveat about an extract's coverage, the kind a real data team would flag. Do not use it to hint at the trap.

### Timestamp coherence

Normalise file mtimes to a single in-fiction export date so the pack reads as one coherent pull. **Check that date against the data's own span**, a pack stamped before its latest records is a hygiene flag reviewers notice.

### Identifiers

Use realistic identifier schemes with structure, allocation blocks, check digits, prefixes by entity type, plausible length. Never `id_001, id_002`. Where a generator depends on identifier structure (allocation ranges revealing a former owner), interleave the ranges so the structure is real but not obvious.

### Scale

Match volume to the domain. A national extract is large; a five-account pipeline is small. A pack where every file has exactly 1,000 rows reads as generated.

### Never ship

- A column named `is_correct`, `true_owner`, `should_exclude`, `reconciled_flag`
- A README that explains the analysis
- Any file whose name broadcasts the trap
- An answer-key artifact of any kind

---

## 10. Build order

1. **Restate the pairing, the ladder and the ask ledger** into `DATASET_NOTES.md`: domain, enumerated subdomain, Axis 1 objective, then every rung, its candidate, its killing fact, and which file will carry each, then every supplemental ask's pool, device, and eight-file path from the `supplemental-stumping` ledger, and which files carry each device's two antidotes. Check the objective row in §1 before choosing the spine, because it names the evidence the pack has to carry, and check the ask paths before fixing the file roles, because nine eight-file paths do not fit a pack built ask-blind.

   Open two sections in the same pass and never delete either. **The stump sentence**: the wrong committed answer a competent solver files, and the step that lands them there. Nothing in house tests stump power, so this sentence is the test. And **`## Tried and rejected`**, empty at first, appended to the moment any approach is abandoned, one line naming what was tried and why it died. Use that exact heading so an iteration can grep it, and read it before designing anything, because it is the only record of what has already been paid for. There is one design note per build: no `DESIGN_V2`, no second note, no snapshot of the old one.
2. **Choose and load the spine.** Confirm it has a natural key, published documentation, genuine mess, and a dimension that can differ from the decision grain.
3. **Build the calibration file** (§4). Hardest first, while you still have freedom. Records first, then the outcome rows computed from them (§4.1), with the twin pair in from the start (§4.2), retrofitting it later means rebuilding the extracts anyway.
4. **Build the operating extracts** around it, carrying the trap mechanics.
5. **Build the dimension tables and dictionary**, pinning grain statements (§6.5).
6. **Compute every rung by script** from the files as built (§6.1). Confirm rung separation, the position table, discriminator dominance and the constructed disagreement (§6.2–§6.4).
7. **Build the context artifact** from those computed numbers (§5), labelled for the question it answers, then **the distractors** (§8.3), asserting the golden recomputes unchanged with each one deleted (and, for a wrong-basis distractor, that its answer is neither the correct answer nor the decoy), and write the task's `metadata.json`.
8. **Write the governing document**: pin, licensed wrong basis, background disclaimer, commit demand (§8).
9. **Write the social layer** (§8.4).
10. **Add authentic mess** (§7), then re-run step 6 and confirm nothing moved.
11. **Write provenance and normalise hygiene** (§9).
12. **Verify** (§11), wire the assertion regime (§11.7) and ship the independent verifier (§11.8), all of it before the build is called finished, since nothing in house solves the pack for you and an unasserted defect ships straight to the portal.

**After every later data edit, re-run step 6 in full.** Not the changed rung, all of them. Most collapsed ladders are caused by a parameter tuned for one rung quietly moving another.

---

## 11. Verification

Run all six, **as assertions inside the generator** rather than as a pass you perform by eye (§11.7). Any failure means revise the data, not the ladder.

### 11.1 Rung reproduction
Re-run the regeneration script against the shipped bundle. Every rung's figure, and every rival-killer's figure, reproduces to zero drift. **Rival-killers are audited as hard as the answer**, a number you cannot reproduce fails review outright.

### 11.2 Naive path
Perform the naive analysis end-to-end the way a competent solver would on first contact, without the benefit of the ladder. It must land on a named wrong answer with a defensible chain. If it does not, rung 0 does not exist and the ladder is a rung short.

### 11.3 Each intermediate path
Perform each middle rung's analysis. Each must land on its own named wrong answer, defensibly. Write down, for each: *"a solver who does everything right up to here commits to ___."*

### 11.4 Correct path
Perform the correct analysis from the pack alone. It must land on the answer with ≥1.2× margin, and every step must use only shipped evidence, no outside knowledge, no domain lore.

### 11.5 Fork grid
Enumerate every unpinned choice (window, grain, population, counting convention, missing-value treatment, tie-break, **and maturity / censoring**, any rate measured over cohorts that are not yet fully observed has two defensible populations and they can differ by 2× on the same candidate). Build the grid. **The answer must win in every cell, or the choice must be pinned in a file.** An answer that wins one cell of four is a fork, not a trap.

**Assert the grid cell by cell, never in aggregate.** "Wins 8 of 12" is a summary, not a check. Each losing cell must be named in the build and mapped to the specific shipped rule it violates, the clause it contradicts, the eligibility gate it ignores, the censoring the dictionary excludes. A cell you cannot map is an open fork wearing a count.

### 11.6 Mess neutrality
For every complication in §7, compute the answer with it handled and ignored. Same winner both ways, unless it is a designed rung or a ledgered ask device. A ledgered device gets the scoped assertion instead: it moves exactly the asks its `supplemental-stumping` ledger row names, by the stated deltas, and the count of its rows, and of every hazard's rows, inside the main call's declared row population is asserted to be zero.

### 11.7 The assertion regime

**Rules that live only in a checklist get broken by a later parameter tweak, and nothing rediscovers it before a solver round or the portal does.** A submission is expensive; assertions are free. Every check in this skill should fail the generator run, loudly, at the moment the tweak lands.

Assert in the generator, at minimum:

- **each rung's winner by name**, and each rung's margin (§6.2)
- the **position table**, the answer's rank and distance from the leader at every rung (§6.2)
- **discriminator dominance**, both ratios and their product (§6.3)
- the **constructed disagreement**, per candidate, in both directions (§6.4)
- the **calibration back-test**, correct rule fits N of N within *x*%; each rival misses by ≥ *y*%; the swept-rule count (§4.2)
- the **fork grid, cell by cell**, each losing cell mapped to the rule it violates (§11.5)
- **mess neutrality** for every complication (§11.6)
- **every graded numeric answer's distance to the nearest rounding boundary**, mid-bin. A figure a few thousand from a boundary is a coin flip on grading, and it is free to fix while the data is still soft.
- **every figure any character quotes** in a memo or thread
- **generation tells**, no headline total landing on a round boundary, no share that is an exact round figure, no uniform row counts
- **the single-statement invariant**, each load-bearing fact appears in exactly one shipped file (a fact stated in three files is a signpost, not findability)

Target **40+ assertions**. A build that only asserts the answer is not verified.

### 11.8 The independent verifier

Ship a second script that **reads only the shipped bundle and no generator state**, no in-memory frames, no seeds, no parameters, no side files, and recomputes every rung, every rival-killer, every calibration outcome and every graded figure.

If the verifier cannot recompute a figure from the bundle, **that figure does not exist**, and it will fail review exactly the same way when a determinism reviewer tries.

Record all outcomes in an internal-only notes file so the pack can be regenerated deterministically.

---

## 12. Repair directions

Match the symptom. Diagnosis and hardening escalation live in `stumping` Part 10; these are the **data-side** moves.

| Symptom | Data-side repair |
|---|---|
| Solvers get the answer immediately | Add a rung **below** the current rung 0: engineer the data so an even more natural basis lands on a different candidate. Do not add complexity above, and do not add an artifact that computes it. |
| Solvers reach every insight then commit elsewhere and defend it from a shipped file | **Determinism bug.** Move the pin to a higher-authority document; delete or reframe the counter-pin; relabel the decoy artifact in-file so it explicitly answers a different question. |
| Wrong answers land on a candidate you did not design | A second self-consistent reading exists. Re-solve from that premise to find it, then close it with a pin or remove the ambiguity from the data. |
| Answers scatter shallowly across many candidates | Too much noise, not enough signal. Cut complications that do no work; make each rung's evidence reachable on a plain group-by or join. |
| A solver caught it from one file | Move the discriminator **behind a join** so no single file reveals it. Split the pin's supporting evidence across two documents. |
| A rung's number does not reproduce | You authored forward from a target. Rebuild §6.1: compute from data, write the result. |
| The answer flips under a reasonable variant | Widen the margin in the data, or add a rung that removes the variant from play. |
| A rival gets close on the calibration test | The test does not discriminate. Change the calibration mechanism, do not loosen the tolerance. |
| Wrong answers reach your designed decoy but **no trace performs the decisive step** | A shortcut is beating the measurement, usually lookup transfer. Ship the twin pair (§4.2), or break the single flag that over-determines the name. |
| A trace says a calibration case "cannot be explained" and uses the file **ordinally** | You shipped a row without its records. Build the underlying half so the correct rule reproduces the outcome and every rival misses it (§4.1). |
| Two adjacent rungs name the same candidate | Rung collision from a parameter tuned for a lower rung. Restore separation in the data and assert per-rung winners by name (§6.2). |
| The final rung computes but never changes the ranking | Discriminator dominance failure (§6.3). Widen the decisive spread or shrink the decoy's carried advantage, this is arithmetic, and more documentation cannot fix it. |
| Two axes that were supposed to disagree give the same profile for every candidate | The correlation was never built. Correlate the driver columns per candidate and assert both directions (§6.4). |
| Responses agree on the name but **split on the figure** | An unpinned parameter each solver fits for itself. Fix before touching difficulty. Pin it empirically in the calibration records (§4), never as a labelled convention column. Compare the figure across the portal's responses to see this. |
| The pack reads as generated | Scale variety, identifier structure, document tone, timestamp coherence. Check for uniform row counts, too-clean tables, totals landing on round boundaries. |

**Never repair by:** adding noise, removing needed evidence, introducing arbitrary thresholds, or making files harder to parse. Those produce ambiguity, and ambiguity gets tasks rejected even when models fail.

**Never repair by deletion.** Deleting a signpost that also carried a parameter ships a second self-consistent reading: each solver fits its own convention and the responses come back split on the figure, which is a determinism defect and strictly worse than the difficulty problem you started with. If a signpost must go, replace it with an empirical pin in the same edit.

**Ship both halves of every patch.** A patch that adds a summary row, a rule or a claim without the records that reproduce it leaves the pack worse than before it, and costs a portal run.

---

## 13. Anti-clone at the data level

The `stumping` skill governs scenario distance. These are the pack-level bans.

- **Do not reuse a spine dataset** across consecutive builds.
- **Do not reuse a context-artifact type.** The loud artifact is banned as an organ (Gate G), so what can repeat is the type of file the stakeholder works from: a monitoring export, an operations log, a register, a published series, a capacity report, a close-out summary.
- **Rotate the distractors' types.** A stale KPI dashboard in every build is a template: vary what the relevant-looking unused files are (a neighbouring measure, a prior cycle's working file, a related programme's report, an out-of-scope register), and for a wrong-basis distractor alternate between an outdated vintage, a retired business unit, a superseded rule and a changed definition, and between the ruling-out facts (clause, effective date, definition, control total).
- **Do not reuse a calibration form.** If you used an acknowledgement reconciliation, use a retry log or a pilot ledger next.
- **Do not reuse the operating-extract shape**, a telemetry stream, a certification ledger, a ticket table, and a disbursement extract feel completely different to a solver.
- **Vary pack size and format mix** so packs are not recognisable by their file manifest.

**Distance check:** strip the numbers and names. If the spine, the artifact type, and the calibration form are all repeats, it is the same pack wearing new labels.

**Two mechanical checks carry these bans, and both are free.** Before any data is cut, the build's fingerprint card has to clear `guard.py check` (`../fingerprint/SKILL.md`), which bans a spine whose entity and grain or whose real source dataset repeats a recent build. After the pack is cut, run `python3 .claude/skills/fingerprint/guard.py surface taskNN`, which runs clone-check's mechanical screen focused on this build: byte-identical files, same-seed tables that survived a rename, identical column sets, shared invented names and masked prompt wording, each ranked against how similar the corpus normally is. It spawns nothing. A promoted pair there is a rename or a regeneration before the bundle is called ready, and the adjudicated `/clone-check` stays the author's call.

---

## 14. Checklist

**Scope and sourcing**
- [ ] One domain, one enumerated subdomain, one Axis 1 objective, written in `DATASET_NOTES.md`
- [ ] The pack ships the evidence that objective requires (§1), and the tagged objective is the natural reading of the files
- [ ] No cross-domain evidence leakage
- [ ] Spine is real public data, or the constructed pack is plausible and fully declared
- [ ] Long documents are genuine publications; constructed documents are short and functional
- [ ] Provenance shipped for every derived file

**Structure**
- [ ] 10+ files, 4+ formats, every file does work
- [ ] All ten roles present or deliberately omitted with reason
- [ ] Calibration file present, gap dramatic, test threshold-free if possible
- [ ] Context artifact reproduces to the last digit and is labelled in-file for the question it answers
- [ ] Dictionary pins the grain statements the generators depend on
- [ ] No file name, column name, or note broadcasts the trap
- [ ] No answer-key column anywhere

**Correctness**
- [ ] Every rung reproduces to zero drift, computed forward from the data
- [ ] Every rival-killer reproduces
- [ ] Every calibration outcome reproduces from its own records under the correct rule
- [ ] Each rung lands on a **different** named candidate, re-checked after the last data edit
- [ ] Correct answer ranks **4th or 5th** on the natural pipeline, leads no intermediate rung, sits 2nd on at most one (≥1.20×)
- [ ] **No shipped artifact ranks the candidates on the decision question and gets it wrong**, a declared wrong-basis distractor excepted (§8.3)
- [ ] Each distractor is unused by the solution (golden unchanged with it deleted) and looks relevant enough to need weighing; none is an unrelated file. Any wrong-basis distractor looks authoritative, its arithmetic reproduces, a quotable shipped fact rules it out, the build still stumps with it deleted, and its answer is neither the correct answer nor the decoy
- [ ] No rung margin under 1.15×; final margin ≥1.2×
- [ ] Discriminator dominance holds: decisive edge ≥ 1.2 × the decoy's carried advantage
- [ ] Any two axes the ladder needs to disagree actually disagree per candidate, by construction
- [ ] All evidence for the correct answer is inside the bundle

**Determinism**
- [ ] Fork grid enumerated, including maturity/censoring, answer wins every cell or the choice is pinned, **asserted cell by cell** with each losing cell mapped to the rule it violates
- [ ] Pin sits at or above every counter-pin in the pack, and is stated in exactly one file
- [ ] Twin pair shipped: two calibration cases identical on every lookup-visible column, outcomes ~2× apart
- [ ] Lookup transfer run by hand and lands on the **decoy**
- [ ] The decisive convention is pinned empirically, not as a labelled column
- [ ] Mess neutrality verified for every complication, scoped by the ask ledger: each ledgered device moves only its named asks, and no device or hazard row sits inside the main call's declared row population
- [ ] **Clean-data test run** on the finished pack, and **the litmus answered**: the reported numbers in the pack are correct, and the difficulty is not catching that a read is wrong (`stumping` Part 1)
- [ ] If the pack is a G18 inverse build, every adjustment invitation has its own shipped document making it legitimate, and the reconciling artifact balances only on the unadjusted figure
- [ ] Where the decision window runs past the data pull, the post-cutoff driver ships as a silent operating file and its three assertions are green (§4.3)
- [ ] Every graded figure sits mid-bin, distance to the boundary asserted
- [ ] 40+ assertions in the generator; independent verifier reads only the shipped bundle and passes

**Governing layer**
- [ ] Pin is one unjustified sentence in the highest-authority document
- [ ] Licensed wrong **basis** present with a named advocate, and no file computes the ranking that basis would produce
- [ ] Large non-decisive documents disclaimed
- [ ] Social layer holds wrong beliefs; nobody advocates the right answer; nobody quotes a computed ranking

**Input gates (pass/fail, asserted in the generator)**
- [ ] 10 or more files
- [ ] 3 or more distinct formats, 4 target
- [ ] Either a file of 25,000 or more rows (any format) or a large database file
- [ ] Two or more distractors (unused by the solution, relevant-looking), named in `metadata.json` and nowhere in `target/`
- [ ] Every deliverable the prompt names is present in the requested format
- [ ] Nothing reads as LLM generated

**Hygiene and anti-clone**
- [ ] Real published code vocabularies, real geography, no placeholder identities
- [ ] Timestamps coherent with the data's span
- [ ] Identifiers structured and realistic; scale varies naturally
- [ ] No generation tells: no total on a round boundary, no exactly-round shares, no uniform row counts
- [ ] Any forced-implausible parameter stated in `DATASET_NOTES.md` with its arithmetic and its mitigation
- [ ] Spine, artifact type, and calibration form are not repeats of a prior build


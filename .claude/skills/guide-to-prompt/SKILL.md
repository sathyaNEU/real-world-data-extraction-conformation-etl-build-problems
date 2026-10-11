---
name: guide-to-prompt
description: Decide what to ask before writing a word of the prompt, then write the prompt. Pick one client domain and task type, one Axis 1 objective, a forward-facing Main Recommendation Ask and the prompt shape that supplies the generated rubric's 25 or more criteria. The prompt is prompt.txt, plain text, one continuous paragraph under 1,000 characters that leads with the question, names one to three output files, keeps every figure's unit inside its sentence and states each rounding rule once at the end, with no persona, job title, sign-off chain, roll call of opinions, sequencing words or markdown character. references/prompt-voice.md carries the ten rules and the question forms, references/prompt-economy.md the budget, and references/voice-check.py is the gate, which exits non-zero on any rule. The references/shapes/ library holds the client's eighteen prompt shapes with 72 worked prompts; every worked prompt is an idea seed, never copied. Use at the start of every build, before the stumping skill designs the ladder, and whenever a prompt is written or edited.
---

# Choosing What To Ask, and Writing It

> The prompt is a person asking for help with their task. It leads with the question, names the files it
> wants back, keeps every figure's unit beside the figure and states the rounding once at the end, in one
> paragraph of plain text under 1,000 characters. It carries nothing a solver could use that the files do
> not also carry, and nothing about who is asking.

## The prompt contract

| Fixed, on every build | Where it is checked |
|---|---|
| The file is `prompt.txt`, plain text: no backtick, asterisk, underscore for emphasis, hash, bullet, pipe, bracketed block or blank-line paragraph | `voice-check.py`, `leak.py` sweep 11 |
| One continuous paragraph, under 1,000 characters | `voice-check.py` |
| The question comes first, in the first two sentences, as a direct question | `voice-check.py` |
| One committed call, forward facing by default, resolving to one defensible answer | `stumping` Part 1, `determinism-check` §1 and §2 |
| One to three output files named with their extensions, three the ceiling | `voice-check.py` |
| Every figure's unit inside the sentence that asks for it; every rounding rule stated once, at the end | `voice-check.py`, `determinism-check` §3 |
| 25 or more rubric criteria, supplied by the prompt shape, never by stacking asks | the shape arithmetic in `references/shapes/README.md`, written into the design note |
| No persona's name, no job title, no sign-off chain, no meeting, no reader of the file | `voice-check.py` |
| No roll call of opinions, no sequencing words, no LLM tell, no em dash | `voice-check.py` |
| No input file name, no governing standard by acronym, no method hint, no trap word, nothing that fixes the basis, the window, the convention or the population | `leak.py` sweeps 4, 5 and 11, the leak reader |

`references/prompt-voice.md` carries the author's ten rules and how a prompt still reads differently from
every other under them. `references/prompt-economy.md` carries the budget. The gate:

```
python3 .claude/skills/guide-to-prompt/references/voice-check.py taskNN            # exit 1 on any FAIL
python3 .claude/skills/guide-to-prompt/references/voice-check.py --file <draft> --task taskNN
python3 .claude/skills/guide-to-prompt/references/voice-check.py                   # the batch report
```

A draft that fails a rule is not done. Stage 2 of the pipeline does not close on a failing gate.

## The reference files

| You are working | Load | Contains |
|---|---|---|
| Fixing the draw | `references/exemplars/index.md`, then the two nearest entries | The client's accepted tasks with the model's measured mean: the depth and the kind of analysis the client pays for. Their withheld-method architecture is capped now; take the depth, never the structure |
| Choosing or checking a domain | `references/domains/README.md` | The twenty-one client domains, their task types and the objectives each serves |
| Choosing where the 25 criteria come from | `references/shapes/README.md`, then one shape file | Eighteen shapes: where the criteria come from, how to size past 25, what makes each hard rather than long |
| Shaping the ask for a fixed objective | `references/objectives/<objective>.md` | The objective's definition and the shapes that carry it |
| Writing the prompt | `references/prompt-voice.md`, `references/prompt-economy.md`, `references/voice-check.py` | The ten rules, the question forms, the budget, the gate |

**Every example is an idea seed, never material.** A lifted scenario, entity, metric, file name or ask
wording is a clone, and the review reads it as one. What transfers from an example is the shape of the
answer and the depth of the analysis.

---

## Step 1. One domain and one task type

The domains are the client's taxonomy in `references/domains/README.md`: seven groups, twenty-one domains,
each with its task types. Pick the domain whose decision-maker would own the call, then one task type in it
(the card's `subdomain`). The task type is where the pitfall comes from: its Layer 2 rigor patterns are in
`../stumping/references/client/layer2-rigor-patterns.md` and the domain's Layer 1 techniques in
`../dataset-generation/references/layer1-messiness.md`.

**The task has to use its domain.** The quantity that decides the call is one the field would estimate,
model or test. The swap test: put another field's nouns in ("hospital" for "school", "megawatt-hours" for
"visits"). If the task reads the same, the domain is a backdrop and the draw is wrong. Write the result into
the design note and the card's `domain_test`: the field's own analysis that decides the answer, and why the
swap breaks it. The nine house domains of the earlier spec stay valid on cards already filed; a new draw in
one of them names the client domain it sits in.

## Step 2. One Axis 1 objective

Eight objectives, exactly one per task, and a task tagged outside them is rejected on the tag alone
("Comparative analysis and explanation" is not one).

| Objective | The decision turns on |
|---|---|
| **Forecasting & Predictive Modeling** (the most wanted, and the tiebreak) | A future value or predicted outcome the supplied history can pin down |
| Root-Cause Analysis | Naming the driver of a move, with rival explanations ruled out on evidence |
| Anomaly Detection & Diagnostics | Separating a real event from an artifact |
| Experiment & Causal Analysis | A causal claim, from a designed test or from observational data with confounders |
| Descriptive & Distribution Analysis | How a population is composed or a metric distributed, not why it moved |
| Data Extraction & Conformation (ETL) | Reconciling messy multi-source inputs into one analysis-ready, contract-conforming dataset |
| Opportunity Sizing & Decision Support | A sized opportunity built up from the addressable pool to what can be realised, driving a committed decision; fails its tag if the prompt could be retagged Forecasting or Descriptive without changing a word |
| Data Quality Monitoring & Alerting | The health of the data or of the pipeline that delivers it, with a monitoring or alerting call; fails its tag if the prompt could be retagged Anomaly Detection or Forecasting without changing a word |

The objective is a claim about what the analyst has to produce. The committed call faces forward by default
(a figure filed, booked, ordered or staffed for a window that has not closed), and that does not change the
tag: an ETL build whose figure is an open-period accrual is still ETL. Retag as Forecasting only when the
answer is a predicted value the history pins down. A retrospective call is legal and needs its reason in the
design note.

**Close calls.** Biomedical & Clinical Research is study data on treatments and trials; Epidemiology &
Public Health is populations, exposures and surveillance; Pharmacology is drug exposure and safety;
Healthcare Delivery & Health Economics is the system's operations, costs and claims. Economics covers macro,
labour, trade and fiscal reads, never corporate finance, markets trading or lending. A platform selling into
a sector is Product Analytics with that sector's data as its market.

## Step 3. Save the pairing and run the guard

Write the domain, task type and objective into the design note's `## Draw` section and carry them into the
submission tags. Then `python3 .claude/skills/fingerprint/guard.py recent` and `coverage` before you choose,
and `guard.py check` on the card once the draw is fixed (`../fingerprint/SKILL.md`). The pairing is the
cheapest thing in the build to change, so check it before anything else exists.

---

## The prompt shape, before the ladder

The rubric is generated and has to reach 25 or more criteria. A one-to-three file prompt is a small surface,
so the criteria come from **the structure of the answer**: a ranked list under a cap grades every candidate,
a forecast across periods grades every period, a grid grades every cell, a bridge grades every reconciling
item. That structure is the prompt shape. Load `references/shapes/README.md`, pick the shape whose structure
the data and the decision already have, load that one shape file, and size it on paper: one repeated
structural unit, times how often it repeats, optionally doubled by a second figure per unit, plus the
decision furniture (the call, the runner-up, the gap, the flip threshold, a chart's named parts, the files).
Under 25 means a denser structure, never more asks. Write the arithmetic into the design note.

The shape is not the mechanism: `stumping` decides why the task is hard. Each shape file's "what makes it
hard rather than long" section is the seam between the two.

---

## Writing the prompt

Write it last, after the golden exists, and write it the way a person asks for help with a job they already
understand. The order is context, question, files, rounding, and the whole thing is one paragraph. The ten
rules in `references/prompt-voice.md` are binding; the short form:

1. **Lead with the question**, as a direct question, in the first two sentences.
2. **Cut who and why.** No names, titles, sign-off chains, meetings or readers. A detail stays only if the
   answer would change without it.
3. **Test every fact before cutting it.** A send date, an extract date, a cut-over, a stop rule that bounds
   the computation stays, because removing it could change the answer.
4. **Keep every ask exactly**: file names, columns, periods, units and rounding carry over word for word.
5. **Do not change meaning while smoothing**: "in cents" is not "dollars and cents"; "whether any, and if
   so how many" is not "how many".
6. **One continuous paragraph**, list items joined with commas and semicolons.
7. **Merge and shorten**; state each rounding rule once, at the end, naming the figures it governs.
8. **Ask, do not specify**: "what is", "put it in", "also give me", never "X is the file, one row per".
9. **Drop claims made only to be rejected.** An opinion arguing the wrong answer is banned as the decisive
   stump and is cut by default.
10. **Run the 10/10 check last**: does the answer turn on real analysis, or only on following a stated
    procedure or reading a field correctly? If the latter, the build is not ready, whatever the prompt says.

Units travel with their figures ("in Australian dollars", "in mg/L", "tons a year") because that is how a
person says them; rounding is a convention and is stated once ("Tons and concentrations go to two
significant figures, days to one decimal and the volume to the nearest thousand cubic yards").

### What the prompt may say

The question, with the candidate set when the decision is one of N and the hold licensed as one option on
the same footing ("or none this cycle") when the answer may be a hold. The forcing fact that bounds the
computation (the window, the date, the cut-over, the stop rule), stated once. The files wanted back, by name
with extension, and what each has to carry at the level of content ("one stacked bar per district ordered
by high-rated releases, each high segment labelled with its count, the title naming the district with the
most"). The standard the call runs on, only where the pack does not carry it and never in a form that fixes
the basis, the window or the population. The generic threat to validity in the open ("participation was
voluntary"), never which evidence resolves it.

### What the prompt may never say

Any sentence that fixes the decision basis, the measurement window, the scoring convention or the
population: the prompt outranks every shipped file, so such a sentence answers the question before a file
is opened. The deciding metric, the eligibility rule, the fee schedule, an input file name, a standard by
acronym, a method hint ("compare A against B"), a trap word (clean, unduplicated, reconcile, attribution,
mix, standardise, grain), more than one metric named as valid, a warning that a view might mislead. And,
under the ten rules, any person, title, meeting, sign-off or reader.

### The committed call, the asks and H18

The call is one whole sentence a reader can quote, carrying its unit. Every other ask's answer is a
component of the call, a direct qualifier of it (its sensitivity, its flip condition, its reconciliation to
another total) or the trail that audits it. An ask a person could act on with the call unmade (a figure for
another period, another population's exposure, a different decision) is a second decision in the same file
and a first-pass rejection (`../reduce-house-fixes/SKILL.md` H18). The asks are designed in
`../supplemental-stumping/SKILL.md` before any data is cut, each multi-dimensional, decoupled from the main
call's computation, and designed to hold against the solver that lands the call.

Every ask passes six tests: a named **use** (who acts on the answer), **provenance** independent of the
criteria count, the right **genre** for the file it sits in, the stakeholder's **vocabulary** rather than
the analyst's, **asymmetry** across the set, and nothing the organisation would **already know**. An ask
that names an entity and asks for an aggregate names the grain, because both readings are computed and
differ. An ask that fails a test is re-cut to the decision it serves or folded into the adjacent
multi-dimensional ask, never deleted, because deletion costs criteria the shape needs.

---

## Handoff

1. Pairing saved, task type named, `guard.py check` clear of BLOCK.
2. Prompt shape picked and its arithmetic at 25 or more in the design note.
3. `stumping` designs the ladder on paper, `supplemental-stumping` the asks, `determinism-check` the closure
   table and the semantic fork table; `precut.py` passes before any data is cut.
4. `dataset-generation` builds the pack; `submission-writeup` and `golden-realism` follow.
5. The prompt is written last against the golden, through `references/prompt-voice.md`, and
   `voice-check.py taskNN` passes.

## Checklist

- [ ] One client domain and one task type, the decision-maker's own; the swap test written into `domain_test`
- [ ] One of the eight objectives, with the discriminating test passed for Opportunity Sizing or Data Quality Monitoring
- [ ] A prompt shape picked, its arithmetic at 25 or more before any file exists
- [ ] `prompt.txt`, plain text, one paragraph, under 1,000 characters, question in the first two sentences
- [ ] One to three files named with extensions; every figure's unit inline; every rounding rule once at the end
- [ ] No name, title, sign-off, meeting, reader, roll call, sequencing word, LLM tell or em dash
- [ ] Nothing that fixes the basis, window, convention or population; no input file, acronym, method hint or trap word
- [ ] The call is one quotable sentence; every ask passes H18 and the six realism tests
- [ ] `voice-check.py taskNN` exits 0

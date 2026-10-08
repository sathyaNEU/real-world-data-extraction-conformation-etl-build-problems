---
name: golden-realism
description: Make every golden deliverable look like a work product a real analyst produced, because a golden that reads as overly LLM-generated is sent back even when every figure recomputes. Carries the tells a reviewer reads at a glance, the per-format editing passes for memos, workbooks, decks, charts, conformed data and code, the metadata scrub, and the hard line that realism is presentation and may never move a graded figure or open a second reading. Use after the golden's numbers are correct and before the bundle is declared ready, on any deliverable an LLM drafted, and when a submission comes back for looking machine-made.
---

# Golden Realism

> A golden has two kinds of correctness. Every figure has to recompute, which `determinism-check`
> measures. And the file has to look like something a person made at work, which nothing measures
> until a reviewer opens it and decides in about four seconds.

**The client's position:** golden solution files that do not look like something produced in a
real-work environment, or that look overly LLM-generated, are sent back. Using an LLM to help is
explicitly fine. **Shipping its first draft is not.** So this skill is not a generation recipe, it is an **editing pass over a
draft that already exists and is already numerically correct.**

**When to run it.** After the golden's figures are right and asserted, before the bundle is
declared ready. It runs alongside `reduce-house-fixes`, which owns the container (H1 metadata) and
the write-up prose (H2, H3). This skill owns what the deliverable looks like when a human opens
it.

**The hard line, and it outranks everything below.** Realism is **presentation**. No move in this
skill may change a graded figure, alter a value the rubric checks, or introduce a second defensible
reading of any ask. A "realistic caveat" that makes a number ambiguous is a Gate E failure, and
trading a determinism gate for a realism impression is the worst trade available in this pipeline.
When a realism move and a determinism gate collide, the gate wins and the move is dropped.

---

## Part 1. The tells, which are format-independent

A reviewer does not audit a golden to decide it is machine-made. They recognise it. These are what
they recognise, and every one of them is a property of the draft rather than of the analysis.

**1. Uniform precision.** Every figure carries the same number of decimals regardless of what it
counts. Real work products vary precision by quantity: headcounts are whole, money is to the cent
at invoice scale and to the thousand at budget scale, rates run to one decimal, and a ratio nobody
acts on gets rounded harder than one that decides something. Uniform precision is the single
fastest tell and it is visible without reading a word.

**2. Default styling, untouched.** The plotting library's first colour, the workbook's default
column width, the deck's stock template, the 8.43-character columns, the legend box where the
library put it. Nobody who cared about a document leaves all of it at default, and a reviewer knows
which library produced a chart from its palette alone.

**3. The four-heading spine.** Executive Summary, Key Findings, Recommendations, Next Steps, in
that order, on a document nobody at that organisation would structure that way. Real internal
documents are shaped by their own genre: a determination has a standard and a finding, a
reconciliation has a bridge, a renewal memo has the test and the result. Take the shape from the
decision, not from the template.

**4. Sections of identical length.** Three to five sentences each, evenly. Real documents are
lopsided: the part carrying the decision is long, the part nobody argues about is one line.

**5. Everything in threes.** Three bullets, three risks, three next steps, three items per list,
forever. Real lists are whatever length the world is: two, or seven, or one.

**6. Bulleted where a person would write, prose where a person would list.** An LLM bullets the
argument and writes prose about the enumerable. Invert it: the decision and its defence are
paragraphs, and the things that genuinely enumerate (the candidates, the periods, the exceptions)
are the list or the table.

**7. No trace of having been used.** This is the deepest tell and the one that survives every
surface fix. A real work product carries the residue of the argument that produced it: a footnote
on a definition somebody disputed, an exclusion noted because a reader will ask, a rounding
convention stated because two people computed it differently, a column that exists because
somebody needed it once. **The honest source of that residue is the pack's own fiction**, which
already contains the disputes, the definitions and the corrections, so the golden references them
rather than inventing texture.

**8. The hedge register.** "This analysis suggests", "it is important to note", "comprehensive",
"robust", "leverage", "key insights", "actionable". A memo whose whole job is to commit to one call
does not hedge in its own voice.

**9. Titles that restate the task instead of the finding.** "Analysis of Regional Performance" is a
draft title. The finding is the title.

**10. The generic file name.** `analysis_report.pdf` is not the best-suited deliverable for every
task and is rarely the right name for any. Name the file after the decision, in the vocabulary of
the organisation that would file it.

---

## Part 2. The per-format passes

Run the pass for each format the golden ships. Each pass is a list of the things the draft will not
have done, because a library's defaults are what an LLM leaves behind.

### Text: PDF, DOCX

- **An identifying block a real document has**, in that organisation's genre: the addressee and
  author, the date, the subject line, a file or matter reference where the fiction has one.
- **Page numbers**, and a running header or footer where the genre carries one.
- **A title that states the finding**, not the assignment.
- **Lopsided sections.** The decision section is the longest thing in the document.
- **The decision written as prose**, with the enumerable material in a table.
- **At least one genuine footnote**: a definitional note, a stated exclusion, a rounding convention,
  an as-of date. It must be true of the pack and must not open a second reading of any ask.
- **A source line under every table**, naming what the figures were computed from in the fiction's
  own vocabulary.
- **Varying precision per quantity**, per the tell above.
- **No "Executive Summary / Key Findings / Recommendations / Next Steps"** unless that genre
  genuinely uses it.

### Data: XLSX

The workbook is where the draft shows most, because a spreadsheet has a dozen affordances an LLM
never touches.

- **Sheet names that say what the sheet holds.** Never `Sheet1`.
- **A frozen header row**, and frozen key columns where the table is wide.
- **Column widths set to content**, not the 8.43 default.
- **Number formats per column**: currency with its symbol, percentages as percentages, thousands
  separators on counts, dates as dates. A raw float showing fourteen decimals is the loudest tell
  in the format.
- **Alignment by type**: numbers right, text left, headers distinguished.
- **A total row that ties**, computed from the unrounded source rather than by summing the
  displayed column, and reconciling to whatever other deliverable cites it.
- **A print area and repeat-rows** where a person would print it.
- **A notes or definitions sheet** carrying the field definitions, the as-of date and the
  exclusions, in the fiction's vocabulary.
- **No leftover autofilter on a sheet that would not have one**, and one on the sheet that would.

### Visual: PPTX

- **Slide titles that state the finding as a sentence**, not a noun phrase.
- **The chart is the slide.** A slide of bullets describing a chart is a draft artifact.
- **Slide numbers**, and a source strip where the deck would carry one.
- **The stock template replaced**, or at minimum the colours and type set deliberately.

### Visual: PNG, SVG, and charts embedded anywhere

**Load the `dataviz` skill before styling any chart**; it carries the palette, the form heuristic
and the accessibility checks. On top of that, the realism-specific pass:

- **Axis labels carrying units**, and tick labels formatted the way a person reads them (thousands
  separators, currency, percentages), never scientific notation.
- **A title that states the finding.**
- **The reference or threshold line labelled with its value**, which the prompt asked for anyway.
- **The key point annotated.**
- **A deliberate palette**, not the library's default cycle, and the recommended item distinguished
  rather than left in sequence colour.
- **A figure size and resolution chosen for where it lands**, a slide, a page or a screen.

### Data: CSV, TSV, JSON, Parquet

- **Column names in the source systems' vocabulary**, not the prompt's wording.
- **A stated, stable sort**, and the same sort every time it regenerates.
- **Consistent precision per column**, and ISO dates.
- **Booleans in the format the consuming system uses**, not Python's `True`/`False` unless that is
  the fiction.
- **A schema or data dictionary alongside** where the fiction would have one.

### Code: PY, IPYNB, SQL, R

- **Constants at the top, read from the pack**, never hardcoded twice.
- **Assertions on the control totals**, which is what a real analyst leaves in after being burned.
- **Formatted output with units**, because the deliverable is what it **prints**, not what it
  computes.
- **Comments only where a choice was made**, never `# load the data`. A comment explaining the
  obvious is the code equivalent of the hedge register.
- **In a notebook: outputs present and consistent with a single top-to-bottom run**, and markdown
  cells that carry the argument rather than restating the next cell.

---

## Part 3. The container

The file's metadata gives away the writer even when the content does not.
`reduce-house-fixes` H1 owns this and ships the tool:

```
python3 .claude/skills/reduce-house-fixes/scripts/scrub_producer_metadata.py <dir>
python3 .claude/skills/reduce-house-fixes/scripts/scrub_producer_metadata.py <dir> --apply \
    --producer "<the organisation in the fiction>" --stamp <the in-fiction date>
```

Audit first, because the right producer name and the right in-fiction date are properties of the
build's own fiction and cannot be guessed. The repair never re-saves through the writing library,
which would reintroduce the signature it removes.

---

## Part 4. Where the texture honestly comes from

The temptation, once tell 7 is understood, is to invent imperfection. Do not. **Every piece of
texture in a golden has to be true of the pack**, or it is a second fiction the reviewer can catch
and the determinism judge can trip over.

The honest sources, in order of preference:

1. **The pack's own governing documents.** A definition the standard states, an exclusion the memo
   files, a tolerance the contract sets. Citing one in a footnote is texture and evidence at once.
2. **The pack's own disputes.** The social layer already contains someone holding a belief and
   someone correcting a record. A golden that acknowledges the dispute and states how it was
   resolved reads exactly like a document that was argued over, because in the fiction it was.
3. **The analysis's own conventions.** The rounding rule, the as-of date, the population after
   exclusions, the grain. Stating them is what a careful analyst does, and every one of them is
   already pinned or the build has a Gate E problem.

**What is never a source:** a fabricated caveat, a fake revision history, an invented reviewer's
initials, a "data quality note" describing a problem the pack does not have, or a deliberate
imperfection in a value. The last one is the dangerous one: a figure made scruffy for realism is a
wrong figure, and Gate A fails on it.

---

## Part 5. The pass, in order

1. **Numbers first, and frozen.** Do not start this pass until every figure is correct and
   asserted. Realism edits presentation, so a figure that changes afterwards invalidates the pass.
2. **Read the draft as a reviewer**, once, from the top, at speed. Note what you recognise from
   Part 1 before you fix anything, because the recognition is the measurement.
3. **Run the format pass** for each deliverable.
4. **Add texture from Part 4's honest sources only**, and check each addition against the asks: it
   must not answer one, contradict one, or open a second reading of one.
5. **Scrub the container** (Part 3).
6. **Re-run the bundle verifier.** Every graded figure must still recompute to the same value, in
   every file, to the same rounding. A realism pass that moves a number has failed.
7. **Read it once more cold.** If it still reads as a template, the problem is usually the
   structure rather than the styling, which is tell 3.

---

## Checklist

- [ ] Every figure was correct and asserted **before** this pass began, and still is after it
- [ ] No realism edit changed a graded value, answered an ask, or opened a second reading of one
- [ ] Precision varies by quantity rather than being uniform across the document
- [ ] No default library styling survives anywhere: palette, column widths, template, legend placement
- [ ] The document's structure comes from its genre, not from the four-heading spine
- [ ] Sections are lopsided, with the decision carrying the most room
- [ ] Lists are whatever length the world is, not uniformly three
- [ ] The argument is prose and the enumerable material is a table or list, not the reverse
- [ ] At least one genuine footnote or note, sourced from the pack's own documents, disputes or conventions
- [ ] No fabricated caveat, revision history, initials or invented data-quality note anywhere
- [ ] Titles state findings; file names are named after the decision, in the fiction's vocabulary
- [ ] No hedge register: no "suggests", "it is important to note", "comprehensive", "robust", "leverage"
- [ ] Workbooks: named sheets, frozen header, set widths, number formats, tied total row, definitions sheet
- [ ] Charts: `dataviz` loaded, units on axes, formatted ticks, labelled threshold at its value, annotation, deliberate palette
- [ ] Code: constants read from the pack, control-total assertions, formatted prints, no narrating comments
- [ ] Container scrubbed via `reduce-house-fixes/scripts/scrub_producer_metadata.py`, audited before applied
- [ ] Bundle verifier green after the pass, every shared figure agreeing across every file to the same rounding

---
name: reduce-house-fixes
description: The register of defects the author has had to fix by hand after a build was already called finished. Each entry carries the general form of the defect rather than the incident, what it costs when a reviewer finds it, and the check that would have caught it before the bundle shipped. Use as the last pass before a bundle is declared ready, when a house fix comes back from submission and has to be recorded, and alongside the stumping pre-ship checklist, which routes here.
---

# House Fixes

> A house fix is a defect the author caught after the build was called finished. Every one of them was cheap to prevent and expensive to catch, and every one of them was invisible to the checks the build already ran, which is the only reason it survived to submission.

This skill is a **register, not a procedure**. It grows one entry at a time, each entry written down at the level where it generalises, so the next build fails a check instead of repeating the incident. The incidents themselves are not interesting. What is interesting is the class each one belongs to, because the class is what recurs.

**The governing idea.** A build has two kinds of correctness. The analysis has to be right, which is what `determinism-check` measures, and the artifact has to be *what it claims to be*, which nothing measures until a reviewer opens it. House fixes cluster in the second kind. They are not analytical errors, so no rung moves and no figure changes, and that is exactly why they slip through: the build's own verification is pointed at the analysis and looks straight past everything the analysis ships inside, the container in H1 and the prose in H2.

**When to run this.** After the data is cut and before the bundle is declared ready, which is the last moment a fix is free. `stumping` Part 12 routes here as the final pre-ship block. Running it earlier is fine and running it later is a house fix.

**Reading the register and writing to it are two different jobs, and only one of them is urgent.** Reading it, and running its checks over the build, is part of delivery and happens before the bundle is handed over. Writing a *new* entry into it is bookkeeping: it happens after the author has the build, and for a defect the portal or the author actually surfaced, never speculatively. See the working-method rules in `CLAUDE.md`.

**Run `golden-realism` alongside it.** The two split the second kind of correctness between them: this register owns the **container** (H1's producer metadata and build clock) and the **write-up prose** (H2, H3), and `golden-realism` owns **what a deliverable looks like when a reviewer opens it**, which is a stated send-back cause. H1's `scripts/scrub_producer_metadata.py` is the tool both of them use for the container.

**Wire every check in the register into the build's own verifier.** A check you perform by eye is a check that stops being performed the moment the build gets long. Each entry below names the assertion, and it belongs in whichever of the build's verifiers already covers that surface, `verify_pack.py` for the bundle and the submission verifier for the write-up, so a rebuild cannot quietly reintroduce the defect.

---

## H1. A generated binary carries its writer's name and the build clock

**The general form.** Every library that writes an Office file, a PDF or an image stamps its own identity and a real-clock timestamp into the file's metadata. `python-docx` writes itself into `dc:creator` and `dc:description`, `openpyxl` writes itself into `dc:creator` and into `<Application>`, `reportlab` writes itself into the PDF `/Producer` and `/Creator`, `matplotlib` writes itself into PNG text chunks. None of this is in the document body, so it survives every check that reads the document's text, and all of it is one click away for anyone who opens the file properties.

**What it costs.** Two distinct things, and they are worth separating because the second is the worse one.

The **signature** breaks the fiction. A nonprofit's finance committee minutes authored by `python-docx` is not an internal record, it is a generated prop, and the input gates require files that do not read as LLM generated. A reviewer who opens one file and sees the writer's name has been told how the whole pack was made.

The **timestamp** does worse, because it is a *fact that contradicts the setting*. A pack set in November 2024 whose workbook records a creation date in the build year is dated to the build machine, and unlike the signature it is a concrete inconsistency a reviewer can point at. `dataset-generation` §9 already requires the filesystem mtimes to be normalised to one in-fiction export date. That rule stops at the filesystem. It says nothing about the timestamps *inside* the container, and those are the ones that are visible without a terminal.

Contradiction runs **both ways**, which is easy to miss because only one direction is intuitive. A timestamp later than the setting is the obvious tell. A library's *default* timestamp is the same tell pointing backwards, and `python-docx` stamps 2013 into every file it writes, so a 2024 document carrying a 2013 creation date is just as inconsistent and sails past an assertion written as "not later than the setting". Assert a plausible band around the setting rather than a ceiling.

**Where the line falls, because not every stamp is a defect.** The rule is about **input files**, the ones the fiction says an organisation produced. A signature there is a lie about provenance. A signature in a **golden deliverable** is not, because the prompt asked for a script-produced artifact and the deliverable genuinely is one, so `matplotlib` in the chart the analysis emitted is honest and should be left alone. Scrub the inputs. Leave the outputs.

**The two halves separate here, and only the signature half stops at the inputs.** `golden-realism` is a gate and its checklist requires the container scrubbed on every golden, which reads against the line above until the signature and the timestamp are taken apart. A signature on an output is honest, so removing it is optional and removing it costs nothing. A **timestamp** on an output is not, whenever the deliverable's own body states a date: a board paper that prints its circulation date and carries a creation date from the build year contradicts itself inside one file, and that is the concrete inconsistency this entry exists to kill wherever it sits. So the timestamp rule binds on **every shipped file whose content states a date**, golden included, and the signature rule stops at the inputs. A build that scrubs both on its goldens satisfies both skills, which is the cheap way out of the disagreement.

**The scrub has to live in whichever generator writes the file, and a build usually has two.** Where the pack generator scrubs and the deliverable generator does not, the bundle ships clean inputs and stamped outputs, and the audit passes because it was pointed at the input tree. Point it at both directories, and read any corpus-wide sweep of the input trees as evidence about inputs only.

**The check.** Sweep every shipped input binary and assert two things: no writer's name anywhere in its metadata, and no timestamp outside a plausible band around the setting's date. For OOXML that means reading the `docProps/` entries out of the zip, for PDF the trailer, and for an image the text chunks, which for this purpose is a substring sweep over the whole file. Wire all three branches even when the pack currently ships no file of one kind, because a promised check that the assertion does not perform is worse than no promise.

**How to repair without collateral.** The repair is a byte-level rewrite, never a re-save, because re-saving through the same library rewrites everything and reintroduces the signature it was meant to remove.

*By format.*

- **OOXML.** Repack the archive with the same entry names in the same order, substituting only inside `docProps/`. Assert afterwards that every other entry's CRC is unchanged, which is the only check that actually proves the document body was untouched. Confirming the new string is present proves nothing about what else moved.
- **PDF.** Substitute in place at **equal byte length**, because the xref is a table of byte offsets and a shorter file silently corrupts every offset after the edit. Spend the surplus bytes as whitespace **between dictionary tokens**, where the format ignores them, and never as padding inside the value, because a `/Producer` padded out to length reads back with trailing spaces and one machine-made tell has been swapped for another. Padding inside a PDF *comment* is fine, a reader never sees it.

*Two ways the repair itself goes wrong*, both found by building the repair rather than by reasoning about it.

- **Swallowing the marker.** The producer name also appears in PDF comment lines. Substituting the whole line replaces the leading `%` along with the text, which turns a comment into loose tokens and corrupts the file. Substitute only the text after the marker, and keep the marker and its indentation.
- **Verifying with a reader that degrades instead of raising.** `pypdf` logs a broken xref and returns whatever it can still parse, so comparing extracted text before and after passes on a file that no longer opens. A verification that compares output rather than asserting the artifact is well formed will confirm a corruption as a success. Assert the repaired file parses with **no errors logged**, then compare the text. The general form carries past PDFs: when the check and the defect share a tolerant reader, the check cannot see the defect.

*Where the repair has to live.* A hand repair is correct exactly once and is undone by the next rebuild, so the scrub belongs immediately after each save call in the generator. Then **run it**, because a scrub that has never executed is a claim and not a fix, and the hand repair sitting on disk hides that, since the bundle looks right either way. Execute it against the pre-repair originals, which you get by re-running the generator into a scratch directory rather than by keeping a backup copy around, and confirm it reproduces the shipped file. The generator is the restore path, so a build that needs a snapshot zip to check its own scrub has a generator that does not rebuild, and that is the defect to fix first. Byte-for-byte agreement is the target and is usually reachable; where it is not, every difference should be somewhere no reader looks, and you should be able to say where and why.

**Tooling.** `scripts/scrub_producer_metadata.py` audits or repairs a bundle directory and carries all of the above. It audits by default and writes nothing, because the in-fiction author and export date are properties of the build's own fiction and cannot be guessed from the pack. Repair needs both stated explicitly, restores the original on any failed assertion, and is a retrofit for bundles already cut, not a substitute for scrubbing in the generator.

*Reading its output, because the two columns are not the same severity.* A producer name is a defect wherever it appears on an input file, with no band to judge and nothing to weigh. A timestamp is a defect only against the band the build's own setting allows, so pass `--floor` and `--ceiling` from the fiction and not from the calendar. Without them the audit reports every stamp it finds and judges none of them, which is the honest behaviour but is not a verdict. The repair rewrites only the stamps the audit flagged, so an in-fiction date is never silently moved by a run aimed at the producer name.

---

## H2. A figure in the write-up whose derivation is not on disk

**The general form.** A supporting figure gets quoted in the design note or the submission, usually a count of enumerated cases or a separation margin, and its derivation lives in a scratch search script rather than in the shipped verifier. The script was a *design tool*, run once to choose the configuration, and it never became a check on the configuration that was chosen. Months later nothing on disk reproduces the number, and often the number does not even reconcile with the script that looks like it produced it.

**What it costs.** It is a direct violation of the standing rule that a number which cannot be recomputed does not exist, and it is worse than an ordinary arithmetic slip in one specific way. The load-bearing figures are all verified, so the build passes its own checks and passes a determinism review, and the unreproducible figure sits in the write-up looking exactly as authoritative as the ones that recompute. A reviewer who tries to reproduce it and cannot has learned that the write-up's figures are not uniformly trustworthy, which is a finding about the whole document rather than about one sentence.

*Why the search script is not the verifier.* A search script sweeps a space of candidate configurations to find one worth building. Its output is a ranking over configurations that were never built. The shipped bundle is one point in that space, and the enumeration a write-up wants to quote is the grid *around that point*. Those are different computations, and the second one usually was never written down at all. If a script `exec`s something out of `/tmp`, it is a scratch tool by definition and it is not evidence of anything.

**Where the line falls, because not every unreproducible number is a defect.** The rule binds on figures the analysis *derived*. A **parameter** is different: the number of places a cycle carries, a band boundary, a payment schedule are choices the fiction made, and they recompute from nothing because nothing computed them. They have to be *consistent* with the bundle, meaning the file that states them says the same thing, but demanding they derive from data is a category error that sends you looking for an enumeration that never existed. The test is whether the figure answers "what did we choose" or "what did the data give us". Only the second has to recompute.

**The check, and the way the check usually fails.** Every figure quoted in a shipped document recomputes from the shipped bundle, and that includes the supporting figures, not only the answer and the rungs.

A build that already ships a submission verifier is not covered by it, which is the part worth internalising, because the sweep catches **only the unit classes its own regex matches**. A sweep written as comma-formatted integers of a thousand or more sees the appropriation and every band total, and it is structurally blind to a percentage, a ratio, a bare count and a decimal. It reports a clean pass over dozens of figures while a claim in an unswept class sits beside them unverified, and the pass is what makes it invisible. The same shape appears in H1, where a tolerant PDF reader confirmed a corrupted file: **when the check and the defect share a blind spot, the check certifies the defect.** Suspect any verification whose clean result is what stopped you looking.

So enumerate the numeric claims in every shipped document **by unit class**, and for each class name the thing that sweeps it. A class nothing sweeps is where the next H2 is. Two extensions follow from that and both are cheap. Sweep the **design note** as well as the submission, since it usually carries several times more derived figures and typically has no verifier pointed at it at all. And read every claim about an enumeration by hand whatever the sweep says, asking of each which script prints this, because such claims are stated as prose rather than as a quantity with a unit and no regex will ever find them.

*The enumeration is usually wrong in its dimensions, not its arithmetic.* A grid claim is a count of combinations, so it is the product of the axes someone listed, and the way it fails is that an axis was missed. A pack carrying six binary conforming moves enumerates sixty-four cells and not thirty-two, and the write-up quoting the smaller number is not describing the space it shipped. Before trusting any such count, re-derive the **axis list** from the bundle rather than the count from the script, because a wrong axis list produces an arithmetically flawless wrong total.

*Measuring almost always strengthens the claim.* A stale separation figure is usually stale in the direction that flatters nobody: the measured margin comes back wider than the one asserted, the shortcut recovers fewer cases than claimed, the bound holds further out. The fear that measuring will weaken the argument is what leaves these figures unmeasured, and it is close to always wrong. Measure and the sentence gets stronger.

*State the tightest margin, not only the comfortable ones.* A build reports the separations that are wide. The one worth recording is the **thinnest boundary in the pack**, the observation that came closest to falling the other way and what it would have moved if it had. A margin of a few dollars on a threshold that does not change the answer is still the number a reviewer wants to see you already knew. Unstated, it reads as undiscovered; stated with its consequence, it reads as controlled.

*Name the cell, not just the margin.* "The answer sits nine per cent clear of the nearest wrong cell" is unverifiable as written. State which cell, what reading produces it, and what it evaluates to, and the claim becomes checkable by anyone and stops being a number you have to be trusted on. It also forces the measurement, which is where these figures usually turn out to be off.

**How to repair without collateral.**

*When it cannot be re-derived, restate rather than reconstruct.* If the enumeration is genuinely gone, do not reconstruct a plausible one, because a reconstructed figure that happens to be wrong is a worse defect than the one being fixed. Replace the specific claim with the weaker claim that is still supportable and still carries the operative content. A margin restated from 12 per cent to a measured 21 per cent, against a floor moved from 10 to 20, says the same operative thing, that no wrong reading lands near the answer, and it says it in a form that reproduces.

*Fix the figure everywhere it appears.* The same claim is usually stated twice in different wording, once as prose in the design note and once as a row in a summary table, and the standing rule is that a figure shared between two deliverables agrees in both. Fixing the sentence the review named and leaving the table row creates exactly the inconsistency the rule exists to prevent. Grep the figure, not the sentence.

---

## H3. The prose around a computed figure is the part nothing checks

**The general form.** The figure is computed by script and correct. The sentence carrying it is written by hand and never re-derived. So the digits are verified and the words are not, and the words make claims of their own: how many things were summed, what the figure is measured against, whose population it describes, what unit it is in, and what the things it names actually are. Each of those drifts independently of the number it sits beside, and a figure sweep confirms the digits while every one of those claims goes unread.

**What it costs.** Always a reviewer's finding rather than a typo, because the number survives the check and the sentence is wrong in a way that reads as authoritative. The recurring shapes:

- **The count word.** A sentence says three and sums four, or names three of the four it summed.
- **The comparator.** The percentages are correct against one baseline and the sentence names a different one. A reader recomputes against what the words say, gets different figures, and concludes the numbers are wrong when it is the sentence that is.
- **The population.** Shares belonging to the whole account get attributed to the subset, or the reverse. Both populations exist in the bundle, so both readings look supported and neither is flagged.
- **The keying parameter.** The script reads a date, a threshold or a cut-off out of a shipped file and the prose beside it restates that parameter by hand, so the figure is computed off the file and described off the author's memory. It is the worst member of this class where the parameter also bounds a window, because a reader who follows the words computes a genuinely different quantity and lands somewhere the pack never says, and the two dates sit one day apart with a boundary population between them. It hides better than the others, since the parameter is not a result and no figure sweep has any reason to look at it. State it once from the file, and where the write-up names it in prose, say which shipped file it was read from in the same sentence.
- **The unit.** A currency total printed under a count label. Dimensionally wrong and invisible, because the digits are real digits that reconcile to something.
- **The label.** A category name applied to members that do not belong to it, which is a claim about the data that the data refutes.
- **The rounding path.** One quantity stated twice in one document, once summed from rounded parts and once rounded from the sum, differing in the last place. Both are defensible and the document cannot assert both.
- **The distance to a rival.** A wrong reading described as one correction away when reproducing it takes two, which understates how far the rival sits and overstates the ladder.
- **The stated reason.** A sentence gives a true conclusion and a false reason for it. The claim survives spot-checking because the conclusion is right, and the reason is what a reviewer actually tests.
- **The bound.** A claim of the form "nothing exceeds Y" is a maximum and has to be computed. Estimated, it is wrong by exactly the case that matters, and one counterexample retires the sentence. And computed is not yet safe: the print format has to round in the bound's own direction, because a floor claim ("at least Y") emitted through nearest-rounding overstates whenever the true minimum rounds up, and the sentence is then false by a fraction of a point with the correct arithmetic sitting right behind it. Emit floors with floor and ceilings with ceil at every surface that states the bound, and have the verifier recompute the extremum and assert the printed token against its own value rather than against the generator's.
- **The referent of a statistic.** A median quoted without saying a median of what, over which population, across which window. The number is right and names nothing, so it cannot be reproduced or contradicted.
- **The rounding rule the pack itself states.** Where a shipped document fixes a rounding convention, the write-up has to apply it. A figure carried at more places, or truncated where the rule says round, makes the key appear to disagree with runs that computed the identical quantity correctly.
- **The twin claim.** "The only thing separating these two is X" is a structural assertion about the whole record, not a remark. Verify it across every field, because a pair differing on two axes is not a twin pair and the sentence resting on it collapses.

**Where the line falls.** Two statements of one quantity may legitimately differ by rounding path when the document says which is which, since an account-level file that totals rounded rows is doing the honest thing. What is banned is presenting both as the same quantity with no such statement, because then one of them is simply wrong.

**The check.** Of every sentence carrying a figure, ask four things of the *words*: how many, against what, of whom, in what unit. None of the four is checked by anything that sweeps numbers. Then prefer to remove the problem rather than police it: **emit the words from the same objects that produced the number.** Take the count from the length of the list, build the enumeration by joining that list, name the baseline from the variable the ratio divided by. A sentence assembled from its own inputs cannot drift from them, and every hand-written sentence is a claim you have undertaken to re-check after every data change.

**How to repair without collateral.** Fix the sentence, then look for the same claim restated elsewhere, since a count word or a baseline that is wrong once is usually wrong in the summary too. Where the fix is to derive the prose, re-run and confirm the artifacts that carry no prose are unchanged, so the edit is provably confined to the words.

---

## H4. What ships is not the asset list that was declared

**The general form.** The delivery carries more than the declared set, or less, or something nobody opened. More: a second copy of an archive under a different name, an enclosing folder inside a zip, operating-system metadata entries. Less: content that is graded but exists in no file. Unopened: an artifact the script emitted successfully and no human ever looked at, the clipped chart title being the standing example, since the script exits zero and the file is there and the defect lives only in the rendering.

**What it costs.** A duplicate asset makes it ambiguous which copy the graded responses ran against, and that ambiguity is unresolvable after the fact. Worse, the copies are often **not identical**. Two packs shipped under different names can differ in container metadata on some members and in row content on others, at which point the delivery contains two different worlds and no record of which one was scored. Resolve it before deleting either: diff the members, and run the golden against both to establish that the committed answer is reachable identically from each. Only then is deleting one a tidy-up rather than a coin toss. A stray folder level breaks every path the prompt states. Metadata entries read as a bundle assembled by hand on a laptop. An unopened visual ships as a deliverable that looks unfinished, which costs on a rubric that grades presentation.

The severe one is **content that is graded but is not in a file.** Where a large share of the rubric's points can be earned only from a script's standard output, the deliverable does not contain what it is scored on. Any grader that reads the shipped files and does not execute the script scores zero on that share, and the golden cannot self-score. If the artifact must be produced by running something, the run has to be part of the declared delivery, with its dependencies named, or the content has to be written to a file that ships.

**Where the line falls.** The rule binds on what is inside the shipped set, so a second copy outside the delivery does not break it. That is not a licence to keep one: the task folder holds no snapshot zips, no `DESIGN_V2`, no `.bak`, because the generator rebuilds the pack and the design note's `## Tried and rejected` section holds the reason a dead end died. Keep a scratch copy while an edit is in flight if you need one, in the scratchpad, and delete it when the edit lands.

**The check.** Enumerate the archive members and compare them against the declared list, name for name. Assert no member sits under a common enclosing folder and none is an operating-system metadata entry. Open every visual artifact and actually look at it. Then take each block of rubric points and name the shipped file that carries it; a block whose only home is a transient output is the finding.

**How to repair without collateral.** After any edit to a generator, regenerate and assert that everything which should not have moved is **byte-identical**. Name those invariants before making the edit, not after, because chosen afterwards they will be chosen to pass. If an artifact that should have been untouched does move, the edit was wrong: revert and redo it rather than reconciling the difference, since a difference you talk yourself into is how a second defect enters under cover of the first.

---

## H5. The rubric grades one reading of an ask that licenses two

**The general form.** Two shapes, both on the grading surface rather than in the bundle. First, a **criterion the golden itself would fail**: a band so tight it excludes the golden's own second statement of the same quantity, or a value demanded that no shipped file states because the golden reaches it by adding two printed lines. Second, an **ask whose shipped wording admits more than one defensible reading**, graded as though it admitted one: a denominator the data dictionary licenses, a comparator whose term count is fixed by a file, a date convention the records show lagging.

**What it costs.** Discrimination, which is the only thing the rubric exists to provide. A solver who did the analysis correctly and took a licensed alternative scores as wrong, so the criterion stops measuring what it was written for and starts measuring which reading was guessed. This is observable rather than theoretical: where several runs of one task exist, an ambiguous ask shows up as several distinct filed answers with one matching the key, and that spread is the measurement.

A quieter version is **wording drift between the artifact and the criterion**. Where a criterion is matched on its phrasing, a label in the deliverable that describes the same quantity in different words can fail a criterion the value satisfies. Make the artifact's label and the criterion's wording the same phrase. This is H3's problem pointed at the grader instead of the reader.

**Where the line falls.** Not every disagreement is ambiguity. Where one reading is incoherent on its own terms, the golden's reading stays the reference value and the band exists to avoid punishing the coherent alternative rather than to bless a wrong one. Say which is the reference and why, in one clause, so the band is not read as the question having no answer.

**The check.** For each ask, name every reading the shipped wording admits and compute what each yields. If two survive the documents, either state the convention in the criterion or accept both. Then **band by the margin you own**: where the nearest wrong answer sits a known distance away and a defensible method choice moves the figure by less than that, band inside the margin and the discrimination is untouched. The margin is the thing that licenses the band, so it has to be measured first, which is H2.

Also count the criteria the way the generator counts them. A generated count is a **parse of your text**, so punctuation inside a criterion can split one criterion into two and move a number that gates the task. When a count looks wrong, check for the split before rewriting anything, and ship the merged reading rather than re-splitting to match.

**How to repair without collateral, and where the repair must not go.** The fix depends entirely on **whether responses have been graded yet**, and getting that condition wrong is how the repair does more damage than the defect.

*Before grading*, close the ambiguity in the **ask itself**. One clause naming the scope, the population or the denominator is the clean fix, it is cheaper than any rubric accommodation, and it removes the reading rather than tolerating it.

*After grading*, the prompt and the inputs are **frozen**. Every run was scored against the shipped wording and editing it invalidates them all, so from that point ambiguity is a rubric problem with a rubric fix, however much cleaner rewording the ask would have been. Fix it in the criterion, and record why the obvious repair was unavailable so nobody applies it later in good faith.

---

## H6. A rule stated in the golden that the record does not obey

**The general form.** The golden states the rule the whole build turns on, in one sentence, and the sentence is under-specified. It is right about the mechanism and silent about a qualifier: a start date, a regime the rule only applies within, a population it only covers, a precedence between two clauses. Applied forward to the question being asked it gives the right answer, which is why it survives every check. Applied **backwards to the record the pack already ships**, it mispredicts cases that are sitting there in the data.

**What it costs.** More than any figure defect, because the rule is the load-bearing sentence and everything else is downstream of it. A reviewer's first instinct on reading a stated rule is to test it against the shipped history, and mispredicted rows are the fastest possible way to conclude the rule is not the real one. That the answer happens to be unaffected does not help, because the reviewer discovers the mispredictions before they discover the exemption, and by then the rule's authority is gone. It also invites the worse repair, which is adjusting the answer to fit a rule that was only ever incompletely written down.

**Where the line falls.** A rule may legitimately be narrower than the record. A regime that begins on a date genuinely does not govern what came before it, and a population genuinely outside scope is not a counterexample. The defect is not the narrowness, it is **leaving the narrowing unstated**, so a reader applying the sentence as written gets contradictions the sentence never claimed to cover.

**The check.** Take every rule the golden states and run it **retrospectively over every observation in the bundle**, then count the mispredictions. Zero is the target. Where the count is not zero, the exceptions will cluster, and the shape of the cluster names the missing qualifier: all before a date means a start date, all in one class means a scope, all on one side of a tie means a missing precedence. Then confirm that the qualifier you add is itself evidenced in the pack rather than invented to fit, and say what brackets it.

**How to repair without collateral.** Add the qualifier to the rule wherever the rule is stated, which is usually three places, the critical components, the step-by-step and the shipped document that carries the same sentence. Then re-run the back-test to zero. State explicitly whether the answer moves; a qualifier that changes no result should say so, because a reader who sees the rule change will assume the answer changed with it.

---

## H7. A shipped archive that disagrees with the tree it was cut from

**The general form.** The bundle a reviewer opens is the zip, not the working directory, and the
zip is cut at one moment while the tree keeps moving. Any rebuild after the cut, including one run
only to confirm the build still passes, leaves the archive describing an earlier state. The two
stay the same size, carry the same file names and pass every check pointed at the directory, so
nothing the build already runs can see the divergence.

Underneath it sits a second mechanism that makes the divergence permanent rather than accidental:
**a generator is not reproducible if any library it calls writes nondeterministic metadata.** A PDF
writer emits a fresh random document `/ID` and a real-clock `/CreationDate` on every run, an image
writer stamps its own timestamp, an archive writer records mtimes. So two runs of the same
generator on the same seed produce byte-different files, and the archive is stale the moment the
generator is run again, forever, for a reason that has nothing to do with the analysis.

**What it costs.** Two things, and the second is the one that bites. A stale archive is simply the
wrong bundle, and if a repair was applied after the cut, the defect the repair fixed is still in
the shipped copy. Worse, a generator that cannot reproduce its own output byte for byte cannot
support the claim that the pack was produced forward from the parameters, because rerunning it
proves nothing: every file differs, so a real regression and a random identifier look identical.

**Where the line falls.** Content has to agree; metadata that the fiction never claimed to fix does
not have to. The test is whether rerunning the generator changes anything a reader could see or a
check could grade. An mtime inside the archive is not that. A document identifier is not either,
until it is the only thing standing between the build and a reproducibility claim, at which point
pinning it costs one substitution.

**The check.** Two assertions, both cheap, both belonging in the bundle verifier.

- **Compare the archive to the directory by content, never by timestamp.** Timestamps are actively
  misleading here, because `dataset-generation` §9 already requires the tree's mtimes to be
  normalised to an in-fiction export date, so the files are routinely dated years from the archive
  and the comparison a reader reaches for first is the one that cannot answer the question.
- **Run the generator twice and assert the two outputs are byte-identical.** This is the assertion
  that finds the nondeterministic writer, and it finds it immediately rather than after the archive
  has already been cut from one of the two states.

**How to repair without collateral.** Pin the nondeterministic field by equal-length substitution
after the file is written, with the constraints in H1: a PDF's xref is a table of byte offsets, so
the replacement must be the same length as what it replaces. Derive the pinned value from the
fiction rather than from the clock or a counter, so it is stable across rebuilds and still looks
like the real field. Then re-cut the archive **last**, after the final build and the final
verification, and let the freshness assertion rather than the build order be what guarantees it,
because the order is what slipped in the first place.

---

## H8. A citation that outlived the thing it cites

**The general form.** A golden, a write-up or a generator comment cites a clause, a section, a
file or a field by name, and the referent was later renamed, renumbered or moved during a
revision of the document that carries it. The sentence around the citation is still true, the
figure beside it still recomputes, and the citation now points at nothing: the governing
document has no such clause, the pack has no such file, the table has no such column. It
survives every check because figure sweeps read digits and determinism reviews recompute
values, and neither resolves a reference. The commonest route in is a draft convention that
moved before filing, so every artifact written against the draft carries the old address, and
the one that was updated is the document itself.

**What it costs.** A reviewer who greps the cited authority and finds nothing has caught the
build citing evidence that does not exist, which reads as fabrication rather than as drift,
and it lands next to the build's real citations and taxes them all. Where the dangling
reference is in a golden deliverable it is a Gate A finding in its own right: the chain the
golden states cannot be followed through the shipped files, however correct the arithmetic is.

**Where the line falls.** A citation into a document the fiction says exists but the pack
deliberately withholds is a design decision, not this defect, provided the design note records
the withholding. The defect is a referent that is supposed to resolve inside the bundle and
does not.

**The check.** Enumerate every reference in the goldens, the submission and the shipped
scripts, clause numbers against the documents that carry clauses, file names against the
archive listing, field names against the headers, and assert each one resolves. Clause
citations are greppable by their document prefix, so the sweep is one pass per authority. Run
it after any revision that renames or renumbers anything, because that is the only time the
class can enter.

**How to repair without collateral.** Fix the address everywhere it appears, not where it was
found: the same citation is usually stated in the deliverable, the write-up and a generator
comment, and repairing one creates the disagreement the standing rules ban. Grep the old
address to zero, then re-derive the artifacts that carry it rather than editing them in place,
so the shipped copy and the generator agree about what was fixed.

---

## H9. A file added late that the pack's own registers never learned about

**The general form.** The pack describes itself: a manifest declares each file's provenance and
coverage, a dictionary declares each extract's grain and fields. Both are hand-maintained lists
inside the generator, written when the pack's shape first settled. A file added in a later
version arrives through its own writer, far from those lists, and nothing connects the two: the
manifest still validates, the dictionary still reads complete, every existing check passes, and
the new file ships with no provenance and no field semantics. The files likeliest to enter late
are the ones a repair or a redesign just made load-bearing, so the class lands exactly on the
files a reviewer scrutinises hardest.

**What it costs.** A reviewer who finds the decisive mechanism resting on files the pack's own
registration layer does not acknowledge reads the omission as those files standing outside the
world, and that converts an oversight into a determinism finding: an unregistered file is one
whose authority and coverage the bundle nowhere states, so every convention it carries is
arguably unfiled. The registered files certify one another and the unregistered ones sit outside
that web, precisely where the difficulty lives.

**Where the line falls.** A registry need not describe itself, so a manifest with no row for the
manifest is the ordinary form. And a file outside the register's own stated scope is not a gap,
since a dictionary of extracts owes nothing about a policy memo. The defect is a file the
register's scope claims to cover and does not.

**The check.** Assert set equality, never spot membership: the manifest's file names equal the
shipped set minus the registers that exclude themselves, and every file the dictionary's scope
covers appears in it by name. Wire it twice, in the generator at write time and in the bundle
verifier, so a regeneration and a hand edit are both caught. Names must match literally, because
a heading that abbreviates a family of files defeats the sweep that exists to protect them.

**How to repair without collateral.** Add the registration in the register's own voice and at
its own level of detail: a manifest row states coverage, a dictionary entry states grain and
field semantics, and neither restates a rule another document files, because a repair that turns
a registration into a second statement of a load-bearing fact trades the omission for a
signpost. Then regenerate and diff, confirming the only bytes that moved are the registers and
the file being registered.

---

## H10. A rival-killer whose every miss the pack's own rules can excuse

**The general form.** A calibration corpus refuses rival bases by counting misclassifications,
and the assertion counts raw misses at the best bar. The pack separately files a discretion
rule about the settled record: a one-slot-per-period limit, a materiality floor, a deferral
clause, any sentence letting the authority decline a case without denying its measure. A
reviewer reading that rule charitably can excuse any miss that is a declined case over the bar
in a period where the discretion plausibly operated, so a rival whose only misses have that
shape reproduces the corpus after all, and where it disagrees with the golden basis on the open
question the build has a second defensible answer. The assertion passed because it counted
misses; the review failed the build because it counted refusals, and the two are the same count
only in a pack that files no discretion.

**What it costs.** Gate C, the expensive way: the review lands `competing_defensible_answer` on
a build whose corpus back-test is green, and the repair needs a data recut rather than a
wording fix, because the corpus genuinely does not refuse the rival. It is the floor-of-one
defect's worse sibling, because the miss count can be honest, asserted and reproduced, and
still prove nothing.

**Where the line falls.** The filed discretion is not the defect and usually cannot be removed,
since it is load-bearing fiction (the discretion is why the settled record is sparse). The
defect is asserting rival refusal by a count the discretion can excuse.

**The check.** Score every rival under the most charitable reading of every discretion the pack
files: classify each miss as excusable (the discretion could explain it) or inexcusable (a
positive case under the bar, or a declined case over the bar in a period where the discretion
had no occasion to operate), and assert min-inexcusable >= 1 over every bar, per rival, in the
generator and again in the bundle verifier. Enumerate the discretions from the pack's own
documents before scoring, because the reviewer will. Assert the refusing cases' rival-basis
values by name with margins, not only the sweep's counts, because an untargeted rival value
drifts silently across retunes.

**How to repair without collateral.** Plant refusal cases where the discretion structurally
cannot reach, periods where it never operated or misses on the positive side of the record, and
build them in the direction opposite the open question's mechanism, so the history refuses the
rivals without ever demonstrating the answer's shape. Keep the recut off every other
statistic's path and re-assert the whole corpus afterwards, because the cases every other rung
reads live in the same record the recut just moved.

---

## H11. A superseded write-up left readable in the task tree gets graded as the live one

**The general form.** A rebuild archives the failed version inside the task folder, directories
and all, so the tree now holds two or more files with the operative name of a graded artifact:
two write-ups called `submission.md`, two prompts, two private ladder files. Every consumer of
the build that takes an explicit path still works, but any consumer that discovers the artifact
**by name**, a review harness collecting inputs, a judge agent globbing the folder, a batch
uploader, can land on the superseded copy, which reads exactly as authoritative as the live one
because it once was. The likeliest moment is immediately after a repair, when the archive is
freshest, the names collide perfectly, and the superseded content describes the same world in
the same vocabulary, so nothing about it looks foreign.

**What it costs.** A full review cycle spent grading the live bundle against a dead solution.
The verdict comes back `solution_incorrect` with quoted figures the live write-up never states,
every classification downstream of the wrong golden is void, and the misgrade is
indistinguishable from a real Gate A catastrophe until someone diffs the quoted figures against
the live file. The nastier half is directional: the judge, finding the shipped deliverables
disagree with the dead write-up, concludes the **solution** is mispasted rather than its own
input, which reads as gross authoring negligence and taxes the build's credibility beyond the
one verdict.

**Where the line falls.** The record of what a superseded build cost is worth keeping, and it lives
in the design note's `## Tried and rejected` section; the build itself is not kept in the task
folder at all, because the generator rebuilds it. The harm this entry names is a superseded copy of
a graded artifact **readable under its operative name** anywhere below the task root, dot-prefixed
directories included, because name discovery does not honour dot-prefixes.

**The check.** Assert, in the bundle verifier, that exactly one file named `submission.md` and
one named `prompt.md` exist anywhere under the task tree, that no markdown lives outside the
task root and the shipped bundle directory, and that no superseded-build directory exists as a
directory at all.

**How to repair without collateral.** Move the record of what each superseded build cost into the
design note's `## Tried and rejected` section, one line per dead end, then delete the superseded
trees. Do not merely rename the stale copies, because the next rebuild recreates the collision, and
do not pack them into an archive in the task folder, because a snapshot there is banned and the
generator is the restore path. Then wire the uniqueness check
so the next rebuild cannot reintroduce the class silently, and if a review already ran against
the stale copy, say so in the resubmission rather than resubmitting quietly, because the
reviewer's quoted figures are the proof of what happened.

---

## H12. A prompt whose precision pins read as a grading sheet

**The general form.** The spec requires every figure's unit and rounding stated inside the
sentence that asks for it, and the cheapest way to satisfy that is to append the same
"in whole <unit>" or "to N decimals" tag to every clause of every ask. Applied uniformly
across a paragraph, the tags turn the requester's letter into an enumerated calculation
list: every ask carries identical specificity, the unit phrase repeats mechanically, and
the prose reads as written against the rubric it will generate. Nothing in the build's own
checks reads the prompt for voice, so the defect ships with every figure correctly pinned,
which is exactly why it survives to review.

**What it costs.** A realism send-back on the prompt itself, named as mechanical or
formulaic enumeration, independent of the analysis being right. It also leaks: a request
where every clause is tagged to its unit hands the solver a tidy checklist of every graded
figure, which is the roll-call defect in units instead of opinions, and it flattens the
asymmetry a real request carries (one thing named to the decimal, another mentioned in
passing).

**Where the line falls.** The pins are not the defect; they are Gate E load-bearing, and
deleting one on a genuinely forkable figure trades a realism finding for a determinism
finding, which is a worse trade. The defect is tagging figures whose type already fixes
their format. A count of discrete things (people, records, events) is a whole number by
nature and carries no rounding fork untagged; only derived quantities, a counterfactual, a
share, an average, a ratio, genuinely need stated rounding, and those statements read as
natural precision when they are the exceptions rather than the pattern.

**The check.** Classify every figure the prompt asks for as a natural integer (a count of
discrete things in the shipped data) or a derived quantity. Assert that every derived
quantity states its rounding inside its own sentence, and that no unit-tag phrase repeats
more than about twice across the prompt. Where a blanket convention sentence carries the
counts ("whole counts, decimals only where I ask"), assert it is present. Wire the phrase
count and the convention sentence into the bundle verifier so a prompt edit cannot
reintroduce the litany.

**How to repair without collateral.** State the convention once, in the requester's own
voice, and keep explicit rounding only on the derived figures, phrased with variety. For
every tag dropped, confirm the figure it covered is integer by construction in the shipped
data (a count over an integer-valued file), so no Gate E fork opens where the tag was; a
figure that is fractional upstream and whole only by rounding keeps its explicit statement.
Then re-enumerate the surviving pins against the full figure list and confirm every
non-integer quantity is still covered, because the failure mode of this repair is dropping
one pin too many.

## H13. A prompt whose committed call reads as one output among several

**The general form.** The spec allows up to three deliverables and puts about fifty-five to sixty per
cent of the score on the asks, so a compliant prompt carries one committed recommendation and a large
supporting layer, and the supporting layer is where nearly all the words go. Written straight down
the page it comes out as one paragraph per deliverable, each opening on a commissioning verb, each
about the same length, and the one call ends up structurally indistinguishable from the outputs
that exist to support it. Two habits do most of the damage. The context states the call somewhere
in the middle of its sentences instead of at the end, so the paragraph closes on housekeeping. And
the clause naming what the committing document leads with holds a comma series of several figures,
which reads as several recommendations rather than one with its supporting detail underneath.

**What it costs.** A first-pass rejection on the prompt alone, before the analysis is examined,
on the ground that the task asks for a collection of outputs rather than one deterministic
recommendation verifiable from the inputs. The finding is about shape rather than content, so
nothing the build already runs can see it: every figure recomputes, the golden leads with the call,
the deliverable count is inside the ceiling, and the prompt still reads as a specification for a
reporting pack. It costs on substance too, because a solver who cannot tell which figure the task
turns on spreads effort evenly across the asks instead of onto the one the ladder was built for.

**Where the line falls.** The supporting layer is not the defect and must not be cut. The asks
carry most of the score and the criteria come from their structure, so dropping a deliverable or
softening an ask into background prose to answer this finding takes the rubric under its floor,
which is a worse failure than the one being repaired. The defect is the **hierarchy**, not the
inventory. Every figure keeps its unit and its rounding, every named content requirement stays a
requirement, and the whole repair is grammar and paragraph order. The one exception is H18: where a
supporting ask answers a different decision rather than sitting in the wrong place, no reordering fixes it, and
retiring the ask is the repair.

**The check.** Three reads, none of which involves a figure. **They also run at authoring time**,
in `../guide-to-prompt/SKILL.md` under "The hierarchy read", because prompts are written under
`guide-to-prompt` while this register runs as the last pass before ship, and a defect whose only
check sits downstream of the work gets found by the client instead. `voice-check.py` prints the three
reads' inputs. The reads themselves: the context's last sentence before the
first deliverable is the committed call, stated bare. The clause saying what the committing
document leads with names exactly one quantity. Every paragraph after the first opens by tying back
to that quantity rather than on a bare commissioning verb. A prompt failing any of the three reads
as a list of outputs however well the call itself is worded.

**How to repair without collateral.** Move the call to the end of the context and demote the
figures that were sitting beside it into the sentence underneath, carrying their wording across
unchanged. Add one short bridging line saying the rest exists to stand that figure up, which is the
sentence a reviewer reads as the hierarchy. Then handle the housekeeping the move displaces: a
blanket rounding or counting convention that governed every ask has to stay above all of them, so
it belongs in the bridge rather than at the end of a context that now ends on the call. Re-read
every clause the edit touched against the pins the build depends on, because this repair moves
sentences carrying stated grain, ordering and precision, and losing one of those trades a shape
finding for a determinism finding. Check the golden's correspondence rather than regenerating it,
since a committing document that already leads with its call usually satisfies the repaired prompt
as it stands.

## H14. An estimation domain the golden picked silently, that the data then argues against

**The general form.** Every rate the golden takes is measured at some grain: by segment, by
period, by cohort, by class, by whatever the pack's structure offers. The golden picks one grain,
usually the coarsest defensible one, and the write-up never names the choice because it does not
feel like a choice. Unit gets pinned because the spec names units, rounding gets pinned because
the spec names rounding, and a named category gets pinned once a review has taught the build to
pin categories. **The grain does not get pinned, because nothing names it.** So a solver who cuts
one level finer is not doing anything the pack forbids, and if the finer cells then say something
different from the coarser ones, the build has two answers and no filed sentence choosing between
them.

The generator half is where the finer cells acquire their voice, and it is quiet. A response,
outcome or selection process that fills a quota by taking a **prefix of a list** makes the list's
sort key perfectly predictive of the outcome. Where the list is laid down blocked by an attribute
and the quota is smaller than the first block, every member of every later block gets the same
outcome, every time, in every period. The aggregate rates the build asserts are all correct, so
nothing fails, and the pack ships a subgroup with a degenerate outcome that no design intended.
The damage is worst where the attribute is **rare in the history and common in the forward
window**, because then the false signal is applied to a large share of the thing being forecast
and the two answers separate by tens of per cent rather than by rounding.

**What it costs.** Gate C, `competing_defensible_answer`, on a build whose every figure
recomputes and whose stump is intact. It is the expensive kind of failure twice over. The
repair is a data recut rather than a wording change, because the pack genuinely argues for the
rival. And it fails **against the strongest solver specifically**: a weak response never reaches
the finer cut, so the defect is invisible against weaker responses and surfaces only once a model
is good enough to find the decisive rung, which is the response the build was built to survive.

There is a second cost that the repair does not remove and that is easy to miss while celebrating
the fix. A solver reaching the rival answer for this reason had already climbed the whole ladder,
so the difficulty that produced the wrong answer was never the designed one. Closing the fork
converts confidently wrong responses into probably correct ones, and stump power has to be
**re-measured** afterwards rather than carried over.

**Where the line falls.** Finer is not automatically better and the repair is not "always pin the
coarsest grain". Some grains are load-bearing and must stay open: where an attribute genuinely
drives an outcome and the forward window's mix of that attribute has moved, cutting by it is the
correction the build is built on. The test is which quantity the attribute governs. An attribute
may legitimately drive one stage of the process and nothing after it, and then the pin says so at
that boundary rather than banning the attribute outright. A pin that closes the fork and closes
the intended correction with it has traded a determinism finding for a wrong answer.

**The check.** Two, and they are independent.

Enumerate, for **every rate the golden takes**, the grains the shipped data would let a solver cut
it at, and for each grain compute the release, ranking or figure that grain produces. Any grain
returning a different committed answer is an open fork and needs either a filed sentence or a
data fix. Wire the finer-grain estimator into the verifier as a live assertion that it returns the
committed answer, so a later retune cannot silently reopen the fork.

Separately, assert that **no subgroup of any attribute has a degenerate outcome rate**: no
category with zero occurrences of the outcome across the whole record where the aggregate rate
predicts many, and none at a rate the pooled figure could not produce. Zero over a few dozen cases
is noise; zero over thousands is a generator artifact, and the assertion should be written on the
count of cases at risk rather than on the number of subgroups.

**How to repair without collateral.** Fix the data first and pin second, because a pin over a
record that contradicts it is worse than no pin.

*The data half.* Repair it as a **relabelling inside the affected pool**, not a re-simulation.
Permute the attribute's labels among the rows that already sit in one outcome group, preserving
each label's count in that group, and every aggregate the build asserts is arithmetically
untouched: the group's totals, the rates measured at the coarse grain, the downstream population
counts, the capacity or budget arithmetic. Re-simulating instead moves every row and every figure
downstream of it, which turns a one-column fix into a rebuild of the whole answer key. Spread the
labels across the outcome cells **proportionally with a carry**, so the cumulative deviation
stays under one case per label per cell within whatever grouping the rival estimator will pool
over, and key the carry to that grouping rather than to the generation order, since keying it
wrongly leaves the pooled figures right and the individual cells noisy, which is the half the
rival actually reads.

*Where the pin goes.* In the shipped document a solver has to open anyway to get a figure the
naive path needs, not in a section they can skip. State it positively, as the domain the model is
specified at, and **do not name the attribute you are protecting against**, because naming it
advertises the correction it drives elsewhere. Then scope the sentence explicitly to the quantity
it governs and say what it does not cover, or it will be read as closing the intended correction
too. Check the scoping clause against the asks: a sentence saying a quantity "is not estimated"
can read as forbidding a projection the deliverable is required to make, where "carries no
estimation domain of its own" says the same thing about grain without denying the forecast.

*Proving the repair was surgical.* Name the invariants before editing, then regenerate against the
pre-repair bundle and assert them: which files are byte-identical, which single column moved, and
that the coarse-grain rates and every downstream population count agree to full precision. State
what was **not** byte-compared and what was checked instead, because a repair applied before the
comparison snapshot was taken cannot claim byte equality for the artifacts written after it, and a
claim of that shape is the thing a reviewer tests first.

## H15. A referee that only arbitrates downstream of a hazard

**The general form.** An ask is made determinate by two routes rather than one: a rule filed at
authority says which of two candidate inputs governs, and a corroborating file independently
confirms it, because the governing input reconciles to the corroborator and the other does not.
That is the right structure. It breaks when the corroboration is only true on a **population the
reader reaches by first defeating a planted device**: an archived block that has to be excluded, a
duplicate delivery that has to be deduped, a scope rule that has to be applied. Computed on the
data as delivered, the corroborator agrees with neither candidate, and often ranks them the wrong
way round.

So the second route is not independent, it is **conditional on the first hazard already being
solved**, and for every reader who has not solved it the referee argues against the answer. The
build's own checks cannot see this, because they compute the corroboration on the population the
golden ends up with, which is the one population where it works.

**What it costs.** Worse than having no referee. A reader who checks a stated basis and finds it
false has not learned that one sentence is loose, they have learned the answer's justification is
wrong, and they will say so in those words. The finding lands as `competing_defensible_answer` on
an ask whose answer is actually forced, and the review's arithmetic looks authoritative because it
was performed on the file as shipped. The build then spends a review cycle defending a pin that
was correct all along, which is the most expensive way to be right.

There is a compounding failure that makes the class hard to spot from inside. The rule that governs
is usually filed in **one register cell**, correctly and once, while the file a reader consults for
that quantity's semantics says something adjacent and routes nowhere. A reviewer enumerates the
obvious authorities, does not reach the register, and concludes nothing pins it. The pin existing
is not the same as the pin being reachable from where the question is asked.

**Where the line falls.** The hazard is not the defect and must not be removed to make the referee
work unconditionally, because the hazard is usually a scored device in its own right. Nor should
the ambiguity be closed by flattening the candidates, marking one input withdrawn or deleting it,
since that turns a rule-application into a lookup and retires the device the ask was built on. What
has to change is only what the pack **declares**: the dependency between the referee and the
hazard, stated where a reader meets it.

**The check.** Compute every corroboration the design claims **on the population a reader would use
before solving each hazard**, not only on the population the golden ends up with, and assert both
results: that the referee arbitrates correctly on the intended population, and what it does on the
naive one. If the naive result reverses the ranking, the pack must say so somewhere a reader
reaches first. Assert separately that every governing rule is reachable from the file whose
semantics raise the question, by a route the assertion can name, and that the rule is still stated
exactly once so the routing has not become a second statement.

**How to repair without collateral.** Declare the dependency, do not engineer around it. The
register that describes the corroborated file states that it carries the hazard's population too,
in the same voice and at the same level of detail as any sibling row that already declares the same
fact about a different file, so the addition reads as the existing convention applied rather than
as a new signpost. Then make the governing rule reachable: the semantic register **routes** to the
authority that files the rule rather than restating it, which keeps the single-statement invariant
and still answers the reader where the question arises. Then repair the stated basis in the golden
and the write-up so it is true **as written**, with the qualifier that makes it true, and name the
rival reading and what it evaluates to rather than leaving a reviewer to find it. A basis sentence
that is true only under an unstated condition is the thing that converts a correct answer into a
finding, and it is the cheapest of the three fixes to make and the easiest to skip.

## H16. A pack whose internal dates run ahead of the documents that cite them

**The general form.** The registers say when each extract was taken and the deliverables say when
they were prepared, and nothing compares the two. Meanwhile the record's own dates are usually
**generated as an offset** from something else, a period start, a prior event, a re-delivery lag,
so their maximum is a consequence of arithmetic nobody looked at. The offsets run past the extract
date the manifest claims, and past the date the memo carries, and the write-up ends up citing a
delivery that had not happened when it was written. Nothing fails, because every figure is correct
and the dates are labels rather than values.

This is H1's contradiction between a timestamp and the setting, moved **inside the fiction**. H1 is
about the build clock leaking into a container. This is the file's own clock running ahead of the
document that reads it, and the two need separate checks because they live on different surfaces
and neither sweep sees the other's.

**What it costs.** A concrete inconsistency a reviewer can point at, in the fiction's own terms and
without any domain knowledge. It is worse where the offending column is **load bearing**, because a
rule of the form "take each item on its latest submission" reads exactly those dates, so the
reviewer is looking at them anyway while checking a graded figure, and finds the file arguing that
it was extracted before some of its own rows existed.

**Where the line falls.** Forward dates are not the defect where the record is forward looking by
design: a planned field calendar, a validity window running years out, a scheduled payment. Those
belong in an explicit allow-list, named file by file, because an allow-list written as a pattern
will quietly absorb the next real one.

**The check.** Sweep every ISO date in every shipped extract against the bundle's stated export
date and assert that the set of files carrying later dates equals the allow-list exactly. Then, per
file, assert the maximum of any column the registers describe as produced by an extract is on or
before that extract's own stated date, reading the date out of the register rather than restating
it. Both belong in the verifier, because the offending values are generated and will move again on
the next retune.

**How to repair without collateral.** Shift the generating offset **uniformly**, never clamp the
dates that overflow. Clamping compresses the tail into ties, and where any rule selects by latest,
a tie changes which row wins and moves a graded figure. A uniform shift with the same random draws
preserves the order exactly, so the selection is untouched and the repair provably moves labels
only. Confirm that afterwards by recomputing every figure the column feeds, and check the other end
of the range too, because a shift large enough to fix the maximum can push the minimum behind the
event the record is about.

## H17. A batch of prompts that are individually fine and collectively one prompt

**The general form.** Every prompt-writing rule in this repo is written about one prompt, every
check is run on one build, and every build passes. The defect only exists at the batch grain: the
same opening move, the same clause order, the same commissioning verbs and the same file set,
repeated across a run of builds until the reviewer reading them in one sitting sees a template
rather than a set of requests. It is invisible to the build's own checks by construction, because
no check in a build can see the build before it. It is also invisible pair by pair, so a clone
check that adjudicates one pair at a time can clear every pair and still be looking at a
monoculture.

The accelerant is that the skeleton is usually **prescribed** somewhere. A worked example in a
skill, a checklist item written as "context, first person, two or three sentences", and a
reference library whose examples are read four at a time, all pull the same way, so every author
follows the guidance honestly and the batch converges anyway.

**What it costs.** A client note on the shipped batch, which is worse than a per-build send-back
in two ways. It arrives after the whole run has shipped, so the repair is retrospective across
many builds rather than local to one, and it is a judgement about the operation rather than about
a task, which is the kind of finding that changes how the next batch is read before it is opened.

**Where the line falls.** Not every repetition is this defect. The **contract** is supposed to
repeat: first person, one committed call, one to three files, unit and rounding inside the
sentence, the asks multi-dimensional. Repetition of the contract is compliance. What must not
repeat is the **carrier**: which move opens, where the role sits, which file is commissioned
first, the verbs, the length, the format mix. An author who fixes this by dropping a rounding spec
or by writing an opening that misrepresents the decision has traded a batch finding for a gate
finding, which is the worse trade.

**The check.** `python3 .claude/skills/guide-to-prompt/references/voice-check.py` bare over the
window, as part of this pre-ship pass rather than only per build, because per build is the grain
that cannot see it. The batch is clean when it shows four or more distinct opening moves across
twelve builds, no carrier phrase in more than a third of them, and a format mix more than one row
deep. Read the counts, not the impression: eighteen consecutive builds passed a self-reported
checklist asking whether the context was first person and short, and every answer was truthful.

**How to repair without collateral.** Repair forward, not backward. Rewriting shipped prompts to
break a pattern re-opens every figure they pin and every golden that answers them, for a defect
that is about the next batch. What actually has to change is the **prescription**: find the worked
example, the checklist line and the reference block that taught the skeleton, and rewrite those,
because an author working from a template will reproduce it however the register is worded. Then
carry the axis into the per-build checklist so the next build chooses its move rather than
inheriting it. `.claude/skills/guide-to-prompt/references/prompt-voice.md` carries the moves, the
requirement-against-carrier table and the structural axes; `clone-check` Track A adjudicates a
finding once the script has measured it.

## H18. A supporting ask that passes the hierarchy reads and is still a second decision

**The general form.** The ask layer is built for difficulty, and the cheapest difficulty is a device
the main call never touches, so an ask designed outward from a device tends to land on a quantity
somebody in the organisation genuinely wants, only not for this decision: next cycle's plan, a
compliance exposure, a second operational call that happens to share the files. Each one is
realistic on its own and each is introduced as riding under the committed figure, so the prompt
passes every hierarchy read in H13 while asking for several independent answers underneath the one
it names. The tie-back is grammatical rather than substantive, because nothing about the ask's
answer is part of the committed figure, qualifies it or audits it.

**What it costs.** A first-pass rejection on the prompt alone, named as a request for multiple
independent deterministic outputs rather than one recommendation, with the prompt as the repair
location. It is harder to answer than H13 because grammar cannot fix it: reordering the sentences
leaves every independent ask in place, and the resubmission fails the same check. The repair also
costs rubric weight, since the retired asks were carrying criteria, and usually the device weight
that was meant to hold a strong solver under the bar.

**Where the line falls.** Independence of difficulty is legitimate and is what the device pool
exists for. Independence of decision is the defect. An ask may be hard for reasons the main ladder
never touches and may cross devices the main call never reads, as long as its answer is a component
of the committed call, a direct qualifier of it (its sensitivity, its flip condition, its
reconciliation to another total), or the trail that audits it. It fails when a person could act on
its answer with the committed call still unmade: a figure for another period, another population's
exposure, a yes-or-no call about a different action. The test runs on the answer, never on the
sentence that introduces it.

**The check.** Give every ask one line in the ask ledger naming how its answer enters the committed
call: as a component, as a qualifier, or as the audit trail. An ask whose line has to name a
different decision, a different window or a different owner is independent, whatever the prompt
says about it riding under the figure. Read that ledger column, not the prompt, before the prompt is
called done, because the prompt's own wording is exactly what hides this defect.

**How to repair without collateral.** Retire the independent asks rather than rewording them, and
win their criteria back inside the decision without coupling them to the main call: carry a second
measure on every candidate that the call does not turn on, grade the trail that audits an input the
call consumes at its natural grain, or reconcile a candidate figure to another system's total, each
on rows outside the main call's population (`supplemental-stumping` Part 2). That is the
denser-structure route of the shape picker, and it keeps the rubric over its floor without bolting
anything on. Splitting the committed figure at the grain its owners book it also passes this entry,
but the split inherits the main trap, so the response that lands the call banks it; use it only when
the author asks for an inheriting ask. Either way, re-derive the pair ceiling and both sheets of the
pair simulation (`supplemental-stumping`), and say plainly in the design note what the pass
condition rests on. Leave the retired asks' devices in the pack as inert context rather than cutting them, which would touch the evidence for no gate benefit, and regenerate the
golden, the verifier's ask checks and the write-up's answer block together, since all three
enumerate the asks and any one left behind is H2 or H3 waiting to happen.

## H19. A sibling build's archive attached under this build's name

**The general form.** Every build names its archives the same way, one target archive and one golden
archive, and a batch is uploaded in one sitting from folders that look alike. So the platform can
receive a sibling's archive under this build's submission, and nothing in the build can see it
happen, because every check the build runs reads the archive on disk, and that archive is correct.
The review then judges the prompt against evidence from a different fiction entirely.

**What it costs.** A full determinism failure, every gate from correctness through uniqueness, on a
build that was never examined. The finding names missing input data with the input files as the
repair location, and an author who takes it at face value starts rebuilding evidence that already
exists. It spends the portal run too: the model correctly reports that nothing can be computed, so
the run carries no stump evidence either way, and the build loses a review cycle to a clerical
slip.

**Where the line falls.** A review saying the decisive files are absent is not always a mixup.
Before treating it as one, confirm that the files the review describes are not this build's and
exist in a sibling folder, and that this build's archive on disk holds every input the write-up
names. If this build's own archive is missing a named input, that is H4 and the repair is in the
bundle.

**The check.** When the bundle is declared ready, record each archive's byte size, member count and
digest, and compare them with the file actually attached before submitting, since an upload form
shows a size even when it shows nothing else. In the bundle verifier, assert that every input file
the write-up names is a member of the target archive and that the golden archive holds exactly the
deliverables the prompt names, and print the receipt so the comparison takes one glance.

**How to repair without collateral.** Re-attach the verified archive and change nothing in the task
in answer to the review, because the review never saw the task, and a repair aimed at it moves the
build away from a bundle that was correct. Say in the resubmission that the wrong archive was
attached, quote the review's own description of the files it saw as the evidence, and give the
correct archive's size and digest. Where the upload form accepts any name, attach the archive under
a name that carries the build's number, which removes the mixup at its source. Then have the author
re-test the build on the portal, since a mixed-up review leaves the build with no evidence on
either stumping or determinism.

## H20. A build whose domain fit is established everywhere except the prompt

**The general form.** The domain is settled early, the subdomain is enumerated in the design note,
and the evidence pack is then built to carry it: the registers name the governing authority, a
boundary layer names the entity's institutional type, a published series names the programme. All
of that is true and none of it is in the prompt, because the prompt is written last and written to
avoid leaks, so the sentences that would have carried the institutional character read as furniture
and get cut. What ships is a request whose surface is the work (a volume series, a service level, a
handling rate) with the character of the decider left implicit. The decision's sector is then
recoverable from the bundle and from the notes, and not from the thing a domain reviewer reads.

**What it costs.** A rejection on the tag, which is the cheapest rejection to earn and the most
expensive to answer, because a task tagged outside the accepted roster is refused on the tag alone
and the analysis is never opened. The finding also arrives in a form that invites the wrong repair:
it reads as a claim that the subject matter does not qualify, so an author who takes it at face
value redraws the domain or the scenario, when the tag was correct and only its evidence was
misplaced. The register the reviewer reached for is usually their own rather than this repo's, so
expect an out-of-scope category that the written standard does not contain, and check the standard
before conceding anything.

**Where the line falls.** The repair is not to explain the domain in the prompt, and a sentence
whose job is to reassure a classifier is furniture a real requester would not write. Nor may the
signal be bought with anything the ban list covers: the governing standard by acronym, the
eligibility rule, the deciding metric, the rate or fee basis, the population. What is licensed is
the **institutional furniture the requester would state anyway**, because a person writing to a
colleague names who decides and what the decision releases. Naming the deciding body's character
and the nature of what it hands over is the requester's own voice; naming how the amount is
computed is a leak, and the two sit one clause apart.

**The check.** Read the prompt cold, with the bundle, the design note and the tags withheld, and
name the domain off it alone. The tagged domain has to be the one it lands on, and a reading that
could as easily land on an out-of-scope sector is the finding. Behind that read, one mechanical
assertion, and it is per build rather than derivable: name the institutional nouns the enumerated
subdomain turns on, as literal strings from this build's own fiction, and assert each appears in the
prompt. Wire it into whichever verifier already reads the repo tree, so a later prompt edit made for
voice reasons cannot quietly drop the last one. Pair it with a leak assertion over the same file and
keep that list to phrases the ban list actually covers, the deciding metric, the eligibility rule or
threshold, the rate basis, the population, the decisive rung, with a comment saying which is which.
A guessed phrase asserted as a gate fires on a licensed rewording and tells the next author nothing
about whether they broke something.

**How to repair without collateral.** Repair inside the sentences that are already there, because
adding a sentence is what produces the explanatory paragraph the prose spec exists to prevent.
Three edits usually carry it: qualify the deciding body where it is first named, say what the
decision releases and who releases it where the committed call already states the unit, and give
the requester's own organisation its institutional adjective where the role sits. Take the nouns
from the shipped bundle rather than inventing them, so the prompt agrees with a golden that already
carries the authority in its own letterhead and with the registers that name it. Then confirm the
edit moved nothing else: re-render the write-up from the prompt rather than editing its quoted copy,
re-run the pack and submission verifiers, and re-run the voice check, since a domain-signal edit
lands in the opening clause, which is the one place the batch surface is measured.

## H21. An invented name that sits a few letters from a real organisation, school or place

**The general form.** A build invents its organisations, sites, schools and venues, checks them
against the real register for an exact match, finds none, and ships names that are one or two
letters away from real ones, or that contain a real one's distinctive word. Saints' names, townland
and parish names, farm and venue words and staffing-firm brands are where this happens most,
because the generator reaches for the words that make a name sound local and those are exactly the
words real organisations already use.

**What it costs.** A reviewer who knows the region reads the invented school or shelter as the real
one, so the pack appears to publish a deprivation score, a migrant shelter or a funding decision
about an organisation that never took part, which is a realism finding at best and a reason to
reject the build outright at worst. A reviewer who does not know the region sees nothing, which is
why the defect survives every read-through.

**Where the line falls.** A generic place word shared with the real map (a river, a bay, a county)
is texture and stays. The line is the distinctive part of the name: after the generic words are
stripped, the invented remainder must not match, contain or sit within two edits of a real
organisation's remainder in the same country.

**The check.** Normalise every invented name and every name in the real reference registers the
pack already uses (lower case, accents folded, punctuation inside abbreviations deleted, generic
organisation and school-type words stripped as stop words), then fail on an edit distance of two or
less, or on containment of a real remainder. Wire it into the verifier so it runs on every build,
and add a second check that no retired name survives in the pack, the prompt or the write-up after
a rename.

**How to repair without collateral.** Rename from the generator, never by find-and-replace in the
shipped files, then rebuild and confirm every figure is unchanged apart from the names, because a
name is a key in more places than the eye finds. Prefer descriptive or place-style inventions over
saints and surnames, and run the check over every invented name in the build, not only the ones
someone noticed, because the first hit is usually one of many.

## H22. Constructed records inside a file the pack presents as a real download

**The general form.** The pack ships a real public file (a register, a grants extract, a registry
listing) and the generator adds the build's fictional organisations to it in the downloaded layout,
so the joins the ladder needs work. The provenance record then describes the file as downloaded and
used as published, which is no longer true.

**What it costs.** Fabricated rows presented as real public data, which the input gates treat as a
send-back cause on their own, however carefully the write-up declares the constructed layer
elsewhere. A reviewer who diffs the file against the public source finds rows that the source never
held under a provenance line saying it does.

**Where the line falls.** A constructed operating layer is legitimate and is the normal way these
packs carry their fiction. What is not legitimate is the silent mixture. Either the real file ships
exactly as downloaded and the constructed records live in their own declared files, or the
provenance record says plainly, file by file, that records for organisations in the case that are
not on the public register have been added in the downloaded layout.

**The check.** For every file the provenance record calls a download, compare its row count and
keys against the raw download the generator kept, and fail when they differ unless the provenance
line for that file declares the additions.

**How to repair without collateral.** The declaration must not single out the organisations that
carry the decisive rung, or it hands the solver the stump. So either move every constructed record
into separately declared files, or add constructed records for more fictional organisations than the
ladder needs, so that "constructed" does not mean "the ones that matter", and then re-check any
camouflage the build relies on with the new records in the distribution.

## Adding an entry

A house fix earns an entry when it is a **class**, not when it is an incident. The test is whether a future build could produce the same defect with entirely different nouns. If it could, write it up. If the defect was specific to one build's data, it belongs in that build's notes and not here.

Write each entry to this shape, in this order, because the order is what makes the register usable at speed:

1. **The general form.** State the mechanism with the incident's nouns removed. Name the class of tool or the class of claim, never the file that happened to carry it.
2. **What it costs.** What a reviewer sees and what they conclude from it. Separate the effects when one is worse than the other, because that is what tells a reader which half to fix first under time pressure.
3. **Where the line falls**, if the defect has a legitimate twin. Most of these rules have one, and an entry that does not say where the rule stops gets applied too widely and starts damaging things that were correct.
4. **The check.** The assertion, stated so it can be wired into the verifier rather than performed by eye.
5. **How to repair without collateral.** The failure modes of the repair itself, which is usually the part the incident actually taught, and where the repair has to live so it survives a rebuild.
6. **Tooling**, only where a tool exists. Say what it refuses to decide for you, since a repair tool that guesses at the fiction is worse than no tool.

Items 3 and 6 are conditional and the rest are not. Everything about repairing belongs under 5 rather than beside it, because an entry whose repair advice has spread into four peer sections has stopped being scannable, which is the one thing a register has to be.

Keep the incident out of the entry. Dates, file names and the specific numbers involved are what stop a register from generalising, because the next reader matches on the noun, does not see their own case in it, and skips the entry that would have saved them.

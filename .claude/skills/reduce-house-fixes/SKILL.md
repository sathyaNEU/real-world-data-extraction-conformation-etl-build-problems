---
name: reduce-house-fixes
description: The register of defects the author has had to fix by hand after a build was already called finished. Each entry carries the general form of the defect rather than the incident, what it costs when a reviewer finds it, and the check that would have caught it before the bundle shipped. Use as the last pass before a bundle is declared ready, when a house fix comes back from submission and has to be recorded, and alongside the stumping pre-ship checklist, which routes here.
---

# House Fixes

A house fix is a defect caught after the build was called finished: cheap to prevent, invisible to the
build's checks. They sit in the artifact being *what it claims to be*, not in the analysis.

- **When.** Last block of the build stage, before the leak and duplicate checks, beside `golden-realism`
  (this register owns the container, H1, and the write-up prose, H2 and H3).
- **Wire every check into a verifier** (`verify_pack.py`, the submission verifier); eye checks lapse.
- **Reading is delivery, writing is bookkeeping.** New entries only after hand-over, for surfaced defects.
- **When the check and the defect share a blind spot** (a tolerant reader, a regex missing a unit class),
  the check certifies the defect.

Entries: **Defect**, **Cost**, **Line** (where the rule stops), **Check**, **Repair**.

---

## H1. A generated binary carries its writer's name and the build clock
- **Defect.** Writers stamp their name (`dc:creator`, `<Application>`, `/Producer`, PNG chunks) and a
  real-clock timestamp into metadata, unseen by text checks.
- **Cost.** The signature says generated; the timestamp contradicts the setting, both ways (`python-docx`
  stamps 2013). Assert a band, not a ceiling.
- **Line.** Signatures: scrub inputs; a script-made golden may keep its own. Timestamps: scrub every shipped
  file whose body states a date, goldens included. Scrubbing both everywhere is the cheap way out.
- **Check.** Sweep the pack and the deliverables (two generators): no writer name, no stamp outside the
  band. Wire OOXML, PDF and image branches even before a file of that kind ships.
- **Repair.** Byte-level, never a re-save (it re-stamps). OOXML: repack same entries in order, change only
  `docProps/`, assert every other CRC unchanged. PDF: equal byte length (xref offsets), surplus as
  whitespace between tokens, never padding inside the value; substitute after the `%` of a comment line,
  never the marker. Verify with zero logged parser errors (`pypdf` degrades silently). Scrub after each
  save in the generator; prove it by regenerating into scratch and matching the shipped file.
- **Tooling.** `scripts/scrub_producer_metadata.py <dir>` audits; `--apply --producer "<fiction org>"
  --stamp <fiction date>` repairs (restores on failure). Without `--floor`/`--ceiling` from the fiction it
  reports stamps unjudged. A retrofit, not the generator scrub.

## H2. A figure in the write-up whose derivation is not on disk
- **Defect.** A supporting figure (enumeration count, margin) came from a scratch search script over unbuilt
  configurations, not the verifier; nothing on disk reproduces it.
- **Cost.** One failed reproduction taxes the whole write-up.
- **Line.** Derived figures must recompute. Parameters (a band edge, a schedule) are choices and must only
  be consistent with the file that states them.
- **Check.** List numeric claims in every document **and the design note** by unit class (integer, %,
  ratio, count, decimal) and name what sweeps each. Read enumeration claims by hand ("which script prints
  this?"); re-derive a grid's axis list from the bundle (six binary moves are 64 cells). State the thinnest
  margin and name the wrong cell, its reading and value.
- **Repair.** Measure (it usually strengthens the claim). If it cannot be re-derived, restate to a weaker
  supportable claim, never reconstruct. Grep the figure, not the sentence, and fix every copy.

## H3. The prose around a computed figure is the part nothing checks
- **Defect.** Verified digits, drifting words: count word, comparator, population, keying parameter (a
  file date restated by memory, worst bounding a window), unit, label, rounding path, distance to a rival,
  stated reason, a bound (an extremum, printed floor for "at least", ceil for "at most"), a statistic's
  referent, the pack's own rounding rule, a "twin" claim.
- **Line.** Two roundings of one quantity are fine when the document says which is which.
- **Check.** Ask of each figure sentence: how many, against what, of whom, in what unit. Better, emit the
  words from the objects that made the number (`len`, the divisor variable, the source file named).
- **Repair.** Fix every restatement; when deriving prose, confirm prose-free artifacts are byte-identical.

## H4. What ships is not the asset list that was declared
- **Defect.** More (a second archive copy, an enclosing folder, OS entries), less (graded content only in
  stdout), or unopened (a visual nobody looked at).
- **Cost.** Copies often differ (diff them and run the golden on both before deleting one); stdout-only
  content scores zero for a grader that does not execute.
- **Check.** Archive members equal the declared list by name; no enclosing folder, no OS entries; open every
  visual; name the shipped file carrying each block of rubric points.
- **Repair.** Name the byte-identical invariants before editing a generator and assert them after; if
  something that should not move moves, revert and redo.

## H5. The rubric grades one reading of an ask that licenses two
- **Defect.** A criterion the golden fails (a band excluding its own restatement, a value no file states),
  an ask licensing two readings (denominator, term count, date convention), or label/criterion wording drift.
- **Cost.** Discrimination: correct work on a licensed alternative scores wrong. Visible as several distinct
  filed answers across runs.
- **Line.** An incoherent reading is not a licensed one; say in one clause why the golden is the reference.
- **Check.** Per ask, list every reading and its value; pin or accept both. Band within the measured
  margin to the nearest wrong answer. Punctuation can split one criterion in two when counted.
- **Repair.** Before grading, close the reading with one clause in the ask. After grading the prompt and
  inputs are frozen: fix in the criterion and record why.

## H6. A rule stated in the golden that the record does not obey
- **Defect.** The load-bearing rule omits a qualifier (start date, regime, population, precedence); it
  answers forward correctly and mispredicts rows already in the pack.
- **Cost.** Reviewers back-test the rule first; mispredictions kill its authority.
- **Line.** A narrow rule is fine; an unstated narrowing is the defect.
- **Check.** Run every stated rule over every observation; target zero mispredictions. The exceptions'
  cluster names the missing qualifier; confirm it is evidenced in the pack.
- **Repair.** Add the qualifier everywhere the rule is stated (components, steps, shipped document), re-run
  to zero, say whether the answer moved.

## H7. A shipped archive that disagrees with the tree it was cut from
- **Defect.** Any rebuild after the cut leaves the zip stale. A nondeterministic writer (PDF `/ID` and
  `/CreationDate`, image stamps, archive mtimes) makes every rebuild byte-different, so staleness is
  permanent and regressions are invisible.
- **Line.** Content must agree; metadata the fiction never fixed need not, until reproducibility rests on it.
- **Check.** Compare archive to tree by content, never mtime (`dataset-generation` §9 normalises mtimes).
  Run the generator twice and assert byte-identical output.
- **Repair.** Pin nondeterministic fields by equal-length substitution from a fiction-derived value. Cut the
  archive last and let a freshness assertion, not build order, guarantee it.

## H8. A citation that outlived the thing it cites
- **Defect.** A clause, file or field cited by name was renamed or renumbered; the citation points at
  nothing.
- **Cost.** Reads as fabrication; in a golden, a Gate A finding.
- **Line.** A citation to a deliberately withheld document recorded in the design note is design.
- **Check.** Resolve every reference in goldens, submission and shipped scripts: clauses against documents,
  file names against the archive, fields against headers. Run after any rename.
- **Repair.** Grep the old address to zero and re-derive the artifacts rather than editing them in place.

## H9. A file added late that the pack's own registers never learned about
- **Defect.** The manifest and dictionary are hand lists; a late file (often the newly load-bearing one)
  ships unregistered.
- **Cost.** Its conventions are unfiled: a determinism finding where the difficulty lives.
- **Line.** A register need not list itself; files outside its stated scope are not gaps.
- **Check.** Set equality, never spot membership: manifest names equal the shipped set minus
  self-excluding registers; the dictionary names every file in its scope literally. Wire in the generator
  and the verifier.
- **Repair.** Register in the register's own voice and detail, never restating a filed rule (that is a
  signpost); regenerate and diff so only the registers and the file moved.

## H10. A rival-killer whose every miss the pack's own rules can excuse
- **Defect.** A calibration corpus refutes rivals by raw miss count, but the pack files a discretion rule
  (one slot per period, a materiality floor, a deferral) that charitably excuses every miss.
- **Cost.** Gate C `competing_defensible_answer` on a green back-test; the fix is a data recut.
- **Line.** The discretion is load-bearing fiction; the defect is asserting refusal by an excusable count.
- **Check.** Score each rival under the most charitable reading of every filed discretion: at least one
  inexcusable miss per rival at every bar, asserted by case name with margins, in generator and verifier.
- **Repair.** Plant refusals where the discretion cannot reach, opposite to the open question's mechanism;
  re-assert the whole corpus after the recut.

## H11. A superseded write-up left readable in the task tree gets graded as the live one
- **Defect.** An archived failed version under the task folder holds a second `submission.md` or
  `prompt.txt`; any consumer that discovers by name (judge glob, uploader) can grade the dead one.
- **Cost.** A review cycle lost to `solution_incorrect` on figures the live write-up never states.
- **Line.** Dead builds live as lines in `## Tried and rejected`; dot-prefixed folders do not hide copies.
- **Check.** Exactly one `submission.md` and one `prompt.txt` under the tree; no `prompt.md` beside
  `prompt.txt`; no markdown outside the task root and bundle; no superseded-build directory.
- **Repair.** One line per dead end in the design note, then delete the trees (never rename or zip). If a
  review ran on the stale copy, say so in the resubmission.

## H12. A prompt whose precision pins read as a grading sheet
- **Defect.** A rounding tag on every clause turns the request into a checklist of graded figures.
- **Line.** Pins are Gate E load-bearing; only counts of discrete things need none.
- **Check.** `voice-check.py` rounding-at-the-close rule: rounding words only in the last sentence, each rule
  naming its figures. Classify every figure as natural integer or derived; every derived one is covered.
- **Repair.** One closing rounding sentence; each dropped tag's figure is integer by construction or named
  there.

## H13. A prompt whose committed call reads as one output among several
- **Defect.** Equal paragraphs per deliverable, the call buried, the lead clause a series of figures.
- **Cost.** First-pass rejection as a collection of outputs, and solvers spread effort evenly.
- **Line.** The supporting layer stays; the defect is hierarchy, not inventory (except H18).
- **Check.** `voice-check.py` question-first rule: the call is a direct question in the first two
  sentences; each file tied to the quantity it stands up; the committing file leads with exactly one
  quantity.
- **Repair.** Lead with the call as a question, demote other figures to the file sentences, rounding to
  the close; re-check every moved pin.

## H14. An estimation domain the golden picked silently, that the data then argues against
- **Defect.** Unit and rounding get pinned; the grain of every rate does not. A finer cut gives another
  answer. The generator often causes it: a quota filled by a prefix of a list blocked by an attribute gives
  every later block a degenerate outcome, worst when the attribute is rare in history and common forward.
- **Cost.** Gate C against the strongest solver, and a data recut. Re-argue stump power after: the old
  wrong answers came from the fork.
- **Line.** Some grains are the intended correction; pin at the boundary of the quantity the attribute
  governs, never the attribute outright.
- **Check.** For every rate, compute the answer at every grain the data allows; a different committed answer
  is an open fork. Keep the finer estimator as a live verifier assertion. Assert no subgroup has a
  degenerate outcome rate, judged on cases at risk.
- **Repair.** Data first: permute labels inside each outcome group (aggregates untouched), spread with a
  carry keyed to the rival's pooling. Then pin positively in a file the naive path opens, scoped to its
  quantity, never naming the attribute or forbidding a required projection. Name invariants first.

## H15. A referee that only arbitrates downstream of a hazard
- **Defect.** A corroborating file confirms the governing input only on the population left after a device
  (archived block, duplicate, scope rule) is solved; on the raw data it backs neither, or the wrong one.
  The governing rule sits in one register cell unreachable from where the question arises.
- **Cost.** A false stated basis lands `competing_defensible_answer` on a forced answer.
- **Line.** Keep the hazard and the candidates; change only what the pack declares.
- **Check.** Compute every claimed corroboration on the pre-hazard population as well as the golden's;
  assert both. Assert every governing rule is reachable from the file whose semantics raise the question,
  and stated exactly once.
- **Repair.** Declare the dependency in the sibling rows' voice; route to the authority without
  restating; make the basis sentence true as written and name the rival's value.

## H16. A pack whose internal dates run ahead of the documents that cite them
- **Defect.** Generated offsets push record dates past the extract date in the manifest and the memo date.
- **Cost.** An in-fiction contradiction, worst on a load-bearing "latest" column.
- **Line.** Forward-looking records (plans, validity windows) go on a file-by-file allow-list, never a
  pattern.
- **Check.** Files with dates past the export date equal the allow-list; each extract column's max is on or
  before that extract's registered date.
- **Repair.** Shift the offset uniformly, never clamp (ties change "latest" winners); recompute every fed
  figure; check the range's lower end too.

## H17. A batch of prompts that are individually fine and collectively one prompt
- **Defect.** The same opening, verbs and file set across a batch, invisible per pair, usually prescribed by
  a skill.
- **Cost.** A client note on the whole batch.
- **Line.** The contract repeats (first person, one call, one to three files, units, rounding); the carrier
  must not.
- **Check.** `voice-check.py` bare over the window: no question form over a third, no repeated six-word
  phrase, a format mix more than one row deep. Read the counts, not self-report.
- **Repair.** Forward only: rewrite the prescription (worked example, checklist line) that taught the
  skeleton. `clone-check` Track A adjudicates.

## H18. A supporting ask that passes the hierarchy reads and is still a second decision
- **Defect.** An ask built outward from a device lands on a quantity someone wants for another decision
  (next cycle, a compliance exposure); it is tied to the call only by grammar.
- **Cost.** First-pass rejection as multiple independent outputs; no reordering fixes it.
- **Line.** Independent difficulty is fine; independent decision is not. The answer must be a component, a
  qualifier (sensitivity, flip condition, reconciliation) or the audit trail of the call.
- **Check.** Each ask's line in the ask ledger names how its answer enters the call; one naming another
  decision, window or owner is independent. Read the ledger, not the prompt.
- **Repair.** Retire it; win criteria back inside the decision (a second measure per candidate, an input's
  audit trail, a reconciliation, on rows outside the main call, `supplemental-stumping` Part 1.3). A grain
  split inherits the main trap. Re-derive the pair ceiling; regenerate golden, verifier and answers together.

## H19. A sibling build's archive attached under this build's name
- **Defect.** Identically named archives across a batch; the wrong one is uploaded and every on-disk check
  still passes.
- **Cost.** A full determinism failure on an unexamined build.
- **Line.** If this build's own archive lacks a named input, it is H4.
- **Check.** Print each archive's size, member count and digest at ready time; compare with the upload.
  Assert the write-up's inputs are in the target archive and the golden archive is exactly the deliverables.
- **Repair.** Re-attach, change nothing, quote the review's file description as evidence, name archives
  with the build number, ask the author to re-test.

## H20. A build whose domain fit is established everywhere except the prompt
- **Defect.** The registers carry the institution; the prompt, trimmed for leaks, does not.
- **Cost.** Rejection on the tag, inviting the wrong repair (redrawing the domain).
- **Line.** No explanatory sentence, nothing on the ban list (standard acronym, eligibility rule, deciding
  metric, rate basis, population). Licensed: who decides and what is released.
- **Check.** Read the prompt cold and name the domain. Assert the subdomain's institutional nouns (literal,
  from this fiction) appear in the prompt, paired with a leak assertion limited to ban-list phrases.
- **Repair.** Inside existing sentences, with nouns from the bundle: qualify the deciding body, say what is
  released, give the requester's organisation its adjective. Re-run verifiers and voice check.

## H21. An invented name that sits a few letters from a real organisation, school or place
- **Defect.** Exact-match checks pass names one or two letters from a real one, or containing its
  distinctive word (saints, townlands, venue words, staffing brands).
- **Line.** Generic geography (river, bay, county) is texture; the distinctive remainder is the test.
- **Check.** Normalise invented and reference-register names (case, accents, punctuation, generic org words
  dropped); fail at edit distance two or less or containment; no retired name survives a rename.
- **Repair.** Rename in the generator, rebuild, confirm figures unchanged; prefer descriptive names.

## H22. Constructed records inside a file the pack presents as a real download
- **Defect.** Fictional organisations added to a real public file in its layout while provenance says
  "used as published".
- **Line.** A declared constructed layer is normal; the silent mixture is not.
- **Check.** For every file provenance calls a download, compare rows and keys with the kept raw download;
  fail unless provenance declares additions.
- **Repair.** Move constructed records to their own files, or declare additions and construct more
  organisations than the ladder needs so "constructed" does not mark the decisive ones; re-check
  camouflage.

## H23. An ask whose wording presupposes what the data holds
- **Defect.** An ask requests a count with a property of the counted items, or names a subset or a direction
  of change as given ("how many of them and what they cost", "the sites where it fell"), so the prompt states
  a fact about the data before a file is opened.
- **Cost.** The client's prompt review fails the prompt on it alone, as a leak; where a rung or device depends
  on the presupposed fact, the step is also handed over.
- **Line.** A fact the requester knows before any analysis (their own sites, the cut-over date) is furniture;
  a fact only the analysis establishes (a count is non-zero, a subset exists, a figure moved one way) fails.
- **Check.** Read every ask about a subset with "none" as its answer; flag
  `how many[^.]* and (what|which|how much) (they|their|those|it|its)` unless the sentence carries "whether" or
  "if so".
- **Repair.** Make "none" grammatical and keep every figure, unit, rounding and per-unit structure, so the
  criteria count does not move; never delete or fold the ask. Where a unit's answer is zero, golden and
  write-up say "none".

## H24. A provenance record that steps outside the fiction
- **Defect.** Every file reads as the organisation's own record except the provenance or licence file, which
  says in the author's voice that the files were constructed, invented or made for an exercise.
- **Cost.** The client's input-asset review fails the pack on authorship, blocking on its own; it is often the
  first file opened and the review stops there.
- **Line.** Who compiled the folder and when, the licence, each file's source and pull date, and real names used
  descriptively stay. Any statement that the world is constructed goes to the design note, the card and the
  portal's provenance field, never under `target/`.
- **Check.** Sweep `target/` for a sentence saying the pack was built ("constructed for this exercise", "are
  invented", "are fictional"); read the bare words "fictional", "fictitious" and "this exercise" in documents.
- **Repair.** Rewrite it in the generator as the organisation's own compile note (a team the pack already uses,
  the pack's export date), rebuild, confirm every other file, the golden and the write-up byte-identical (H7).
- **Tooling.** `leak.py` sweep 2: the built-pack sentence is LEAK in any file, the bare words REVIEW in
  documents; it cannot tell an in-world "fictitious vendor" from a tell.

## H25. A shipped document validated by the same permissive reader that wrote it

- **Defect.** A document under `target/` is unreadable to a parser a solver would reach for, while the
  generator's own "the text is unchanged" assertion reads it with the lenient reader of the library that
  produced it, so the defect ships green. The decisive rule can sit in that document, which puts the whole
  build out of reach on the commonest route into it.
- **Cost.** A solver on the ordinary route cannot read the governing clause at all, so the response is
  graded against a call the pack never showed it. It also reads as a corrupted pack in the input review.
- **Line.** A document a writer library emits is fine; what is not fine is an in-place byte substitution in
  a structured container. Patching a `/Info` string, a sheet name or a container header by offset moves the
  bytes that the cross-reference table or the escaping depends on. Re-serialise through a library that
  rewrites the structure instead.
- **Check.** Open every shipped document with every reader a solver is likely to use, not one, and assert
  the decisive sentences are present in each: for a PDF, a lenient reader and a strict one and at least one
  independent text extractor. Assert the strict reader's text equals the lenient reader's. Assert any string
  the generator rewrote is still a balanced, correctly escaped literal.
- **Repair.** In the generator, re-serialise the document rather than patching bytes, then confirm the
  rebuild is byte-identical twice and the golden that shares the code path is fixed by the same change.
  Normalising through a second library also drops the writer library's header and trailer comments, so the
  toolchain signature goes away rather than being overwritten in place (H1).
- **Tooling.** `leak.py` sweep 10 reads the container's writer signature and sweep 7 reads hidden content;
  neither opens the document twice, so neither can see this. The assertion belongs in `checks.py`.

---

## Adding an entry

An entry is a **class** a future build could repeat with other nouns; anything else goes in the design
note. Order: Defect, Cost, Line (if a legitimate twin exists), Check (a wireable assertion), Repair (its
own failure modes), Tooling (only if a tool exists; say what it refuses to decide). No dates, file names
or incident numbers.

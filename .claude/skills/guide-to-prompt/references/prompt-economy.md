# Prompt economy

> **Read this alongside `prompt-voice.md`, after the shape is picked and before the draft is
> called done.** `prompt-voice.md` governs what the request sounds like. This file governs how
> many words it takes to say it, and they are different defects. A prompt can pass every variety
> check in that file, open on a move nobody has used, ship an unused format, and still be twice
> the length of anything the client has paid out on.

**The instruction, in the author's words:** the prompt has to be concise. No yapping, nothing
lengthy, nothing that reads as LLM generated, not too much context about the work. Straightforward.

That is not a style preference sitting on top of the spec. It is the single measurable difference
between a set of 25 prompts the client paid out on and the builds this repo is shipping now, and
the paid-out set's longest prompt is shorter than our median one.

---

## 1. The measurement

Twenty-five paid-out prompts, measured against the current twelve-build window. Counts only. Nothing from
that set is stored in this repo and nothing from it is ever copied into a build.

| | paid-out set (n=25) | ours, the current window (n=12) |
|---|---|---|
| Words, median | **227** | **404** |
| Words, range | 115 to 334 | 290 to 664 |
| Sentences, median | 10 | 13 |
| **Words per sentence**, median / p90 / max | **21.6** / 32.8 / 44.3 | **31.4** / 39.9 / 46.5 |
| Longest paragraph, median / p90 / max | 90 / 180 / 269 | 124 / 212 / 246 |
| **Commas per sentence** | **1.5** | **2.1** |
| **Subordinating connectors per 100 words** | **0.8** | **1.5** |
| Context paragraph as a share of the prompt, median | 22.4% | 22.8% |
| Context paragraph in words, median | 53 | 95 |
| Carries a sentence under 8 words | 18 of 25 | 7 of 12 |
| States the file count as a number | 8 of 25 | 0 of 12 |
| Rounding tags per prompt, median | 0 (21 of 25 carry none) | 2 (one build carries 13) |

**The two rows about the context paragraph are the trap in this table, so read them together.**
Our context paragraph is nearly twice as long in words and **exactly the same share of the
prompt**. It is not independently bloated. It is 22 per cent of a prompt that is 78 per cent too
long, so an author who cuts only the context will lose the framing and still miss the budget. The
same caution applies to the longest-paragraph row: the two distributions overlap heavily (three
paid-out prompts are a single paragraph, one of them 269 words), so that row is a flag on the
extreme, not a target.

**What survives being normalised for length**, and is therefore a real difference in how the
sentences are built rather than an artifact of there being more of them: words per sentence,
commas per sentence, connectors per hundred words, the rounding tags, the "because" clauses, and
the missing short sentence.

**Our prompts are 78 per cent longer and our sentences are 45 per cent longer at the median.** The
extra words are not one long section that could be deleted. They are spread through every sentence
in the prompt, which is why this is not fixed by cutting a paragraph, and why the gate that
discriminates is the total.

**Length as a prose rule does not bite.** `prompt-voice.md` §6 says "vary the length, 575 is our
median and theirs is far shorter". The median came down to 404 and words per sentence went **up**. A rule in this repo bites when `voice-check.py` counts it, which
is why the load-bearing half of this file is section 5.

---

## 2. What is not being cut

Concision here is per-sentence compression. It is never requirement deletion, and an author who
reads "shorter" as "ask for less" trades a realism finding for a Gate E or a 25-criteria finding,
which is the worse trade in both directions.

The paid-out set carries **all** of the following, in a quarter fewer words than we spend:

- **The shape's repeated structural unit, stated in full.** Every jurisdiction ranked. All
  thirty-four states. Month by month across the fiscal year. All nine cells of the grid. One row
  per calendar month with four measures on it plus projected rows plus a total row. This is where
  the 25 criteria come from and the paid-out set is denser on it than we are, not thinner. It is
  carried in **one sentence** with a list in it.
- **The decision furniture.** The committed call, the runner-up named, the gap on the deciding
  metric, the flip condition, the hold option where the evidence may not support a call.
- **The chart's parts.** Series, ordering, the marked threshold, the annotation, and a title that
  states the finding. All named, in one sentence, not in a paragraph with a reason hung on each
  part.
- **Unit and rounding coverage.** See §4, move 3. The coverage is unchanged; the carrier moves.
- **The data-quality warnings**, stated flat at the end in a sentence or two with no framing.

If a compression pass removes any of these, it was the wrong pass.

---

## 3. The four places the words actually are

Named with their measured cost, because an author can act on a named class and cannot act on "be
concise". They are in the order the measurement supports, which is not the order they feel like.

**1. The sentence that will not end.** 31.4 words per sentence against 21.6, 2.1 commas per
sentence against 1.5, and 1.5 subordinating connectors per hundred words against 0.8. Every element
of a deliverable arrives as its own clause, chained onto the last with "so", "which", "rather
than", "together with", "because". This is the only class that is a genuine difference in how the
prose is built rather than a consequence of there being more of it, and it is spread across the
whole prompt rather than sitting in one place. It is also what absorbs a length rule: the
prose rule took the median from 575 words to 404 and words per sentence went up over the same
stretch, so the words came out of the count and went back into the clauses. The paid-out set puts the same elements in a list inside one sentence, or behind a colon
as a delimited series, and every element survives intact.

**2. The reason hung on every ask.** Ours carry a median of one "because" clause per prompt and up
to three; the paid-out set carries a median of zero and never more than one. A clause explaining
why the requester wants a figure is fifteen to twenty-two words that grade nothing. **One** of
these, on the ask that genuinely needs a motive, is realistic and worth keeping. One per ask is the
tell.

**3. The rounding tag repeated per figure.** This is `../reduce-house-fixes/SKILL.md` **H12**,
already in the register, and the measurement says it is being ignored: 21 of 25 paid-out prompts
carry no rounding tag at all and none carries more than two, while task94 carries thirteen. H12's
line is the right one and it is restated in §4 move 3.

**4. The narration the context paragraph carries, which is a smaller prize than it looks.** The
organisation's business model, its footprint, its market, its product line, and the history of how
the decision got here. None of it is gradable, none of it constrains the answer, and a reader skips
it: task99 spends eighteen words on what the company manufactures and who it sells to in a decision
that turns on neither. **But read §1 before spending a pass here.** Our context paragraph is the
same share of the prompt as theirs (22.8 per cent against 22.4), so it is not independently
bloated, and cutting it alone costs the framing and still misses the budget. Delete the bio and the
pack inventory because they are dead weight, then do the real work in class 1.

---

## 4. The compression moves

Each move keeps every requirement and costs words. They are moves, never sentences: nothing in
this file and nothing from the paid-out set is a phrase to reuse, and a reused sentence is a clone
tell under the rule governing every example in this library.

**1. The colon-list column spec.** A data file's columns arrive as one sentence naming the grain,
then a colon and a delimited series. Every column is still named and still gradable, and the
paragraph that would have introduced each one is gone. Worth thirty to sixty words on any build
shipping a CSV or a workbook sheet.

**2. The one-sentence chart spec.** Chart type, what each bar or line is, the ordering, the marked
threshold at its value, the annotation and what the title has to carry, all in one sentence, in
that order, with no reason attached to any of them. The parts are what earn the criteria and they
all survive. What goes is the narration between them.

**3. The block rounding convention, with pinned exceptions.** State the convention once in the
requester's own voice, then pin rounding explicitly only on figures whose type does not already
fix it. H12 draws the line: a count of discrete things in the shipped data is a whole number by
nature and opens no fork untagged, while a derived quantity (a share, an average, a rate, a
ratio, a counterfactual, a difference in points) keeps its explicit statement. Re-enumerate the
surviving pins against the full figure list afterwards, because the failure mode of this repair
is dropping one pin too many.

**4. The stated file count.** A short sentence giving the number of things wanted, before they are
listed. Eight of twenty-five paid-out prompts do this and none of ours does. It replaces the
narrated transition into each deliverable, so it buys words back, and it makes the deliverable
count checkable at a glance for the reviewer who is checking the ceiling of three.

**5. The short sentence that breaks the chain.** Eighteen of twenty-five paid-out prompts carry a
sentence under eight words. A short flat sentence after a long one is the cheapest thing that
stops a paragraph reading as generated, and it costs nothing because it replaces a subordinate
clause that was going to be chained on anyway.

**6. The purpose clause in place of a content inventory, where the content is not graded.** The
audit file's job can be stated by what somebody has to be able to do with it (follow a row back to
the register, rerun it next quarter, reproduce the result from the supplied files) rather than by
listing contents that carry no criteria. This applies **only** to ungraded contents. Anything the
rubric grades is named explicitly, because a purpose clause is not gradable.

**7. Delete the pack inventory.** Listing what is in the folder, file by file, is the largest
single deletable block in a long build and the pack is attached where the solver can see it.
`prompt-voice.md` §5 already logs "everything my team works from is in the folder" as a calcified
carrier; the shorter form is to say nothing at all, or to name only what the pack does **not**
contain.

---

## 5. The budget, and the check

**Per build, on the draft, before the prompt is called done.** The **target** is the paid-out
median, which is where to aim. The **flag** is set at the paid-out set's own p90 or observed
maximum, so a flag means the draft is outside the range of anything that has been paid out, not
merely above average. Where the two distributions overlap, the flag is deliberately loose.

| Gate | Target | Flag over | Why the flag sits there |
|---|---|---|---|
| **Words** | 250 | **330** | The paid-out maximum is 334, and our median is 404. This is the gate that discriminates, and 8 of the 12 builds in the current window breach it |
| **Words per sentence** | 24 | **33** | The paid-out p90 is 32.8 and its maximum is 44.3, so the distributions overlap. A draft over 33 is building sentences nothing paid out has built |
| Longest paragraph | 110 | **180** | The paid-out p90. Its maximum is 269 and three paid-out prompts are a single paragraph, so this is a flag on the extreme |
| Context paragraph, as a share | 25% | **46%** | The paid-out p90 for multi-paragraph prompts. The absolute word count is **not** a gate, because the share does not differ between the two sets |
| A sentence under 8 words | present | absent | 18 of 25 paid-out prompts carry one |
| Rounding tags | 0 to 3 | **more than 3 with no block convention sentence** | H12. 21 of 25 paid-out prompts carry none |
| "because" clauses | 0 or 1 | **2 or more** | The paid-out maximum is 1 |

```bash
python3 .claude/skills/guide-to-prompt/references/voice-check.py task96   # the draft
python3 .claude/skills/guide-to-prompt/references/voice-check.py          # the batch
```

The ECONOMY block prints every row above with the paid-out medians beside them, and flags each one
that breaches. Nothing here is a hard fail on its own: a build whose shape genuinely needs 300
words is fine, and a build at 480 has narration in it whatever its author believes.

**The order matters.** Draft at whatever length the ideas arrive in, then compress. Compressing a
draft that already carries every requirement is safe, because every deletion is visible against the
requirement it would remove. Writing short from the start is how requirements go missing.

**Then re-run the gradability check, both halves of it.** After a compression pass:

1. **Walk the figure list.** Every graded figure still named, still carrying its unit, and still
   covered on rounding by the convention or by its own pin.
2. **Re-count the criteria off the shape's arithmetic**, the same arithmetic worked on paper at
   design time in `SKILL.md`, "Reaching 25 criteria, through the shape". It was worked on the
   uncompressed draft, and move 1 and move 6 are the two that can silently drop a named element
   from the repeated structural unit, which is where the bulk of the count lives. A compressed
   prompt that has fallen under 25 has failed, however well it reads.

These are the only two ways this pass fails, so they are the only things worth checking
afterwards.

---

## 6. What this does not license

- **Not a licence to cut the repeated structural unit.** The 25-criteria floor is unchanged, and
  the paid-out set hits it in 227 words by putting the whole repeated unit in one sentence.
- **Not a licence to drop rounding on a derived figure.** §4 move 3 moves the carrier and keeps
  the coverage. A figure that is fractional upstream and whole only by rounding keeps its pin.
- **Not a licence to drop the file names.** Twenty of twenty-five paid-out prompts name their
  files with extensions. It costs three words and it makes the deliverable set gradable.
- **Not a licence to write a vague ask.** "Tell me what the data shows" is short and ungradable.
  Short is a property of the wording, never of the demand.
- **Not a reason to loosen the hierarchy read.** A compressed prompt still has to carry the
  committed call as one quotable whole sentence, and compression that fuses the call into a
  clause of another sentence has broken `SKILL.md`'s read 1.
- **Not a reason to reuse a sentence from the paid-out set or from this file.** What transfers is
  the move.

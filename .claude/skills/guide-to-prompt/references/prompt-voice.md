# Prompt voice and structure

> **Read this after the shape is picked and before the prompt is drafted.** The shape decides
> where the criteria come from. This file decides what the request sounds like, and that is a
> review-visible property of the batch rather than a matter of taste.
>
> **Then read `prompt-economy.md`, which is the other half and is a different defect.** This file
> is about variety and that one is about length. A prompt can pass every check here, open on a move
> nobody has used and ship an unused format, and still run 60 per cent longer than anything the
> client pays out on, with sentences 40 per cent longer. Asking for shorter prompts in section 6
> brought the median down from 575 words to 404 while words per sentence went up, which is why the
> budget lives in `prompt-economy.md` and is counted by the script.

**The note, in the client's words:** the majority of prompts are following the same exact voice
and structure, *"I'm a X working at Y. Here's some context. Give me this main recommendation and
here are the two deliverables that I need from me."* The instruction is to switch it up and make
every prompt feel different.

That is a batch-level finding, which is what makes it different from every other style rule in
this repo. A prompt that reads perfectly well on its own is still a defect when it is the
thirteenth in a row built to the same skeleton, because the reviewer reads the batch in one
sitting and the skeleton is the first thing they see.

---

## 1. The finding, measured on our own corpus

Eighteen builds were drafted under the prose spec, task66 through task83. Run
`voice-check.py` over them and the monoculture is not a matter of opinion.

| What repeats | Builds |
|---|---|
| Opens in first person with a role verb, sentence one, clause one | **17 of 18** |
| Opens with the exact words "I run" | **12 of 18** |
| "Lead with" or "Open with" as the first instruction to the text deliverable | 10 of 18 |
| "and a title that states ..." closing the chart ask | 10 of 18 |
| "everything my team works from is in the folder / pack" | 8 of 18 |
| "Write it up as `file.pdf`" as the commissioning verb | 8 of 18 |
| "drawn as a labelled line ..." | 8 of 18 |
| Ships a PDF | **18 of 18** |
| Ships three files, which is the ceiling | **16 of 18** |
| Ships one file, which the spec allows and the client library uses twice | 1 of 18 |
| Uses DOCX, PPTX, HTML, JSON, SVG, SQL, IPYNB, R, TSV or Parquet | **0 of 18** |

Median length is 575 words. Measured since, over 25 prompts the client actually paid out on: their
median is **227 words** with a maximum of 334, at **21.6 words per sentence**, against our 404 and
31.4 across the current window, so their longest prompt is shorter than our median one. `prompt-economy.md` carries that measurement and the budget.

**The template we converged on**, stated plainly so it can be recognised and avoided:

> I run *[function]* at *[org]*, and *[body with a date]* forces *[the call]*. It is one number,
> fixed once made, no ranges. Everything my team works from is in the folder. Write it up as
> `x.pdf`, leading with *[the figure]*, then *[the breakdown]*, closing on the one thing that
> would move it. Then chart it so the board sees it at a glance, `y.png`, with a labelled line
> and a title that states the call. And hand the workings over as `z.xlsx`, because they will
> open that rather than take my word for it.

Every one of those eighteen builds passed the old checklist honestly, because the old checklist
prescribed exactly this. The prescriptions have been rewritten. What follows replaces them.

---

## 2. What varies, and what never varies

Variety is a property of the wording and the ordering. It is never bought by weakening what makes
the task gradable, and a reviewer sending a build back for a missing rounding spec costs more than
one sent back for a familiar opening.

**Never varies, whatever the voice:**

- **First person prose.** The client's contract is "prose, first person, the way you would ask a
  colleague". What is banned is *"I run X at Y" as sentence one* and the fixed context, then memo,
  then chart, then workbook ordering. The role can sit mid-paragraph or last, and the client's own library does both.
- **One committed call**, forward facing by default, resolving to one defensible answer.
- **One to three named deliverables**, three being the ceiling.
- **Every figure's unit and rounding is covered.** This is Gate E and it is not negotiable.
  Section 5 varies the carrier, never the requirement, and the default carrier is a convention
  stated once with explicit pins on the derived quantities only.
- **No roll call** of colleagues' opinions. At most one stakeholder belief, as one clause.
- **Nothing that fixes the basis, the window, the convention or the population**, no input file
  name, no standard by acronym, no method hint, no trap word.
- **The six realism tests on the asks**: use, provenance, genre, vocabulary, asymmetry,
  already-known.

**Varies, and should differ from the last three builds on each axis:**

the opening move · where the role sits · the order the deliverables are commissioned in · the
verbs that commission them · sentence rhythm and paragraph count · length · the number of files ·
the format mix · whether the standard is stated up front or arrives with the ask that needs it.

---

## 3. The opening move

The bank below is derived from the client's 72 worked prompts in `shapes/`, which vary their
openings far more than we have. Each entry is **a move plus what has to be true for it to work**,
never a sentence to reuse. Twelve ready-made openers would produce a monoculture with a period of
twelve, and twelve reusable sentences would be a clone tell under the rule that governs every
example in this library.

| Move | The first line does | It only works when | Where it fails |
|---|---|---|---|
| **Decision-first** | Names the call before anything else, role second | the decision is a one-of-N a reader recognises with no setup | the candidate set needs explaining, so the first line becomes a paragraph |
| **Deliverable-first** | Commissions a named file in the imperative, then explains why | one file is genuinely read before the others, so the ordering carries meaning | the file is the appendix, and leading on it buries the call |
| **Question-first** | Opens on the literal question, then says who has to answer it | the question fits in one line and survives being asked cold | it needs a clause of context to parse, which the form does not allow |
| **Rule-first** | States the governing standard as the first fact | the rule is what makes the answer non-obvious, rather than the data | the rule is furniture, and stating it early leaks the path |
| **Constraint-first** | Opens on the capacity that binds | a cap or capacity is what makes this a decision rather than a list | the constraint is not actually binding, and the opening oversells |
| **Symptom-first** | Opens on what moved | the task is diagnostic and the movement is why anyone is asking | the movement is not the subject, and the reader is pointed the wrong way |
| **Stakes-first** | Opens on the cost of getting it wrong | the consequence is concrete and sits outside the analysis | the stakes are generic, and it reads as throat-clearing |
| **Evidence-first** | Opens on what is sitting in the folder | the pack itself is the forcing event | it invites the solver to inventory the pack rather than decide |
| **Number-first** | Opens on the figure owed, in its unit | the unit of the answer is itself informative | the figure needs the standard beside it to mean anything |
| **Options-first** | Lays the candidate calls out as a short closed set | the decision is a small set, often including the hold | the set is long, and listing it eats the paragraph |
| **Calendar-first** | Opens on the meeting, the filing or the deadline | the date is what makes the call forward facing | every build has a date, so this one calcifies fastest |
| **Situation-first** | Opens on the state of the world at the period close | one fact about the period frames everything after it | it is a fact nobody would state out loud, so it reads as scene-setting |

**Choosing.** Take the move from what actually forces this decision, then check it against the
last three builds and take the second-best fit if it repeats. A move chosen because it is next in
the table is the same defect one layer down.

**The table is append-only.** A move seen in client material that is not here gets a row, with its
condition and its failure mode filled in, rather than being folded into a neighbouring row.

## 4. Where the role sits, and how much of it there is

The client's library states the role in at least four positions: opening clause, mid-paragraph
after the decision is on the table, a single short sentence of its own near the end
("I own monetization."), and the closing line of the context ("I own supply resilience."). Ours
puts it in the opening clause seventeen times out of eighteen.

The role has to be there, because the asks have to sound like a person with a job asking for them.
It does not have to arrive first, it does not need a subordinate clause describing the
organisation's business model, and it does not need the org's name at all when the function is
enough. Two of our recent builds spend twenty-five words on the company before reaching the
decision, which is twenty-five words the client's examples do not spend.

## 5. The requirement against its carrier

The left column is spec and appears in every build. The middle column is the wording we happen to
have reached for, and its count is what a reviewer reading the batch sees. **Vary the carrier,
never drop the requirement.**

| The requirement, which is invariant | Our carrier, and its count over task66 to task83 | Ways to carry it instead |
|---|---|---|
| Every figure's unit and rounding is covered | "as a whole number", "to one decimal place" | The coverage is spec and stays. **The block carrier is the default**, not one option among three: state the convention once ("counts are whole numbers unless I ask for a decimal") and pin explicitly only on derived quantities. 21 of 25 paid-out prompts carry no rounding tag at all. See H12 and `prompt-economy.md` §4 move 3 |
| The pack is handed over | "everything my team works from is in the folder" 8/18 | Say nothing at all, the pack is attached and the solver can see it. Or name what the pack does not contain. Or let the ask imply it |
| A text deliverable is commissioned | "Write it up as `x.pdf`" 8/18 | Name the reader and let the file follow. Name the meeting the file is read at. Commission it in the same sentence as the call. Or ask for it last |
| The text deliverable opens on the call | "Lead with", "Open with" 10/18 | Say what the first line has to survive ("the line that gets signed"), or state the call in the context and let the file inherit it |
| A chart's title states the finding | "and a title that states ..." 10/18 | Ask for a title a reader could quote back. Say what the title has to contain rather than that it states it. Put the title requirement first among the chart's parts rather than last |
| A threshold is drawn and labelled at its value | "drawn as a labelled line carrying its value" 8/18 | Name the line by what it is (the tolerance, the cap, the contract line) and say it carries its number |
| A table reconciles | "with a total row that ties" 5/18 | Ask the total to match a figure named elsewhere, by naming that figure |
| The visual is quick to read | "reads / sees it at a glance" 3/18 | This is the client's phrase and it is fine once. Six times in a batch it is ours |
| A stakeholder holds a belief | "has been working on the basis that" 3/18 | State the belief in their words. Attribute it to a role. Report it as something said in a meeting |
| The call is one value | "one committed figure, no range" 7/18 | Say what a range would cost. Say the number gets signed. Say it is fixed for the year once made |
| The rest of the asks support the call | "everything else is there to stand that number up" 3/18 | Say who asks for each piece and why, or say nothing and let the asks stand on their own |

Nothing in the middle column is banned outright. A phrase used once is a phrase, used in a third
of the batch it is a template, and `voice-check.py` prints the count so the judgement is made on
the number.

## 6. Rhythm, length and paragraph count

Our prompts are two to three times longer than the client's and they are all built the same way:
a context paragraph, then one paragraph per deliverable, in the same order every time.

- **Vary the length, and cut it.** 404 words is our current median and 227 is theirs, with a
  paid-out maximum of 334, which sits below our median. A short prompt with a multi-dimensional ask is stronger than a long one,
  because length comes from narrating the furniture and the furniture is where leaks live. The
  budget and the compression moves are in `prompt-economy.md`; this bullet is where the requirement
  is named and that file is where it is counted.
- **Vary the paragraph count.** Not every build needs one paragraph per deliverable. A two-file
  build can be two paragraphs, or four, or one.
- **Vary the sentence length.** Every one of these prompts runs long compound sentences chained
  with "and" and "then". Real requests contain short sentences. "That is the line that gets
  signed." is a sentence.
- **Asymmetry is the point.** A real request is lopsided: the thing that matters is named to the
  decimal, and something else is mentioned in passing. An evenly weighted prompt reads as
  generated for the same reason evenly sized sections do.

## 7. The structural monoculture underneath the voice

Three of the numbers in section 1 are not about wording at all, and no amount of rewriting the
opening fixes them.

- **18 of 18 ship a PDF.** The spec says in terms that `analysis_report.pdf` is not the best-suited
  deliverable for every task. A determination can be a DOCX, a return can be a CSV, a scorecard
  can be a single deck, and shape 10 and shape 17 in the client's library ship **one** file.
- **16 of 18 ship three files.** Three is the ceiling, not the target, and the client's library
  norm is two. Building at the ceiling every time also multiplies the cross-file agreement cost
  for no gain.
- **Ten formats have never been used.** DOCX, PPTX, HTML, JSON, SVG, SQL, IPYNB, R, TSV and
  Parquet are all live, and several of the client's worked examples ship an HTML page a stakeholder
  opens in a browser or a PPTX the review runs off.

Pick the files a real analyst would produce for this decision. Where two format choices are equally
honest, take the one this batch has not used.

## 8. The check

```bash
python3 .claude/skills/guide-to-prompt/references/voice-check.py            # last 12 builds
python3 .claude/skills/guide-to-prompt/references/voice-check.py task84     # a draft against them
```

It prints the opening-move spread, the opening clause of every build in the window, the carrier
phrases with their counts, any unlisted six-word run shared by a third of the batch, and the
length, file-count and format mix.

**Per build, before the prompt is called done.** Run it with the draft's task number. The draft's
opening move is not the move used by the last three builds. No carrier phrase in the draft is
flagged as calcified. The file count and the format mix are not both the batch mode.

**Per batch, before submission.** Run it bare. The window should show four or more distinct
opening moves across twelve builds, no carrier phrase in more than a third of them, and a format
mix that is not one row deep.

**How this sits with `/clone-check`.** Same territory, different jobs. The batch surface is
clone-check's Track A, and this script is what measures it: the script counts, clone-check
adjudicates whether a repeat is a clone and what the repair is. Run this bare before a Track A
adjudication on a batch. Neither is a substitute for the other, because a monoculture spread evenly
across a batch is invisible pair by pair and obvious in the counts, which is exactly the shape of
the client's note: no two of our prompts were clones of each other, and all eighteen shared one
skeleton.

**Self-report does not work here.** Eighteen builds passed a checklist that asked whether the
context was first person and two or three sentences. Every one of them answered yes truthfully.
They would not have passed `grep`.

## 9. What this does not license

- Not a licence to drop first person, which is the client's own contract.
- Not a licence to write an opening that misrepresents the decision to be novel. The move comes
  from what forces the call, and a symptom-first opening on a build with no symptom is worse than
  a familiar one.
- Not a licence to weaken an ask. Every figure keeps its unit and its rounding, every ask stays
  multi-dimensional, and the 25-criteria arithmetic is unchanged.
- Not a licence to leak. A rule-first or constraint-first opening states **that** the standard
  binds, never which file settles it or how it resolves, and the ban on naming the deciding
  metric, the eligibility rule and the file survives whichever move you pick.
- Not a reason to reuse a sentence from this file or from the client's library. What transfers is
  the move, and only the move.

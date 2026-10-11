# The prompt's voice: the ten rules, and how prompts still differ

> The prompt sounds like a person asking for help with their task, not a backstory about them. It mentions
> only what the task needs. `voice-check.py` is the gate; this file says what each rule means and how a
> batch of prompts written under the same rules still reads as many voices rather than one.

## The ten rules

1. **Lead with the question.** Turn "The number I need is" or "Tell me" into a direct question, "How many
   lots should we order?", and put it near the start. The gate wants a question mark in the first two
   sentences.
2. **Cut who and why.** Drop names, job titles, sign-off chains, meetings and who reads the file. A detail
   stays only if the answer would change without it. "She chairs the committee", "the board votes on the
   24th", "this is what he reads first" all go.
3. **Test every fact before cutting it.** If removing it could change the answer, keep it: the 8 February
   send date, the Labour Day extract, "nothing bought or sold after cutover", "no repairs after 15 December".
   The test is whether the computation changes, not whether the sentence sounds like context.
4. **Keep every ask exactly.** File names, columns, periods, units and rounding rules carry over word for
   word. Rephrase around them and never reword them.
5. **Do not change meaning while smoothing.** "In cents" becoming "dollars and cents" changes the unit.
   "Whether any, and if so how many" becoming "how many" assumes the answer exists.
6. **One continuous paragraph.** Context, question, files, rounding, in that order. List items are joined
   with commas and semicolons, never bullets or "Then" and "Last".
7. **Merge and shorten.** Two clauses that make one point become one. Each rounding rule is stated once, at
   the end, naming the figures it governs.
8. **Ask, do not specify.** "What is", "put it in", "also give me", never "X is the file, one row per".
9. **Drop claims made only to be rejected.** A manager's or memo's opinion that argues for the wrong answer
   is banned as the deciding stump under the three rules, so cutting it is the safe default.
10. **Run the 10/10 check last.** Does the answer turn on real analysis, or only on following a stated
    procedure or reading a field correctly? If it is only the procedure or the field, flag it: the build is
    not ready, and no prompt fixes that.

## Plain text, and why

The prompt is `prompt.txt`. No backtick around a file name, no asterisk or underscore for emphasis, no
heading mark, no bullet or numbered list, no pipe, no bracketed block, no blank line between paragraphs. A
file name is written bare, `forebay_sediment_build.xlsx`, and the underscore inside it is a character of
the name, not emphasis. The portal's prompt checks read the file as the solver does, and a markdown
character is the first sign of a draft nobody edited.

## The order inside the paragraph

Context is one clause or sentence, only the fact the computation needs (the grant rule, the window, the
cut-over). Then the question, which is the committed call, as one sentence a reader can quote. Then the
files: each named with its extension and what it carries, at the level of content a person would state
("one stacked bar per district ordered by high-rated releases, each high segment labelled with its count").
Then the rounding, once, at the end, each rule tied to the figures it governs. Units stay with their
figures throughout, because that is how a person says a figure.

## Where the variety lives now

The client's note said every prompt felt the same because every prompt opened on a role and ran context,
call, deliverable, deliverable. Under the ten rules there is no role to open on, so variety comes from three
places, and the batch report in `voice-check.py` measures the first two.

**The question's form.** A prompt can lead with how many, how much, which, whether, what, when, who or where,
and the form follows from the decision: a count asks how many, a pick asks which, a gate asks whether, an
amount asks how much, a date asks when. Take the form from the decision. The batch report shows the spread
and flags a form carrying more than a third of the window.

**The sentence.** Short questions and long file sentences alternate differently in every prompt because the
files differ. One prompt carries its forcing fact as a clause inside the question, another as a sentence
before it. One names two files in one sentence, another gives each its own. A prompt that reads as a list
of asks hung on one skeleton is a prompt whose files were specified rather than asked for.

**The files.** One file is legal, two is the norm, three the ceiling; the format is the one a real analyst
would hand over for this decision. The batch report shows the format mix, and a window that ships one
format or one pairing throughout reads as a template whatever the sentences do.

## The gate, rule by rule

| Rule | What `voice-check.py` checks | Level |
|---|---|---|
| file | the prompt is `prompt.txt`; a `prompt.md` is a build from before the rule and fails the gate for a build under check | FAIL |
| plain text | no backtick, hash, pipe, bracket, bullet, label-colon line, or asterisk or underscore outside a file name | FAIL |
| one paragraph | no line break inside the prompt | FAIL |
| question first | a question mark in the first two sentences | FAIL |
| under 1,000 characters | the whole file, file names included | FAIL |
| no em dash | none | FAIL |
| no persona or title | no persona from the card's `world.people`, no capitalised pair followed by a role verb, no job-title introduction, sign-off, board vote or reader of the file | FAIL |
| no sequencing | no sentence opening on Then, Next, First, Second, Last, Finally, After that | FAIL |
| no LLM tells | none of the tell lexicon (leverage, robust, comprehensive, seamless, delve, ensure, make sure, note that, in order to, furthermore, stakeholders and the rest), no en dash | FAIL |
| no roll call | no attributed opinion; one is a warning, two fail | FAIL at two |
| rounding at the close | rounding words in the last sentence only; a prompt with none anywhere warns | FAIL when repeated |
| deliverables named | one to three output file names with extensions | FAIL |

Run it with the task number for the per-rule list and the exit status; bare for the batch.

## What the rules do not license

- Not a licence to drop a fact the computation needs. A date that bounds the window, a stop rule, a
  cut-over, a grant rule, the candidate set: each stays, because the answer would change without it.
- Not a licence to weaken an ask. Every figure keeps its unit, every derived figure has a rounding rule at
  the close, every file keeps its name, and the 25 criteria come from the shape as before.
- Not a licence to leak. A clause that states that a standard binds is fine; a clause that says which
  file settles it or how it resolves is not, and the bans on naming the metric, the eligibility rule and
  the input file stand.
- Not a licence to write the same question twice. Two prompts that both open "How many X should we order
  for Y?" on the same shape read as one prompt; the batch report shows it.
- Not a reason to reuse a sentence from this file or from the client's library. What transfers is the
  rule, never the wording.

# Prompt economy: the budget and the compression moves

> Read this beside `prompt-voice.md` after the shape is picked. The voice file says what the prompt sounds
> like; this one says how many words it takes, and the two are different defects. The budget is the gate's
> hard ceiling of 1,000 characters, which is about 150 to 170 words, and the client's paid-out prompts
> show the ceiling is generous: their median was 227 words at 21.6 words a sentence, their maximum 334,
> and every one of them carried the full repeated structural unit, the runner-up, the gap, the chart's
> parts and the rounding coverage.

## What is not being cut

Concision is per-sentence compression, never requirement deletion. A compression pass that removes any of
these was the wrong pass:

- the shape's repeated structural unit, stated in full and in one sentence ("every district", "all nine
  cells", "one row per month with four measures");
- the decision furniture: the call, the runner-up where the shape has one, the gap, the flip condition, the
  hold where the evidence may not support a call;
- a chart's parts, named in one sentence (series, ordering, the marked threshold at its value, the
  annotation, what the title carries);
- every figure's unit, and every derived figure's rounding, stated once at the close;
- the fact the computation needs (the window, the cut-over, the stop rule, the grant rule).

## Where the words were, and the move that takes them out

| Where our prompts spent words | The move |
|---|---|
| The sentence that would not end: every element of a file as its own clause chained with "so", "which", "rather than", "because" | **One sentence with a list in it.** The file's contents arrive after a colon or a comma series: every column, every chart part, every row grain still named and gradable, the narration between them gone |
| A reason hung on every ask (one "because" per ask) | **Cut every reason.** A person asking for help does not justify each figure. At most one motive, on the one ask that genuinely needs it |
| A rounding tag on every figure ("to one decimal place" nine times) | **Rounding once at the close**, each rule tied to the figures it governs: "Return probabilities go in per cent to one decimal and projected returns as whole numbers" |
| The role, the organisation's business, the meeting, the sign-off, who reads the file | **Cut all of it** (rule 2). The forcing fact stays if the computation needs it, as a clause |
| The pack inventory ("everything my team works from is in the folder") | **Say nothing.** The pack is attached where the solver can see it |
| A specification voice ("X is the file, one row per Y, with columns A, B, C") | **Ask for it**: "put the count in X with the probabilities at 12, 24 and 36 months, the projected returns and the county totals" |

## The check after compressing

Compression is what silently drops an element of the repeated unit or a rounding rule, so after every pass:

1. **Walk the figure list.** Every graded figure still named, still carrying its unit, still covered by a
   rounding rule at the close (a count of discrete things in the shipped data is a whole number by nature
   and needs no rule; every derived figure needs one).
2. **Re-count the criteria off the shape's arithmetic**, worked on paper at design time. A compressed prompt
   that has fallen under 25 has failed, however well it reads.
3. **Run the gate.** `python3 .claude/skills/guide-to-prompt/references/voice-check.py taskNN` exits 0.

## What this does not license

Not a vague ask ("tell me what the data shows" is short and ungradable), not a dropped file name (it costs
three words and makes the deliverable gradable), not a dropped rounding rule on a derived figure (a Gate E
finding), not a fused call (the committed call stays one quotable sentence), and not a sentence reused from
the client's library or from this file.

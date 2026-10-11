---
name: determinism-check
description: "The determinism spec for every build. What must be filed literally (the estimand and every convention), what may stay open (the method, and only behind a filed criterion the data settles), the literal-reader test that decides whether a golden is forced, the closure moves, the generator assertions, the judge's gates and the judge rehearsal. Invoke while the ladder is designed, while the generator is written and on the finished build. The rehearsal thread is spawned only when the author asks or /build reaches stage 7."
---

# Determinism

> A build is deterministic when a reader who follows the shipped sentences word for word, and infers
> nothing the files do not say, lands on the golden. That is how the portal's judge reads. Our builds fail
> it for one reason in several costumes: the golden is right only under a reading the author supplies, in
> the write-up, the design note or "plain sense", and the shipped text, read literally, supports another.

## Why builds fail, counted

25 in-house judge reports over 14 builds (task117 to task445) plus the shipped ledger:

| Cause | Findings | Where it is fixed |
|---|---|---|
| A write-up figure that does not reproduce (an incidental figure, a figure on a bin edge, a count no filed definition forces) | 19 in 14 builds | §5 |
| The estimand not filed literally (population, window or inclusion left implicit) | 16 in 13 | §1 |
| A convention or threshold not pinned (rounding path, tie, as-of date, boundary) | 13 in 13 | §3 |
| The method left open with no filed criterion for choosing it | 9 in 9 | §1 |
| A filed rule whose literal reading gives another answer | 7 in 7 | §1 |

Two facts decide how the work is done. task445 came back DETERMINISTIC twice from our judge and failed the
portal (`answer_contradicts_files`, `golden_wrong`): its methodology defined ownership over "managers that
file" for the period, the literal reading counted only the reports on file, and nothing filed licensed
completing the rest. And eight builds were solved soon after a determinism repair added a pin, because
their stump had been living in the ambiguity the pin removed.

## 1. WHAT is filed literally, HOW may stay open

**WHAT: the estimand, filed so that its literal execution is the golden's quantity.** Population (name
its members in terms the data executes, and say outright whether members not yet observed at the as-of
date are in it), outcome, window, unit, comparison, inclusion and exclusion, threshold, rounding. Each is
fixed by the prompt's question or by one filed sentence at authority (a governing standard, policy or
contract), stated once. Never leave a part of the estimand for the solver to infer, and never word it so
that its literal reading is the easy answer.

**HOW: the method may stay open only behind a filed selection criterion.** If the decisive step is the
choice of method, file the criterion that selects it in general terms, never the method itself: "the
basis that, applied at the same point in the last closed period, comes closest to that period's final
figure on every unit (closeness: the largest miss)", "only measures that held steady across the closed
cohorts", "the standard's general method for this estimate". Then build the data so every reasonable
candidate is separated under that criterion with margin, and assert it. With no filed criterion, two
defensible methods survive and the judge fails the build (`underspecified_objective`). With the method
itself filed, the decisive step is rule application and the stump is gone.

**Never file a procedure, basis or formula whose literal application gives an answer other than the
golden.** It is an official decoy (banned on the card) and a determinism fork at once.

**The stump lives in HOW, never in WHAT.** If filing the estimand literally makes the call easy, the stump
was a fork. Redesign the decisive step (`stumping`, the ladder) so that the easy METHOD fails on a
precisely stated estimand. Do not keep the estimand vague to keep the stump.

## 2. The literal-reader test

Run it on paper before any data is cut, and again on the finished pack. Write the result into the design
note as the `Literal reader` line.

1. Execute the prompt and every filed definition and rule word for word. Infer nothing the text does not
   state. Where the text is silent on a choice, list every option and compute each.
2. The build passes only if every literal reading gives the golden, or each reading that differs
   violates a sentence you can quote from a shipped file, or the records are built so the readings
   converge (C1, asserted on the figure and on the row and entity counts).
3. The easy answer must come from an easy method applied to the same literal estimand, never from a
   different reading of the text.
4. Every step of the write-up passes the same test. A step that needs an inference no file states is an
   open fork, however obvious it feels.

## 3. Close every convention

- **Walk the 22 axes** (`references/forcing-the-answer.md` Part 1) and write one line per axis in the
  design note: the reading chosen and the move that closed it. An axis that cannot move the answer today
  still gets its line, because it becomes load-bearing when another parameter moves.
- **The closure moves, strongest first.** C1 converge: build the records so every reading selects the same
  rows. C2 confirm: a filed criterion is shown, on closed data, to select one candidate (family size, N of
  N, every rival's worst miss); C2 never recovers a rule nobody filed. C3 corridor: the parameter is
  unrecoverable and the answer is identical across its whole admissible range. C4 separate: every cell of
  the fork grid computed and mapped to the shipped sentence it violates, the nearest wrong cell at least
  6 per cent away. Details and worked cases: `references/forcing-the-answer.md` Part 2.
- **Pin at authority, once.** The prompt states the question and carries no convention. Below it,
  authority runs: a governing standard or policy, a contract or schedule, a decision memo, a data
  dictionary (field semantics only), method notes on an export, informal notes. A pin must sit at or
  above every sentence that could argue the other way (`references/forcing-the-answer.md` Part 6.1). Sweep the
  pack for sentences quotable against the answer (the constraint's nouns, and words such as defensible,
  added, raised, increased near them) and qualify or remove them.
- **Bins.** Every graded figure sits mid-bin on a non-round value, with its flip condition stated as a
  number. Never grade the count of an iteration, a median of an even-sized set, or a percentage near a
  one-decimal edge where a count would do.
- **No decision metric in the prompt's own voice** that a filed policy contradicts; demote it to an
  attributed claim.
- **No artifact ranks the candidates on the decision question and gets it wrong**, except a declared
  wrong-basis distractor (`dataset-generation` §8.3) that a shipped fact rules out and that is never the
  stump.

## 4. Assert in the generator, verify independently

Assert in the generator, and recompute in an independent verifier that reads only the shipped bundle:

- the literal reading's answer equals the golden, or the readings' asserted convergence;
- every C1 convergence (the figure and the row and entity counts), every C2 candidate's error and the
  winner's margin under the filed criterion, the C3 corridor, every C4 cell with its violated sentence;
- every graded figure's distance to its bin edge;
- the clean-data test, once per suspect file (repair it in the generator: the answer and the naive
  answer are unchanged and still differ), and the lens-swap test (the naive read and the answer are not
  the same population at the same moment under two lenses);
- the input gates (10 or more files, 3 or more formats, a file of 25,000 or more rows or a large
  database, two or more distractors named in `metadata.json`, 1 to 3 deliverables, unit and rounding in
  every ask) and two consecutive builds byte-identical.

Compute forward: build the data, then compute every figure from it. Where a rung turns on two axes
disagreeing (date against period label, row against entity), build the disagreement per candidate, since
independent draws make it inert.

## 5. The write-up

Every figure in `submission.md` is a claim the judge recomputes. State the answers the rubric owes and a
reproducible path, nothing more: no incidental figure, no count unless a filed definition forces it, no
sentence saying two readings agree unless the generator asserts it. Blocks and wording:
`submission-writeup`.

## 6. The gates, in the judge's order

| Gate | The question | Fails as |
|---|---|---|
| H | Does the task do its domain's own analysis (the swap test breaks it), are both layers there, and would a strong analyst who read every field and rule correctly still get it wrong the easy way? | SEND_BACK |
| G | Does the difficulty survive deleting every wrong number from the pack, and is it not a lens swap? | SEND_BACK |
| A | Does every figure recompute from the shipped files alone, at the file's own grain? | `solution_incorrect` |
| B | Is every decisive fact in a shipped file, and does every distinctive term in the recommendation occur in some input? | `missing_input_data`, `answer_contradicts_files` |
| C | Does any answer flip under a definition, threshold, scope, window or rounding path the pack leaves open? The literal reading first. | `underspecified_objective` |
| D | Would rigorous solvers disagree because they read a term differently rather than analysed differently? | `semantic_fork` |
| E | Is the decision pinned, every ask single and precise? | `prompt_ambiguity` |
| F | Can the stump sentence be written, and do the asks hold both top responses near a fifth of the ask weight? | too easy |

The judge's own text: `guidelines/determinism_judge_system_prompt.md`.

## Running the judge rehearsal

- **Licence.** The author asks in their own words, or `/build` reaches stage 7. Nothing else.
- **One isolated thread** (model and effort per `build-pipeline`, Models and effort). It sees a fresh
  unzip of `target.zip`, the prompt, the submission's graded blocks inlined, and
  `guidelines/determinism_judge_system_prompt.md` inlined verbatim. It never sees the design note,
  `pipeline.json`, the solver rounds, the stump sentence, an earlier report or anything its orchestrator
  has read.
- **The thread runs the literal reading first** (§2), then the gates, and counts a fork closed only by
  inference or by the write-up as open.
- **Spawning.** The `determinism-judge` agent orchestrates and spawns the thread. Where it cannot spawn
  (no `Agent` tool in the runtime), it writes the spawn brief beside a fresh unzip and returns its path,
  and the main session spawns the thread from that brief under the same contract. An orchestrator that
  has read anything beyond the bundle never judges in its own thread.
- **After it returns.** Relay the verdict, the disposition, the Gate G line and the Gate H line. FIX_NOW
  is fixed and re-judged once; SEND_BACK re-roots or retires (`build-pipeline`).
- **Our judge is the floor, not the bar.** The portal reads more strictly. A fork our thread settles "by
  the plain reading" or "as the natural intent" is a FIX_NOW, not a pass.

## Checklist

- [ ] Estimand filed literally: population (unobserved members stated), outcome, window, unit, comparison, inclusion, threshold, rounding
- [ ] Method either filed (and then not the stump) or open behind a filed selection criterion the data settles with margin, asserted
- [ ] No filed rule, basis or formula whose literal reading gives another answer
- [ ] `Literal reader` line in the design note; every literal reading gives the golden, violates a quotable sentence, or converges (asserted)
- [ ] 22 axes walked, one closure move each; pins at authority, counter-pin sweep clean
- [ ] Every graded figure mid-bin, flip condition stated; nothing graded on an edge
- [ ] Generator assertions and the independent verifier green; two builds byte-identical; input gates met
- [ ] Write-up states only owed figures, each recomputed from `target/`
- [ ] Judge rehearsal isolated, literal reading first; FIX_NOW fixed and re-judged once

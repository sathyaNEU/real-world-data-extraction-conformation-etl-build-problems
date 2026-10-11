---
name: stumping
description: Design and harden the main recommendation's difficulty for a Project Mark build. Methodology first: find the analytical pitfall the dataset itself produces (the three rules, the two layers, the four gaps), write the default competent path and show it ends on the wrong answer, screen every rung for readability against the measured opponent, rule out every semantic fork on the main call, build the ladder and its arithmetic, and argue the stump on paper in a design note that precut.py gates before any data is cut. Carries the draw protocol, the organs a strategy may need (a pin, a confirming corpus, distractors, voices), the diagnosis table and the hardening and stopping rules. Use when authoring a Main Recommendation Ask, hardening one a solver landed, or re-rooting a spent architecture. Determinism is determinism-check's; the asks are supplemental-stumping's; the prompt is guide-to-prompt's; the pack is dataset-generation's.
---

# Stumping

> A stump is the analytical step a competent analyst does not take because the default competent path
> looks finished without it. Every figure in the pack is correct, every rule the organisation would
> have in writing is filed, the solver reads all of it, builds the natural pipeline, reconciles it,
> and commits to a specific wrong answer. Nothing in the pack is broken and nothing is hidden. The
> difficulty is a question the solver never thinks to ask, and the design note has to name that
> question, the wrong answer the default path files, and why the opponent in Part 0 cannot read it.

**Navigation.** Part 0 the goal and the opponent · Part 1 find the pitfall · Part 2 make it survive
(the readability screen, the semantic fork table, the deletion tests) · Part 3 the ladder and its
arithmetic · Part 4 force one answer · Part 5 argue it on paper (the design note and `precut.py`) ·
Part 6 the draw · Part 7 the organs · Part 8 diagnosis and repair · Part 9 what is dead

**Prerequisites.** The domain, task type and objective are fixed via `guide-to-prompt` and the prompt
shape is picked there. `determinism-check` binds every ladder (its §1 and §2 are read before the
decisive step is chosen). `supplemental-stumping` designs the asks after the ladder is fixed, and
`dataset-generation` cuts nothing until `precut.py` passes.

**The references, and how each is used.**

| File | What it is | How a build uses it |
|---|---|---|
| `references/client/two-layer-task-design.md` | the client's standard: the three rules, the two layers, the pre-ship check | the test every design is answered against, in writing |
| `references/client/layer2-rigor-patterns.md` | 300 rigor patterns by domain and task type (pitfall, tempting shortcut, what pins it) | pick the task type's patterns, choose the one this data's structure invites, write your own version; the card records `layer2_pattern` and the guard blocks the same pattern on the same data structure |
| `references/traps/_measured.md` | the 26 habits the client's model actually failed on, counted over 64 accepted tasks | evidence of which analytical habits fail; never an architecture to copy. The top four share the withheld-rule architecture, which is banned |
| `references/proven-in-production.md` | what measured builds taught: the laws, the deaths, the per-build index of measured architectures | read Part 1 (laws) and Part 4 (what is dead) before the draw; a shape in Part 4 is not drawn |
| `references/shipped-ledger.md` | one row per portal result | which strategies and pairings are spent, and what each result taught |
| `../guide-to-prompt/references/exemplars/` | the client's own measured tasks | the depth and the voice the client pays for; their withheld-method architecture is capped, so take the depth, never the structure |
| `analytical_tasks/` | 300 seed notes, all written to the withheld-rule-with-decoy architecture | a seed supplies a world, a decision and a quantity. Its mechanism is discarded: the rule it withholds is filed, its decoy is cut, and the pitfall is re-found from the data under Part 1. A seed used as a build plan is a planted-rule build and the guard blocks it |

The portal is the only stump oracle. The solver round (`solver-round`) filters what reaches it, and the
determinism judge (`determinism-check`) recomputes the golden. Neither replaces this skill's paper work,
which is where every repair the record counts could have been avoided.

---

## Part 0. The goal and the opponent

**The pass bar.** The top two responses average under 50 per cent against the generated rubric and at
least one response is genuinely stumped. **Build to 40**, because the on-platform verifiers are inexact
and the task is regraded more accurately after submission. The rubric puts 30 to 40 per cent on the
recommendation and its critical components, 5 to 10 on instruction following and about 55 to 60 on the
asks. A response that lands the main call banks about 45 before it answers an ask, so **two responses
on the call anywhere in the field take both top slots and the build fails**: the ladder has to keep every
response but one off the call, and the asks have to hold both top responses to about a fifth of the ask
weight each (`supplemental-stumping` Part 0).

Three ways a build fails, and they pull against each other:

| Failure | The judge's name | Cause |
|---|---|---|
| The solver lands the call | too easy, Gate F | the decisive step is readable (Part 2), or the default path is already the golden (Part 1.5) |
| Rigorous solvers disagree | not deterministic, Gates A to E | an unpinned convention, a semantic fork on the main ask, a thin margin over real uncertainty |
| The difficulty is the wrong kind | Gate G or H | the task exists to catch a wrong reported number, a planted defect, a field reading or a rule to apply |

### The opponent, measured

The record (79 in-house rounds, 21 portal results since task99) converges on one solver. Design against it.

1. **It reads every document and executes every clause.** A filed sentence that names the decisive
   quantity is a work order (12 of the 36 landed in-house rounds in the last window, cause 1a of the
   diagnosis record).
2. **It sees the schema.** A column, key or marker that makes the move a row predicate, or a join found
   by inspection, is one line of code (6 landings).
3. **It corrects by reflex.** Hold the pool to every visible attribute, re-screen the residual, decompose
   the pilot, build the analog, add the control, reweight, shrink. A pitfall whose fix is one of these is
   spent before it is built (10 landings: task228 rounds 3 and 4, task230 rounds 1 and 2, task180 x4).
4. **It reconciles and back-tests everything it can.** Control totals, closed corpora and published
   figures are search benches: a corpus that scores the rival rules nominates the survivor (task120,
   task125).
5. **It runs the hygiene battery.** Key uniqueness, exact duplicates, unmatched joins, fan-out, counts
   that tie. Anything the battery surfaces is found, and the filed rule then says what to do (task73 v2,
   task117).
6. **It runs the event study unprompted**, so a dated cause with a step in a series is solved by alignment.
7. **It does the default construction well.** Kaplan-Meier censored at the data cut, a cohort survival
   curve, the textbook conditional probability. If the default construction is the golden, it lands in
   minutes (task134 loop 0 round 1, 33 navigators and 7,441 returns in four minutes).

What it does not do: ask what one row is when the file's grain looks natural; ask what population the
decision funds when the file's population is complete; ask whether a quantity is generated by a process
the window never saw; ask which method the stated criterion selects when the obvious one fits the closed
record. Difficulty lives there, and only there.

**Solver strength.** The portal's strongest model takes a reading our in-house solver declines: task133
v1 passed two in-house rounds because both solvers refused the survival-conditioned reading "because the
policy does not spell it out", and a portal model took it and scored 100. The in-house round therefore
runs at the highest effort the pipeline sets (`build-pipeline`, Models and effort), and a step the design
note defends with "a solver would not think to" is screened in Part 2, not assumed.

---

## Part 1. Find the pitfall

### 1.1 The litmus and the three rules, in writing first

> **Is the reported number or conclusion the task overturns actually wrong, and is catching that the
> main thing that defeats the model?** Yes to both is banned at any depth. The reported figures stay
> correct and the difficulty lives elsewhere.

Then the client's three rules, each answered in one sentence in the design note and on the card:

1. **The task really uses its domain.** The quantity that decides the call is one the field would
   estimate, model or test. Swap the nouns into another field; if the task reads the same, the domain
   is a backdrop. The card's `domain_test` names the field's method and why the swap breaks the task.
2. **Two layers.** Layer 1 is realistic mess a real system produces; Layer 2 is the analytical pitfall.
   The stump is always Layer 2.
3. **Banned as the decisive step**: a planted defect, decoy or hidden rule; data semantics (the answer
   flips on reading a field, code, unit or definition); rule application (the answer comes from applying
   stated rules, however many). **The analyst test**, written as the card's `analyst_test`: could a
   strong analyst who cleaned the data and read every field and rule correctly still get the answer
   wrong by doing the analysis the easy way? Name the easy route and the wrong answer it gives. If no,
   redesign, never harden. Choosing the right estimand or unit of analysis counts as analysis.

The card's `stump_class` takes only `analytical` on a new draw; `guard.py check` blocks the rest.

### 1.2 The stump lives in HOW, never in WHAT

The estimand (population, outcome, window, unit, comparison) is filed so that its literal execution is
the golden's quantity (`determinism-check` §1). The method may stay open only when something forces it:
the design and the data's structure (preferred), a standard's general method, or a filed selection
criterion (a counted organ, never in consecutive builds). So the stump is never a reading of a term: if filing the estimand literally makes the
call easy, there was no stump, only a fork, and the decisive step is redesigned.

### 1.3 Couple the pitfall to the domain, from the libraries

The decisive step is the field's own method for the quantity that decides the call, the one an expert
applies and a capable generalist replaces with a generic move. Before the stump sentence is written, read:
the task type's patterns in `references/client/layer2-rigor-patterns.md`; the two or three exemplars
nearest the domain; `references/traps/_measured.md` for the habits that fail; and
`references/proven-in-production.md` Part 1 and Part 4. The design note carries one line per source read:
what it teaches and how this build differs. Learning is the point and copying is a guard block.

### 1.4 The four gaps, and the patterns with a measured record

A pack full of correct numbers leaves four gaps open. Pick the gap, then the mechanism, then the scenario.

| Gap | The question that opens it | Gate G labels |
|---|---|---|
| 1 Time | what is the shipped evidence a statement about, and what is the decision a bet on? | `forecasting` |
| 2 Population | what is one row, and what is one unit of the thing being decided? | `method_or_model_selection`, `decomposition_attribution` |
| 3 Objective | what is the decision scored on, and does the reported metric answer that question? | `binding_constraint`, `decomposition_attribution` |
| 4 Rule | which method does the filed criterion select, when the obvious one fits the closed record? | `method_or_model_selection` |

Gap 3 degrades into the banned shape when the task reads "their metric misleads, catch it"; it passes
when their metric is correct and the constraint they never checked disqualifies their pick, built as a
removal that re-places nobody (task58 v3 and v4 died on a re-placing constraint). Gap 4 is legal only as
a filed criterion the data settles (`determinism-check` C2 confirms; it never recovers a rule nobody
filed). A rule withheld to be recovered from settled cases is the banned architecture and the guard
blocks the card.

Patterns are where difficulty can live, not a stump by themselves; each has been solved with its label
intact when the discriminator underneath it was missing:

| Pattern | Gap | Fires only when | Measured death |
|---|---|---|---|
| A past exceedance against forward yield | 1 | the resolving candidates resolve for an ordinary reason the series shows, and the horizon is pinned by a filed logistics fact | a past ranking shipped as if it answered the decision (Gate G) |
| C serviceable share behind a join | 3 into 2 | the share is an estimate the analyst builds, absolute rather than graded, and the winner's edge clears the decoy's carried advantage (Part 3) | the share a column states, or a stated eligibility rule (rule application) |
| D two grains, both flawless | 2 | the grains differ in shape, not level, the decision grain is pinned by what the decision funds, and no key column bridges them in one group-by | task44, an order id that turned the bridge into a group-by |
| E conditioned yield | 2 | the split is absolute, confounders are controlled by construction, and the conditioning property is not a column name | task43, a stronger moderator manufactured by an uneven assignment rate |
| B the rule recovered from a closed corpus | 4 | never as the decisive step | the banned architecture |

### 1.5 Write the default path first

**Before the stump sentence, write the default path step by step**: the pipeline a competent analyst
builds without thinking, from the prompt's words and the files' grain, each step naming the files, the
joins, the filter and the construction, ending on a named figure or candidate. Then check: **does it end
on the golden?** If it does, there is no stump, whatever the design note planned.

The record pays for this twice in one window. task134 loop 0: the design assumed a solver "censors
removals and deaths along with the data cut", an over-correction off the default path; the default path
(Kaplan-Meier censored only at the cut, deaths as non-returners, the detainer log never opened) was the
golden, and the round landed it in four minutes. task130 v3: the analog construction the design treated
as the insight was the default, and the round landed at proxy 100. The older record is the same shape:
task62 s.29 and task87 v6b (confirm draws whose natural route lands the unadjusted figure), task100 v1
(every response found the four). **A rung that only bites a solver who chooses an extra correction is not
a rung.** The stump has to sit on the default path, where the default construction is wrong.

### 1.6 The stump sentence

One sentence: **the wrong committed answer the default path files, and the step that lands it there.**
It names the figure or candidate the default path in 1.5 ends on, and that figure differs from the
golden. No sentence, no stump, no build. `precut.py` refuses a note whose default path ends on the golden
or whose stump sentence does not name the default path's answer.

### 1.7 The data-native sentence

One line: *what about this dataset makes this the stump a real analyst would trip on here* (its
generating process, grain, calendar, censoring, selection, identity or capacity structure). A decisive
move that would read the same on any other dataset has no data-native sentence and is not built.

---

## Part 2. Make it survive the opponent

### 2.1 The readability screen, per rung, before any data is cut

Every rung, and above all the decisive one, is run through six tests on paper. A rung is **readable**
when any test fires, and a readable decisive rung is dead: it is the cause of 36 of the 79 in-house rounds
and 13 of the 21 portal results on record.

| Test | The rung is readable when | Record |
|---|---|---|
| 1 filed sentence | a shipped clause, definition or formula names the decisive quantity, so executing it is the rung | 12 landings (task117 L2, 119, 122, 123 x4, 124, 229, 228, 446) |
| 2 schema | a column, key or marker makes the move a row predicate, or a join a solver finds by inspecting headers | 6 landings (task117 L1, 119 L2, 121 x2, 124, 128) |
| 3 reflex correction | the move is one of the opponent's defaults: hold the pool to every visible attribute, re-screen the residual, decompose, build the analog, add a control, reweight, shrink | 10 landings (task230 x2, 228 x2, 180 x4, 181, 130 v3) |
| 4 control bench | a control total, published figure or closed corpus scores the candidate rules and nominates the survivor, or refutes the naive read | task120, task125 |
| 5 hygiene battery | key uniqueness, duplicates, unmatched joins, fan-out or a count that does not tie surfaces the rung | task117 L3, task73 v2 |
| 6 linear arithmetic | the decisive quantity is one subtraction, one ratio or a half of a reported figure | task125 x2 |

A rung passes the screen as **silent** when none of the six fires: its quantity is named by no sentence
and no column, it is not a reflex, no control can see it, the battery comes back clean on the wrong path,
and it is not linear in anything reported. The design note carries the screen as a table, one row per
rung, with the verdict in the last cell; the decisive rung's row reads `silent` or stage 3 does not open.

**Two shapes have held against this opponent.** A quantity the solver believes needs no construction
(a date read with `.year` when the period opens on 1 August, the corpus reconciling identically under
both readings, task60 v4). And the maturity attack: the graded object crystallises after the extract,
closed periods tie under the naive basis because they are fully developed, the tail is computable from an
operational registry the natural pipeline never joins, and no as-of dates ship (task73 world seven).

### 2.2 No semantic fork on the main recommendation

A term read two ways is a fork (Gate C or D) and data semantics (rule 3) at once, and it was built or
defended as a stump six times in one window: task134's "booked again" against the guidance's "return"
(35 against 33 navigators), task133's PD reading (declined in-house, taken by a portal model at 100),
task127's capped installs in time, task128's "hosts it reaches", task131's unrounded thousands, task119's
code. **The semantic fork table** closes it at design time:

| Id | Term or convention in the main ask or the main computation | Golden reading | Alternative reading | Call under the alternative | Ruled out by |
|---|---|---|---|---|---|
| SF1 | ... | ... | ... | ... | a quoted sentence of the prompt or a named shipped document, or `same call` |

One row per term in the main ask (every noun, every unit, every period word) and per convention the main
computation depends on (as-of date, inclusion, grain, rounding path, tie-break). Every alternative is
ruled out by a cited sentence or shown to land on the same call, and **the stump is never one of the
readings**: if the design's wrong answer is the alternative reading of a term, that is the fork, not the
stump. `checks.py` asserts every row (the alternative reading computed and either equal to the golden or
refused by the cited text) and `precut.py` refuses a note with an empty `Ruled out by` cell.

### 2.3 The deletion tests

Run them on every candidate decisive step, in this order; each kills in one line.

1. **Delete every wrong number and misleading claim from the pack. Is it still hard?** If not, the
   build is a surface-read rejection.
2. **The clean-data test.** Repair every suspect file in the generator (fill the gap, correct the
   semantics, replace the instrument with one that observes the decision's own quantity). Assert
   `answer(repaired) == answer(shipped)`, `naive(repaired) == naive(shipped)`, `answer != naive`
   (`determinism-check` §4). A build that cannot pass all three has its difficulty in the defect.
3. **The lens-swap test.** The naive read and the answer are not the same population at the same
   moment under two lenses. If they are, the mechanism is `single_conceptual_flip`, banned on clean data.
4. **The identity test.** Write the decision's governing arithmetic as an identity. If it closes over
   quantities the pack must ship, every construction feeding it is readable or a lens swap; change the
   graded quantity, never the construction (task73 world six, task36).
5. **The corpus-direction test.** State in one sentence what every control total, published figure and
   closed corpus returns under the naive path. Only a device that nets at the control's grain leaves the
   control reproducing the naive read; a device whose losses accumulate makes the control refute it, and
   a refutation is a search bench (task92 v2, task89 v5). Anything other than "it reproduces" disqualifies
   the device.
6. **The first-moves test.** Play the opponent's first moves on paper: the one-period group-by, the
   decomposition of any pilot, the natural operationalisation of each filed clause, the back-test over
   each corpus, the hygiene battery. If any lands on the answer, the build is dead there (task58 v2,
   task44 v2).

### 2.4 Oracles

List in the design note every control total, published figure, reconciliation column and closed corpus
the pack ships, with what each confirms on the wrong path. Anything that ties only under the golden
basis is an oracle (seven landings: task117, 118, 120, 122 x2, 123 x2, 128): it is cut, or built to tie
on every basis. The ask layer's one referee is the only sanctioned exception, and it arbitrates an ask,
never the call (`supplemental-stumping` Part 1).

---

## Part 3. The ladder

**The unit of design is a ladder of three to five rungs, four the working default.** Each rung is a
complete, defensible analysis a competent analyst would file; the solver climbs by refusing the rung
below. Two rungs: one correction defeats it. Six or more: machinery, and scatter reads as ambiguity.

```
RUNG 0   the default path's answer (Part 1.5)      -> candidate A
RUNG 1   the obvious correction                    -> candidate B
RUNG 2   the sophisticated correction              -> candidate C
RUNG 3   the decisive move, silent under Part 2.1  -> THE ANSWER
```

**Rung 0 is built by the solver, never shipped.** No artifact ranks the candidates on the decision
question and gets it wrong, at any depth; the one exception is a declared wrong-basis distractor
(`dataset-generation` §8.3) that a shipped fact rules out and that is never the stump. A dimension table
the naive pipeline needs is rung 0 wearing a file name (task42).

**Every rung**: reproduces exactly from the raw files (a wrong rung is dismissed as a data error and the
solver climbs free); names a different candidate or figure than every other rung; is killed by exactly
one shipped fact or one construction (two independent discoveries make the solver hedge, and hedging is
unfair, not hard); and is genuinely satisfying to stop at, with the sentence written down. An arithmetic
a competent engineer fixes in the loop it is writing is not a rung (task58 v5); a rung reached with one
group-by is not a rung (task36). Cleaning sits at rung 1 or 2, never last.

**Depth is a Gate F device, not a Gate G defence.** Depth makes a solver spend insight on the wrong
candidate; it never legalises a shape.

**The arithmetic, settled on paper before any row exists:**

- **Winner's position.** The answer ranks 4th or 5th on the default path, leads no intermediate rung,
  sits 2nd on at most one and there by at least 1.20x. No margin under 1.15x anywhere.
- **Margin on the correct basis.** Floor 1.2x over the runner-up, target 1.5x to 2x.
- **Discriminator dominance.** `edge(winner, decisive axis) >= 1.2 x advantage(decoy, carried axis)`,
  both ratios computed and the product asserted. This failure is silent: the rung computes perfectly and
  stops naming a different candidate (task36, a correction the leader survived by 2.3x).
- **Sign discipline, when the answer is a figure.** Every correction walks the figure one way and only
  the decisive move reverses it, per-rung percentages stated, so no partial application lands near the
  answer.
- **Grade a quantity the rungs can move.** A quantile absorbs a selection rung; a share cancels a rung
  that moves numerator and denominator together; totals, counts and levels carry rungs faithfully.
  Compute each rung's worth on the graded quantity itself, never on an intermediate.
- **Enumerate the grid, not the path.** With three independent corrections there are eight cells, each
  landing on a named wrong candidate or asserted outside the separation floor. For a figure, with `n`
  monotone corrections at factor `f` and one reversing decisive factor `g`, the binding cell is rung 0 at
  `1/(g f^n)`, so `g >= 1 / ((1 - floor) f^n)`: every rung below the decisive one makes the decisive
  move bigger. Partial-application cells (the rule applied to one source and not the other) are swept
  separately. Hazards (pipeline mistakes refuted by a shipped control) add path length, never a cell.
- **The rung-collision guard.** After every parameter change, recompute every rung's winner by name;
  two adjacent rungs with one winner means the ladder is a rung shorter than the note claims.
- **Every single-error cell files a feasible figure.** A wrong route that breaks the arithmetic
  self-discloses as an alarm rather than a wrong answer (task44).

**Mechanisms a rung can run on** (the card's `generators` vocabulary, `fingerprint/vocab.json`). Each is
the question the rung turns on; the scenario is drawn fresh every time.

| Code | The rung asks | Note from the record |
|---|---|---|
| G1 unit of value | what are we actually paid on or constrained by? | the natural metric leads by 5x to 20x and the correct unit flips the ranking |
| G2 grain | what is one unit of the thing being decided? | dead when a key column bridges the grains in one group-by (task44) |
| G3 record against operation | who actually did it? | never alone: alone it is a lone defect flip |
| G4 attribution at transition | who holds it now? | sub-period misattribution cannot carry an annual figure (task40) |
| G5 provision elsewhere | is the need already met outside this record? | the asymmetry by category is the whole trap |
| G6 composition | did the population change underneath the metric? | one band has to move against the others or standardisation never binds |
| G7 operating window | when can this physically happen? | pin the window in an operations file, never the prompt |
| G8 reachability | can we actually move it? | pattern C's form; binary reachability, never graded |
| G9 downstream survival | is the measured outcome the acquired outcome? | the survival class behind a join |
| G10 cross-dimensional duplication | what is one real-world unit? | never alone |
| G11 eligibility precondition | is the leader in the candidate set? | the predicate is a quantity, never a status word (task89) |
| G12 absence against record of absence | does a blank mean zero or nobody answered? | the rollup reconciles only when blanks stay blank |
| G13 horizon | which period does the decision cover? | the decision window differs from the pilot window (task44 v2) |
| G14 conditioned yield | does the pooled rate apply to this pool? | pattern E's form |
| G15 evidence-standard exclusion | can the rival's figure even be computed from what shipped? | a rival-killer, never the main rung; structural impossibility over contested statistics |
| G16 method selection | which method is this data entitled to support, under the filed criterion? | the client's most wanted family; a shrinkage choice carries about 8 per cent at most (task60) and an enumerable model class behind a shipped back-test is an answer key (task38) |
| G17 statistical rigor | does the difference survive its uncertainty? | supporting only, paired with one of the seven pass labels; assert the distance to the boundary |
| G18 resisted over-correction | is the reported figure actually wrong? | died every time (task38 v2, 40, 62 s.29, 87 v6b): the default path keeps the figure. Drawn only where the default path lands elsewhere |
| G19 contract conformance | does the output satisfy the spec? | depth only; conforming to a stated contract is rule application and never the top two rungs |

**Stack two to four mechanisms from different gaps**; the decisive rung's gap is not rung 1's gap.
Same-pattern stacking is one mechanism in a trench coat.

**Hold as the answer** is a determinate call (`signal_vs_noise_or_hold`): forced by a computed blocking
quantity that reproduces, every candidate failing for a named reason, the prompt licensing a non-pick on
the same footing as the candidates without advertising it, the default path still committing to a named
candidate, and the note stating what would have made it a pick. A hold justified by "the data is unclear"
is a hedge and fails.

---

## Part 4. Force one answer

Determinism has one home, `determinism-check`, and three of its rules shape the stump itself:

- **WHAT is filed literally; HOW stays open only when the design, a standard's general method or a filed
  selection criterion forces it** (§1). A filed method makes the step rule application; nothing forcing
  it leaves a fork. A filed back-test is a recognisable organ: not in consecutive builds.
- **The literal-reader test** (§2) runs on the ladder before data is cut: execute the prompt and every
  filed sentence word for word, list every option where the text is silent, and require that each literal
  reading gives the golden, violates a quotable sentence, or converges by construction. Its line goes in
  the design note.
- **No filed rule, basis or formula gives another answer when read literally.** That is an official decoy
  and a fork at once, and the guard blocks the card.

**A pin fixes the basis, never the answer.** Delete the clause and ask whether the answer is still
forced: if it is, the clause was handing over the insight (task57 v21, a half-sentence executed at 94 per
cent). A pin names the observable, never a file, field or join, and never the move; the readability
screen re-runs on every pin added, because six pins in one window turned a rung into a work order
(task118, 119, 123, 128, 228). **Close by convergence first** (C1: build the records so every reading
selects the same rows), by a filed fact only when it names the observable, never in the prompt.

**Every graded figure sits mid-bin on a non-round value** with its flip condition stated as a number;
round-value receipts tell a solver the intended method (task100). The 22 axes are walked and closed in
the design note's closure table (`determinism-check` §3), which `precut.py` requires before stage 3.

**The committed call is forward facing by default**: a quantity about a window that has not closed. A
retrospective ask is legal with its reason written in the design note; the objective tag never changes
because the window is open.

---

## Part 5. Argue it on paper: the design note and `precut.py`

Nothing is cut until the design note carries the sections below and `precut.py` passes. The gate is
mechanical and free; every repair in the diagnosis record except realism was a design decision that
could have been checked here.

```
python3 .claude/skills/stumping/precut.py taskNN          # exit 0 when stage 3 may open
```

The note is one file, `DESIGN_NOTE.md`, with these H2 headings (exact spelling, so the gate can read them):

| Heading | What it carries | What `precut.py` checks |
|---|---|---|
| `## Draw` | the card id, pairing, shape, strategy, the data-native sentence, one line per library source read | the card exists under `fingerprint/cards/` |
| `## Default path` | numbered steps of the competent default pipeline, then `Ends on:` the figure or candidate, and `Golden:` the golden | both lines present and different |
| `## Stump sentence` | one sentence: the default path's wrong answer and the step that lands it | present, and it names the `Ends on:` figure or candidate |
| `## Three rules` | `Domain test:`, `Analyst test:`, `Layer 1:`, `Layer 2:` lines | all four present |
| `## Readability screen` | a table, one row per rung, the six tests, the decisive rung marked `(decisive)`, the verdict in the last cell | every verdict `silent` or `readable`; the decisive rung `silent` |
| `## Semantic fork table` | the table of Part 2.2, ids `SF1`, `SF2`, ... | at least one row, no empty `Ruled out by`; when `generator/checks.py` exists, every id appears in it |
| `## Ladder` | rungs with winners, margins, the position table, dominance, the grid, per-rung worth | present |
| `## Closure table` | the 22 axes, one row each with the reading and the closure move | 22 rows numbered 1 to 22, no empty closure |
| `## Literal reader` | the `determinism-check` §2 line | present |
| `## Oracles` | every control, published figure and corpus with what it confirms on the wrong path, or `none` | present |
| `## Ask sheet` | the asks, their devices and spans, the cracker sheet, `Pair ceiling:` a number | pair ceiling at or under 40; every cracker-sheet row misses |
| `## Tried and rejected` | append-only, one line per dead approach | present |

`precut.py` also runs the prompt gate (`guide-to-prompt/references/voice-check.py`) on `prompt.txt`.
A FAIL anywhere exits 1 with the failing rows listed; stage 3 of `build-pipeline` does not open past
exit 1, and a hardening loop re-runs it before the rebuild because a hardening moves the default path,
the screen and the closure table.

Three working rules. **One note per build**, no `DESIGN_V2`, no snapshots: the generator rebuilds the
pack. **A dead approach is written into `## Tried and rejected` the moment it dies**, with the reason.
**The stopping rule is written before the first portal test**: what result files the build as at ceiling,
and what licenses one more repair.

---

## Part 6. The draw

A trap recognisable from its shape has already lost, and a reviewer who matches a build to a delivered
one by domain, role and artifact has found a clone. The draw comes first, as a fingerprint card.

1. `guard.py recent` and `guard.py coverage` (`../fingerprint/SKILL.md`): what the last builds spent and
   what has never been drawn.
2. Draw each dimension independently: gap, pattern or generator, domain and subdomain, objective (assigned
   against the graded quantity's tense, never retagged for a forward window), shape, decision type,
   answer unit, role family, forum, forcing event, organisation family, calibration form (or none),
   context-artifact type, stump strategy from the dataset's own structure, people with
   `guard.py names --geo <geography> --seed <task>`.
3. Run `corr(decisive measure, unit size)` at the decision grain before committing to a world; a world
   where the two track each other cannot hold a ladder (task57, +0.98 in the dead world).
4. `guard.py check` on the card: clear every BLOCK, answer every WARN in the design note, then
   `guard.py register` **before the ladder is written**, so a build in flight is visible to the next
   one. The standing bans (pairing, pattern, strategy, calibration form, role, artifact, spine, shape,
   forum, forcing event, organisation family, people) reach the last three builds; the same-puzzle test
   the last twelve; the driver sentence every driver on file.
5. Nothing drawn appears in `references/proven-in-production.md` Part 4, and the discriminator the drawn
   pattern needs (Part 1.4) can be built in this world.

The card records identity only; the outcome goes in the shipped ledger when the portal reports.

---

## Part 7. The organs, only where the strategy needs them

**The pin.** One sentence, in one shipped document at authority, stated as a filed fact, never
justified, never repeated, never in the prompt. It fixes the basis and names the observable (Part 4).

**The confirming corpus.** A closed record ships only when the strategy needs one (a forecast chosen by
honest back-test, a filed criterion shown to select one method), and then C2's rules bind
(`determinism-check/references/forcing-the-answer.md` Part 2): the whole candidate family run, zero
tolerance, one survivor, blind to the decisive move for a stated structural reason, rerunnable from the
bundle. It confirms a filed criterion; it never recovers a rule nobody filed, and it never refutes the
naive read (Part 2.3, test 5). Every calibration outcome has the records that reproduce it, or it is a
fabricated intermediate. Where a lookup shortcut would transfer a rate, a twin pair (two cases identical
on every visible column, outcomes about 2x apart, reproduced by the correct rule and no rival) kills it.

**The distractors.** Two or more files the solution never reads that look relevant enough to weigh, named
in `metadata.json` and nowhere in the pack. A wrong-basis distractor (correct arithmetic on a basis a
shipped fact rules out) is the one licensed wrong answer in the pack, and never the stump
(`dataset-generation` §8.3).

**Voices.** Optional, and never a roll call. At most two named people holding beliefs, never quoting a
ranking or endorsing a quantity to carry forward. No licensed wrong basis: a rival method arrives as the
shortcut a capable analyst reaches for, never as a document filed to be refuted.

**Context artifacts** report what happened, labelled in-file for the question they answer, and never
rank the candidates on the decision.

No organ ships out of habit. A corpus, a twin pair, a control set or a voice shipped because earlier builds
shipped one is the habit the client reads as a template.

---

## Part 8. Diagnosis and repair

A diagnosis arrives from a solver round's path, the judge's report or a portal result, never from a solve
in the main thread. Read the trace for route and for assumptions: the step the solver never performed is
the finding, and an assumption every solver holds without checking is where the physics of the scenario
can be changed. Diff the solver's figures against the golden cell by cell before diagnosing.

| Symptom | Diagnosis | Direction |
|---|---|---|
| The solver lands the call in minutes with the default construction | the default path was the golden (Part 1.5) | redesign the decisive step so the default construction is wrong; a rung below rung 0 from a different gap, never a rung above |
| The path executes the decisive step as a work order | readable rung: a filed sentence, a column or a reflex (Part 2.1) | re-run the screen; move the quantity off every sentence and column; if the only silent form is a plant, the architecture is spent |
| The path names the quantity and argues it away | the pin is weak or the criterion is not filed | file the selection criterion (Part 4), never the method |
| The solver reaches every insight and lands elsewhere, defended from a file | a fork, not difficulty | `determinism-check` §2 and §3; close by convergence first |
| Two readings of a term in the main ask give two calls | a semantic fork (Part 2.2) | add the row, cite the sentence that rules the alternative out or build the records so both land on the call |
| The final rung computes and never changes the ranking | discriminator dominance failed | widen the edge or shrink the carried advantage; documentation cannot fix arithmetic |
| Two adjacent rungs name one candidate | rung collision | recompute every winner after each parameter change |
| A corpus or control is quoted back as the evidence for the rung | the control was a search bench (Part 2.3 test 5) | make it tie under every basis, or cut it |
| Wrong answers converge on a candidate nobody designed | a second self-consistent reading | re-solve from the rival's premise, close it in the data |
| A response misses the call and still scores well | the asks are free (`supplemental-stumping`) | the ask gate (`grade.py` ASKS LEAK); rebuild the asks against the cracker sheet |
| The name comes back right and the figures wrong, result after result | an over-determined name | re-root the ask so the name is not the graded call |
| The trace's whole reasoning is "the reported figure looks wrong" | Gate G | rebuild, never harden |

**Hardening escalation**, in order: a rung from a different gap below the current decisive one; the
discriminator behind a join; the pin's evidence split across two documents; the winner's rank worse on
the default path; a conditioned yield; the confirming corpus tightened. **Never harden by** adding noise,
removing evidence, inventing a threshold, making files harder to parse, shipping a wrong-answer artifact,
or deleting a signpost that also carried a parameter (the next round splits on the figure).

**Stopping rules, written before the first portal test.** Two consecutive exact solves by different
correct routes is the signature of a computation, and the move left is re-rooting the ask. Two
consecutive determinism repairs that each turned the rung they touched into a reading mean the
difficulty is re-rooted. After repeated solves, change the decision, not the mechanism.

**The repair loop.** Every repair after a round runs in a fresh agent from the committed state
(`build-pipeline`, Running the stages): the round's log, `pipeline.json` and the design note with
`## Tried and rejected` read first. One mechanism per iteration, both halves of every patch (a rule and
the records that reproduce it), the dead end written the moment it dies. A returned shipped task is
repaired on the fast path (`build-pipeline`, Returned tasks): design, build, commit, ship, with the free
mechanical gates only.

---

## Part 9. What is dead

`references/proven-in-production.md` Part 4 carries every measured death with its build. The shapes
not to draw, in one line each: a committed figure that is the output of a filed formula; a recovered
rule that is one scannable parameter; a device announced by its own columns; a device whose only
defence is silence in a pack that names it; an argmax under a stated rule over a filed candidate list;
the correct basis being the natural basis; a figure computed to see which side of a line it falls; a
decisive cause with a cutover date; a world additive over rows once its map ships; a forward window
whose every input is filed; a decisive step that is the last link of the obvious chain; a graded
quantity that is what a counterparty will invoice under published terms; an eligibility gate on a
status word; a corpus built to refute the naive read; a forward population named by a filed clause; a
default construction that is the golden.

**Anti-patterns**, each a measured rejection: a shipped artifact that computes a wrong answer to the
decision; depth as a Gate G defence; a lens swap on honest data; a prompt clause that fixes a basis,
window or convention; a corpus whose resemblance nominates the winner; a calibration outcome nothing
reproduces; a rival-killer that does not recompute; a load-bearing fact stated in three files; a
number authored and data reverse-engineered toward it; hedge-friendly framing; a hold nobody can
overturn; a decision needing a real-world standard not shipped; a knife-edge margin; a stump that is a
reading of a term; a stump sentence that names an over-correction instead of the default path's answer.

## Checklist (the pre-cut gate, mirrored by `precut.py`)

- [ ] Litmus and the three rules answered in writing; `stump_class` analytical; `analyst_test` and `domain_test` on the card
- [ ] Default path written step by step and it ends on a wrong answer; the stump sentence names that answer and the step
- [ ] Data-native sentence written; one line per library source read; two layers named
- [ ] Readability screen: every rung a row, the decisive rung `silent` on all six tests
- [ ] Semantic fork table: every term and convention of the main ask, every alternative ruled out or convergent, the stump none of the readings, every row asserted in `checks.py`
- [ ] Deletion tests: wrong numbers deleted and still hard; clean-data and lens-swap asserted; the identity does not close over shipped quantities; every control reproduces the naive read; the first moves do not land
- [ ] Oracles listed, none ties only under the golden
- [ ] Ladder: three to five rungs, each a different candidate, position table, dominance, grid and partial cells, per-rung worth on the graded quantity, winners by name re-asserted after the last change
- [ ] Estimand filed literally, method open only behind a filed criterion, no filed rule reading to another answer, pins name observables, every graded figure mid-bin, 22 axes closed, literal-reader line written
- [ ] Card drawn, checked and registered before the ladder; nothing drawn is in Part 4 of the production record
- [ ] Organs only where the strategy needs them; two distractors named in `metadata.json`; no roll call
- [ ] Stopping rule written; `## Tried and rejected` present; `precut.py taskNN` exits 0

---
name: stumping
description: Design, build and harden the trap architecture for a deterministic analytical task under determinism judge v3 and the pass bar, the top two responses averaging under 50 per cent with at least one model genuinely stumped, and a build target of 40, which leaves room for at most one response in the field to land the main call. Carries the capability model of the solver being designed against, the litmus that decides whether a build is even legal, the four gaps where difficulty can live when every number in the pack is correct, the five patterns with the best approval record, the properties a decisive move needs to survive, the refusal ladder whose rungs are analyses the solver constructs rather than artifacts the pack reports, the organs (the pin, the calibration corpus, the advocate structure), the determinism machinery, the prose prompt contract of one to three deliverables with uncapped multi-dimensional asks carrying about 55 to 60 per cent of the score, the prompt shape that supplies the 25 criteria, a symptom-to-repair diagnostic loop, and a draw protocol that forces every build into fresh territory instead of recycling a shape. Use when authoring a new Main Recommendation Ask, hardening one a strong model already solved, or repairing a task that failed a determinism review.
---

# The Trap Engine

> A stump is not a hidden fact and it is not a broken file. It is a **staircase of defensible wrong answers**, where every step reproduces perfectly from shipped data that is entirely correct, every step names a different candidate, and only the last step survives a test the data itself performs.

**Read Part 0 and Part 1 before anything else.** They decide whether the build is legal. Everything after them is craft, and craft applied to an illegal shape is wasted.

**Navigation.** Part 0 the goal, the pass bar and the opponent · Part 1 how to think toward it, the litmus, the four gaps, where a decisive move survives · Part 2 the five mechanism families and the decision shapes · Part 3 the ladder · Part 4 the organs · Part 5 determinism machinery · Part 6 the draw, the generators, composition, and hold as the answer · Part 7 the prompt, the deliverables and the asks · Part 8 the evidence pack · Part 9 build order · Part 10 diagnosis and the repair loop · Part 11 determinism failures · Part 12 pre-ship checklist · Part 13 worked skeleton and design note

**Scenarios are the one thing that never transfers.** Every worked shape in this skill is structural, meaning it shows the form an argument or a file request takes, with the nouns left as blanks. Fill the blanks fresh on every build. Lifting a scenario, an entity, a metric, a file name or an ask's wording out of here, out of a reference file or out of a prior build is a clone tell, and the mechanisms are the only part that carries over.

**Prerequisite.** The domain and the Axis 1 objective are fixed and saved before this skill opens. Run `guide-to-prompt` first. Eight objectives are valid (the six of the taxonomy plus Opportunity Sizing & Decision Support and Data Quality Monitoring & Alerting, defined in `guide-to-prompt`), and a task tagged outside them, Comparative analysis and explanation included, is rejected on the tag alone. Nine domains are accepted (the roster is in `guide-to-prompt` Step 1); Biology, Biostatistics, Epidemiology & Bioinformatics is not one of them, so no build starts there.

**Trap catalogs.** `references/traps/<objective>.md` for your objective, plus `references/traps/_cross-objective.md`, which carries the constraint, comparison and monitoring families that belong to no single objective. Read both after Part 1 and before you pick a mechanism.

**The fingerprint cards and the ledger.** Every build already drawn has a fingerprint card under `../fingerprint/cards/`, and `../fingerprint/guard.py` checks a new draw against all of them before the ladder is written (Part 6.1). Without the cards the anti-clone bans cannot be checked, and a card is filed the moment the draw is fixed, so a build in flight is visible to the next one. `references/shipped-ledger.md` is the outcome record, one row per build written when the author reports the portal result, and it is where the lessons each build paid for are kept.

**What has actually stumped, and what has actually died.** `references/proven-in-production.md`, drawn from tasks 35 to 83. **Read it before Part 2 and before the draw.** Part A holds the nine strategies that carried a main recommendation and, on each one, the discriminating property that decides whether it bites or gets solved, because a strategy reused without its discriminator is how a build goes weak while looking right. Part C holds the twelve shapes that are measurably dead and what killed each one. Part D tiers every build by what was actually measured, and most of the corpus is **[B]**, built and never measured, which is evidence of nothing.

---

## Part 0. The goal

You are building one thing: **a task where a strong model does competent analysis, commits to a specific wrong answer with high confidence, and a hostile reviewer who recomputes every figure from the shipped bundle cannot find a second defensible answer.**

> **The pass bar.** A task passes when the **top two responses average under 50 per cent** against
> the generated rubric **and at least one response is genuinely stumped**, well below the bar. The
> rubric is generated from your prompt, your golden and your requested files, you do not write it,
> and a task under **25 criteria** does not advance.
>
> **Build to 40, not to 50.** The on-platform verifiers are not perfectly accurate and the task is
> **regraded more accurately after submission**. That is two-sided risk on a number you cannot see,
> so a build measuring 48 can regrade past the bar after you have stopped working on it. Ten points
> of margin is the cheapest insurance available.
>
> **Where the score sits:** **30 to 40 per cent** on the recommendation and its critical
> components, **5 to 10 per cent** on instruction following, **about 55 to 60 per cent** on the
> asks. At the planning weights (38 / 7 / 55) a response that lands the main call banks about
> **45** before it answers a single ask, and the bar averages the top two of the field (about twelve
> responses). So **two responses landing the call anywhere in the field take both top slots**, and
> the build cannot reach 40 and in practice cannot get under 50 either. **At most one response in
> the whole field may land the main call: the ladder has to stump every other response, the second
> strongest included.** That is the genuine stump the pass condition names, and it sits on the
> critical path of the average, not only of the stump condition. The ask layer cannot rescue a
> build where two responses land the call.
>
> **The ask layer holds the pair.** With one top response landing the call and the other missing
> it, the average reaches 40 only when the two together keep under about 23 of their 110 ask points
> (`55 x (Lc + Ls) <= 28 - r`, where `L` is the share of ask weight a response still earns and `r`
> the recommendation criteria that survive a wrong call, about 5), roughly a fifth of the ask weight
> each.
> That is the pair ceiling, and `supplemental-stumping` builds to it. Both halves of the build are
> load bearing and they fail in different directions: a perfect trap with lookup-grade asks hands
> the pair the ask weight before they open a file, and hard asks with no ladder fail the stump
> condition and the average together. Design the ladder against the main ask exactly as the rest of
> this skill describes, then give the asks real analytical work, which is Part 7 and
> `supplemental-stumping`.

Three ways that fails, and they pull against each other, which is the whole difficulty of the job.

| Failure | What the review calls it | What causes it |
|---|---|---|
| The model solves it | too easy, Gate F | one correction defeats the task, or the correct basis is the natural basis |
| Two rigorous solvers disagree | not deterministic, Gates A to E | an unpinned convention, a reasonable definition the prompt never fixes, a thin margin over real uncertainty |
| The model fails for the wrong reason | wrong type, Gate G | the difficulty is recognising that a reported number or a stakeholder conclusion is misleading |

The third one is what kills builds now. The tempting shape is: ship an artifact that computes a plausible wrong answer, and make the solver refuse it. **That shape is banned at any depth.** A three-rung correction chain is not a defence, a four-rung chain is not a defence, and neither is an official artifact whose methodology is wrong and takes real recomputation to refute. The client's reason, in their words: in a hundred out of a hundred tasks the surface read was misleading, so the model learned to reject the stakeholder by reflex and invent a defect where none exists, and in production most reported numbers are fine.

So the target shape is narrow, and more interesting than it sounds. **Every figure in the pack is correct. Every stakeholder claim about their own numbers is true. And the model still gets it wrong.** Part 1 is where that difficulty can live. Part 2 is the five mechanisms that have actually cleared review.

### The opponent, measured, not imagined

The approved builds in this repo were hardened across dozens of solver rounds and portal results against frontier solvers, and the record converges on one capability model. Design against this solver, because this is the solver that shows up:

1. **It reads every governing document exhaustively and implements every clause.** Any decisive step that is written down anywhere gets found, parsed and executed, including clauses buried mid-paragraph. A rule filed in a standard is a computation, not a stump. Filed, corpus-recoverable and requires-search are one category to it, things it evaluates correctly: it writes the bisection for a constrained minimum as readily as it reads the clause, so search is not a capability gap to build on (task60 v2).
2. **It reconciles as a matter of course.** It ties its build to control totals, checks record counts across joins, asserts grain, validates against any corpus it recognises, and aborts its own run if a reconciliation fails. A build has to make all of those habitual checks pass while the figure is still wrong.
3. **It runs the event study unprompted.** Any decisive cause that is a dated event whose effect steps an outcome series is discovered by aligning the series to the date. That is competent analysis, not a shortcut, and no build whose answer has a cutover date survives it.
4. **It back-tests any corpus it can sweep.** Given settled cases and a family of candidate rules, it runs the rules forward and keeps the survivor. A corpus that can be swept end to end nominates its own answer, so what the corpus is allowed to determine has to be chosen, and what it must be blind to has to be constructed.
5. **It builds per-row pipelines superbly.** One row per unit, conditions as columns, filter and count. Any decisive step expressible as a predicate on a row gets executed. Steps that need a group, a rank inside a group, a cut at a recovered constant, or a property of a different entity behind a join are where it stops.
6. **It refuses stated objections and decomposes by default.** Controlling a confound, splitting a pooled effect, rejecting a rival a voice argues for: these are its reflexes, trained by years of tasks where the surface was misleading. Difficulty built on those reflexes is spent difficulty.
7. **It cleans well and treats arithmetic anomalies as invitations.** A visible symptom, a count that does not tie, a duplicate structure, gets found and fixed. The decisive move therefore has to be the rung with **no arithmetic symptom at all**: nothing fails, nothing looks wrong, and no check the solver writes for itself can see it.

Everything in this skill follows from designing against that opponent. The difficulty cannot live in what the solver reads, reconciles, aligns, sweeps, filters, refuses or cleans. It has to live in a question the solver never thinks to ask.

---

## Part 1. How to think toward the goal

### The litmus, answered in writing before anything else

> **Is the reported number or stakeholder conclusion the task overturns actually wrong or misleading, and is catching that the main thing that defeats the model?**

**Yes** to both means the build is illegal and needs redesigning rather than hardening, however many corrections it takes. **No**, the reported numbers are correct and the difficulty lives elsewhere, means you are eligible to continue.

Write the answer into the design note as a sentence, not as a checkbox. If you cannot write the sentence without hedging, the answer is yes.

**The limb that gets missed is the framing, not the number.** Ask not only whether the stated number is wrong but whether the task exists to correct the way somebody reads a correct number. A correct residual a voice states, a pooled figure a stakeholder carries forward, a basis that honest data refutes: each makes the task a correction of a read, and the litmus comes back yes however correct every figure is (task57 v16, task56).

Then set three flags in the design note, using the judge's own vocabulary, so the review reads your classification instead of guessing it:

- `surface_read_dependency: yes | no` (yes as the primary strategy is the ban trigger)
- `stumping_family: surface_read_rejection | analytical_non_defect | mixed`
- `sole_data_defect: yes | no`, by the clean-data test: on perfectly clean, correct data, would this still stump a strong model for a genuine analytical reason

And name your primary mechanism, the one whose removal collapses the difficulty, from the judge's list:

**Banned:** `planted_defect_flip` · `single_conceptual_flip` (honest data, a correct stated number, and one lens or definition swap that flips the naive read; this is banned too, so passing the clean-data test does not rescue you)

**Passing:** `forecasting` · `method_or_model_selection` · `binding_constraint` · `decomposition_attribution` · `signal_vs_noise_or_hold` · `confirm_surface_read` · `etl_conformance`

`statistical_rigor` is a real mechanism in the judge's list but it is **not** on Gate G's explicit pass list. Never lean on it alone. Pair it with one of the seven.

### The four gaps, which is where difficulty lives when nothing is wrong

This is the working model for the whole skill. A pack full of correct numbers still leaves four gaps open, and every passing mechanism is an instance of one of them. Pick your gap first, then pick the mechanism, then pick the scenario. Picking the scenario first is how builds end up recycling a shape.

#### Gap 1. Time. The measurement is backward, the decision is forward.

Every figure in the pack describes a window that has closed. The decision buys a window that has not opened. Nothing in the pack is wrong and the trailing number still mispredicts, for a reason the history itself supports: a level shift rather than a trend, a saturation, a lead time, a censoring, a regime that changed on a dated event, a signal that has already resolved.

Gate G labels: `forecasting`, and it leads the wanted list. The model that extrapolates the correct trailing figure fails.

*The question that opens this gap:* what is the shipped evidence a statement about, and what is the decision a bet on?

#### Gap 2. Population. The file is not the thing.

The file is a sample with a design, a delta feed that emits only changes, an attempt log, a snapshot, a set of records at one grain when the decision funds another. Every row in it is correct. The population the decision is about has a different shape, and recovering that shape is a method choice with a right answer.

Gate G labels: `method_or_model_selection`, `decomposition_attribution`, supported by `statistical_rigor`.

*The question that opens this gap:* what is one row, and what is one unit of the thing being decided?

#### Gap 3. Objective. The metric everyone reports is correct and is not what the decision is scored on.

Two things both look like size and rank the candidates differently. A limit binds before scoring starts. A horizon scopes the total. The correct figure answers a different question than the one being asked, and it answers it honestly.

Gate G labels: `binding_constraint`, `decomposition_attribution`.

**This is the gap that most easily degrades into the banned shape,** so it needs care. The line is whether the reported figures are demonstrably correct. If the task reads as "the metric they use is misleading, catch it", it is a surface-read rejection wearing a constraint costume and the judge will say so. If it reads as "the metric they use is correct, and the constraint they never checked disqualifies their pick", it passes. Make that unarguable in the design note rather than leaving it to be inferred.

**Where the line sits in practice.** A constraint passes when the naive placement stays right and the constraint only decides what is filed; it fails the moment applying it moves anything from one candidate to another, so build a binding constraint as a removal that re-places nobody. A class of honest records the solver has to infer it should exclude is a surface read however deep the join that enumerates it, and filing the exclusion rule does not rescue it if applying the rule re-places anyone (task58 v3, v4). A hinge of the form `sum of max(0, floor - allocation)` carried by flips of which column is the floor or which basis is the allocation is the same failure: change what the hinge is a hinge on (task58 v7, re-rooted onto the smallest supplemental that clears every floor).

#### Gap 4. Rule. Nothing in the pack states the decisive rule.

No governing document, no method note, no dictionary line. The rule exists, it is unique, and it is recoverable only by running candidate rules forward against a corpus of settled cases and keeping the one that reproduces them. A model looking for a sentence to cite finds none, picks the most natural convention, and loses.

Gate G label: `method_or_model_selection`, by construction.

**This is the strongest single move available under v3** and it is the one the approved builds kept reaching for. It is discussed as the empirical pin in Part 4 and as the calibration corpus, and it is why the calibration file is the load-bearing organ of the whole architecture.

*The question that opens this gap:* if I delete every document that states a method, is the answer still forced? If yes, the pack does not need those documents and they were signposts.

### Where the decisive move survives

The four gaps say where difficulty can live. The opponent model in Part 0 says what a decisive move has to look like to survive contact. Check every candidate mechanism against all seven before committing to it, because each one was learned by losing rounds:

1. **It is written in no shipped sentence.** Not in a clause, not in a dictionary line, not in a labelled column. The strong solver reads everything. Whatever the pack states, the pack has already conceded. **A clause does not have to state the answer to concede it. It only has to make the solver ask the question.** "The clause names the concept and leaves the join to be built" is not a defence, because a join forced by a key column the solver is already holding is one line of code, and a clause the solver cannot avoid reading (the one that defines the quantity being computed) sends it looking whether or not the sentence names a file. Run the test on the wording you actually shipped: if a solver who has read this clause now has a reason to go looking, the rung is free, and burying the join deeper only changes how long the free step takes.
2. **No sweepable corpus nominates it.** Either the corpus is structurally blind to the decisive rule (built so that, over the corpus's own cases, every candidate rule returns the same result, which you assert), or every rival that also reproduces the corpus provably converges on the same answer.
3. **It has no arithmetic symptom.** Row counts reconcile, control totals tie, grain assertions pass, the general reconciliation is identical under the wrong reading and the right one. If the wrong path trips any check a diligent solver writes, the solver is alerted and climbs for free. That includes the default hygiene sweeps (duplicate keys, exact-duplicate rows, unmatched joins, fan-out, a count that does not tie): a symptom one of them surfaces is found, and the adjudicating rule then says what to do. A surviving device leaves the wrong path clean and complete and parks its inconsistency at a cross-file or cross-grain cut nothing invites (task73 world six).
4. **It is not a per-row predicate.** It needs a group and a rank inside the group, a constant recovered from closed cases, a property of a *different entity* reached through a join nothing signposts, or a fit run within units. A condition that can be attached to a row as a column is a filter, and the solver is a filter machine. The form that has satisfied this against live solvers is a group-and-rank on the spine itself: a unit filed by two filers, one statewide group-by on the entity, then a rank inside the group under a filed two-level tie-break, with no single column separating the affected units (task60 v5, the best column running 0.09 to 0.57 duplicated).
5. **Its enumeration is itself arithmetic.** Any population or class that has to be assigned over thousands of units needs a rule that assigns all of them, and a rule that assigns all of them from visible columns is readable. The decisive class can only be enumerated by a fit, a back-test or a forward run, with the corroborating evidence split so that no single half suffices. Run this check on every candidate before any other, because it kills in one line: a world whose quantities are additive over rows (hours sum, cases count, balances subtract) fails it at once (task56, five candidates). Ask first whether the decisive move is a **selection** among candidate rules or the **construction** of a quantity: a selection has a menu, a menu is enumerable, and any corpus worth shipping scores it end to end, while a construction has no menu (task57, three candidates killed after measurement that this one line would have killed). A recovered rule whose content is one scannable parameter is an enumerable class however well its existence is hidden; the repair is an excluded set that is non-monotone in every column a solver can scan, reachable only through a join the natural recovery never touches (task40).
6. **It has no cutover date.** A dated cause with a step in an outcome series is an event study, and event studies are solved. If the mechanism turns on a dated event, the dated event belongs in the decoy, where its loudness makes solvers wrong instead of right. The corpus must not carry a series that spikes at the same date, and a shipped configuration file whose diff is the mechanism is a signpost no surrounding noise buries (task36).
7. **It survives the deletion.** Which is the one-line test for a legal build:

> **Delete every wrong number and every misleading claim from the pack. Is it still hard?**

If the difficulty survives that deletion, the build is v3-legal. If it does not, you have a surface-read rejection and no amount of depth will save it.

**Before the seven, run the first-moves test.** Play the opponent's first moves on paper (the one-period group-by, the decomposition of any pilot, the natural operationalisation of the filed clause, the corpus back-test). If any of them lands on the answer, the build is dead there (task58 v2, task44 v2).

**Two shapes have a surviving record against this opponent.** A quantity the solver believes needs no construction at all, such as a date field it reads with `.year` when the period opens on 1 August, built so the corpus reconciles identically under both readings (task60 v4). And the maturity attack: the graded object crystallises after the extract date, the naive basis ties every closed period because closed periods are fully developed, the tail is computable exactly from an operational registry the natural pipeline never joins, and no received or as-of dates ship, so estimation is structurally impossible (task73 world seven).

#### Run the clean-data test in the generator, because a flag you set yourself is not a check

**The three flags are self-reported, and a build that sets them honestly can still be wrong about
them.** The failure has a signature worth recognising: the design note argues the litmus from
**intent** rather than from the test. *"The register is correct and incomplete by the design of the
business process, not by defect"* is an argument about why the gap exists, and the judge does not
ask why it exists. It asks what happens without it, in one line: *had that file been complete, the
main number is a routine sum.*

**So make the file complete and see.** Unlike most things in Part 1 this one mechanizes exactly,
because the generator already holds both worlds:

```
repair the suspect file in the generator      (fill the gap, correct the record, complete the feed)
recompute the answer and the naive figure
ASSERT  answer(repaired)      == answer(shipped)
ASSERT  naive(repaired)       == naive(shipped)
ASSERT  answer                != naive
```

**Repair the SEMANTICS and the INSTRUMENT, not only the nulls, because that is the repair the judge
actually runs.** A file can be complete to the row, carry no blank, no sentinel and no missing
record, have its every field defined correctly in the dictionary, and still be the whole difficulty,
because what the field *means* is narrower than what the decision needs. The judge's version of the
test is one sentence long and it imagines a better instrument rather than a fuller file: *had this
measurement carried the thing the decision is about, what is left?* So run the repair at three
depths and assert all three: fill the gap, correct the semantics, and **replace the instrument with
one that observes the decision's own quantity directly.** If the third repair collapses the task,
the difficulty was a correction to what the instrument reported, `sole_data_defect` is `yes`
whatever the note claims, and no depth of recovery chain is a defence.

The first two assertions say the file's defect is **not** load-bearing anywhere. The third says a
decisive move still exists. A build that cannot pass all three has its difficulty sitting in the
defect, `sole_data_defect` is `yes` whatever the note claims, and Gate G fails.

**Run it once per suspect file, not once per build.** The candidates are every file the ladder
touches that is incomplete, stale, superseded, delta-shaped or filtered. Wire each one as an
assertion, because the property is cheap to hold while a world is being tuned and expensive to
rediscover after a review.

**The two bans are independent and a candidate has to clear both.** Passing the clean-data test
kills `planted_defect_flip` and says nothing about `single_conceptual_flip`: a build whose answer
rereads a wholly correct record through a second lens passes every assertion above and is still
banned. Ask both questions of every candidate mechanism, in this order, before drawing:

1. Repair every file. Does the answer move? If yes, it is the defect, and the build is illegal.
2. Are the naive read and the answer the **same population at the same moment** under two lenses?
   If yes, it is a lens swap, and the build is illegal.

**The repairs that have worked in a banned world.** Move the answer to a population at a **different date** that moves in **both directions**, each limb pinned by a filed fact, so no arithmetic on a shipped figure reaches it and a solver netting only one limb is wrong in the same direction as one carrying the extract forward (task56 v3, task57 v17). Or grade a **component rather than a correction**: two real causes that begin within days of each other cannot be separated by any time-series method, enumerating one of them is a group-and-order construction across two files, nothing reported is overturned, and the stakeholder who names the cause is right and gets quantified. That is `decomposition_attribution` with `confirm_surface_read` support, and it survives the instrument repair because no instrument in the pack is lying (task89 v6).

**And run task73's pre-draw test above both of them,** because it is cheaper still: write the
governing arithmetic of the decision as an identity. If it closes over quantities the pack must
ship, every construction feeding it is either readable or a lens swap, and no cleverness inside the
identity escapes that. The repair is to change the **graded quantity**, never the construction.
The test binds when the inputs are constructions too: once each construction is either filed or
symptom-discoverable, the identity closes over filed documents, so ask which quantity is neither
filed nor visibly forced, and if the answer is nothing the build is an execution exercise before it
is drawn (task73 world six). A closed identity also lets a solver reach the name by elimination,
ruling out every other term until one is left, so the name is never built (task73, task36).

**Run the corpus-direction test beside it, with its own line in the design note.** State in one
sentence what the calibration corpus returns under the naive path. Only a device that **nets** at
the corpus's grain can leave the corpus reproducing the naive read; a device whose losses
**accumulate** makes the corpus refute it, and a refutation is an alarm. This opponent back-tests
unprompted, so the miss does not falsify a rival it was about to file: it hands a solver that had
not found the rung the direction to search in, and the winning response quotes the corpus back as
its evidence (task92 v2, refuting the naive read by 18.45 per cent; task89 v5, whose parallel-run
workbook was cited in those words). Anything other than "it reproduces" disqualifies the device
before a row is cut. A world with no netting device re-roots the graded quantity rather than keeps
hunting, and a design note that concludes its device space is saturated re-derives the conclusion,
because it is about the graded quantity, not the domain.

---

## Part 2. The five mechanism families with the best record

These are the mechanisms that carried the approved builds. They are stated as patterns rather than as scenarios on purpose: the scenario is the part you must not reuse, and the pattern is the part that transfers. Each one is legal under v3 on its own, each one runs on a pack where every number is correct, and each one is worth more than a clever new idea, because these have already survived a review.

Pick one as the decisive rung. Pick a second, from a different gap, as the rung below it.

**Draw the decisive rung from the measured catalogue first.** `references/traps/_measured.md` ranks
26 traps by how many of the client's 64 accepted tasks each one decided, with the build recipe and
the way each goes wrong for authors. The top four (a failed back-test shipped anyway, the file's row
grain taken for the unit, a close but inexact match accepted, a reading never tested against the
control) decided 37 of the 64 and share one architecture: a published control set produced by a
method the documents do not spell out, a governing clause that makes exact reproduction the condition
of using a method, a unit or population the governing document defines but no file stores, an obvious
construction that reproduces most but not all of the controls, and exactly one construction that
reproduces all of them and changes the decision. That architecture is Pattern B with the reproduction
clause as its gate, and it is the one with a measured record. A decisive rung drawn from outside the
catalogue is a bet, and the design note says in one line why the bet is taken. The client's own
records of those tasks, prompt and solution and the model's miss, are in
`../guide-to-prompt/references/exemplars/`.

**The five patterns are where difficulty can live. They are not by themselves a stump.** Each one has been solved at least once in this corpus with its pattern label intact, because what fires a pattern is a property underneath it: whether the recovered rule is scannable, whether the two grains disagree in shape or only in level, whether the conditioning property is also a column name. Those properties are collected per strategy in `references/proven-in-production.md` Part A, and picking a pattern here without checking its discriminator there is the single most common way a build reaches the portal and does not stump.

### Pattern A. Past exceedance against forward yield

**Gap 1.** The pack carries a correctly measured statement about something that has already happened: an alert score, a breach magnitude, a quarter's movement, a completed run. The decision buys a future window. Some candidates are resolving and some are ongoing, and the ranking on what happened is close to the reverse of the ranking on what will happen.

**Read this before you build the ranked list, because this is where the banned shape leaks back in.** A detector output or watch list that ranks the candidates is legal here, on two conditions, and it fails Gate G without both. First, it reports a **past quantity it measures correctly** and makes no claim about the decision. A list of exceedance scores is a statement about exceedances. Second, it is **labelled in-file for the question it answers**, in one line: *"Alert scores are computed on the trailing four weeks and describe the breach, not the forward burden."* A list that presents itself as a deployment ranking, or that carries a method note implying it answers the decision question, is the banned loud artifact and the task gets sent back. Rank on the past. Never rank on the decision.

**Why it stumps.** Every ranking input is correct, and there is nothing to correct. The model has to notice that an exceedance is a statement about the past and an intervention is an investment in the future, then build the forward quantity from a property the pack supports (a fitted level shift, a decay, an ongoing versus resolved classification recoverable from the series).

**What makes it deterministic.** The forward quantity has to be pinned by the data rather than by the modeller's choice of horizon. Pin the horizon operationally (the length of a deployment, the term of a commitment, the cycle the funding covers) in a filed logistics fact, and pin the functional form empirically against closed cases.

**Where it degrades.** If the "resolving" candidates are resolving because of something broken, you are back in the banned shape. They must be resolving for an ordinary reason that the series shows.

**The off-chain form.** Decomposing a pilot is default behaviour, so the strongest version puts the moderator in how a **period** treats the unit rather than in the unit, and the decision buys a different period (task44 v2: eaches per line is how a quarter orders an item, so the pilot window gives 138 and the decision window 66). Make the flip bidirectional so no haircut or partial correction of the on-chain answer reaches it, assert that no cutoff on any wrong window selects the answer set, and ship the twin pair on the decision set, identical on every visible column and on the pilot window's own measurement.

### Pattern B. The rule recovered from a closed corpus

**Gap 4.** The decisive rule is written down nowhere. What ships instead is a corpus of cases that are already settled, with their inputs and their outcomes, and enough raw material underneath them that a candidate rule can be run forward and scored. Exactly one rule reproduces the whole corpus. Every rival misses at least one case badly.

**Why it stumps.** The model's strongest habit is to find the governing sentence and quote it. There is no sentence. It falls back to the most natural convention, which is one of the rivals, and it is confident because the convention is genuinely standard.

**What makes it deterministic.** This is the strongest determinism story available, because the rule is not a preference, it is the unique survivor of a back-test that the reviewer can rerun. State the back-test as a number: the correct rule reproduces N of N within x percent, and every rival in the swept family misses at least one case by y percent or more. Both numbers go in the design note and both get asserted.

**Where it degrades.** A corpus case that no rule in the pack reproduces. Then the model declares it unexplainable, uses the corpus ordinally, and lands on the decoy anyway. See fittability in Part 4.

### Pattern C. Serviceable share behind a join

**Gap 3 into Gap 2.** The magnitude of each candidate's problem or opportunity is correctly reported and the model can reproduce it exactly. What the intervention can actually touch is a fraction of that magnitude, and the fraction depends on a structural property that lives in a different file: how concentrated the volume is, whether the units are reachable, whether the capacity exists, whether the records are the kind the mechanism can act on. The largest problem is the least serviceable.

**Why it stumps.** The model ranks on magnitude, which is correct, and never asks what share is addressable. There is no error to find. The join it has to make is not signposted, and the property it has to compute is not a column, it is a statistic over the raw records.

**What makes it deterministic.** The serviceability split has to be absolute rather than graded. Threshold-free is the target: a record either was or was not on the governing list, every attempt with property P succeeded and every attempt without it returned nothing. An invented cutoff is a fork you left open.

**Where it degrades.** Discriminator dominance, in Part 3. If the decoy's carried advantage on magnitude is bigger than the winner's edge on serviceability, the rung computes perfectly and never changes the ranking.

### Pattern D. Two grains, both flawless

**Gap 2.** The pack carries the same measurement at two grains, and both are arithmetically perfect. The two differ in **shape**, not only in level, because the collection design over-represents something or because size correlates with the measure.

**Draw axis:** what the two grains are (records as collected against units in the population, events against entities, a delta feed against a reconstructed panel, a billing grain against an operating grain, an attempt grain against a case grain) · what makes the second grain recoverable (a roster, a weight column, a membership history with effective dates, a reconciliation) · what correlates with the measure and so changes the shape rather than the level · whether the correct grain is pinned by a filed statement about the unit of work or by the corpus.

**Why it stumps.** Nothing is broken and both numbers are defensible in isolation. The model computes one of them, usually the one that needs no join, and reports a distribution or a rate that describes a population nobody is deciding about.

**What makes it deterministic.** The decision grain has to be pinned by what the decision funds, in one filed sentence about the unit of work, and the weighting convention has to be either pinned in the dictionary or convergent (both handlings give the same answer). A rate computed over a delta feed without reconstructing the panel is the classic version of this and the judge checks for it explicitly.

**Where it degrades.** If both grains give the same winner, the rung is decoration. Build the correlation that makes them disagree, per candidate, and assert it in both directions.

**A key column that turns the grain bridge into one group-by is a hand-hold** (an order id for an order-line grain). The honest alternatives are an unpinned bridge (a fork) or a bridge the corpus pins, and neither stumps, so a grain rung bridged that way is variance against careless solvers (task44). **Where two causes are collinear, the decisive grain move is often a standardisation**: when the causes separate only in partial-exposure groups, the group is usually not a miniature of the base its effect will be applied to, and standardising it decides the attribution (task73, a price effect of 0.24 read straight against 0.59 standardised). Measure on a grid whether the standardisation can flip the call before designing for a flip; where it cannot without collapsing dominance, put the stump on the magnitude and say so in the design note.

### Pattern E. Conditioned yield

**Gap 2.** An aggregate that looks recoverable has near-zero yield for one subgroup, and the rivals' pools are concentrated in that subgroup. The attempt log ships. The split is visible on a one-line group-by, and confounders are controlled by construction: the failing and succeeding attempts share operators, sites and timing, so only the property separates them.

**Why it stumps.** The model applies the pooled success rate uniformly. The pooled rate is correct. It is just not the rate that applies to any particular candidate's pool.

**What makes it deterministic.** The data draws the line rather than the author. Absolute splits, not gradients.

**Where it degrades.** If the property that conditions yield is also a column name, it is a two-column lookup and the rung is a signpost.

**Build rules for a pilot with a moderator**, each paid for by a solved or failed build:

- **The naive uncontrolled read must be correct and point at a wrong action, never at a wrong number.** Delete any period confound rather than balancing it, and assert that the pooled read is right under no control and under every control. The difficulty then comes from transport: invert the mix, so the pilot's composition is the reverse of the decision set's and the pooled figure is simultaneously correct and untransportable (task44 v2, 144 gainers to 72 losers in the pilot against 108 to 180 in the request).
- **The cross-section has to be wrong**, or the pilot is decoration: run the one-period group-by a solver runs first, and build selection into treatment with persistent unit effects, so the cross-section reverses in every window while the within-unit comparison cancels the unit effect (task44 v2).
- **Decorrelate every visible column from the moderator by construction and assert it**, velocity included, calibrating weights in a second generator pass where one pass cannot. Where line-weighted and unit-weighted pools carry opposite signs, pin the metric in the criterion and record the other as a wrong-metric cell (task44).
- **Keep the assignment rate flat across every covariate a solver would test.** A fixed amount of treatment delivered to a subset selected on an observable manufactures a moderator on that observable, and it can beat the designed one (task43, budget at t 3.81 against the designed 1.90). Assert the designed contrast dominates every rival's by a stated margin, cross the designed moderator with each rival and assert the carry is unchanged, and buy power from the design (another closed period, more of the property in the pool) rather than from the effect size.

### Which to reach for

| If your objective is | Native pattern | Already spent on | Draw from instead |
|---|---|---|---|
| Forecasting & Predictive Modeling | A, then B | B on task29, E on task30 | C or D, or B with a calibration form the ledger has not used |
| Root-Cause Analysis | C or D | B on task36 | C or D, and put the driver behind a join |
| Anomaly Detection & Diagnostics | A | A on task33, C on tasks 25 and 28 | B or D |
| Experiment & Causal Analysis | D with statistical rigor | never built | anything, the pairing itself is clone-free |
| Descriptive & Distribution Analysis | D | D on task34 | A, B or E |
| Data Extraction & Conformation | B with `etl_conformance` | never built as the primary | anything, the pairing itself is clone-free |
| Opportunity Sizing & Decision Support | not established, one build so far | task106 (`binding_constraint`, no Part 2 pattern) | any of A to E, with the sizing kept as the graded figure |
| Data Quality Monitoring & Alerting | not established, one build so far | E on task107 | A, B, C or D |

**Read the middle column as a warning, not as a recommendation.** The native pattern is where the objective naturally sits, which is exactly why the delivered builds are clustered there, and a builder who takes the native pattern for an objective it has already carried lands on a delivered task. The ledger is what tells you which cell you are in.

**Do not reuse the pattern that carried your last build's decisive rung.** Patterns are the scarcest resource in this repo, and burning one on a build that also repeats its domain is how a batch starts looking like one task.

### Decision shapes, and which of them still carry difficulty

The approved run also settled which *shapes of decision* can carry a trap at all. This is a separate axis from the pattern, and getting it wrong wastes every round spent on the build.

**Shapes with apparatus, proven to carry:**

- **Which of N candidates gets one scarce thing.** The workhorse. It supports a candidate list, a ground-truth position rule, discriminator dominance, a serviceable share and a calibration corpus, which is the full architecture. The naive ranking is by magnitude, the correct ranking is by what the intervention can realise.
- **One figure certified, filed or booked at a date**, reached through a ladder of corrections with disciplined signs (Part 3). The trap terminus is an arithmetically perfect pipeline that passes every check it writes for itself.
- **An allocation under a cap.** When a corrected-rate ask keeps getting solved, or reads as refusing a stated rate, re-root it: the scarce places have to be put somewhere, the naive figure becomes an incomplete optimisation rather than a rejected read, and `binding_constraint` carries it. File the cap plainly and put the difficulty in the unit it counts: a cap whose parameter carries the difficulty is dead three ways (guessed is Gate C, read is arithmetic, scanned is a threshold scan), while a cap on households over an operating layer counted in case files makes the scored quantity a group property (task57). Keep the cap tight, because as P places approach K acceptors the naive and optimal allocations converge (task43, worth 9 per cent at P/K near 0.86 and 29 at 0.57), and re-sweep every cell after changing P. The same move rescues a projection: replace an estimated rate with a countable ceiling, `sum over bands of min(filed_places, population) x amount`, which is `binding_constraint` with nothing left to estimate (task57 v21).
- **A structure the body adopts** (how many populations, which characterisation), with the ask naming what the characterisation is **scored on**, because a characterisation ask admits many true partitions and only the scoring clause makes exactly one operative.
- **A conformed table delivered against a contract**, where the contract states grain, columns and checks but deliberately not the unit of observation or the spreading rule, and the ladder is a ladder of complete pipelines the solver constructs, each a defensible build, separated by a certified back-year only one ruleset reproduces.

**Before reading the list below, read `references/proven-in-production.md` Part C**, which carries the same ban list extended through task83 with the measured death beside each entry: a filed formula's output (67, five rounds), a one-parameter recovered rule (40, one threshold scan), a device announced by its own columns (48, one group-by), a device whose only defence is silence in a pack that names it (76 v1, 65 v1), and the two-consecutive-solves stopping signature (44, 60, 83).

**Shapes that are exhausted on the round record:**

- **A figure computed to see which side of a line it falls.** The figure is either written in governing text or recoverable from a control total, because determinism requires one of those, and the opponent reads text and reconciles totals. No threshold-crossing build has beaten it.
- **An argmax under a stated rule over a filed candidate list.** Reading the rule plus running the sweep is mechanical for the opponent, and if the corpus can confirm the rule end to end, it hands the answer over too.
- **Any decision whose decisive cause is a dated event stepping an outcome series.** Solved by alignment. The dated cause is decoy material now, never the answer.
- **A world whose quantities are additive over rows once its structural map ships**, and Gate C makes the map ship when the map is the charging rule: hours sum, cases count, balances subtract, and the correct basis is the natural basis (task56).
- **A forward window whose every input is filed.** It is a simulation the solver builds as its first move, and a mechanism that only moves *when* something becomes available changes nothing against a filed quantity plan; the mechanism has to move *what the thing is* (its code date, its unit, its eligibility) (task55).
- **Any decision whose decisive step is the last link of the obvious chain.** Decomposing, controlling and refuting are default behaviour; a build whose decisive rung is simply the deepest of those steps is already solved. Move the decisive rung off the chain, into a gap where thoroughness on the chain does not help.
- **Any decision whose graded quantity is what a counterparty will invoice under published terms.** An accrual, a settlement, a rebate, a royalty, a chargeback, a reconstruction of what the other side is about to bill. The terms have to ship for the figure to be determinate, and enforceable terms are by construction a **complete specification of the charge**: every clock, every allowance, every stop event and every rate is written down, because a term nobody wrote down could not be enforced. There is nothing left for the solver not to think of, and the build is a reading exercise however messy the operational records underneath it are. This is the statutory world by another name, and **drawing an operational domain does not escape it, because what files the rules is the graded quantity rather than the domain.** Charge reconstruction is fine as depth and cannot carry a decisive rung. The escape is to grade what the terms do not define: what the operation **could have avoided**, or what it **commits to next**, neither of which any tariff, schedule or contract speaks to.

---

## Part 3. The ladder

**The unit of design is not a trap. It is a ladder of three to five rungs.** Each rung is a complete, defensible analysis a competent analyst would be satisfied with. The solver climbs by refusing the rung below it.

```
RUNG 0   The natural pipeline's answer         -> candidate A
RUNG 1   The obvious correction                -> candidate B
RUNG 2   The sophisticated correction          -> candidate C
RUNG 3   The decisive move                     -> THE ANSWER
```

### Rung 0 is built by the solver, not shipped by you

**Never ship an artifact that computes a wrong answer to the decision question.** An in-pack file that ranks the candidates on the decision basis and gets it wrong is `surface_read_dependency: yes` by construction, and it is the Gate G ban trigger no matter how many rungs sit above it. This is the most common way a build gets rejected, and it is easy to do by reflex because the rest of the architecture reads the same. The one exception is the declared distractor (`dataset-generation` §8.3): wrong on a basis a shipped fact rules out, named in `metadata.json`, and never the stump.

Rung 0 is **the answer the most natural correct pipeline produces**. The solver opens the pack, does the obvious competent thing, gets an arithmetically perfect number, and that number names candidate A. You never wrote it down anywhere. You did engineer the data so that it comes out that way, and you assert it in the generator like any other rung.

What you may still ship, and should:

- **Context artifacts whose numbers are correct**, that describe the situation without answering the decision question. A monitoring export, an operations log, a register, a published series. They report what happened. They do not rank the candidates on the decision basis.
- **An artifact that answers a different, clearly labelled question correctly.** A capacity report is not a ranking. A prior-period close-out is not a forecast. Label it in-file for what it is, and it carries authenticity with no Gate G exposure.
- **A stakeholder who advocates a wrong basis as a belief.** See Part 4.

What you may not ship: a scorecard, workbook, filed model or review memo that ranks the candidates on the decision question and gets it wrong. Nor a dimension table the naive pipeline needs: a one-to-one dimension plus a stakeholder narrating their use of it is a reported read in everything but name, and deleting it turns the same insight into method selection on a join the solver builds itself (task42). Before shipping any dimension table, ask whether the naive pipeline needs it; if it does, it is rung 0 wearing a filename.

### Rung requirements, all four mandatory

| Requirement | Why |
|---|---|
| **Reproduces exactly from the raw files** | If a rung is arithmetically wrong the solver dismisses it as a data error and climbs for free. The wrongness must be conceptual, never computational. Aim for zero drift; the review recomputes it. |
| **Names a different candidate than every other rung** | This is the whole mechanism. Partial insight must land on a specific wrong name, not on uncertainty. If two rungs produce the same winner, one rung is doing no work. |
| **Is killed by exactly one shipped fact** | One fact, one rung. If a rung needs two independent discoveries to fall, the solver finds one, gets stuck, and hedges. Hedging is unfair-hard, not hard. |
| **Is genuinely satisfying to stop at** | Write down why a good analyst would file the report at that rung and go home. If you cannot write that sentence, the rung is fake. |

Two rungs fail the fourth requirement on sight. **An arithmetic a competent engineer fixes in the loop they are already writing** (a day counted twice by summed spans) is not a rung however blind the corpus is to it, because corpus blindness defends against a back-tester selecting a rule, never against a solver reasoning about the observable (task58 v5). **A rung a solver reaches with one group-by** is not a rung: run the one-key and two-key group-bys a solver would actually run and confirm the conclusion is not sitting in them (task36).

### Depth

**Three to five rungs, four is the working default.** Two rungs: one correction defeats it. Six or more: the task becomes machinery, answers scatter, and scatter reads to reviewers as ambiguity rather than difficulty.

**Depth is not a Gate G defence.** It is a Gate F device: it is how you make a competent solver spend its insight on the wrong candidate.

### Sign discipline, when the answer is a figure

Give the correction chain a direction and make the decisive rung reverse it: every correction walks the figure one way, and only the decisive move turns it back. A solver who stops anywhere short is then wrong in a consistent direction by a stated percentage, no wrong cell sits near the answer by accident, and the decisive rung cannot be absorbed by a partial application of the others. State the per-rung percentage moves in the design note.

### The winner's position rule, checked at every rung

**The correct answer ranks 4th or 5th on the natural pipeline, and it never leads an intermediate rung.**

| Where | Required position |
|---|---|
| Rung 0, the natural pipeline | 4th or 5th |
| Every intermediate rung | never 1st |
| At most one intermediate rung | 2nd, and there by at least 1.20x |

A winner that already looks good on the natural read cannot stump, because the solver arrives at it by accident and the ladder never engages. A margin under **1.15x** anywhere in the ladder is a knife edge: a solver computing that rung under a slightly different convention lands on the right answer by accident and the trap never fires. If you cannot put two candidates above the answer at a given rung, widen the leader's margin rather than accept the near-tie.

The correct answer should usually be **on the candidate list** the prompt bounds. An answer off the menu is legitimate but needs an explicit licence in the prompt, otherwise it reads as unfair.

### Where cleaning belongs

**Deduplication, defect removal and record hygiene belong at rung 1 or 2. Never at the final rung.** Solvers are good at cleaning. Make cleaning necessary but not sufficient: the solver does the hygiene correctly, the number moves, the ranking changes, and the new winner is still wrong. This converts the solver's competence into confidence in a wrong answer.

State it explicitly in the design note: *"A solver who cleans perfectly and stops here commits to ___."*

Note what this is not. Cleaning at rung 1 is texture. If cleaning is the **decisive** move, the litmus in Part 1 comes back yes and the build is illegal.

### Margin

The winner beats the runner-up **on the correct basis** by a stated factor. Floor 1.2x, target 1.5x to 2x.

Gate C treats a thin margin as fully deterministic when the gap is definitive, meaning it falls out of the shipped data the same way for every rigorous solver, and it fails only when thinness meets real uncertainty. So a 0.1 percent lead can pass review. Keep the 1.2x floor anyway: this skill's margin is about whether the **rung fires reliably**, not about whether the answer is forced.

### Grade a quantity the rungs can move

**Before shipping, compute what each rung is worth on the graded quantity itself, not on an intermediate.** A quantile absorbs any rung that works by selecting observations, because the selected and unselected sets share the dense mode; a share cancels any rung that moves numerator and denominator together. Totals, counts, converted amounts and levels are linear in their inputs and carry rungs faithfully. If the hard rung is inert on the graded quantity and the rung that moves the quantity is easy, no patch to either fixes it; change what is graded. And never let the deliverable asks over-determine the system: filing enough related quantities to solve back for the decisive constant hands the constant over.

**What a rung is worth on the graded quantity, measured:**

- **Grade the sensitive root.** Where a quantity is recovered from two equations and every split error moves the same absolute amount, the small root carries the rungs (task44: a grain rung worth 19 per cent on the large root and 18 on the small, a sizes rung worth 2 against 11), and a constant can carry a rung when it has an owner the campus average erases.
- **On a banded schedule the amount spread prices composition, not the rate spread**: a rung's worth is `sum (r_b - r_bar) n_b a_b`, so tune the amounts, because a rate spread alone cannot buy separation when the amounts track the band sizes (task57 v20).
- **A rate model re-fits around any distortion that is stable across the fit window**, so only a distortion that grows into the forward year carries a rung (task57 v19), and a `min()` survives re-fitting only if the quantity it bites on grows forward: compute the capped and uncapped figures for the forward year and every scored year before building, because a cap that bites harder in the window is sign-inverted (task60). Two mechanisms can need the same structural knob turned opposite ways and cannot both be live in one world.
- **A constrained minimum amplifies honest-data rungs** (a move in the binder's share moves the figure by about that share of the whole pot, task58 v7) **but is no stump by itself**, because the solver writes the search; its value is amplification of upstream errors, which buys nothing against a solver that made none (task60 v2).
- **Two rungs on one graded sum interfere**: one can swallow the other and leave a half-applied pipeline next to the answer, so separate their populations by construction (task57 v19, a cap that cut a covariate rung from +55.4 to +30.5 per cent until the populations were split).
- **Do not make the decisive quantity a top-k share of a cell whose bound, count and aggregate are all reported**, because that triple brackets the answer with no model at all (task38).

### Discriminator dominance, the arithmetic that decides whether the last rung can fire

The decoy arrives at the final rung carrying an advantage from the rung below: more exposure, more volume, a bigger book. The final rung flips the ranking **only if** the winner's edge on the decisive axis exceeds that carried advantage by the margin floor.

```
edge(winner, decisive axis)  >=  1.2 x  advantage(decoy, carried axis)
```

If the decoy leads by 1.3x on the carried quantity, the winner needs at least 1.56x on the decisive one. **Compute both ratios explicitly and assert the product.** A discriminator worth a few percent set against a carried advantage worth tens of percent cannot fire, no matter how well documented or findable the mechanism is.

This failure is silent and expensive: the rung still computes, the solver could execute it perfectly, and it simply stops naming a different candidate. Nothing in house will tell you the last two rungs agree, so you find out from a portal result or never. Settle it on paper before any data is generated. Check that the band exists and is reachable as well: the naive reading of the decoy has to beat the answer and the corrected reading has to lose to it, and where the answer's magnitude and the size of the move are the same quantity, shrinking the answer into the band shrinks the move with it (task36, a correction the leader survived by 2.3x, which a solver found, computed both ways and generously ignored).

### The rung-collision guard

**After every parameter change, recompute every rung's winner by name.** A parameter tuned to strengthen one rung routinely hands the final rung to the same candidate as the rung beneath it. Two adjacent rungs with the same winner means the last rung is dead and the ladder is a rung shorter than the design note claims. Assert per-rung winners by name so the collision fails the build instead of the round.

### Enumerate the grid, not the path

With three independent corrections there are eight builds, not four. The answer must be reachable only through the decisive combination, and every other cell of that grid must land on a named wrong candidate. Work the grid on paper before generating data, because it is arithmetic and it is cheap there.

**When the answer is a figure rather than a name, the grid has a separation floor and the floor
decides how big the decisive rung has to be.** A reviewer's test is that no wrong cell lands within
a stated percentage of the answer, and with `n` monotone corrections at factor `f` plus one
reversing decisive factor `g`, the binding cell is always **rung 0 itself**, at `1/(g * f^n)`. So:

```
g  >=  1 / ((1 - floor) * f^n)          and         (1/f) - 1  >=  floor
```

At three corrections removing 9.5 percent each against an 8 percent floor, that forces `g >= 1.45`:
**the decisive rung has to be worth about half the answer on its own.** Three consequences, and all
three are decidable before a row exists.

- **Every rung you add below the decisive one makes the decisive move bigger, not smaller.** Depth
  is not free, and a five-rung ladder can be arithmetically impossible where a four-rung one is not.
- **Choose the decisive mechanism against this number rather than after it.** A move that restores
  or reallocates a whole population carries that weight. A move that reprices a slice usually
  cannot, and you find out after the data exists.
- **Putting the answer below rung 0 is the gentler packing.** The constraint is symmetric in `g`,
  but the decisive move stated as a fraction of the pre-decisive figure is `d/(A+d)` going down
  against `d/(A-d)` going up, so the same separation buys a smaller-looking move. task42 shipped the
  down direction and landed at 1.143x for exactly this reason, which is under the 1.20x rung-margin
  floor and legitimately so: **that floor guards a decisive rung against failing to change a winner
  in a ranking, and a figure graded to the cent has no ranking to change, so the separation floor is
  the guard that binds.** Say which guard applies in the design note rather than leaving it to be
  inferred.

**Partial application is not in the grid and needs its own sweep.** The grid enumerates corrections
omitted whole. A solver that applies the decisive rule to one source system and not the other, or to
the records it can date and not the rest, produces a cell that is not an omission, and when the
decisive move is small those cells land inside the band. Sweep them and assert each one's distance.

**The corridor theorem.** In a mixed-sign grid each opposite-sign stack value casts an exclusion
band of plus or minus the applicable floor around itself, so compute the bands before designing any
new cell. A new rung of sign opposite to the ladder has to clear every band (task60's reorganisation
needed `r >= 26.4` per cent or `r <= 0.6` against stacks at +16.5 and +10.6, and was unbuildable),
and a mechanism that creates a complementary cell pair summing to a fixed weight can be provably
impossible on paper (task44). With three opposite-sign toggles the theorem bites at every retune,
and the honest exit is to build the smallest toggle as a hazard (task56 v4).

**Hazards are not rungs.** With `n` monotone corrections and one reversing decisive factor, a
further independent toggle has to be worth about a third of the answer before any cell clears the
floor, which no coding error is. Ship pipeline mistakes as hazards refuted by a shipped control,
where they add failure surface and path length without adding a defensible wrong answer to the grid
(task42). A hazard is a single deviation from the truth walk, never from the naive rows, and a
hazard block worth under 1 per cent of the figure is a near-miss cell, not texture (task57). When a
figure-shaped ask has been solved twice by one route, demote the free rungs to hazards and rebuild
the ladder as same-sign constructions, so no partial reading lands near the answer (task57 v18).

**More grid rules, each measured:**

- **Every partial reading should land on the same wrong figure**, so the work is all-or-nothing (task57 v21, nearest wrong cell 51.9 per cent away).
- **Every single-error cell must file a feasible figure.** A wrong route that breaks the arithmetic (negative counts, absurd magnitudes) self-discloses as an alarm rather than a wrong answer (task44).
- **With careless errors of both signs, assert the full stacked-error grid cell by cell**, because two errors cancel (task44, a stack inside 1 per cent of the answer).
- **Give the naive side clearance and the true side depth separately**, each sized to the convention slip that could reach it (task55).
- **Decompose a near-answer cell by cohort before touching a parameter**; a generator bug no parameter sweep can find shows up there (task58 v4).
- **Sweep the forward paths before believing a shape discriminates**: seven paths that all turn at the same year make the turn a computation (task73).
- **Sweep every classifier and partition a solver can reach.** Compute the rung's partition again from every single column and two-key join a solver can reach, including every artifact added in a patch, and assert each lands at least 8 per cent away or collapses the population (task44: `zone in (RSV, OVF)` reproduced a three-table effective-dated join exactly). A route **equal to the truth** deadens the rung for the solver class most likely to take it, a shortcut that reproduces the partition exactly is as bad as one that misses it, and a rival whose exclusion set is a superset or subset of yours errs in one direction only, so break the containment, because under-filtering is the direction that separates (task44).
- **Re-run every careless cell when a constant is introduced**, and check that a rival's separation is not an artefact of the generator's own implementation (task44's hygiene rung read -60 per cent for three builds on duplicated keys and was 3.5 measured honestly).

---

## Part 4. The organs

Four supports. No artifact computes a wrong answer to the decision (Part 3, rung 0), and the sanctioned decoy is a belief rather than a computation.

### 4.1 The calibration corpus, the load-bearing organ

**This is the highest-leverage artifact in the build and the one most often missing or half-built.**

A calibration corpus is a shipped record of **outcomes the decision does not cover but the method must explain.** The solver computes each candidate basis, then checks which basis reproduces the known outcomes. The right basis fits. The rivals do not.

It is the engine of the whole architecture, because it turns *"I prefer this method"* into *"this is the only method that survives a test"*, and a rule that survives a back-test is `method_or_model_selection`, which is on the Gate G pass list. Without it your final rung is your opinion, and a strong solver that reaches every insight can still commit elsewhere and defend it. That is the single most common way a well-designed trap dies in review: not as too easy, but as not deterministic.

**Forms that work:** a ledger of settled transactions · an acknowledgement or confirmation file from a counterparty system · a pilot log with filed decisions · the book of existing accounts or markets with actuals · a prior-period close-out summary · a revision or retry log · a parallel-run overlap where two sources were observed simultaneously · a gold-standard verification subsample.

**It must nominate the decoy, never the answer.** If a solver can pattern-match the answer to whichever calibration case it most resembles (same flags, same design columns, same profile) then the corpus is solving the task for free and the winner arrives without a single measurement. Build the resemblance so it points at the decoy. The corpus falsifies rivals; it never nominates a candidate.

**The gap must be dramatic, not marginal.**

| Test form | Weak, do not ship | Strong, ship |
|---|---|---|
| Predictive fit | R2 0.88 vs 0.84 | R2 **0.92 vs 0.59** |
| Reconciliation | 2 percent vs 5 percent error | **0.000 percent vs no match** |
| Success-rate split | 70 percent vs 50 percent | **226/226 vs 0/75** |
| Prediction error | 400 vs 900 | **3 vs 27,000** |
| Cross-unit stability | 1.4x vs 1.9x spread | **1.26x vs 5.30x spread** |
| Rule reproduction | "mostly matches" | **180/180 filed decisions reproduced** |

If the gap is marginal, "it is a judgment call" stays available and you do not have determinism.

#### The twin pair, the highest-value single edit available

**The most common solver shortcut is lookup transfer beating measurement:** match each candidate to a reference case on a few columns, transfer that case's rate, skip the measurement. The whole ladder above it can be perfect and the solver never touches it.

Kill it by shipping **two calibration cases identical on every column a lookup can see, with outcomes roughly 2x apart.** No transferred rate can then reproduce the file, and the solver is forced to measure.

Three conditions, and the pair is worthless without all three:

1. **Identical on every lookup-visible column**, including the corresponding entry in every document that describes them. One prose line distinguishing the twins and the shortcut survives.
2. **Outcomes about 2x apart**, far outside anything a rounding or window choice explains.
3. **The difference is reproduced by the correct rule from the shipped raw records, and by no rival rule.** This is the half that gets forgotten.

Where an ask names the twin pair, the ask states the construction (the window, the tolerance, the matching keys), and the generator asserts that exactly one pair survives and that the unscoped reading lands somewhere else. "The pair matching on every attribute" isolates nothing when the attributes are identical across the whole family (task55, a literal widest ratio of 7.78 against the committed 1.90).

#### The corpus has to refuse a rival in aggregate, not only case by case

**State the back-test as two numbers, the share of cases the rival misses and the gap on the
corpus total.** A corpus can refuse a rival on individual cases and still reconcile to it in
aggregate, because misses in both directions cancel, and then a solver that checks the corpus
as a total is handed a **false confirmation of the wrong rule**, which is worse than no corpus
at all. task42 shipped exactly that: the cash basis missed one case out of 432 and matched the
corpus total to +0.00 per cent, so a solver read the pilot, concluded the cash basis was the
Fund office's own basis, and defended a wrong figure with the corpus as its evidence.

Two rules follow, and both are cheap:

- **Build the divergence directionally.** A mechanism that pushes some cases up and others down
  nets to nothing on the total. Give the corpus a block that moves one way only (a prior-period
  settlement, an accrual that never reverses inside the window) so the rival's total is out by a
  share nobody can call rounding. Target 10 per cent or more on the total.
- **The corpus must share the operating data's conventions.** If the corpus pays on one timing
  convention and the operating data pays on another, the corpus cannot score the convention,
  and you will not notice, because every case still reproduces under the correct rule. Check it
  directly: count the corpus units on which the two rival rules return different numbers. If
  that count is small, the corpus does not pin the rule, however many cases it carries.

**Never assert a rival-killer with a floor of one.** `misses > 0` passes on a single case and
reads as a pin in the design note. Assert the share, assert the aggregate gap, and state both.

#### Fittability, ship both halves or it is a fabricated intermediate

A calibration outcome that **no rule in the pack reproduces** is not a hard case, it is a broken one. It fails review as a shipped number that does not recompute, and it fails as a trap, because the observed solver behaviour is not "measure harder", it is to declare the case unexplainable, use the corpus **ordinally**, and land on the decoy anyway. You spend a round and learn nothing.

When you add a calibration case you are adding **two** things: the summary row, and the underlying records whose measurement produces it. Build the records, then compute the row from them. Assert the full back-test:

> the correct rule reproduces **N of N** calibration outcomes within *x* percent; every rival rule in the swept family misses **at least one** case by *y* percent or more.

State both numbers. That assertion is what converts "my basis is better" into "no other basis reproduces the file".

#### Every rule the answer composes needs a case that exercises it

A rule the corpus never tests is unpinned even when it looks pinned. Two defensible compositions both reproduce every closed case, because none of the closed cases contains the situation, and solvers split on the graded figure while agreeing on the name. This bites hardest on **interaction** rules, how a gate, a window or a floor composes with the main clock, because the main clock is well calibrated and the interaction silently is not.

Audit: list every rule the golden applies and, for each, name the calibration case that would break if you flipped it. A rule with no such case gets a case added to the corpus, not a paragraph of prose.

#### Defeat ordinal agreement

Solvers accept a model that is off by 1.2x to 3x in magnitude if it **ranks** the calibration cases correctly, and they say so explicitly in the trace. Order the cases so any wrong model gets the order wrong, not merely the levels. The twin pair does most of this work: two cases a lookup cannot tell apart, converting 2x apart, have no defensible ordinal reading at all.

#### Thresholds and empirical pinning

**Prefer threshold-free tests.** A test that needs a cutoff you invented is a fork you left open. The strongest form is binary and definitional: a record either was or was not on the governing list on that date. Second strongest: an empirically derived split where the data draws the line.

**Pin parameters empirically, not documentarily.** When the decisive rung needs a parameter (a window, a horizon, a cut-off), the strongest place to fix it is the corpus's own arithmetic: the parameter is recoverable as the unique value that reproduces every calibration outcome, and nowhere else. A column labelled with the convention (`..._measurement_basis`, `projection_convention`) is a **louder** signpost than the prose line it replaced, because it turns the decisive rung into a two-column lookup. But do not simply delete the parameter either: an unpinned parameter with no empirical anchor is a determinism defect and solvers each fit their own and split on the figure. Empirical pinning is the way out of that trade.

**Keep it unsignposted.** The prompt never mentions it. Solvers routinely open the corpus and use it for something incidental while missing the decisive check inside it. That is the trap working.

#### What a corpus can and cannot pin, measured

- **Structural blindness is a construction, not an omission.** Draw every corpus case from a slice where the decisive rule cannot vary, so the corpus scores the rules you want pinned and is arithmetically incapable of scoring the one you do not, and assert it twice: on the structural property itself and by re-running the corpus under both bases case for case (task42). It is legal only where the corpus is blind because the situation never arose, never because the corpus was settled on a wrong reading (task57 v16). A corpus half of whose rows are capped certifies a basis only through the uncapped half, so assert blindness and refusal over those rows (task58 v7).
- **Let the sweepable corpus certify the wrong basis, and put any refusal determinism needs in a second, less inviting corpus**: blindness by policy (provisional runs drawn on the wrong basis by policy, close-outs nothing invites a solver to rebuild) survives Gate C (task56 v4). The exception is a `confirm_surface_read` build, where a corpus that confirms the natural pipeline confirms the answer and is an answer key (task40).
- **Enumerate the classes of rule a solver could adopt, not the variants inside yours**, and assert the corpus refuses each class; a uniqueness proof scoped to your own hypothesis class reads as rigour and settles nothing (task56, a third figure filed from an eligibility class the post-to-award corpus could not score). Enumerate too every mechanism by which a rival can misclassify an observation and assert the corpus holds cases of each, because a corpus can certify a rival you never thought of while looking perfect (task44, 89 of 89).
- **Score rivals charitably and assert inexcusable misses.** Enumerate every discretion the pack files over the settled record (slot limits, materiality floors, deferral language), score each rival under the most charitable composition of them, and assert at every bar at least one miss the discretion cannot excuse. Assert the refusing cases' rival values by name, because an untargeted rival value drifts across retunes, and plant refusals in the direction opposite the answer's mechanism so no historical row demonstrates the answer's shape (task68).
- **An empirical pin is dead unless the corpus observes the rule's input as well as its output.** If the record shows what a constrained period completed and nothing shows what it demanded, every allocation reproduces it equally, and filing the rule instead gets it read and executed. Ship the missing observability (the orders the constraint refused, at the grain it allocates at) so the discipline becomes the unique candidate reproducing the refusals, word every residue no corpus can carry so it is inert before discovery, and run the delete test on each (task64, truth 0 mismatched cells of 3,614 against rivals at 700 to 3,041). A returns or exceptions log is the quiet form of such a corpus, and its months must be free of the pack's other devices.
- **A filed forward-pricing formula invites its own denominator into the calibration**: when the pricing basis is a prior period, give the prior period designed churn against the measurement basis per cell, or the rival calibration fits the corpus as well as the true one (task69, 127/455 against 127/517).
- **A corpus of closed periods has no power over the open tail.** Compute the share of the graded figure that comes from activity after the pack's cutoff, and if it is not near zero, ship that span as an operating artifact published before the freeze rather than leave it to be projected (task47, 17 to 22 per cent of every closed cycle's volume).
- **Check every back-tested baseline against the live case it validates**, and file the availability argument (a period settles N months after it closes, so the latest settled period at a decision is two back), or the back-test scores a different basis from the live figure (task60 v8).
- **A constructed class needs one lookback deeper than the calibration window**, or every early unit looks like a member and the class rate comes out wrong (task56 v4).

### 4.2 The pin, and when you should not have one

**One sentence, in one shipped document, that fixes the decision metric or the scope rule.**

- Lives in a **shipped file**, never in the prompt. The prompt is the highest-authority document in the task and nothing shipped can outrank it, so any prompt sentence that fixes the decision basis, the measurement window or the scoring convention hands the answer over before a file is opened.
- Stated **once**, in one file. Never repeated, never restated, never explained. A load-bearing fact stated in three files is not findable, it is a signpost.
- Written as a **filed fact**, not as guidance. *"Success is measured as X at H. That is the number on the scorecard"*, not *"You should measure success as X, because otherwise you might be misled."*
- **Never justified.** A justified rule reads as arguable and reopens the fork you just closed.
- Buried in operational noise so it does not read as the thesis of the document.

**When not to have one.** Gap 4 builds deliberately ship no pin for the decisive rule, because the absence is the mechanism: the rule is recoverable only from the corpus. That is legal and it is strong. What is never legal is a decisive rule that is neither filed nor empirically recoverable, because then each solver fits its own and the round comes back split on the figure. **Every convention is either pinned in a file or pinned by the corpus. There is no third option.**

Scope rules, eligibility, grain and unit-of-work definitions usually want a filed pin. Method and parameter choices usually want an empirical one.

**What a pin may say, measured:**

- **The pin fixes the basis, never the answer.** Delete the clause and ask whether the answer is still forced: if it is, the clause was handing over the insight; if it is not, it was doing real work (task57 v21, where the second half of one sentence was the whole insight and a response executed it at 94 per cent).
- **The clause names the observable, not an abstract concept**, while naming no file, field or join. A clause that names only a concept ("under standard conditions") and leaves the corpus to operationalise it fails Gate C even behind a 91-of-91 back-test (task44). A clause that defines a term exhaustively is a counter-pin the moment the golden adds a condition the definition omits.
- **A filed formula pins every population its own sentences name**, so filing the arithmetic while leaving the population open is not available: the population is either filed or filed wrong. File the applicability (a defined term) and leave the identification as arithmetic, enumerate the readings the new sentences admit and close each with its own clause, and state the cost, because a filed exclusion turns a discovery rung into an execution rung (task67).
- **A projection is an open fork unless its method is filed or corpus-recoverable.** The test is the judge's: name the shipped sentence a solver violates by taking the other reading. If the honest answer is that the write-up explains why, there is no pin (task57 v20).
- **Build to the stricter judge.** Two judges will classify one fork oppositely, so every layer of the decisive mechanism either violates a nameable shipped statement when skipped or is the unique survivor of a shipped corpus, and the applicability layer (whether a constraint enters the computation at all) always needs the nameable kind, because a corpus can pin a parameter but not a scope question. A chain of small statements at mixed authority, each useless alone, satisfies it at least cost; soften in the same edit any verb that counter-pins the new sentence (task64).

### 4.3 The advocate structure, and the licensed wrong basis

**Every human voice in the pack points somewhere else.** The prompt names a stakeholder holding a wrong position. In-pack notes carry two to four named people arguing for wrong options. **The correct answer has zero support anywhere in the materials.** The sharpest version is the owner of the correct answer arguing against it.

This is social pressure the solver has to overcome with evidence, and it makes the correct answer feel like a contrarian call rather than a default.

**Advocates hold beliefs, not figures.** A voice may say *"we have always ranked these on throughput and I would not change that now"*. A voice may not quote a computed ranking of the candidates on the decision question, because that is the banned artifact in dialogue form. Useful side effect: the burden of making every figure a character quotes recompute mostly disappears, because they are not quoting figures.

**A voice may hold a belief about what the data is like and may argue for a rule, never endorse carrying a particular quantity forward**, because on a build whose answer is a figure the quantity is the decision: a voice that says to carry the measured effect as-is converts an honest transport problem into an endorsed read the task overturns (task43), and a voice that endorses carrying a count forward is a counter-pin the judge quotes back (task57 v20). A factual statement about the past ("the line has filled its places in every cycle it has run") points at the decoy and contradicts nothing. On a build whose answer is a residual, no voice states the naive residual at all, even correctly, because that is the surface read (task56).

**The licensed wrong basis.** The same governing document that carries the pin also states, as a matter of record, that a named authority works from a different basis and will present it at the review. The basis is real, it is legitimately available in writing, and the evidence still refutes it. That is what separates a fair hard task from a gotcha. Keep it to the basis and the endorsement. Do not let the document compute the ranking. A licensed wrong basis is graded wherever an ask asks for it, so the governing document names its population in words that exclude the other reading, the advocate's belief language selects the same group, and the rejected reading is separated so it does not land on the main answer (task43, two readings of one committee basis 14 per cent apart).

### 4.4 The distractors

Every pack ships two or more distractors: files the solution never reads that look relevant, so a solver has to open them and decide whether they bear on the question (same organisation, entities, keys or period, an adjacent measure, a related programme, an out-of-scope register). A completely unrelated file is padding, not a distractor, because nothing about it has to be weighed. Each is named in the task's `metadata.json`; no file name or line in the pack calls it a distractor. A distractor may also be the stronger wrong-basis kind: it looks authoritative, gives a clean wrong answer (correct arithmetic, wrong basis: an outdated year or business unit, a superseded or amended rule, a changed definition) and is ruled out by a shipped fact a careful analyst can quote (a clause, an effective date, a definition, a control total). That kind is the one licensed exception to the ban on shipping a wrong answer to the decision question, and only because it is never the stump: delete it and the build still stumps, its wrongness is a matter of record rather than an error in its numbers, and its answer is neither the correct answer nor the decoy rung 0 lands on. Build rules: `dataset-generation` §8.3.

A large genuine reference document shipped for authenticity is a different thing and is disclaimed in the governing document: *"[Document] is in the folder as background on [topic]; it is not one of our documents and it does not speak to this decision."* The disclaimer leaves the solver nothing to weigh, so it never counts as a distractor.

---

## Part 5. Determinism machinery

Difficulty gets you a stump. Determinism gets you an approval.

### 5.1 Pin authority hierarchy, where most tasks die

**Your pin must sit at or above every counter-pin in the pack.** Authority order, highest first:

0. **The prompt.** Outranks every shipped file and cannot be argued with, which is exactly why no pin and no convention of any kind may live there.
1. Governing standard, policy document, regulatory terms
2. Signed charter, SOW, contract, rate schedule, product terms
3. Decision memo from the accountable executive
4. Data dictionary or codebook, authoritative for **field semantics** only
5. Method notes attached to an operational export
6. Planning thread, notes, informal correspondence

**Two fatal patterns.** The **counter-pin**: a different shipped file states the opposite convention, so the pack argues against your own answer. The **outranked pin**: your pin sits at level 5 and a level-1 document implies the opposite, so a solver that follows the governing document is right and your golden is wrong.

**Fix:** move the pin up the hierarchy, relabel any artifact in-file so it explicitly answers a different question, and delete any endorsement of the wrong basis that outranks your pin.

**A rule stated at two authority levels that agree on one side of the calculation and diverge on the other** is not fixed by adding a sentence to the lower document, which puts it in open conflict with the higher one. Make the situation not arise and assert that both readings return the same figure (task60 v8). **Sweep the pack for sentences quotable against the answer**: grep for the constraint's nouns and for *defensible*, *added*, *raised* and *increased* near them, and qualify every absolute claim with its grain, because a hostile judge quotes them (task64).

### 5.2 The fork grid, asserted cell by cell

List every choice a competent analyst could make differently: window, grain, population, counting convention, treatment of missing values, tie-break, maturity. Build the grid. **Your answer must win in every cell, or the choice must be pinned.**

**Assert cell by cell, never in aggregate.** "The answer wins 8 of 12" is a summary, not an assertion. Each losing cell must be named in the build and mapped to the specific shipped rule it violates: the clause it contradicts, the eligibility gate it ignores, the censoring the dictionary excludes. A cell you cannot map is an open fork wearing a count.

**Maturity and censoring is an axis and it is the one most often missed.** Any rate measured over vintages, cohorts or periods that are not fully observed has two defensible populations, all of them or only the mature ones, and the two can differ by 2x on the same candidate. Pin the maturity convention in one flat dictionary sentence, or prove convergence. Check it even when it does not currently change the winner, because it becomes load-bearing the moment any other parameter moves.

**Test:** for each assumption, ask *"would ten competent analysts, given only these files, all make this choice?"* If no, it is not an assumption, it is a decision, and it must be pinned or the answer must change. A model that did 99 percent of the analysis right and diverged only on one of your assumptions is not a valid stump, it is `underspecified_objective`.

**Axes the grid has to carry, each one a measured death:**

- **Rounding paths** (per line, per day, per entity, per period, per total). Every summary artifact the generator emits pins the paths its lines demonstrate, so the emitter and the golden share one arithmetic, asserted (task70, three pence apart on a penny-graded ask). A strata choice that straddles a rounding boundary is closed by a filed rounding convention, never by pinning the strata (task73).
- **The sign across every window a cohort claim admits**, not only its value under yours (task73, +217 under one window and -72 under the widest natural one).
- **Window terms.** Any window a graded figure depends on is a filed, nameable date that falls in a gap in the records, so neighbouring cutoffs select identical rows; assert the gap (task55).
- **Codings of a filed criterion on a real coded field.** Real public data brings its own conventions, so enumerate the codings a competent solver could adopt and measure the set difference before writing the clause (task57 v20, three of seven tests admitting two readings each).
- **Inclusion readings of a delta or cumulative feed** (latest value, reconciled only, the batch closing the window): assert they converge or violate a shipped sentence, and compute the golden on reconciled values (task44).
- **Tie-breaks on a duplicate mechanism.** File two levels (a date, then an identifier), ship enough distinct dates that the first level resolves nearly everything, and assert the attribution is unique for every case (task60 v5, 31 of 2,718 pairs reaching the second level).
- **Mid-period proration.** Day-versus-month proration never converges at month boundaries, so a mid-period convention is either unpinned or pinned by an enumerable test; move whole periods at boundaries instead (task40).
- **Things never to grade**: the run count of an iteration (a freeze reading and a re-evaluate reading agree on every allocation and disagree on the count, task57 v19), a median on an even-sized set, and a percentage near a one-decimal edge where a count would do (task57 v20).
- **Pin the nuisance axis, never the decisive one**, and remember that rounding cannot absorb a modelling spread: in a bin of width w the maximum clearance is w/2, so re-centring the answer is not a repair (task47).

### 5.3 Convergence construction, the strongest close

**A semantic pin fixes a meaning, and a meaning still has to be operationalised.** This is the
failure that survives every other check, because the pin reads as decisive and the design note
records it as closed. task42 pinned chargeability with "assistance is chargeable for the period
of the household's enrolment in the Project", which is a clean level-2 filed fact naming no
join, no table and no field, exactly as this skill asks. It still admitted four readings:

| Reading | Figure |
|---|---|
| the whole covered period lies inside the enrolment span | 5,746,538.25 |
| the covered period starts inside the span | 6,631,832.46, the golden |
| the warrant clears inside the span | 6,610,873.75 |
| the covered period overlaps the span at all | a fourth |

A 13.35 per cent spread, and a strong solver that reached **every** planted insight still
diverged on it. That is `underspecified_objective`, not stump power, and the signature is
exactly that: the solver performs the decisive move and lands somewhere else anyway.

**The repair is convergence, never a second pin.** A clause naming the field ("charged to the
Project of the enrolment open on the payment's coverage_start") closes it and simultaneously
turns the decisive rung into a two-line lookup, which trades a Gate C failure for a Gate F one.
Build the records so every reading selects the same rows instead: in task42 every certifiable
payment's covered period **and** its warrant date were made to lie wholly inside one enrolment
span, and all four readings then returned one figure on identical line and household counts.

**The check, and run it on every interval the answer touches.** Enumerate the readings a
period-shaped clause admits, compute each one, and assert they are equal, in the generator and
again in the independent verifier. Two specific boundaries generate almost all of these and
both are easy to miss because the natural join hides them:

- **The far edge.** An as-of join keyed on entry ignores the exit entirely, so a covered period
  running past the exit still resolves to the exited enrolment. Check the covered period
  against the span the reading itself selects, not against any span.
- **The gap.** Between one enrolment closing and the next opening the entity is enrolled in
  nothing, and a backward as-of join silently attributes that gap to the enrolment that closed.

**And never write "the figure is identical either way" without an assertion behind it.**
task42's write-up carried exactly that sentence about the warrant key while the two keys
differed by USD 20,958.71 on 113 lines, and the review found it, which converts a convergence
claim into evidence that the author never controlled the fork.


Where an ambiguity cannot be fully closed, engineer the data so **both defensible handlings give the same answer.** *"Reattributing the transferred units to the party that produced the measurements, or dropping them as unattributable, returns the same winner either way."* This closes the fork by construction rather than by argument and it is unanswerable in review.

**More convergence by construction, each measured:**

- **Integerisation on a forward quantity is unpinnable by any corpus of observed outcomes.** Make every discipline return the same integers by aligning the quantised units with the capacity constants (whole bundles sized from divisors of the conversion constant), and assert that floor, round, largest remainder and no integerisation coincide (task64, six tie-breaks spanning $6,700 before the repair).
- **Build convergence at the grain of the finest pool a solver could defend.** De-meaning a control side as one group leaves its subsets drifting; de-mean inside each subgroup, and set each group's measure equal across periods so differently weighted aggregations agree (task43, 5.4 per cent between two control pools).
- **Close silent sweep forks in the data**: the end-day convention and the order of same-day events at a limit converge once no event ends on a day another lands in the same unit and events are unique per day within a unit (task57).
- **Convention robustness and grid separation are different sensitivities, tuned separately**: convergence is bought with sample density at the quantile, separation with the size of the block each rung moves (task44).
- **Re-sweep every separation after closing a fork**, because a separation can be borrowed from the defect the fork carried (task44).

### 5.4 The robustness sweep, stated with counts

- "Holds across N of N combinations of choice A x choice B x choice C, narrowest margin 1.16x."
- "Holds at inclusion floors of 1, 5 and 25."
- "Holds on both the record basis and the constructed-unit basis."
- "Holds on both periods, and with the largest rival excluded entirely."

**Sweep the whole family and state the count you actually ran.** Rival-killers are audited as hard as the answer. If you claim seventeen alternative rules were tested, run seventeen, and report the **worst** miss across the family, not the average.

A monotone classifier family (drop addresses held by more than t persons) must cross the answer at some t: put the crossing at an unnatural value, assert every round threshold lands at least 10 per cent off, and make the corpus refuse the whole family; sweep string heuristics on an entity exactly like columns (task58). Before claiming N rival readings, test each against a careful read of the clause, because claiming rivals the wording already excludes is the overclaim a hostile reviewer turns into "the difficulty is semantic" (task44).

### 5.5 Construct the disagreement, it does not emerge from independent draws

If a rung turns on **two axes disagreeing** (measured by date versus by period label, per-record versus per-entity, gross versus net, cohort versus calendar) then the generator must **build the correlation that makes them disagree**, per candidate. Draw the two axes independently and every candidate ends up with near-identical profiles on both: the mechanism is documented, findable and inert.

Build it, then assert it in both directions. The design intent is usually "the winner looks slow on axis A and fast on axis B, the decoy is fast on both", and that sentence has to appear as an assertion, not only as a paragraph. Put decoy instances of the construction where they change nothing as well as where they decide everything, or the constructing field becomes the giveaway column no anti-signpost grep sees (task60 v4, 29 spring executions of which 16 were load-bearing).

### 5.6 The assertion regime

**Rules that live only in prose get broken by a later parameter tweak, and nothing in house rediscovers it.** A submission is expensive, assertions are free.

**Compute forward, never backward.** Build the data, then compute every figure from it by script. Never author a number and reverse-engineer records to hit it.

Assert, at minimum:

- each rung's winner **by name**, and each rung's margin
- the ground-truth position table, rank and distance from the leader, every rung
- discriminator dominance, both ratios and their product
- the calibration back-test, N of N within x percent, each rival missing by at least y percent
- the fork grid **cell by cell**, each losing cell mapped to the shipped rule it violates
- the rival sweep count, the number of alternative rules actually tested
- every graded numeric answer's distance to the nearest rounding boundary
- the generation tells: no headline total on a round boundary, no share that is an exact round figure
- the anti-signpost invariants: each load-bearing fact appears in exactly one shipped file
- the input-pack gates: file count, format count, the row count of the largest dataset

Target **40 or more assertions**. A build that only asserts the answer is not verified.

**Ship an independent verifier** that reads only the shipped bundle and no generator state. If it cannot recompute a figure, that figure does not exist.

**Generator disciplines, each one a build that shipped wrong without it:**

- **Assert agreement between the generator and the golden**, not only within the generator: any structure the design depends on exists in the shipped records, not in a variable (task56), and the extract-date cut is applied at source, never at pack-write time (task60).
- **The generator's ground truth is the projection a solver can make**, not the realised value it knows (task56 v4). Run the golden deliverable script against the shipped bundle before anything else, because it is the first solver.
- **Build the verifier first and treat a disagreement as the measurement**: the strongest evidence a stump is live is your own verifier, written before the mechanism existed, falling into it (task60 v5).
- **Build the ladder by construction and let the seed decide texture only**, because a which-of-N ladder whose decoys are sums of a few hundred random records rides on sampling noise and a seed sweep is a lottery (task56 v4). Use one RNG stream per period, so a parameter change in one period does not re-roll the graded one (task69).
- **Read shipped constants from the single definition the model implements**, derive parameters from the record rather than stating them, and check the rounding distance and adjacency of every ordered pair on every redraw, not only the top two (task60 v8, task73). Measure a one-decimal figure's distance to x.x5, not to the hundredths (task55).
- **A column whose rows and whose total row are computed different ways**, and a rank or share that does not say whether it runs on the rounded or the unrounded value, are defects the generated rubric charges for: assert both in the verifier, rebuilt from the unrounded source (task60).

---

## Part 6. The draw, then the generators

### 6.1 The draw comes first, before the ladder

**A trap recognisable from its shape has already lost.** Solvers primed on similar problems look past familiar surfaces, and a reviewer who can match your task to a delivered one by domain plus stakeholder role plus artifact type has found a clone.

Every approved build in this repo opens its design note with a draw table checked against the previous builds. That is not documentation, it is the step that produced the build. Do it first, write it down as a table, and let it constrain everything downstream.

**Run the fingerprint guard first** (`../fingerprint/SKILL.md`). `guard.py recent` shows what the last builds spent and `guard.py coverage` shows what has never been drawn, each in one screen. The bans below are unenforceable without a record of which pattern carried which build, and the cards are that record: write your draw as a card, run `guard.py check` on it, clear every BLOCK, answer every WARN in the design note, then `guard.py register` it **before writing the ladder**. A card filed after the fact is a card the next build did not get to use. The card records identity only. The portal outcome goes in `references/shipped-ledger.md`, one row written when the author reports it, never a `drawing` row. A row is rewritten in the same edit as the abandonment of the version it describes, because a row describing a dead version disables the pattern ban for every build drawn after it (task89), and any multi-label cell, on a card or in the ledger, states the decisive gap and pattern first, because the screens normalise a multi-label cell to its first label (task55).

**Then open `references/proven-in-production.md`.** The ledger tells you which pattern and calibration form are spent; that file tells you which of them ever worked and on what property. Draw against both. Two checks belong here rather than after the ladder is written: nothing you are about to draw appears in its Part C, and the discriminator named in its Part A for the strategy you are taking is one you can build in this world. If you cannot build the discriminator, you are drawing the pattern without the thing that makes it bite, and the draw is the cheapest place to find that out.

**Draw each dimension independently.** Do not let one choice drag the others toward a familiar combination.

| Dimension | Draw from |
|---|---|
| Gap | time · population · objective · rule (Part 1) |
| Pattern | A past-vs-forward · B recovered rule · C serviceable share · D two grains · E conditioned yield (Part 2) |
| Domain and subdomain | one you have not used recently, then an unusual sub-function inside it |
| Objective | one of the eight, preferring one not shipped recently; Forecasting is the tiebreak |
| Monetisation or scoring unit | per active unit per period · per accepted item · per settled transaction · per boarded entity · per episode · per certified output · per covered member · per resolved case · index points · units served · flat per seat · take-rate on flow |
| Decision type | which one of N to fund · which to launch · which to fix · renew, replace or lapse · which root cause · which template to standardise on · which to deprioritise · a structural verdict with no candidate list at all |
| Stakeholder role | an operations director · a capacity planner · a portfolio manager · a research desk · a statistical office head · a field unit lead · a programme officer |
| Calibration form | settled-transaction ledger · counterparty acknowledgement · pilot log · existing-book actuals · prior-period close-out · retry or revision log · parallel-run overlap · gold-standard verification subsample |
| Context-artifact type | monitoring export · operations log · register · published series · capacity report · close-out summary |
| Generator pair | two from 6.2 in **different** families, optionally a third |
| Rival-killer | one from 6.2 that is not in your main pair |

**The similarity test.** Strip the numbers and the names. Would this read as the same puzzle as anything already built? If the gap, the pattern and the decision type are all repeats, it is the same puzzle wearing new clothes.

**Standing bans.**
- Do not reuse the **domain plus objective pairing** from your last build. Either axis alone may repeat, both together is the same task shape.
- Do not reuse the **pattern that carried the decisive rung**.
- Do not reuse the **calibration form**.
- Do not reuse the stakeholder role or the context-artifact type.
- Do not reuse a spine dataset across consecutive builds.
- Do not reuse the **prompt shape** of either of the last two builds, because the shape shows in the prompt's wording and in the deliverables.
- Vary the answer type. A renew-replace-lapse disposition, a which-of-five pick and a structural verdict feel completely different to a solver even on the same mechanism.

**The objective is assigned, not drawn.** Choose the Axis 1 tag at the draw against the graded quantity's tense (a forward-facing committed figure reads as Forecasting to a reviewer even when nothing is estimated), keep it through every rebuild, and where a mechanism only works under a different objective, ask the author rather than retag (task56 v4, task55). Run `corr(decisive measure, unit size)` at the decision grain before committing to a world, because a world where the two track each other cannot hold a ladder (task57, +0.982 in the dead world against -0.373 to +0.294 in the redraw).

`guard.py check` enforces every ban above against the **last three builds**, not only the last one, because builds are often drawn two or three at a time and a reviewer reads them as one batch. It runs the similarity test against the last twelve, asks for a one-line differentiation where gap, pattern and decision type repeat an older build, and compares the driver sentence against every driver on file, including retired architectures, so a reskinned clone with no surface overlap is still caught.

### 6.2 The generators

These are **mechanisms, not examples.** Each is a machine for producing a rung. For each: **Asks** (the question the rung turns on), **Flip** (what changes the ranking), **Build** (the recipe), **Findable** (how the solver can discover it, mandatory or the task is unfair), **Draw axis** (the dimensions to instantiate it along, which is where your scenario comes from).

Instantiate along the draw axis. Do not ask for an example, because an example is a scenario and a scenario is what you must not reuse.

**G1 · Unit-of-value swap** · gap 3
- **Asks:** what are we actually paid on, or constrained by?
- **Flip:** a headline size metric that is 5x to 20x the monetisable metric, ranking candidates differently.
- **Build:** fix the revenue or capacity model in a terms, rate or product file. Give the naive metric a large lead in the natural pipeline. Verify the correct unit flips the ranking cleanly.
- **Findable:** the business-model clause in the prompt's first sentence plus the rate schedule in the pack.
- **Draw axis:** which two quantities both read as size; how far apart their ratios run across candidates; whether the correct unit is a count, a weight, a duration or a settled amount.

**G2 · Grain mismatch** · gap 2
- **Asks:** what is *one* unit of the thing being decided?
- **Flip:** the natural aggregation is at the record grain; the decision funds one unit at the operating grain.
- **Build:** establish two grains that both look reasonable. Ship a membership or roster file that maps one to the other. The operating grain must be recoverable via a join, not signposted.
- **Findable:** a roster or mapping file plus a scope clause naming what one unit of work is.
- **Draw axis:** which two grains; whether the mapping is many-to-one, one-to-many or both; whether the mapping file is a roster, a crosswalk or a membership history with effective dates.

**G3 · Record versus operation** · gap 2
- **Asks:** the record says party A owns this, but who actually did it?
- **Flip:** a label field is stale or administrative; physical evidence shows a different party carried the activity.
- **Build:** ship a label column and two or three independent physical signatures of the true owner. Independent corroboration is what makes this fair rather than a guess.
- **Findable:** the signatures agree with each other on exactly the same set of records.
- **Draw axis:** what the signatures are (identifier ranges, routing evidence, a behavioural profile that shifts on a dated event); how many of them; whether the label is stale, administrative or aspirational.
- **Caution:** on its own this reads as a lone defect flip. Frame it as the label being correct at its stated meaning and the decision needing a different one, and never let it be the only mechanism.

**G4 · Attribution at transition** · gap 3
- **Asks:** who holds it now?
- **Flip:** historical rows still name the original owner; a transition moved it, and the decision scopes to current holders.
- **Build:** include a transition marker in the operational file. Ship a scope rule limiting the decision to holdings at a named date.
- **Findable:** the transition code is defined in the documentation; the scope rule is in the governing document.
- **Draw axis:** the transition type; whether it is instantaneous or phased; whether the scope date sits before, during or after the transition window.
- **Caution:** sub-period misattribution cannot carry a decisive rung on an annual figure, because under an effective-dated join only the straddle sliver misattributes and effective dating is the solver default; move whole periods at period boundaries instead, with output conserved so no series steps (task40).

**G5 · Provision elsewhere** · gap 3
- **Asks:** is the need already being met by someone outside the record you are looking at?
- **Flip:** the naive gap counts absence from one provider's books; a second provider layer covers that gap **asymmetrically by category**.
- **Build:** ship a second layer whose coverage is dense for the decoy category and near-zero for the winner. The asymmetry is the whole trap.
- **Findable:** a type or classification lookup identifying which entities exist to serve others, joined to the capacity file.
- **Draw axis:** what the second layer is; how the asymmetry is distributed; whether it is visible as capacity, as agreements or as historical flow.

**G6 · Composition shift** · gap 2
- **Asks:** did the population change underneath the metric?
- **Flip:** a pooled rate moves one way while the standardised rate moves the other.
- **Build:** move mix share between bands substantially, driven by a documented cause. **Make the within-band moves non-uniform**: if every band moves the same direction, a solver rescues the answer by inspecting bands and standardisation is never load-bearing. One band must move against the others.
- **Findable:** a segment field plus a documented event explaining the mix change.
- **Draw axis:** which dimension carries the mix; the size of the share move; which band moves against the others; whether the reference population for standardisation is pinned or convergent.

**G7 · Operating window** · gap 1
- **Asks:** when can this physically happen?
- **Flip:** annual or cumulative totals are irrelevant because the work can only occur inside a bounded window.
- **Build:** pin a physical constraint in an operations or catalog file. Make annual totals rank one way and window-scoped totals rank another. The winner should be a candidate whose activity is concentrated in the window while rivals' is spread.
- **Findable:** the window in a memo section plus the physical precondition in a catalog or spec file.
- **Draw axis:** what bounds the window (season, calendar, licence, crew, cutover); how concentrated each candidate's activity is; whether the window is fixed or negotiable.

**G8 · Reachability versus magnitude** · gap 3, pattern C
- **Asks:** can we actually move it?
- **Flip:** the largest gap is unclosable; the closable gap is third-largest.
- **Build:** make the natural pipeline rank by size of problem. Give the biggest problem a structural ceiling. Give two higher-value rivals apparent reachability that dies when yield is conditioned correctly.
- **Findable:** a mechanism document explaining what can and cannot be recovered, plus an attempt log to measure yield.
- **Draw axis:** what makes the biggest problem unreachable; whether the ceiling is physical, legal or contractual; whether reachability is binary or graded (prefer binary).

**G9 · Downstream survival versus upstream acquisition** · gap 1
- **Asks:** is the measured outcome the same as the acquired outcome?
- **Flip:** the channel that acquires fastest retains worst, and the decision is scored on the retained figure.
- **Build:** pin the success metric to a downstream horizon. Split a survival property by an **upstream class**, which is the join the solver must make. Make the candidates' class compositions extreme and opposite.
- **Findable:** the class field on one file, the survival mechanism on another, joinable on a shared key.
- **Draw axis:** what the upstream class is; the horizon; whether survival is measured as duration, as a rate or as a realised amount.

**G10 · Cross-dimensional duplication** · gap 2
- **Asks:** what is one real-world unit?
- **Flip:** the natural sum runs across a dimension that double-counts entities; the unduplicated figure changes the ranking, not just the magnitudes.
- **Build:** the dictionary must state the grain so the sum is provably not an entity count. Ship an authoritative unduplicated extract elsewhere, unnamed in the prompt. Make one candidate's inflation factor far larger than the others'.
- **Findable:** a grain statement in the dictionary plus an unduplicated summary file.
- **Draw axis:** which dimensions multiply; how the inflation factor varies across candidates; whether the unduplicated extract is a summary, a distinct-key file or a reconciliation.
- **Caution:** same as G3, never the only mechanism, and framed as right-number-wrong-question.

**G11 · Eligibility precondition** · gap 3, `binding_constraint`
- **Asks:** is the leader even in the candidate set?
- **Flip:** a hard floor, cap, band or gate disqualifies the naive winner before scoring begins.
- **Build:** every candidate must be evaluable against the constraint and the naive winner must fail it. The constraint must be **non-optional**, a filed eligibility rule or contractual floor rather than a soft preference, so it cannot be argued past.
- **Findable:** an eligibility export, a terms clause or a rate-card note.
- **Draw axis:** what the gate is; whether it is a floor, a cap or a band; whether it binds on one candidate or on several; what quantity its bindingness is arithmetic over.
- **Caution (task89):** the predicate has to be a **quantity**, never a **status word**. Gate C forces the predicate to be filed, and a filed status word (certified, licensed, accredited, in force, approved, bonded, eligible, registered) names the entity that holds the status, which names the register that dates it, so the identification is one as-of join for any reader who asks the question the word itself raises. Burying the date one entity deeper does not help, which is why *a certification* is not on the draw axis above. A gate carries a decisive rung only where its bindingness is arithmetic that no file states at the gate's grain.

**G12 · Absence of record versus record of absence** · gap 2
- **Asks:** does a blank mean zero, or does it mean nobody answered?
- **Flip:** treating missing as zero produces an enormous gap; treating non-response as unknown collapses it.
- **Build:** create **structured** non-response: whole jurisdictions, periods or reporting groups that never filed the field. Ship a rollup that reconciles **only when blanks are left blank**, which is the proof. The winner then requires a second correction after this one.
- **Findable:** the reconciling rollup plus visible block structure in the missingness.
- **Draw axis:** what structures the missingness; how large a share of the population it covers; what artifact proves the convention.
- **Caution:** same as G3 and G10.

**G13 · Horizon mismatch** · gap 1
- **Asks:** which period does the decision actually cover?
- **Flip:** cumulative or multi-period potential against a single named cycle; retrospective actuals against a prospective window.
- **Build:** put a specific horizon phrase in the middle of the prompt. Make cumulative totals large and obvious and horizon-appropriate totals require re-scoping. Ship a delivery history showing that comparable prior commitments landed one unit per cycle.
- **Findable:** the horizon phrase plus a delivery-history file.
- **Draw axis:** the cycle length; whether the mismatch is cumulative-versus-single or retrospective-versus-prospective; what the delivery history is a history of.

**G14 · Conditioned yield** · gap 2, pattern E
- **Asks:** does the observed success rate apply uniformly, or does it depend on a property of each case?
- **Flip:** a pool that looks recoverable in aggregate has near-zero yield for one subgroup, and rivals' pools concentrate there.
- **Build:** ship an attempt log where the split is **absolute and self-evident** and confounders are controlled by construction, so the failing and succeeding attempts share operators, sites and timing and only the property separates them. Threshold-free: the data draws the line.
- **Findable:** the attempt log joins to the pool records on a shared key; the split is visible on a one-line group-by.
- **Draw axis:** the conditioning property; whether it is a record attribute, an age, a class or a provenance; how concentrated each candidate's pool is in the dead subgroup.

**G15 · Evidence-standard exclusion** · rival-killer, not usually the main rung
- **Asks:** can the rival's claimed number even be computed from what shipped?
- **Flip:** a rival's figure is real, reproducible from its own export, and structurally impossible as the quantity it names.
- **Build:** prefer **structural impossibility over contested statistics**. The cleanest form is a calendar contradiction: the comparison window the rival's memo names does not close until after the memo's own publication date. Second cleanest: the governing document carries an evidence clause requiring figures be computable on records this evaluation can examine, and the rival's population ships no such records.
- **Findable:** two dates in two shipped files, or one clause plus a file inventory.
- **Why it matters:** rival-killers get audited as hard as the answer. One that rests on a number you cannot reproduce fails review outright.

**G16 · Method selection** · gap 4, `method_or_model_selection`
- **Asks:** which approach is this data entitled to support?
- **Flip:** two or more defensible methods are available, they disagree on the answer, and exactly one survives a property of the data the pack makes checkable.
- **Build:** engineer the data so the convenient method is invalidated by something measurable in it, never by a rule you assert. Ship the evidence that discriminates: a holdout the naive method fails, a baseline the complex model loses to, a diagnostic that fails on one method and passes on the other.
- **Findable:** the discriminating property is visible on a plain plot or group-by, and the calibration corpus settles which method reproduces the known outcomes.
- **Why it is strong:** the wrong method is competently executed and arithmetically perfect, so there is no defect to find and no cleaning step that rescues it. This is the family the client asked for most directly.
- **Draw axis:** what invalidates the convenient method (a level shift, a short history, a leaked split, a mixture, an intermittent series, a calibration-versus-discrimination gap); what the discriminating evidence is; how far apart the two methods' answers land.
- **Caution:** check the basis spread before building any method-selection rung, because a rate-model choice cannot carry a figure separation: shrinkage is mean preserving on the fit population, so the spread from unsmoothed to fully pooled is bounded by the weighted covariance between forward exposure and each cell's lift, about 8 per cent on an honest world (task60, six tuning passes never past 8.7). Decide whether the model choice carries the figure or the asks. A wrong basis is a rule violation, not a defensible reading, when the criterion is filed, so the separation floor does not apply to those cells; and the criterion's grain decides which basis wins, so sweep every grain a solver could score at. A shipped back-test over an enumerable model class is an answer key however wide the fit gap (task38), and a one-parameter rule is beaten only by an excluded set non-monotone in every scannable column (task40).

**G17 · Statistical rigor** · supporting mechanism only
- **Asks:** does this difference survive the uncertainty around it?
- **Flip:** the point estimate ranks the candidates one way, and the property governing whether the estimate means anything ranks them the other way, or refuses to rank them at all.
- **Build:** pick one axis and make it decisive, with the arithmetic built rather than asserted. Power: the sample can only detect an effect several times larger than the one observed. Confidence: the leader's interval straddles the decision boundary while a lower point estimate sits entirely on one side. Multiple comparisons: ship the full comparison set so the count is recoverable. Regression to the mean: ship the pre-selection distribution so the expected drift is computable. Confounding: the association collapses once a shipped variable is conditioned on.
- **Findable:** every input the test needs is in the files, including sample sizes per arm and the full comparison set rather than the winner alone.
- **Determinism note:** this family is where knife edges hide. The blocking quantity has to clear or fail its boundary by a stated margin, or two solvers using slightly different conventions split on the verdict. Assert the distance to the boundary.
- **Gate note:** not on Gate G's explicit pass list. Pair it with one of the seven.

**G18 · Correct number, resisted over-correction** · `confirm_surface_read`
- **Asks:** is the reported figure actually wrong, or does it only look wrong?
- **Flip:** the headline number is **right**, the pack is full of plausible reasons to adjust it, and every adjustment moves the answer away from the truth. The naive solver corrects and lands on a wrong candidate; the correct answer is to leave the figure alone and say why.
- **Build:** ship three or four adjustment invitations that each look like a defect and each turn out legitimate on inspection: a duplicate-looking key that is a real repeat event with its own identifier, a gap that is a documented decommissioning, a denominator that changed because eligibility genuinely widened with the rule change filed and dated, a spike that is a documented seasonal or promotional event. Then ship the reconciling artifact that only balances when the figure is left as reported.
- **Findable:** the reconciling total, plus the one document per invitation that explains it as legitimate. Neither alone is sufficient, which keeps it behind a join.
- **Why it is strong:** solvers have been trained by years of planted-defect tasks to hunt for a break and adjust. This turns that competence into a wrong answer and it cannot be solved by cleaning harder. It is the exact inverse of the banned shape and the judge gives it its own pass label.
- **Where it dies, and it has died every time it was tried here:** the unadjusted figure is what the natural pipeline produces and what a solver who checks each invitation keeps, so it catches only a solver that adjusts without checking, and the top responses check. task38 v2 was retired after four solves, task40's confirm draw was solved twice in round 1, task62 s.29 was solved on its first round by the natural pipeline, and task87 v6b was filed by both top responses on the portal. A confirm rung earns a draw only where the natural route lands somewhere other than the unadjusted figure; write that route into the design note before the draw is registered.
- **Determinism note:** the burden is heavier than usual. Every invitation needs a shipped document making it legitimate, or a solver who corrects it is right and your golden is wrong. Sweep every combination of adjustments and assert the unadjusted figure is the only one that reconciles.

**G19 · Contract conformance** · `etl_conformance`
- **Asks:** does the output actually satisfy the spec, or does it merely look right?
- **Flip:** a plausible headline figure is reachable by shortcuts (dropping the hard rows, approximating a conversion, inner-joining past the unmatched records) while the conformed table violates the contract. The correct path produces a different figure **and** a table that passes every stated check.
- **Build:** ship the target schema, grain, types and required outputs as a real contract, or deliberately withhold it so the canonical shape has to be derived from the sources and domain convention. Make the shortcut attractive: an inner join that silently drops unmapped codes should land within a few percent of a plausible answer. Put the decisive difference in the rows a shortcut discards. Reconcile row counts at every join so the discrepancy is discoverable.
- **Findable:** the contract, plus a control total the conformed table must hit, plus the orphan rows themselves.
- **Determinism note:** state the grain, the type of every key, and the treatment of unmatched records in one file. Conformance traps split on the figure faster than any other kind when the target shape is left implicit.
- **Strip the join key the solver would use and file the fact that makes the natural key wrong**: a remittance file with the donor key and the remitting account but no pledge id, plus a filed takeover, drops 5,455 lines silently from the safe-looking join (task56 v4).

### 6.3 Composition

**Stack two to four generators from *different* families, and from different gaps.** One generator: a single correction defeats it. Two to four: each partial insight lands on a different decoy, and only full synthesis reaches the answer. Five or more: machinery, not insight.

**Same-pattern stacking does not count.** Three grain mismatches at three aggregation levels is one generator in a trench coat.

**The decisive rung must sit in a gap that is not the one carrying rung 1.** If cleaning is rung 1 and the decisive rung is also a population question, the ladder has one idea in it.

### 6.4 Hold as the answer

**"Not enough information to make a decision" is an acceptable final answer**, and under v3 it is one of the wanted shapes (`signal_vs_noise_or_hold`). It is not a hedge, and the difference decides whether the task passes.

A hold is a **determinate answer**: every competent analyst who does the work lands on it, for the same stated reason, and the reason reproduces from the shipped files exactly like any other rung. The ladder is unchanged. Rungs 0 through 2 still name specific wrong candidates. The final move refuses **every** candidate on the same evidentiary standard.

| Requirement | Why |
|---|---|
| The hold is **forced by a computed quantity**, not by absence | "The interval spans the decision boundary", "the gap is smaller than between-slice variation", "the test has power to detect only 3x the observed effect". A hold justified by "the data is unclear" is a hedge and fails. |
| The **blocking quantity reproduces** from the shipped files | It is graded like any other number. Assert it and assert its distance from the boundary it fails to clear. |
| **Every candidate fails, and you can name why each fails** | If two fail and one is merely unproven, the answer is that candidate, not hold. |
| The prompt **licenses a non-pick without advertising it** | "Name the single candidate to fund, or state that none should be funded this cycle." That is a licence. "Tell me whether there is enough evidence" is the answer wearing a question mark. |
| A **naive path still commits to a named candidate** | If the natural pipeline already looks inconclusive, solvers hedge from the start and the task grades as ambiguous rather than hard. |
| The **hold is falsifiable** | State in the design note what would have made it a pick: the sample size, the interval width, the margin. |

Grade the blocking quantity, not the verdict. A trace that says "the evidence is mixed, so I recommend waiting" without computing the blocking quantity has not solved the task.

---

## Part 7. The prompt

**Prompts do not carry difficulty, evidence packs do.** A short prompt with a well-built pack stumps reliably. What the prompt has to do is state the decision, demand a commitment, and specify the deliverables precisely enough that every requested figure is gradable.

### The shape

The prompt is **prose**, first person, the way you would write to a colleague, with no bracketed
blocks, family-tagged headers or bulleted asks.

**No skeleton is prescribed.** Every prompt has to feel different in voice and structure, and a
fixed order (context in two or three sentences, then one paragraph per deliverable) is what makes a
batch read as one template.

What the prose has to **contain**: first person with the role somewhere in it, what
forces the call now, the standard where the pack does not carry it, one to three named files, and
every figure's unit and rounding inside the sentence that asks for it. What order it arrives in,
where the role sits, which file is commissioned first and how long the whole thing runs are all
yours to choose per build. The twelve opening moves, the requirement-against-carrier table and the
batch check live in `../guide-to-prompt/references/prompt-voice.md`, and the check is
`../guide-to-prompt/references/voice-check.py`.

**One to three deliverables, and three is the ceiling**, so a four-file set is a spec failure. One
file is legal, two is the observed norm. Build at the low end: every deliverable has to agree with
every other on every shared figure, to the same rounding, and that cost compounds with each file.

**No format family is assigned.** Data (CSV, TSV, JSON, XLSX, Parquet) · Visual (PPTX, PNG, SVG,
HTML, JPG) · Text (PDF, DOCX) · Code (PY, IPYNB, SQL, R) describe what a file is *for*, but
nothing requires the set to span two of them and nothing assigns you a pair. Pick the one to three
files a real analyst would produce for this decision, and be honest about it: an
`analysis_report.pdf` is not the best-suited deliverable for every task.

**Prioritize a visual where it makes the decision read at a glance.** Not mandatory, but it is
what a stakeholder reads first and it is one of the cheapest honest routes to a wide rubric,
because naming a chart's parts is worth five to seven criteria where "include a chart" is worth
one. A table can live inside the memo, inside a workbook, or be printed by a script rather than
taking a slot of its own, and with a ceiling of three, slots are scarce.

**The committed call is forward facing by default.** The retrospective recommendation is the shape
the strong models have learned to handle, so the Main Recommendation Ask commits to a quantity
about a window that has not closed, and a retrospective ask needs a reason written into the design
note. It changes the ask, not the tag:
the objective stays whatever the analyst actually has to produce, and retagging a build as
Forecasting because its window is forward is a rejection risk.

**The asks are uncapped and untargeted, and each one has to be multi-dimensional and hard.** One ask
should span many rows, periods or cuts and still resolve to one defensible answer. "Every
shortlisted candidate ranked worst first, its score, and whether it clears the gate" is one
sentence and thirty criteria; "give me the score for candidate four" is a lookup and belongs
nowhere. A multi-dimensional ask fails **everywhere at once** under a wrong analytical path, which
is exactly what makes it discriminating.

**Every figure's unit and rounding has to be covered**, and the default carrier is a convention
stated once rather than a tag on every clause. A figure whose precision is
not settled is a Gate E finding, because two correct solvers format differently and only one
matches the golden. What settles it is either the block convention or an explicit pin, and the pin
is required on every derived quantity (a share, an average, a rate, a ratio, a counterfactual, a
difference in points) while a count of discrete things in the shipped data needs none. Tagging
every clause is `../reduce-house-fixes/SKILL.md` H12, and
`../guide-to-prompt/references/prompt-economy.md` carries the repair.

**Every figure inside an ask is separately gradable and separately determinate**, so an ask
spanning ten rows on three measures owes thirty determinate answers and each is graded on its own.

**Where the 25 criteria come from is a design decision you make first.** A one-to-three file
prompt is a small surface, so the criteria come from the **structure of the answer**, which has a
name: the prompt shape. Pick it from `../guide-to-prompt/references/shapes/README.md` before the
ladder is drawn, size its arithmetic on paper, and read that shape's "what makes it hard rather
than long" section, because that section is the seam where the shape meets this skill.

### Worked shapes live in guide-to-prompt, three ways

`../guide-to-prompt/SKILL.md`, "The same contract, three surfaces", shows the contract three ways
on one decision, `../guide-to-prompt/references/prompt-voice.md` carries the twelve opening moves
and the carrier table, and `prompt-economy.md` carries the budget. Never paste a fixed opening
("I run `<function>` at `<organisation>`", "write it up as", a rounding tag on every figure),
because a batch built from one skeleton reads as one template.

What carries the criteria: **one ask covering every option
on several measures at once**, which is where the bulk of the rubric lives; the committed call
quotable as one whole sentence; the chart's parts (series, ordering, the threshold at its value,
the annotation, the title's content) named in one sentence; and no sentence fixing a basis, a
window or a population.

### Prefer artifacts a script produces

Where a deliverable can be **generated by code rather than written**, make it so. A chart rendered by a plotting library, a workbook written by a script, a conformed CSV emitted by a pipeline: none of these can read as LLM-generated text, all of them recompute from the pack, and the reviewer can rerun them. This is the cheapest available defence against the "obviously LLM-generated, rejected" failure.

The practical pairing that satisfies every constraint at once, at two files: **one deliverable that commits to the call in prose and carries the numbers at an explicit grain inside itself, and one the script renders.** A chart asked for inside a text deliverable is still produced by the script, not described in prose. Where a third slot earns its place, the script itself becomes the deliverable and **prints** the graded figures rather than merely emitting them, which is the cheapest criteria-dense file available and the one that cannot read as LLM-generated.

### What Context plus Main Ask has to contain

No order is prescribed and no component has a fixed sentence. The moves are in
`../guide-to-prompt/references/prompt-voice.md` and the budget (about 250 words, about 24 words a
sentence) is in `prompt-economy.md`.

1. **A real person behind it**, first person, with the role somewhere in the context and on most
   builds not in the first clause. The organisation's business model gets a clause only when it is
   the decisive constraint in disguise, fixing the monetisable unit without naming a metric, and
   then it is one clause.
2. **The forcing event and the scope**: what makes the call now, and the candidate set when the
   decision is one of N.
3. **At most one stakeholder belief, as one clause**, stated as a belief and never as a computed
   ranking. A second belief makes it the roll call banned below; the full advocate structure lives
   in the pack's social layer (`dataset-generation` §8.2).
4. **The commit demand, as one whole sentence a reader can quote**, forward facing by default. If
   the answer is a hold, the licence goes here and nowhere else, as one option on the same footing
   as the candidates.
5. **Nothing else.** No pack hand-off and no pack inventory, because the pack is attached where the
   solver can see it, and no organisation bio.

### Delete on sight

- **Any sentence that fixes the decision basis, the measurement window, the scoring convention or the population.** The prompt outranks every shipped file, so such a sentence is the most load-bearing sentence in the task and it answers the question before a file is opened. Write the prompt, then read every clause back asking *"does this fix a choice the data was supposed to fix?"*
- The decision metric, the eligibility rule, the fee schedule. Bury these in the data.
- Any **input** file name. Output file names are required and are the deliverable request.
- Any governing standard named by acronym, which is the solver's next search delivered free.
- Any instruction to combine named tables, which is method dictation.
- Any method hint ("compare A against B", "cross-reference the extracts").
- Any word that names the trap: *clean, unduplicated, reconcile, attribution, mix, standardise, reporting-versus-operating, grain*.
- Any signposting that a metric might mislead, and any warning that a view might be wrong.
- More than one candidate metric named as valid, which invites hedging.
- Any roll call of stakeholder opinions, which pre-frames the ladder as a refutation checklist. It is a design problem rather than a style problem: each named opinion is a rung handed over as a checklist of things to refute, so the work of finding the candidates disappears.
- A context that narrates the furniture. First person is the default and the length is yours to set per build, but every extra sentence of scene-setting is another chance to fix a basis, a window or a convention the data was supposed to fix. Cut for leak risk, not to a sentence count, and note that our own prompts run two to three times longer than the client's worked examples.

**What is licensed:** naming one belief a stakeholder holds, as a belief, in one clause; naming the generic threat to validity in the open; naming the operating constraint; naming the candidate set. The line is that you may say **that** the analyst faces a confound, never **which** evidence defeats it.

### The asks carry most of the score, so they carry most of the risk

Only the Main Recommendation Ask has to **stump**, and the stump is half the pass condition and on
the critical path of the average (Part 0). It is not the whole story. The generated rubric puts **30 to 40 per cent** on the recommendation and its
load-bearing components, **5 to 10 per cent** on instruction following (the file exists, is named
correctly, has the required rows, columns, ordering, total row, page length, printed figures), and
**about 55 to 60 per cent on the asks**. So the arithmetic of passing is blunt in both directions:
a build whose trap fires perfectly and whose asks are lookups hands the whole field the ask weight
before it opens a file and the average never gets under 50, while a build with hard asks and no
ladder fails the stump condition and the average together.

**The target is the single strongest response.** The bar averages the **top two**, so the question to ask of every ask is: "**could the strongest solver in the room, the one who cracked the trap, get this**". If yes, it is a free criterion for exactly the response you are trying to hold down.

The deliverable asks carry no stumping requirement, but
every one of them must be deterministic, correct and genuinely difficult, and **difficult means a
wrong analytical path gets it wrong**. That is the single test. An ask a solver can answer
correctly while holding a wrong view of the whole problem is a free criterion for the whole field.
Earn the difficulty from real work, and design it via the `supplemental-stumping` skill, which
carries the ask layer as its own architecture: every ask decoupled from the main call and carried
by planted data-quality devices that never touch the main call's row population, proven devices
reused freely at that layer, the span floor per ask, the **pair ceiling of 40** against a bar of 50,
and the ask-level determinism contract. Never from an obvious intermediate of the main ladder, which hands the
ladder over.

**Multi-dimensionality is the lever that does the most work here, and it belongs on the device-carried asks.** The spec requires asks to be multi-dimensional rather than a litany of basic ones, and that requirement has a natural home. An ask spanning every candidate on three measures is not just wide, it is **correlated**: a solver holding the wrong structure gets all thirty figures wrong together, so one wrong turn costs a third of the rubric instead of one criterion. Put that width on the asks the cracker cannot get right, meaning the device-carried ones, where it costs the strongest response everywhere at once. Width spent on an ask that inherits the main trap is spent on a solver who already holds the corrected structure and gets all of it right. Stacking simple asks does the opposite of both: it decorrelates the block and hands the cracker many small wins.

**The ask arithmetic, measured on generated rubrics:**

- **Score the rubric before hardening anything.** Bucket the criteria into those a solver holds free once it lands the main call, those independent of it, and those needing their own construction, then compute what a response scores if it lands the main call and does nothing else well. If the free block is large, no ladder work reaches the bar (task60 v1, 66 of 100 points free; task55, 85 of 100 downstream of one `score()` call; task56, about 69 per cent from the main call and its forward asks alone). Asks fail on correlation before they fail on difficulty.
- **The denominator drags both top scores down together.** With a rubric of W weight points and the top two responses passing A and B, adding N asks both fail moves the average to `(A + B) / (2 x (W + N))`. task60's pair at 65 and 32 on 87 points crosses under 50 at N = 11 and reaches the 40 target at N = 35, where cutting the stronger response alone looked like it needed far more. It is the lever when the ladder is measured out.
- **Every new ask needs its natural wrong construction computed beside its answer**, because an ask with no plausible wrong answer scores free (task60). Mine scored responses for a root cause rather than a list of misses, and prefer asks that put a shipped file to work for the first time (task60 v7).
- **Keep the asks off the main chain's plumbing.** An ask that exercises the main chain's joins teaches them, and the response that missed the main call still collects it (task57 v21). Assert the decoupling numerically: recompute the whole ask set with the decisive parameter cleared and assert every decoupled answer is unchanged, which is also the over-determination sweep (task55, task57). A counterfactual replay of closed periods under the coming rules is safe to grade only where it points at the decoys (task55).

**Blatantly easy asks get the task rejected** on their own, independent of the main stump.

### Getting the rubric to 25, through the prompt shape

The rubric is generated from the prompt, the golden and the requested files, and a task under **25
criteria does not advance**. You do not write it and you do not edit it into shape. When it comes
back short, the fix is upstream, in the prompt or the golden.

**The criteria come from the structure of the answer**: a ranked list under a cap grades every
candidate's score, a forecast across many periods grades every period, a grid grades every cell, a
bridge grades every reconciling item. That structure is the **prompt shape**, eighteen of them are
documented in `../guide-to-prompt/references/shapes/`, and picking one is a design decision made
**before** the ladder, not a rescue after a thin rubric.

Size it on paper first. The arithmetic is always **one repeated structural unit, times how often it
repeats, plus the decision furniture**: ten to twenty units, optionally doubled by a second figure
on each unit, plus the committed call, the runner-up, the gap, the flip threshold, the named chart
parts, and the files themselves. Under 25 means a **denser structure**, more units or a second
figure per unit, never more asks bolted on the side.

Five levers put genuine material behind that structure, and each one buys rubric density and trap
depth with the same work:

1. **Build in three different findings, not one restated.** A median, a p90 and a top-tier share are
   one distribution finding wearing three hats, and the rubric counts them once. Make the task turn
   on distinct facts: a headline number, a driver, a threshold, a trend.
2. **Ask for one criteria-dense visual, and name its parts.** "Include a chart" is worth one
   criterion. The same chart is worth six or seven when you name the chart type, each series or
   panel, a labelled reference line carrying its value, an annotation on the key point, an ordering,
   and a title that states the finding. A visual is also the thing the stakeholder reads first, so
   this lever pays twice.
3. **Add a second decision axis.** A recommendation resting on one number is thin, for the rubric
   and for the trap alike. Force the decision to weigh two things (the effect and its cost, the
   growth and the retention, the forecast and the capacity limit), which adds the second value, its
   comparison, and the reconciliation between them.
4. **State the repeated unit for every instance, in one ask.** This is the multi-dimensional ask and
   it is where the bulk of the criteria live. Name the grain outright, name the measures, and ask for
   an ordering or a total row, in groupings where the values genuinely differ and matter.
5. **Demand a robustness or validity check.** A back-test error against a naive baseline, a placebo
   or pre-period check, an interval, a sensitivity or leave-one-out, a cross-file reconciliation.
   These are the criteria a wrong path fails most reliably.

One rule underneath all five: **every criterion is a distinct, determinate answer a wrong analytical
path would get wrong.** Do not pad with rounding or units, which ride inside their values, and do
not count one fact twice because two files display it.

There is one hard constraint pulling the other way, and it is Part 3's: **the ask set must not over-determine the system.** Filing enough related quantities that a solver can solve back for the decisive constant hands the constant over, and that is a worse failure than a thin rubric. Sweep the set for it before shipping.

Write the asks **after** the golden exists, never before.

---

## Part 8. The evidence pack

### The input gates, non-negotiable

- One zip.
- **Ten or more files.**
- **Either a file of 25,000 or more rows in any format, or a large database file.**
- **Three or more distinct file formats** (four is the working target).
- **Two or more distractors**, files the solution does not use that look relevant enough to need weighing (never an unrelated file), named in the task's `metadata.json` and never in a file name (Part 4.4).
- Nothing that reads as LLM generated. Obvious artifacts get the task rejected outright.

Assert all five in the generator. They are cheap to check and expensive to discover late.

### Ten roles, filled as slots

| # | Role | Count | Purpose |
|---|---|---|---|
| 1 | **Spine dataset** | 1 to 4 | Bulk, authenticity, realistic mess, and the volume gate (25,000 or more rows, or a database file). |
| 2 | **Publisher documentation** | 0 to 1 | Long, genuine, defines codes. Disclaim it if it is not decisive. |
| 3 | **Operating extracts** | 2 to 4 | The entity's own telemetry. **This is where the trap physically lives.** |
| 4 | **Context artifact** | 1 to 2 | Correct numbers about a question that is not the decision question. |
| 5 | **Calibration corpus** | 1 | Part 4.1. Build this first after the spine. |
| 6 | **Governing document** | 1 to 2 | Carries the pin and the licensed wrong basis. |
| 7 | **Social layer** | 1 | Named humans holding wrong beliefs. |
| 8 | **Dimension and lookup tables** | 3 to 6 | Realistic warehouse shape, forces joins. |
| 9 | **Data dictionary or codebook** | 1 | Pins field semantics and grain statements. |
| 10 | **Provenance note** | 1 | States what each derived file is and how it was produced. |

Size: 10 to 19 files, median around 13.

### The single-statement rule

State each load-bearing fact **exactly once**, in the highest-authority file that carries it. Findability requires one statement, not three. A fact repeated across a memo, a manual and a dictionary is a signpost, and solvers clear that rung in one step and quote the file back at you.

When a rung needs to be discoverable without any single file being sufficient, **split it**: one file carries the rule, a second carries the layout fact the rule operates on, and neither alone gets you there.

**A sentence written for fairness is the likeliest place the decisive rung leaks.** Take each sentence that exists to make the mechanism discoverable and ask whether a solver could write the decisive step from it alone; if so, the fairness has to come from a structure the solver reads out of the records instead (task73, where deleting one runbook sentence and nothing else turned a solved round into one 13 points wrong). **Do not state a derivable mechanic**: a dictionary that explains row grain, header spellings across releases or identifier formats converts a methodological error into a reading exercise, so keep what nobody can derive (opaque code lists, which vintage a process ran against) and delete the rest (task57 v21). **An identifier that encodes a load-bearing field is a signpost** the anti-signpost greps cannot see (task60, an agreement id carrying its program year).

### Data realism, which is a rejection criterion

The pack has to read like an export from a system that has been running for years, not like a generated fixture.

- **Real vocabularies.** Published code systems (NAICS, SOC, HS, ISO, FIPS, agency series codes), real geography, real institution and program naming conventions, real release calendars, real revision and vintage behaviour.
- **No placeholder identities.** No John Doe, no Acme Corp, no Company A, no Lorem Ipsum, no obviously sequential fake names.
- **Mess as bad as real systems get:** inconsistent casing, trailing whitespace, mixed date formats, legacy encodings, orphan rows, superseded vintages, footnote markers inside numeric columns, columns that changed meaning between years, files exported by three teams with three conventions.
- **Mess must never change the answer.** Know exactly which complication you preserved and confirm it only makes the path longer.
- Never corrupt, truncate, pad or obfuscate to manufacture difficulty.
- Keep fictional documents **short and functional**. Long generated reports with thin content are the most recognisable tell there is.
- Normalise file timestamps to a coherent in-fiction date, consistent with the data's own span.
- Every derived file needs explicit provenance.
- Instruments and vintages are coherent: an instrument signed after the filing that priced it is an in-fiction impossibility that can make the corpus refuse the correct rule (task44).

**Realism is a constraint, not a rounding error.** When the arithmetic forces a parameter that is implausible in the real world, say so in the design note, show why it is forced by the ladder's ratios, and state the mitigation. Reviewers accept a stated, motivated extreme. They reject an unexplained one.

---

## Part 9. Build order

Cheap de-risking first. Do not build data before the ladder is written down.

0. **Draw** (Part 6.1). Run `../fingerprint/guard.py recent` and `coverage`, then draw gap, pattern, domain, objective, shape, unit, decision type, role, calibration form and generator pair. Write the table into the design note, write the same draw as a fingerprint card, and **file it with `guard.py register` before going further** (it refuses a card that still carries a BLOCK). This is the cheapest step to change and the one that decides whether the build is a clone.
1. **Answer the litmus in writing** and name the Gate G mechanism and the three flags (Part 1). If the litmus comes back yes, stop and redraw.
2. **Fix the business model and the unit of value.** One sentence: *"[Entity] does X and is scored on Y."* Choose a unit where **two different size metrics both look reasonable and rank candidates differently.** If you cannot name both in one sentence, choose a different business model.
3. **Write the ladder** into the worked skeleton (Part 13). Do not proceed until every blank is filled, every rung names a different candidate, every rung has the one shipped fact that kills it, and every rung has a written sentence explaining why a careful analyst would stop there and file.
4. **Settle the arithmetic on paper.** Discriminator dominance, the correction grid, the fork grid. All three are decidable before a single row exists, and no amount of data work rescues a rung that fails them. Then design the ask layer on paper via `supplemental-stumping`, every ask's devices and eight-file span and the device ledger, because the spans are schema decisions the pack build has to honour and a device retrofitted into a cut pack breaks mess neutrality silently.
5. **Choose the spine dataset.** Pick something whose subject is the market the entity operates in, not the entity's own product data. Check it clears the volume gate (25,000 or more rows in any format, or a large database file).
6. **Build the calibration corpus first**, then the operating extracts around it. Build its underlying records and compute the outcomes from them. Include the twin pair from the start; retrofitting it later means rebuilding the extracts anyway.
7. **Write the governing document**: pin, licensed wrong basis, background disclaimer, realistic logistics. Build the distractors (Part 4.4) and name them in `metadata.json`.
8. **Write the social layer**: two voices for wrong bases, one voice arguing against the right answer, all of them holding beliefs rather than quoting rankings.
9. **Solve it cold from the ZIP alone.** Every number must recompute. Write the golden with the robustness sweep and explicit counts.
10. **Wire the assertion regime** and ship the independent verifier **before** the build is called finished. The assertions are the only thing that catches a collapsed rung, because nothing in house solves the build for you, so a defect an assertion would have caught for free is a defect the portal charges a whole submission for.
11. **Write the prompt**, then delete every noun naming a metric, input file or method. Write the deliverable asks last, after the golden, against Part 7's five levers and the ask sheet fixed via `supplemental-stumping` before the data was cut, and sweep the set for over-determination.
12. **Read the generated rubric before you call the build finished.** It is generated from what you shipped, so it is the cheapest available reading of what the task actually grades, and it is the last reading you get before the portal. Under 25 criteria means the material is thin and the fix is upstream. Criteria that a solver can satisfy from a surface read mean the asks are free points, and that is a Part 7 repair, not a ladder repair.
13. **Name the stump in one sentence in the design note**: the wrong committed answer a competent solver files, and the step that lands them there. If you cannot write that sentence, there is nothing for the portal to measure.
14. **Invoke `determinism-check`.** The skill is free to run; only its judge rehearsal is author-triggered. Its `references/forcing-the-answer.md` should already have been read at step 5, when the ladder was designed.
15. **Run the Part 12 checklist, then `submission-writeup`.**

---

## Part 10. Diagnosis, when the trap is not biting

Read the failure texture, then apply the specific repair. **Do not reach for "make it harder".**

| Symptom | Diagnosis | Direction |
|---|---|---|
| Solvers get the answer on the first pass | **Ladder exhaustion**, too short, or your correct basis *is* the natural basis | **Add a rung below**, from a different gap. Make the natural basis produce a different named candidate. Do not add a rung above (machinery), and do not delete signposts instead (determinism). |
| Rounds agree on the name but **split on the figure** | Determinism defect, an unpinned parameter each solver fits for itself | Fix this before touching difficulty. Pin the parameter empirically in the calibration corpus rather than by a labelled column. This is a cross-result symptom, so keep each portal result's figure to compare. |
| Solvers reach every insight you planted, then commit elsewhere **and defend it from a shipped file** | **Determinism bug, not difficulty.** An unpinned axis. | Pin the axis in the highest-authority document, relabel any artifact in-file as answering a different question, delete any endorsement of the wrong basis that outranks your pin. |
| All wrong answers land on the designed decoy, **and the trace shows the decisive step being performed and refused** | Working exactly as built | Ship. |
| All wrong answers land on the designed decoy, but **no trace performs the decisive step** | **Right answer, wrong route.** A shortcut reaches the decoy and the rung you built was never tested | Find the shortcut and close it, usually lookup transfer (the twin pair) or a single flag that over-determines the name. The hold is real but you learn nothing until the chain is forced end to end. |
| A trace says a calibration case "cannot be explained" and uses the corpus **ordinally** | An unfittable calibration row: you shipped the summary without the records that reproduce it | Build the underlying records so the correct rule reproduces the outcome and every rival misses it. Until then the file supplies no foothold and the solver falls back to the decoy. |
| Two adjacent rungs name the same candidate | **Rung collision**, usually a parameter tuned for a lower rung | Recompute all rung winners after every parameter change. |
| The final rung computes correctly but never changes the ranking | **Discriminator dominance failure** | Widen the decisive edge or shrink the carried advantage until edge is at least 1.2x advantage. More documentation cannot fix this, it is arithmetic. |
| Two axes that were supposed to disagree give the same profile for every candidate | The correlation was never built | Construct it in the generator, per candidate, and assert it in both directions. |
| Wrong answers converge on a candidate you **did not** design | A second self-consistent reading exists in your files | Find it by re-solving from the rival's premise. Kill it with a pin, or remove the ambiguity from the data. Do not paper over it in the rubric. |
| Answers scatter across many candidates with shallow work | Unfair ambiguity, not difficulty | Cut noise. Make each rung's evidence discoverable on a plain group-by or join. Confirm each rung is genuinely satisfying to stop at. |
| A solver caught the trap by reading one file | Signposted, or the discriminator is single-source | Move the discriminator **behind a join**, two files, neither sufficient alone. |
| A solver dismissed your decisive file as a distractor and still failed | Working as intended | Keep it. Optionally add a second corroboration path. |
| Zero partial progress anywhere | Reads as impossible, not hard | Make one middle rung more reachable. The healthy shape is: some solvers make real partial progress and still miss the final rung. |
| Answer flips under a reasonable variant | Knife edge | Widen the margin, or add a rung that removes the variant from play. |
| An assumption does not clear "ten of ten analysts" | It is a decision, not an assumption | Pin it in a file, or change the answer. |
| Rival-killer cannot be reproduced from the files | Fatal, fails review outright | Replace the statistical rival-killer with a structural impossibility (G15). |
| The trace's whole reasoning is "the reported figure looks wrong, let me correct it" and that is the path you built | **Gate G failure, not a difficulty problem** | Rebuild, do not harden. Every round spent on this shape is wasted. |
| A response misses the main call and still scores well | **The asks are free points**, and when only one response cracks the trap this response is the *second* slot of the top two, so its score enters the average directly | A Part 7 repair, not a ladder repair. Rebuild the asks until a wrong path fails them. `supplemental-stumping` carries the pair-ceiling arithmetic and its mirror sweep measures exactly this response. |
| The name comes back right and the graded figures come back wrong, result after result | **An over-determined name**, a Gate F problem | Added rungs do not fix it. Re-root the ask so the name is not the graded call, or grade figures the name does not determine (task36). |
| The trap fires only against a solver that already chose the harder route | **Inverted trap**: the natural path reaches the refutation before the decoy | Check which of the two computations a solver reaches first, and build the decoy on the natural path (task36). |
| The generated rubric comes in under 25 criteria, or its criteria read as surface lookups | The prompt and golden are thin on material, and hardening cannot fix it | Go upstream. Add a distinct finding, a second decision axis, an explicit grain, a named-parts visual or a robustness check, then regenerate. |

### Reading a trace

**Read the trace for route, not just answer.** Grep for whether it cited the governing fact, performed the decisive join, ran the decisive arithmetic. Absence is the finding, and it is invisible if you only read the final recommendation.

**Read the trace for assumptions, above all.** The strongest repair the approved run found came from asking what a correct trace silently held fixed, not what it computed. Every identity a solver builds carries an assumption, and an assumption every solver makes without checking is a place where the physics of the scenario can be changed so the assumption goes false. Attack what the traces assume, and the repair lands where no patch to the existing rungs could.

**Read the trace against the asks too, because they carry most of the score.** A trace that misses the main call and answers every ask correctly is telling you the build fails the bar, and that finding is invisible if you only diagnose the recommendation.

**Diff the solver's artifact against the golden cell by cell before diagnosing.** Its answer says whether it solved the main call; its outputs say whether the whole ask block was free too, which changes the repair from hardening to re-rooting (task60 v2). Author-introduced Gate E defects hide inside a solved result (an unpinned rank tie-break on a rounded column, a rate on the rounded value, a ratio admitting either denominator), and they are found by diffing, not by proofreading. **Chase a wrong response's constants to exact fractions before dismissing them**: 0.279 read as noise twice and was 127/455, and the denominator named the mechanism (task69). **When the judge's model files a different answer to a peripheral ask, check whether its reading is the better supported one** before defending the golden (task64).

### Hardening escalation, in order of preference

1. **Add a rung from a different gap, below the current final rung.**
2. **Move the discriminator behind a join** so no single file reveals it.
3. **Split the pin's evidence across two documents** so one read is insufficient.
4. **Add an advocate for the runner-up** so the strongest wrong answer has social weight.
5. **Make the winner's rank worse** on the natural pipeline and re-check its position at every intermediate rung.
6. **Introduce a conditioned yield** so an aggregate that looks reachable is not.
7. **Tighten the calibration corpus**: add a twin pair, add a case that exercises an untested rule, widen the fit gap.

**Never harden by:** adding noise, removing needed evidence, introducing arbitrary thresholds, making files harder to parse, or shipping an artifact that computes a wrong answer. The last one buys difficulty with a Gate G rejection.

**Never harden by deletion.** When a trap does not bite, the instinct is to delete signposts. Deleting a signpost that also carried a parameter is how you ship a second self-consistent reading: each solver fits its own convention and the round comes back split on the figure, which is a determinism defect and strictly worse than the difficulty problem you started with. If a signpost must go, replace it with an empirical pin in the same edit.

### Stopping rules, written before the build is tested

**Fix the stopping rule in the design note before the build goes to the portal, not after reading the result.** State what result ends the scenario: how many materially identical solves file the build as at-ceiling, and what result licenses another repair. This matters because portal results are rare and slow, and a scenario nobody agreed to stop gets repaired forever. Rules the record settled:

- **Two consecutive exact solves by different correct routes is the signature of a computation, not a stump.** A fully pinned method whose every input has a natural-correct operationalisation is a computation, and further route-conditional traps are variance. The move left is re-rooting the ask, and the cost of doing it late is every round already spent.
- **Count the valid stumps, not the misses, after every determinism repair.** Every repair that pins a fork in a sentence or a column hands that rung to a solver who reads pins. When two consecutive repairs have each converted the rung they touched into a reading, the difficulty has to be re-rooted.
- **After repeated solves, change the decision, not the mechanism.** Four versions of one world additive over persons were solved or banned whatever form the rule took (corpus-pinned, hidden class, filed class, self-evident arithmetic), and the shape that carried was a which-of-N under a cap whose scored quantity is a group property (task58 v6, task44).
- **When a scenario is exhausted, say so in the design note rather than claiming otherwise**, and write the structural finding into that note's `## Tried and rejected` section so the next iteration pays for it once. Pivot in place: do not snapshot the dead build, do not open a `DESIGN_V2`, the note carries the finding and the generator rebuilds the pack.

### The repair loop

A diagnosis arrives from a solver round's path (`solver-round`, which runs on the finished build
and sees nothing but the prompt and the pack) or from a portal result; never from a solve run in
the main thread, which has read the design note. The round is cheap and the portal is a day, so the
round is where hardening happens and the portal is where the ledger is written; neither changes
what a repair is.

1. **Build.** All assertions green, verifier green.
2. **Diagnose on paper before the portal.** The design-side checks tell you the ladder computes, not that it bites, and nothing in house will tell you the difference. Name the wrong committed answer a competent solver lands on and the step that lands them there, in one sentence. A ladder whose author cannot name that sentence has no stump in it.
3. **When a portal result comes back, read it for route and for assumptions**, per the section above. Absence is still the finding.
4. **Diagnose from the table above**, then apply the matching repair.
5. **Change one mechanism per iteration** so the next result is attributable. If you must bundle edits, bundle only edits to the same mechanism.
6. **Ship both halves of every patch.** A patch that adds a summary row, a rule or a claim without the records that reproduce it leaves the pack worse than before.
7. **Do not treat a check agent's verification claims as authoritative.** Recompute contested numbers yourself from the shipped bundle before acting on them.
8. **Write every dead end into the design note's `## Tried and rejected` section as you abandon it**, one line with the reason it died. That section is the whole memory of the build now, and a repair tried twice is a build paid for twice.
9. **Invoke `determinism-check` when the build is finished**, and again while the ladder is designed and while the generator is written. Only its judge rehearsal is author-triggered.

---

## Part 11. Determinism failure modes and their repairs

### Failure A, the unpinned convention
The answer requires two unpinned choices to coincide, and a shipped file endorses the opposite of one of them.
**Repair:** pin the convention in a shipped file at appropriate authority, and remove or reframe the counter-pin so it no longer states a governing method.

### Failure B, the wrong basis better supported than the answer
The pin exists but sits in a low-authority location while a high-authority document implies the rival.
**Repair:** rewrite the governing document to state the criterion explicitly, relabel any artifact in-file, delete endorsements of the wrong basis from the social layer. After this the wrong basis becomes a **licensed** wrong path: real, available in writing, explicitly out of scope, which is the strongest form it can take.

### Failure C, the fabricated intermediate
A number in the golden, usually a rival-killer, does not reproduce from the shipped files, or two blocks of the golden contradict each other about the same artifact. **The most common instance is a calibration outcome with no underlying records.**
**Repair:** recompute everything from the raws, including every rival-killer and every calibration outcome. Build data first and compute figures from it. Where a rival-killer is fragile, replace it with a structural impossibility.

### Failure D, the Gate G misclassification
The build is genuinely analytical but the design note does not say so unarguably, so the judge cannot tell a binding constraint from a surface-read rejection wearing one, calls the type borderline, and routes the task to live testing.
**Repair:** write the litmus answer, the mechanism label and the three flags into the design note in the judge's own vocabulary, and state in one sentence why the reported figures in the pack are correct.

**Standing rule:** every number in the golden, the answer's numbers, the numbers that kill the rivals, the calibration outcomes, and every figure any character quotes, must recompute from the shipped files alone.

---

## Part 12. Pre-ship checklist

**Gate G, run this first because it is the most expensive thing to discover late**
- [ ] The litmus answered in writing: the reported numbers in this task are **correct**, and the difficulty is not catching that a read is wrong
- [ ] Primary mechanism named from the pass list, not `planted_defect_flip` and not `single_conceptual_flip`
- [ ] `surface_read_dependency`, `stumping_family` and `sole_data_defect` written into the design note
- [ ] **No shipped artifact ranks the candidates on the decision question and gets it wrong**, a declared wrong-basis distractor excepted (Part 4.4), and the build still stumps with it deleted
- [ ] No advocate quotes a computed ranking of the candidates on the decision question, and no voice holds a position the shipped data contradicts
- [ ] No reliance on depth as a defence: a two, three or four rung correction chain is banned exactly as a one rung flip is
- [ ] If the mechanism is `binding_constraint`, `decomposition_attribution` or `method_or_model_selection`, the reported figures are demonstrably correct so it cannot read as a rejection in disguise
- [ ] Delete every wrong number and misleading claim from the pack: it is still hard
- [ ] **The clean-data test run in the generator and asserted**, per suspect file: repair the file, recompute, and assert the answer and the naive figure both hold while answer and naive still differ. A self-reported `sole_data_defect: no` with no assertion behind it is the v1 failure this box exists to stop
- [ ] **The lens-swap test run separately**, because the two bans are independent: the naive read and the answer are not the same population at the same moment under two different lenses
- [ ] **The pre-draw identity test run before the draw**: the decision's governing arithmetic does not close over quantities the pack must ship, or the graded quantity was changed until it did not

**Architecture**
- [ ] 3 to 5 rungs, each producing a **different named candidate**
- [ ] Rung 0 is produced by the natural pipeline, not by a shipped artifact
- [ ] Every rung reproduces exactly from the raws
- [ ] Every rung is killed by exactly one shipped fact
- [ ] Every rung is genuinely satisfying to stop at, written down why
- [ ] The rung that carries the stump is named, and it clears **every one of the seven survival properties** in Part 1
- [ ] Cleaning sits at rung 1 or 2, never last, and is never the decisive move
- [ ] Winner ranks **4th or 5th** on the natural pipeline
- [ ] Winner leads **no** intermediate rung, sits 2nd on at most one, and there by at least 1.20x
- [ ] No rung anywhere has a margin under 1.15x
- [ ] Winner beats runner-up by at least 1.2x on the correct basis, or the separation floor binds and is stated
- [ ] **Discriminator dominance**: winner's edge on the decisive axis is at least 1.2x the decoy's carried advantage, both ratios computed
- [ ] No two adjacent rungs name the same candidate, re-checked after the last parameter change
- [ ] The correction grid enumerated, every non-decisive cell landing on a named wrong candidate or asserted outside the separation floor, partial-application cells swept
- [ ] Each rung's worth computed **on the graded quantity**, and the graded quantity does not absorb the decisive rung
- [ ] Where the answer is a figure, the correction chain has a direction and only the decisive rung reverses it, per-rung percentage moves stated

**Organs**
- [ ] Calibration corpus present, fit gap dramatic, test threshold-free if possible
- [ ] The corpus's power stated: which rungs it settles, and what it is structurally blind to, asserted
- [ ] Corpus resemblance points at the **decoy**, never at the answer
- [ ] **Twin pair shipped**: two cases identical on every lookup-visible column, outcomes about 2x apart
- [ ] **Every calibration outcome recomputes from shipped records** under the correct rule, and no rival rule reproduces the set
- [ ] Every rule the golden composes is exercised by at least one calibration case
- [ ] Wrong models get the calibration **order** wrong, not merely the levels
- [ ] Every convention is either pinned in a file or pinned by the corpus, with no third option
- [ ] Pin is one sentence, in a shipped file, unjustified, unrepeated, at or above every counter-pin, naming the observable
- [ ] **No sentence in the prompt fixes the basis, window, convention or population**
- [ ] Licensed wrong basis present with a named advocate, stated as a basis rather than a ranking
- [ ] No voice anywhere advocates the correct answer
- [ ] Large reference documents disclaimed if not decisive

**Determinism**
- [ ] Fork grid enumerated, answer wins every cell or the choice is pinned, **asserted cell by cell**, each losing cell mapped to the rule it violates
- [ ] Maturity and censoring axis checked and pinned or convergent
- [ ] Every assumption clears "ten of ten analysts", or is pinned in a file
- [ ] Where ambiguity is structural, both handlings converge
- [ ] Robustness sweep stated with counts, and the count matches what was run
- [ ] Any two axes the ladder needs to disagree actually disagree per candidate, by construction
- [ ] Every number in the golden recomputes, **including rival-killers, calibration outcomes and every figure a character quotes**
- [ ] Every graded numeric answer sits mid-bin, distance to the boundary asserted
- [ ] 40 or more assertions in the generator, independent verifier reads only the shipped bundle and passes
- [ ] No two statements about the same file can both be true

**Prompt and deliverables**
- [ ] Prompt is **prose**, first person with the role present, no roll call of opinions, naming no metric, input file, method or standard
- [ ] Its opening move, ordering, length and file set were chosen from `../guide-to-prompt/references/prompt-voice.md` rather than inherited, and `voice-check.py` on this task number flags nothing calcified
- [ ] Main Recommendation Ask is a single question and the only part that has to stump
- [ ] **At most one response in the field is expected to land the main call**, so every other response, the second strongest included, is genuinely stumped: that is half the pass condition and on the critical path of the average, and the ladder is designed for it rather than for spread alone
- [ ] The committed call is about a window that has not closed, or the design note carries the reason it is retrospective, and the Axis 1 tag was **not** changed to Forecasting on that basis alone
- [ ] Prompt demands one committed call with explicit anti-hedge language
- [ ] **One to three deliverables**, three being the ceiling, each a named output file a real analyst would produce for this decision, and no file carrying material another could have held
- [ ] **A visual included wherever it makes the decision read at a glance**, with its parts named
- [ ] No slot spent on a table that the memo, the workbook or a script's output should have carried
- [ ] The asks are **multi-dimensional and hard**, none a lookup, and none stacked simply to raise the count
- [ ] Every figure inside every ask has its unit and its rounding covered, by a convention stated once or by an explicit pin on a derived quantity, with no unit phrase repeating more than about twice across the prompt (H12), and no ask is about unit or rounding alone
- [ ] The prompt was compressed against `../guide-to-prompt/references/prompt-economy.md` and the ECONOMY block in `voice-check.py` is clean
- [ ] At least one deliverable is produced by a script rather than written
- [ ] Every golden run through `golden-realism` **after** its figures were frozen, so no deliverable reads as an unedited LLM draft, which is a send-back cause in its own right
- [ ] **Every ask fails under a wrong analytical path**, with the per-ask verdict written into the design note's deliverables block rather than judged here, because about 55 to 60 per cent of the score sits on these asks
- [ ] The **pair ceiling is at or under 40** against a bar of 50 (one top response landing the call, the other missing it, `55 x (Lc + Ls) <= 28 - r`), the ten points being margin against the on-platform verifier's inaccuracy and the post-submission regrade
- [ ] The ask layer designed via `supplemental-stumping`: every ask decoupled from the main call and device-carried, devices ledgered, spans at the file floor, the pair ceiling and the mirror sweep computed, and every device and hazard proven off the main call's row population by zero-counts
- [ ] **A prompt shape picked from `../guide-to-prompt/references/shapes/`**, its criteria arithmetic worked on paper and landing at 25 or more before any file was generated, and its "what makes it hard rather than long" section read against the ladder
- [ ] The ask set covers **three or more distinct findings**, not one finding restated in three shapes
- [ ] At least one visual with its parts named, at least one breakdown at an explicit grain, and at least one robustness or validity check
- [ ] The generated rubric reaches **25 or more criteria**, and where it did not, the material was added upstream rather than the rubric edited
- [ ] No deliverable ask is blatantly easy, none leaks an obvious intermediate of the main ladder, and the set does **not** over-determine the decisive constants
- [ ] Deliverable asks written **after** the golden
- [ ] If the answer is a hold: blocking quantity computed and reproducing, every candidate's failure named, prompt licenses a non-pick without advertising it, rung 0 still commits to a named candidate, and the design note states what would have made it a pick
- [ ] I can name at least 2 defensible wrong answers, each failing for a **different** business reason

**Pack**
- [ ] **10 or more files**, **3 or more formats** (4 target), **a file of 25,000 or more rows in any format or a large database file**, **two or more distractors (unused by the solution, relevant-looking) named in `metadata.json`**, all five asserted
- [ ] Authentic mess that cannot change the answer
- [ ] Real code vocabularies, real geography, no placeholder identities
- [ ] Nothing reads as LLM generated, fictional documents short and functional
- [ ] Each load-bearing fact stated in exactly one file
- [ ] Provenance stated for every derived file
- [ ] Any forced-implausible parameter stated in the design note with its arithmetic and its mitigation

**Draw**
- [ ] Fingerprint card written at the draw, `guard.py check` clear of BLOCK, every WARN answered in the design note, and the card filed with `guard.py register` before the ladder (no ledger row until the portal result)
- [ ] Draw performed independently and written as a table checked against the fingerprint cards
- [ ] Gap, pattern, domain plus objective pairing, stakeholder role, context-artifact type, calibration form and decisive mechanism all fresh, or the clone exposure recorded with the axes that differ
- [ ] Similarity test passed: stripped of names and numbers this does not read as a prior build, stated as a one-sentence "no prior build is ..." claim
- [ ] Similarity test passed: stripped of names and numbers this does not read as a prior build

**The container, run this last and invoke `reduce-house-fixes` to run it**

Everything above checks the analysis. This block checks whether the artifact is what it claims to be, which nothing above looks at, and which is where almost every fix the author has had to make by hand after calling a build finished has landed. `reduce-house-fixes` carries the register and the repair procedures; the boxes here are what it currently asserts.

- [ ] No shipped **input** binary carries its writer's name in its metadata: `python-docx` and `openpyxl` in `docProps/`, `reportlab` in the PDF trailer, `matplotlib` in PNG text chunks. Golden deliverables are exempt, they genuinely are script output
- [ ] No shipped input binary carries a timestamp outside a plausible band around the setting's date, checked **inside** the container and not only on the filesystem mtimes. Both directions: a build-clock stamp is the obvious tell and a library's default stamp, `python-docx` writes 2013, is the same tell pointing backwards
- [ ] Every figure quoted in the submission and the design note recomputes from the shipped bundle, **including the supporting figures**, and a figure whose only source is a scratch search script does not count as recomputable
- [ ] The submission sweep's **unit coverage** stated: a sweep matching comma-formatted integers is blind to percentages, ratios, bare counts and decimals, so name what sweeps each class and treat a class nothing sweeps as unverified however clean the pass reads
- [ ] The design note swept too, not only the submission, since it carries the most derived figures and usually has no verifier pointed at it
- [ ] Every sentence carrying a figure checked on its **words**, not its digits: how many, against what, of whom, in what unit. Count words, baselines, populations, unit labels, stated reasons, quoted bounds and twin-pair claims are all unverified assertions that a figure sweep passes over
- [ ] Every rule the golden states **back-tested over the whole shipped record**, mispredictions counted, and a non-zero count resolved by naming the missing qualifier rather than by moving the answer
- [ ] The **thinnest** margin in the build stated with what it would have moved, not only the comfortable separations
- [ ] Archive members enumerated against the declared asset list: no duplicate pack under a second name, no enclosing folder, no operating-system metadata entries, every visual artifact actually opened and looked at, and every shipped binary deliverable's text extracted and read as the reviewer would (task64's committee paper never stated two of its twelve required answers)
- [ ] No block of rubric points lives only in a script's standard output; if it must be produced by running something, the run and its dependencies are part of the declared delivery
- [ ] Ambiguity closed in the **ask** while that is still legal. Once responses have been graded the prompt and inputs are frozen and the only remaining fix is in the rubric
- [ ] Any figure stated twice, once as prose and once as a table row, agrees in both to the same rounding
- [ ] Both sweeps wired as assertions in the verifier, not performed by eye, so a rebuild cannot reintroduce either

---

## Part 13. Worked skeleton, and what the design note must state

Fill this before building anything. It is the highest-value artifact in the process and it is private, it never ships. Every arithmetic failure it catches costs nothing here and a portal submission anywhere else. The blanks are blanks on purpose: the structure transfers, the nouns never do.

```
DRAW  (independent draws, checked with ../fingerprint/guard.py)
  Card filed with guard.py register before the ladder was written? ____   Verdict: PASS / WARN
  Shape: ______   Gate G mechanism: ______
  Gap: ______   Pattern: ______
  Domain: ______   Subdomain (enumerated): ______   Objective: ______
  Pairing repeated from last build? ____
  Stakeholder role: ______   Context-artifact type: ______
  Calibration form: ______   Decision type: ______   Decisive mechanism: ______
  Repeats from prior builds: ______   (must be none)

GATE G  (answer before anything else)
  Litmus, in a sentence: ______
  Primary mechanism label: ______
  surface_read_dependency: ____   stumping_family: ____   sole_data_defect: ____
  Delete every wrong number from the pack. Still hard because: ______

ENTITY + UNIT OF VALUE
  ______ does ______ and is scored on ______ .
  Two metrics that both look like "size": ______ and ______ .
  They rank the candidates differently because ______ .

DECISION
  Exactly one ______ from { ______ }, for ______ .

ANSWER: ______        Rank on the natural pipeline: ____ of ____  (must be 4th or 5th)
MARGIN over runner-up on the correct basis: ____ x

LADDER
  RUNG 0  natural pipeline ______ gives ______        -> candidate A: ______
          killed by: ______
  RUNG 1  correction ______ gives ______              -> candidate B: ______
          killed by: ______
  RUNG 2  correction ______ gives ______              -> candidate C: ______
          killed by: ______
  RUNG 3  decisive move ______                        -> ANSWER
  "A solver who does everything right up to rung 2 commits to ______ ."
  Every rung names a different candidate? ____
  Which rung carries the stump: ____
  It clears all seven survival properties (Part 1)? 1__ 2__ 3__ 4__ 5__ 6__ 7__
  Worth of each rung ON THE GRADED QUANTITY: r1 ____ % r2 ____ % r3 ____ %
  Sign direction: corrections walk ______ , decisive rung reverses it? ____

GROUND-TRUTH POSITION TABLE  (assert every row)
  rung 0: rank ____ , behind #1 by ____ x
  rung 1: rank ____ , behind #1 by ____ x
  rung 2: rank ____ , behind #1 by ____ x
  rung 3: rank ____ , behind #1 by ____ x
  Leads no intermediate rung? ____   2nd on at most one, by >=1.20x? ____
  Any rung margin under 1.15x? ____  (must be none)

DISCRIMINATOR DOMINANCE
  Decoy's carried advantage on ______ : ____ x
  Winner's edge on the decisive axis ______ : ____ x
  Product check: edge >= 1.2 x advantage? ____

CORRECTION GRID
  Independent toggles: ______  ->  ____ cells
  Every non-decisive cell lands on a named wrong candidate? ____

CALIBRATION CORPUS
  Form: ______   Cases: ____
  Correct rule reproduces ____ of ____ within ____ %
  Worst rival miss across ____ swept rules: ____ %
  Twin pair: cases ______ and ______ , identical on ______ , outcomes ____ x apart
  Every rule the golden composes has a case that would break if flipped? ____
  Resemblance nominates the DECOY, not the answer? ____

PINS
  Filed pins: ______  (file, authority level)
  Empirical pins: ______  (recoverable as the unique value reproducing ______ )
  Counter-pins in the pack: ______  (must be none, or outranked)

FORK GRID  (cell by cell)
  Axis: ______   cells: ______   losing cell ______ violates shipped rule ______
  Maturity / censoring axis: ______   pinned or convergent? ____

PACK GATES
  Files: ____   Formats: ____   Largest dataset rows: ______

DELIVERABLES  (one to three files, three the ceiling; no format family assigned)
  Prompt shape: ______   criteria arithmetic: ____ units x ____ + furniture ____ = ____ (25+)
  1. ______ : carries ______
  2. ______ : carries ______
  3. ______ : carries ______   (only if it earns the slot)
  Script-generated file? ____   Every figure's unit and rounding covered? ____
  Distinct findings across the ask set (not one restated): ______ , ______ , ______
  Named-parts visual? ____  Breakdown at explicit grain? ____  Robustness check? ____
  Each ask fails under a wrong analytical path, one by one: ______
  Ask set does NOT over-determine the decisive constant? ____
  Generated rubric criteria count: ____ (must be 25+; if short, fix upstream)

ASSERTION REGIME
  Assertions in the generator: ____ (target 40+)
  Independent verifier reads only the bundle and passes? ____
  Every graded figure mid-bin, distance to boundary: ______

REALISM DEBTS  (stated, not hidden)
  Forced-implausible parameter: ______ ; forced because ______ ; mitigation ______

STOPPING RULE  (written BEFORE the build goes to the portal, not after reading the result)
  What result files this build as at-ceiling: ______
  What result licenses one more repair: ______

PORTAL LOG  (one line per portal result: result, route taken, the one thing changed;
             a mechanism tested and rejected goes in ## Tried and rejected)
  P1 ______   P2 ______   P3 ______ ...

DETERMINISM CHECK
  Invoked while the ladder and the generator were designed, and again when the build is finished.
  Verdict: ______   Findings: ______   Applied: ______
```

**The skeleton is the form, and these are the things it exists to force into writing.** A blank that cannot be filled is not a formatting problem, it is a design that does not exist yet. In particular the note must state, before any data is generated: the draw table with its one-sentence similarity claim, the litmus as a sentence with the three flags, the entity and unit of value with the two quantities that both read as size, the decision and its shape from Part 2, the answer with its natural-pipeline rank and its margin, the ladder rung by rung with the sentence for why each is satisfying to stop at, the arithmetic (position table, both dominance ratios, the correction grid, per-rung worth on the graded quantity), the organs including what the corpus is blind to, the fork grid cell by cell, every realism debt with the arithmetic that forces it, and the stopping rule for the next portal result.

A design note that cannot state one of these does not have a design yet, it has an intention.

---

## Anti-patterns

- **Shipping an artifact that computes a wrong answer to the decision question.** The leading cause of Gate G rejection.
- **Believing depth defends the shape.** A four-rung rejection chain fails exactly as a one-rung flip does.
- **A lens or definition swap on honest data that flips the naive read.** `single_conceptual_flip`, banned even though the data is clean.
- **Naming the standard, metric or rule in the prompt.** Bury it in a file.
- **A prompt clause that fixes the basis, window or convention.** The prompt outranks every shipped file, so that clause *is* the answer.
- **A calibration corpus whose resemblance nominates the winner.** It should nominate the decoy.
- **A calibration outcome nothing in the pack reproduces.** Solvers go ordinal and you lose the round; reviewers call it a fabricated intermediate.
- **A discriminator smaller than the advantage it must overturn.** Arithmetic, not documentation.
- **Two adjacent rungs with the same winner.** The last one is decoration.
- **Stating a load-bearing fact in three files.** That is a signpost, not findability.
- **Hardening by deletion.** You buy difficulty with a determinism defect and the next round splits on the figure.
- **Authoring a number and reverse-engineering data toward it.** Compute forward or not at all.
- **Signposting.** "One of these metrics is misleading" ends the task.
- **Method dictation.** "Compute A, then B, then rank by C" solves it for the solver.
- **Cleaning as the final rung.** Solvers are good at cleaning.
- **Same-pattern stacking.** Three grain mismatches is one generator.
- **Hedge-friendly framing.** "What are the trade-offs" cannot be graded. A licensed hold is not this.
- **Hold as an escape hatch.** A hold nobody can overturn, or one justified by "the data is unclear" rather than by a reproducible blocking quantity, is a task with no answer.
- **External-knowledge dependency.** If the answer needs a real-world standard not shipped in the bundle, it is unfair, not hard.
- **Knife-edge margins.** Under 1.15x makes every rounding choice a fork.
- **An unpinned convention the answer depends on.** The most common cause of rejection.
- **A rival-killer you cannot reproduce.** Audited as hard as the answer.
- **Manufactured difficulty.** Corruption, padding, truncation, arbitrary thresholds.
- **Deliverable asks that are blatantly easy.** Rejection cause in its own right, independent of the main stump, and a direct handover of the roughly 55 to 60 per cent of the score that sits on the asks, to the whole field at once.
- **One finding restated three ways.** A median, a p90 and a top-tier share are one distribution fact, and the rubric counts them as one. This is the commonest reason a task stalls under 25 criteria.
- **"Include a chart."** One criterion where a chart with its parts named is worth six or seven.
- **An ask set that over-determines the decisive constant.** File enough related quantities and a solver solves back for the constant, which is worse than a thin rubric.
- **Editing the rubric to reach 25.** You do not write it, and a short rubric is a message about the prompt and the golden. Fix it upstream.
- **An ask with no stated unit or rounding.** Gate E finding, and free to avoid. Equally, an ask that grades unit or rounding on its own, which is padding.
- **Recognisable shape.** Same gap, pattern and decision type as anything prior.
- **A decisive cause with a cutover date.** Event study is competent analysis, so the dated cause is decoy material, never the answer.
- **A decisive step a row predicate can express.** The solver is a filter machine; the decisive step needs a group, a join to another entity, or a recovered constant.
- **Lifting anything from an example, a reference file, a prior build or this skill's own wording.** Scenarios, entities, metrics, file names and phrasings are all clone tells. The prompt sketch in Part 7 and the draw lists in Part 6.1 are shapes to instantiate, never wording to paste. The mechanisms transfer, nothing else does.

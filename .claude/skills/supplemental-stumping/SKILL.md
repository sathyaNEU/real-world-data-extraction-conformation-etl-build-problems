---
name: supplemental-stumping
description: Design the supplemental ask layer, the asks that carry about 55 to 60 per cent of the generated rubric, against a pass bar of the top two responses averaging under 50 per cent with at least one genuinely stumped, built to 40. Runs after the stumping skill fixes the main ladder and before dataset-generation cuts any data. Every ask carries two layers, the decisive construction's output on a segment (so a wrong unit, population or method fails every figure at once) and a planted device on a path the main call never reads (so a response that cracked the construction still loses the ask); no ask is keyed to the call by name, the main call's rows stay clean while the ask paths carry the pack's planted mess, and proven devices from earlier builds are reused freely at this layer, re-skinned. Carries the pair arithmetic (each of the top two responses keeps about a fifth of the ask weight), the silent-mess rule (mess a default hygiene sweep finds gets executed, so only mess that reconciles on the wrong path counts), device stacking on every graded figure, the separation line with its row-level zero-count proof, the device book with the nine laws every device obeys and the proven devices sorted by whether they survive the habitual hygiene battery, the per-ask ladder, the file and column span floor, the use test and H18, ask-level determinism, the in-generator audit loop, and the ask ledger the design note must carry. Use when designing or hardening the asks of any build, when a review says the asks are lookups, when a top response lands the main call and the asks still yield, and whenever a data-quality issue is being planted to serve an ask.
---

# The Ask Layer

> The main ladder defends 30 to 40 points of the rubric. The asks defend about 55 to 60. The bar is the **top two responses averaging under 50 per cent**, and a response that lands the main call banks about 45 before it answers a single ask, so the main ladder has to keep every response but one off the call and the ask layer has to hold **both** top responses, the one that cracked the trap and the best one that did not, to about a fifth of the ask weight each. A build whose asks yield to a competent solver fails, however well the trap fires against the rest of the field.

**Prerequisites, in order.** The pairing is fixed via `guide-to-prompt`, and the main ladder is designed and written down per the `stumping` skill Part 13 before this skill opens. The ask layer is designed **on paper before any data is cut**, because the span floor in Part 6 is a schema decision the pack build has to honour, and a device retrofitted into a cut pack breaks mess neutrality silently. Ask wording is finalised last, after the golden, exactly as `stumping` Part 9 orders it; what is fixed here first is the ask sheet, which asks exist, what each one falls to, and what each one spans.

**What has actually been built, and what it measured.** `references/proven-in-production.md`, from the
shipped submissions of tasks 35 to 83. **Read it before Part 3 and before you pick a device.** It
carries the two arithmetic laws with the real numbers that killed a build (reachability, and the
rubric denominator), the three device sets worth copying with their measured wrong values, the coupled
blocks where one choice moves sixteen criteria (what coupling buys, and why it is not built), the
ceilings actually measured, and the five ways an ask layer has died. The laws below are the doctrine;
that file is the evidence, and a device chosen from Part 4 without checking a worked instance there is
the most common way this layer ships weak.

**Navigation.** Part 0 the goal and the pair arithmetic · Part 1 legality and the line that must not be crossed · Part 2 decoupled asks · Part 3 the failure budget and the hazard layer · Part 4 the device book · Part 5 the nine laws every device obeys · Part 6 the per-ask ladder and the span floor · Part 7 ask-level determinism · Part 8 the audit loop · Part 9 build order, the ledger and reuse · Part 10 diagnosis · Part 11 pre-flight checklist

**Scenarios never transfer, devices do.** A supplemental device's mechanism, organ form, ladder shape and measured magnitude can be spent again in build after build (Part 9). The surface around it, the fiction's nouns, the file and column names and the ask wording, is written fresh for each build, because that surface is what a reviewer compares.

---

## Part 0. The goal and the pair arithmetic

The generated rubric splits **30 to 40 per cent** onto the recommendation and its critical components, **5 to 10 per cent** onto instruction following, and **about 55 to 60 per cent** onto the asks (`guidelines/rubric.md`). A task passes when the **top two responses average under 50 per cent** and at least one response is genuinely stumped, and the build target is **40**.

### What the bar forces

At the planning weights (38 / 7 / 55) a response that lands the main call banks about **45** before it answers a single ask. Two such responses anywhere in the field take both top slots, and the pair cannot reach 40 (it gets under 50 only if each keeps under about 5 ask points). So **at most one response in the field may land the main call**, which is the main ladder's job (`stumping` Part 0), and no ask layer can rescue a build where two land it.

With one response on the call and the second slot taken by the best response that missed it:

```
C  =  38 + 7 + 55 x Lc        the response that landed the call
S  =   r + 7 + 55 x Ls        the best response that missed it
(C + S) / 2  <=  40     when     55 x (Lc + Ls)  <=  28 - r
```

`L` is the share of ask weight a response still earns, its leakage, and `r` is the weight of the recommendation criteria that survive a wrong call, read off the generated rubric (Part 3). At `r` about 5 the pair may keep about 23 of its 110 ask points, **roughly a fifth of the ask weight each**. Against the bar itself the same pair may keep about 43, roughly two-fifths each, and the gap between the two is the margin.

> **The pair ceiling is the single most important quantity in this skill.** It is computable on paper before any data exists, Part 3 computes it, and it means every ask is designed for an excellent reader: the response that cracked the main trap and the best response that did not both have to miss about four-fifths of the ask weight.

### Why 40 and not 50

The bar is 50 and the target is 40, and the ten points are not caution for its own sake. The on-platform verifiers are not perfectly accurate, and **the task is regraded more accurately after submission**. That is two-sided risk on a number you cannot see: a build measuring 48 on the platform can regrade past 50 and fail after work has stopped, and nothing in the pipeline catches that. Ten points is the cheapest insurance in the build, and it is bought in this layer, because the ladder's own margin is spent on determinism.

### What the portal shows

The asks are where builds lose the average. task98 v3 came back with its top response at 100 per cent and the second at 62, then 100 and 66 after hardening, and in task98 v4 one top response filed the golden with every rung named in its summary (`../stumping/references/shipped-ledger.md`). In each case the top slot sat at or near 100, which means the asks gave way entirely to the strongest solver, and the second slot banked most of them without the call.

### The asks are multi-dimensional and hard

Each ask is uncapped and untargeted, spans many rows, periods or cuts, and resolves to one defensible answer. That is a spec requirement, so this layer cannot answer it with "keep the asks narrow". Part 2 puts the width on device-carried asks, where it costs the strongest response everywhere at once.

### The stump is a separate condition

At least one response has to be genuinely stumped, well below the bar. Under this bar the main ladder has to do more than that, it has to keep every response but one off the call, and this layer cannot substitute for it (`stumping` Part 0).

### Where the difficulty comes from

Two layers, and every ask carries both. **The construction layer**: the asks are the outputs of the decisive construction cut by segment (the same count by region and by type, the runner-up and the gap, every tier's boundary, every period's figure), so a response on the wrong unit, population or method is wrong on every figure at once. That is what the client's own hardest tasks do (`../guide-to-prompt/references/exemplars/index.md`: every task under 0.25 asks for the construction's outputs by segment, and the model's path that misses the unit scores 0.13 to 0.21 because nothing it files is right). **The device layer**: each ask also carries one **planted data-quality device** on a path the main call never reads, a dirty-data structure whose correct handling is uniquely forced by shipped evidence and easy to miss, so a response that cracked the main construction still loses the ask's weight to the device.

The pair arithmetic decides which layer carries which case. When no top response lands the call (the measured outcome on the client's hardest tasks), the construction layer costs the pair everything and the device layer is margin. When one does, the construction layer hands that response its ask weight and only the device layer holds it under the pair ceiling. A build needs both because it cannot know in advance which case it is in; Part 2 carries the rules for each.

This is the register era's craft, re-homed. Tasks 10 through 23 carried their difficulty in planted data-quality devices aimed at the main answer; Gate G bans that shape for the Main Recommendation Ask (`planted_defect_flip`, surface-read rejection at any depth), and the craft lives at the ask layer instead. Each supplemental ask is a small committed answer judged on Gates A to E, with no Gate G of its own, and the rubric's own doctrine says every criterion is a determinate answer a wrong analytical path would get wrong. Mishandling a discoverable, adjudicated device is a wrong analytical path. The design notes and generators of tasks 14 to 23 are the sources of the device book in Part 4 and the laws in Part 5, and task63's per-ask ladders with overlapping silent hazards are the working model for Part 6.

---

## Part 1. Legality, and the line that must not be crossed

Three tripwires decide whether this layer is legal, and the first one is the reason this skill exists as a separate discipline rather than a paragraph in `stumping`.

**1. The no-trace rule.** The main recommendation must never be attributable to a data-quality device, not in the answer, not in the margin, not in the trace a solver leaves. Walk the main golden's full recomputation path, every file, column and row population it touches, and require of every device and every hazard the off-path proof, written into the ledger and asserted in the generator:

- **Off path.** The rows and columns the device corrupts never enter the main computation, proven by zero-counts against the main call's declared row population (its files, columns, window and entities), asserted in the generator. Off path by whole file is cleaner where the span floor allows it, but an eight-file span usually crosses the main call's files, so the row-level count is the standing proof.

There is no inert-on-path proof: the main path carries no ledgered device or hazard rows at all. Authentic texture on the main path that cannot move the call is `dataset-generation` §7's business, tested there, and is not a device.

- **Off path in prose too.** No document the main call depends on carries an organ an ask device needs. A definition of a device's population placed in the notes a solver reads for the main call points that solver at the business the population belongs to, and that business can be the main call's own (task105 v3: such a section was the one change between two portal runs, and the average rose). The organ goes in a document on the ask's own path.

This is `dataset-generation` §11.6 mess neutrality run against the main call for **every** device with no exceptions, and it is the exact inversion of the register era's rule. Those builds required the defect to move the answer; this layer requires the defect to be provably unable to. A device that leaks into the main call is the highest-severity defect this skill recognises, because it converts a legal build into a Gate G rejection.

**2. The litmus stays clean.** Delete every device from the pack and the main task is still hard, because the main ladder is analytical and was designed before this skill opened. The Gate G flags in the design note (`surface_read_dependency: no`, `sole_data_defect: no`) describe the main mechanism and stay true. If deleting the devices collapses the main difficulty, the build was leaning on them and the fix is upstream in the ladder, not here.

**3. The pack still reads authentic.** Every device is real system behaviour from the good-mess families, a migration, a cutover, a vendor feed, a bureau outage, a reporting lag, never corruption, truncation or sabotage. A pack that reads as booby-trapped fails the input gates before any ask is graded, and a reviewer who can see intent behind the mess has been told how the pack was made. The device count per pack is bounded by the root-cause fictions that can plausibly coexist, which is why Part 5's ninth law lets one cause feed several devices.

**The ETL caveat.** On a build tagged Data Extraction & Conformation the main difficulty is already conformance-shaped and the standing house ban (conformance never in the top two rungs of the main ladder) applies. The ask layer on an ETL build must then draw its primary devices from families the main ladder is not using, or the build becomes one long conformance exam, the rubric's findings collapse into one finding, and the clone check reads a repeated driver.

---

## Part 2. Two layers on every ask

Every ask is the decisive construction's output on a segment **and** carries a planted device on a path the main call never reads. The prompt shows no seam in either.

### The construction layer

The ask's quantity is computed on the construction the main ladder forces (the admissible unit, population or method), cut by a segment the stakeholder would ask for anyway: by region, by tier, by period, the runner-up and the margin, the count that moves when the unit is right. It is never keyed to the call by name ("for the option you recommend"), because that wording hands a rung over; it is keyed to the construction by being unanswerable without it. A response that took the wrong unit files a complete, internally consistent, wrong figure for every one of them, which is the measured shape of a 0.13 to 0.21 task. Ask for enough segments that the shape fails everywhere: the runner-up and the gap, not only the winner, so a near miss shows (`../stumping/references/traps/_measured.md`, trap 3).

### The device layer

Each ask's path also crosses **one primary device** on rows the main call's declared row population never touches, plus at least one shared hazard (Part 3), so the figure is wrong whenever the device is mishandled whatever the solver concluded about the construction. The device layer is the part the rest of this skill engineers: the silence, the stacking, the fairness guarantees and the row-level off-path proof all belong to it. It is what holds a build whose main trap one top response cracked.

### Why the device layer is still needed when the construction layer exists

An inheriting ask, a quantity computed on the corrected structure or keyed to the recommendation, falls with the trap. With one of the top two on the call, the response that cracked it banks the whole ask and the response that missed it loses the whole ask, so across the pair it costs its full weight once, handed over in the top slot, where the average is decided. A device ask costs the pair `2L` of its weight, so the two break even at `L = 0.5`, and at the target leakage of about a fifth the device ask is far better. Only when neither top response lands the call does an inheriting ask cost the pair nothing (the shipped ledger's task58 v12.1 lesson argues from that case), and the record does not let you plan on it: the top slot sat at or near 100 on the portal (Part 0). So inheriting asks are not built. If the author asks for one, it stays narrow (close to one graded value), device-free, worded as a quantity and never as a treatment (the `stumping` Part 7 delete-on-sight list applies), and swept so the ask set cannot be solved back for the decisive constant or teach the ladder by repetition.

**So the construction layer is never the only layer.** An ask that needs the main ladder's decisive move correlates with the main call and hands a cracker its construction weight; the device on its path is what takes that weight back. The devices live in the parts of the pack the main ladder does not privilege, which is also what makes their eight-file spans natural rather than forced.

### Decoupled in computation, never in decision

`../reduce-house-fixes/SKILL.md` H18 binds every ask: independence of difficulty is the point, independence of decision is a first-pass rejection. Every ask's answer enters the committed call as a component of its case, a reconciliation of it to another total, or the trail that audits it, and the ledger names which. What decoupling decides is where the ask's path runs. The homes that are both decoupled and inside the decision:

- **The other measures the deliverable carries for every candidate, on which the call does not turn** (the cost beside the forecast, the capacity beside the demand, the exposure beside the gain), computed from rows outside the main call's population.
- **The trail that audits an input the call consumes**, worked through device-carrying rows the call itself never reads, back to the input's control total.
- **A reconciliation of an input or a candidate figure to another system's total**, where the gap is made of the devices.

Sensitivities, flip conditions and splits of the committed figure at a denser grain pass through the main trap, so they are inheriting asks (H18's own repair notes that a split of the committed figure inherits the trap). If the only asks that pass H18 for a decision are inheriting ones, the decision is too narrow to carry a decoupled ask layer, and the fix is upstream in the draw (a decision whose case has more than one axis), never a second decision bolted on.

Decoupling does not make an ask harder by itself. A response that misses the call loses only the recommendation block, so the second slot's score rests on the devices as much as the first slot's does. What decoupling buys is the licence for the two mess regimes below; silence and stacking are what make the layer hold.

### The pack carries two mess regimes: the main path clean, the ask paths dirty

The main call's path is mess-neutral, meaning authentic texture that cannot move the call (`dataset-generation` §7), never pristine, because a spotless file fails the authenticity gate. The ask paths carry the pack's planted devices, as many as authentic root causes can carry (law 9). An eight-file span in a 13-file pack means the asks cross the main call's files, so separation is proven at **row level**: the generator declares the main call's row population (its files, columns, window and entities) and asserts zero device rows and zero hazard rows inside it, with the counts written into the ledger (task64's zero-count pattern, `references/proven-in-production.md` Part 4). A device whose whole file sits off the main path is the cleaner proof where the span allows it, but it is not required.

### Messier means silent, never louder

The top responses run a hygiene battery by reflex (key uniqueness, exact duplicates, unmatched joins, fan-out, counts that tie) and then carry out whatever filed rule adjudicates what the battery surfaced, so a device the battery finds is a work order, not a trap: in task73 v2 every rebuilt device (batch corrections, standing double-posts, register-blind straddles) was executed by both top responses. task98 shows the other half: a filed construction is only a computation to a top solver, and in v4 the one thing that caught a response was a stored version taken before a silent switch. So the mess that scores is mess whose wrong path completes and reconciles everywhere it is habitually checked, with the inconsistency visible only at a cross-file or cross-grain cut nothing invites. Part 4 sorts the proven devices by exactly this. More nulls, more duplicates and broken formats cost realism and buy nothing.

### Stack devices on every graded figure

One device per ask hands an excellent solver the whole ask the moment it finds that device. Every ask carries **one primary device**, the thing it is silently about, drawn from Part 4 (the silent list first) with no family repeated across the set, **plus at least one shared hazard from Part 3**, so the path of every graded figure crosses two or three independent devices and catching one still leaves the figure wrong. Make each device move every figure in its ask together, so a miss costs the whole ask rather than one criterion. The primary device is what the ask's own ladder (Part 6) is built around. Every added device is also one more reading the determinism judge tests, so stacking never loosens Parts 5 and 7: each device keeps its filed organ and its asserted fairness guarantee, and the composed deltas for every subset of mishandlings stay outside the rounding bin.

### Every ask passes the use test

This is where device asks fail most often. A device ask is designed backwards, from a device outward to a quantity that crosses it, and that construction has no reason on its own to land on something a person would want. The result reads as a request written against a scoring sheet, which is a stated rejection cause and is exactly what the client means by an unrealistic litany of asks. The full six tests are in `../guide-to-prompt/SKILL.md`, "Every ask has to be an ask a real person would make"; the three that bite here:

- **Use.** Name who acts on the answer. If the honest answer is "nobody, it exercises the migration device", the ask is not finished.
- **Vocabulary.** The ask is worded in the stakeholder's words, never in the analyst's. This is not only realism: the wording rules in Part 6 ban naming a treatment or a device, and analyst vocabulary is where that leak happens.
- **Genre.** The ask belongs in the file it sits under. A per-row reconciliation requested of a one-page brief is a genre mismatch a reviewer reads immediately.

**The repair runs device-first, then use-first, and meets in the middle.** Having chosen the device, do not search for any quantity that crosses it. Search for the quantity **the decision already needs** that happens to cross it: the figure the stakeholder would have asked for anyway, on a path the device sits on. That ask is realistic and device-carried at once, and it is stronger as a trap too, because a quantity the decision needs is one a solver cannot skip. If no such quantity exists, the device is planted in the wrong part of the pack, and the fix is to move the device rather than to justify the ask.

### The line, drawn in three sentences

No device or hazard row sits inside the main call's declared row population. No ask needs the main call, the corrected structure it forces, or its decisive move. Every graded figure sits under at least two independent devices. Everything else in this skill is engineering inside those three sentences, and the ledger asserts all three per ask and per device.

### Sizing under the shape

There is no ask floor and no target count. The asks are uncapped, each multi-dimensional and hard, so the split is over **rubric weight**, not over ask count, and the count itself falls out of the prompt shape (`../guide-to-prompt/references/shapes/`), which is where the 25 criteria come from.

At a typical build that is **three to five asks, all device-carried and wide**, none keyed to the call. Read it as weight: one ask stating a ranked list of twelve candidates on two measures is twenty-four criteria on its own, and it is twenty-four criteria a device-blind response loses together.

Two rules hold. **Difficulty is bought per ask**, through span, device mass and ladder depth, never through more asks. And **ten shallow asks hand a strong solver ten small wins** while three deep ones hand it three probable losses, which is why the spec asks for multi-dimensional asks instead of a litany of basic ones.

---

## Part 3. The failure budget and the hazard layer

### Two arithmetic checks that come before the ceiling

Both are measured in `references/proven-in-production.md` Part 1 and both killed a build with a
working trap. **Reachability:** a response that lands the main call banks `0.30 + 0.60c` where `c` is
the share of ask weight reachable **from** that landed call, so task58 v15 scored 62.5 per cent with
13 of 24 reachable and task58 v1 put 75 per cent of the ask weight downstream of the main discovery
and could not clear the bar however hard the trap was. Count `c` on paper first; with every ask
decoupled it is near zero by construction. **The denominator:** with the rubric at `W` weight points
and two responses at `a` and `b`, adding `N` asks both fail gives `(a+b)/(2(W+N))`, which for task60
v7's real numbers (87 points, 65 and 32) drops under the 50 per cent bar from `N = 11` and under the
build target of 40 from `N = 35`; solve `(a+b)/(2(W+N)) < 0.40` for `N` on the build's own numbers.
That is the move when the ladder is measured out, and it is the only move that works then.

### The pair ceiling, computed before any wording exists

Build the pessimistic ledger on paper. Credit the response that lands the call with everything correlated with being generally excellent: the full recommendation block (plan at 38) and the full instruction-following block (plan at 7). Credit the best response that misses it with `r` and the same instruction-following block. Everything left on both sheets is device-carried:

```
pair ceiling  =  ( rec block + 2 x IF block + r + ask leakage of both responses ) / 2
```

**Target 40 or below**, against a bar of 50 (Part 0 says why the ten points). At the planning weights that holds the pair's combined ask leakage to about 23 of its 110 ask points, a fifth each.

The three levers this part exists to name:

- **Build no inheriting asks**, so no ask weight is decided by the main trap.
- **Pull criteria density into the device asks.** Rubric weight follows criteria, not asks, and one multi-dimensional ask generates many criteria when its golden content is dense: a value plus a direction, a named-parts visual, a breakdown at an explicit grain, a reconciliation that must tie. This is also where the spec's multi-dimensionality requirement gets satisfied, so the two pressures point the same way.
- **Drive ask leakage toward zero** with silent primaries (the sort at the head of Part 4), stacked devices on every figure, the laws in Part 5 and the audit in Part 8. Leakage is the share of ask weight a device-blind solver still earns, and every point of it is exposure.

**`r`, the partial credit a wrong-path response keeps, is read and not guessed.** It is the weight of the recommendation criteria that **do not depend on the decisive rung**, readable off the generated rubric once it exists and estimable as that same share before it does. It enters the pair ceiling directly, so every point of it is a point of ask leakage the pair cannot afford, and it is what Part 8's mirror sheet measures.

The generated rubric is the ground truth for the weights, so after it generates, rerun this sum with the real numbers (`stumping` Part 9 reads the rubric when it generates; add this sum to that reading). If the recomputed pair ceiling clears 40 with only one response on the call, the fix is in this layer, not in the main ladder. The rubric's own denominator is a design variable too: task60's lesson was that adding asks both responses fail drags every score down together.

### Device independence, and the hazard layer that cuts the other way

**No two asks share a primary device family.** A solver who discovers the duplicate structure must gain nothing on the timezone ask. Independence is what makes seven asks seven separate chances for a strong solver to miss, rather than one discovery amortised seven times.

**Then lay the silent hazards across them.** A hazard is a cross-cutting device that sits on the shared backbone of the pack and moves the answers of **several** asks at once, on top of each ask's own primary device. Three to five hazards per build, each moving three to seven asks, each obeying every law in Part 5, and each recorded in the ledger's hazard table with the exact list of asks it moves and the per-ask delta. The two layers punch in opposite directions and the design wants both: primary-device diversity multiplies the number of independent misses available, hazard overlap multiplies the cost of each miss. task63 shipped this two-layer shape and its hazard table is the model, one row per hazard, the asks it moves, the count.

**Direction discipline inside an ask.** Where an ask crosses its primary device and two hazards, the three mishandlings must not be able to cancel back onto the golden. Know each device's direction and magnitude per ask, compute the composed deltas for every subset, and assert none lands inside the rounding bin. This is the register era's grid discipline applied per ask, and it is cheap while the data is still on paper.

---

## Part 4. The device book

**Before instantiating any family, read the three shipped sets in
`references/proven-in-production.md` Part 3**: task63's four devices each with its own named referee,
task65's seven families with measured wrong values (24,247.8 and 5,715.9 tons against a true 19,081.6
on one county-year, and a dimensional error worth 22.4 per cent), and task69's single arbiter. Those
are what the families below look like when they are built to bite, and two of the deaths in Part 4 of
that file are devices from this book that were sound and were handed over by prose. The register era's own
instances (tasks 1 to 24), each with what a default sweep sees, its organ and what it measured, are in
`references/register-era-instances.md`.

### The proven devices, sorted by the habitual battery

This sort is a reading of the record (the task73 v2 hygiene lesson applied to the shipped instances in
`references/proven-in-production.md` Part 3), not a measurement of each device. Reuse from it freely,
re-skinned.

**Silent under the battery: reach for these first, as primaries.**

- **A vintage whose totals are invariant** (task74, hierarchy v4 against v5, 2,196 items moving between
  departments with both totals unchanged). No reconciliation can see it. D2.
- **The version of record is the latest accepted, not the latest delivered** (task74, two suppliers),
  and its cousin, **a stored label or segment taken before a silent switch** (task98 v4, the one thing
  that caught a top response). Every row looks valid and the wrong vintage is complete. D2.
- **Codes reissued to different entities** (task65, nine freed codes). The raw join and the current-code
  filter both land silently on wrong values, 24,247.8 and 5,715.9 against a true 19,081.6, so it breaks
  the repair as hard as the carelessness. D7.
- **An absent reporter or channel** (task65's delegated district missing from the portal export,
  task80's provider that never uploaded a month). There is nothing in the data for a sweep to find. D4.
- **Units set per source by agreement** (task80, one provider in minutes where the rest are hours).
  Every value parses and the error is dimensional. D3.
- **A clock against a filed cutoff** (task83 converting UTC before quartering, task39 facility-local
  time through each IANA zone). Rows change period with no error. D8.
- **Deliberate, stated non-additivity** (60, 64, 80, 81). It inverts the tie check itself, so the battery
  points the solver the wrong way.
- **A reconciliation column that reads zero only on the correct path** (task64's `meter_to_billed_gap`,
  three devices handled before it reads zero). This is the natural stacking vehicle, one graded figure
  carrying several devices.
- **An event's quantity repeated on every line the event covers**, in an extract whose grain is not
  stated (task20 DEC-6: on the portal the responses summed the repeats on the asks, 92.0 per cent yield
  against 97.48). A fan-out check could see it in principle; the tell, a line larger than the receipt it
  covers, sits in another file. D6.

**Visible to the battery: hazards only, or ship with the over-cleaning half.**

- **Exact or near-exact duplicates and replays** (D1). A duplicate sweep finds them and the dictionary's
  grain says what to do (task16 revision 3: both top responses removed all 494 migration duplicates and
  filed every figure). Use them only with genuine repeats a blanket dedup destroys (law 5), so the
  reflexive repair lands on its own wrong value.
- **Sentinels and suppression markers** (D4). A type sweep finds most forms; task74's five forms at once
  is what kept partial handling wrong.
- **Roll-up lines inside detail** (D6). A sum or fan-out check finds them where the rollup exceeds its
  sibling.
- **Fields displaced by a widened record** (task63, three fields right). Blanks in required columns invite
  a look at the trailing spares.

The families below are the recovered catalog of the register era (tasks 10 to 23), reconciled with the live ETL trap catalog (`../stumping/references/traps/data-extraction-conformation-etl.md`) and the client's proven-trap families and twelve targeted failure behaviours (`guidelines/techniques.md`). They are mechanisms, not examples: instantiate along the stated axis and re-skin the surface, never copy a scenario's nouns or files. For each family: **Errs** is what the careless path does, **Organ** is what forces the single correct handling, **Aim** is where the miss lands.

**D1 · Duplication and identity.** Re-delivered batches and replays under fresh ids with the stable key preserved (idempotency key, authorisation code, ARN, ticket number), near-duplicates with one re-quoted field so full-row dedup finds nothing, keys recycled across unrelated entities so a global dedup deletes real records, later-cycle refilings of the same case, migration backloads under a second id scheme, casefold twin keys.
**Errs:** counts and sums inflate, or a global dedup deletes the genuine twin. **Organ:** the dictionary's key and grain definition, plus a register or manifest that declares what one real event is; scope the dedup to the entity the key belongs to. **Aim:** a count or total wrong by the replay mass, in a stated direction.
**The over-cleaning half is mandatory:** ship genuine repeats that a lazy dedup destroys (real paired records, legitimate re-events with their own identifiers), so the correct handling is interior, not "drop everything that looks doubled".

**D2 · Version and vintage.** Two accepted vintages of the same cells with the version-of-record rule filed (latest accepted by timestamp, both clauses load-bearing because a rejected resubmission is latest), a version history loaded as if it were a state, a snapshot poisoned for history (a type-2 dimension read current for a past window, a post-window rollback), a workbook whose polished FINAL tab is the superseded cut, a restated batch that replaces rather than adds.
**Errs:** the solver keeps the wrong vintage, or keeps both. **Organ:** the filed version-of-record clause at authority, supersession declared in the manifest, effective dates on the dimension. **Aim:** a level or rate from the wrong world.

**D3 · Meaning, units and encodings.** Quote conventions that vary per row with the convention column present, a unit switch mid-file conditional on a date, quantities denominated in cases or packs against an each-based question, scale units (thousands) pinned only by one ledger figure, per-source date conventions, crosswalks with retired codes and mixed vintages, fixed-width layouts that drifted, a sign overpunch, per-file delimiters and encodings, two columns one word apart with different meanings.
**Errs:** a blanket conversion, a global date parse, a join on the wrong namesake. **Organ:** the convention column itself, the dictionary's field semantics, the published standard's exponent or code list. **Aim:** magnitude errors far outside the bin, in a direction the ledger records.

**D4 · Absence and sentinels.** Structured non-response whose blanks mean nobody filed, with the rollup that reconciles only when blanks stay blank; reporters missing from one period recovered only against the register's population; sentinel values and sentinel dates that read as data; suppression markers; absence-as-signal semantics declared once (no line means the event completed); a whole channel absent from the ledger and shipped as a partner file in its own namespace; fields displaced one column right for one source's rows.
**Errs:** missing read as zero, sentinels averaged, the absent channel never found. **Organ:** the reconciling rollup, the register as the population authority, the dictionary's sentinel conventions, the matched-population clause. **Aim:** a gap or rate manufactured or erased.

**D5 · Scope and population.** Silently partial extracts (one processor's book, media-only cost, the platform channel only), rows outside the decision population identifiable only structurally (internal accounts, sandbox tenants, QA harness traffic whose only witness is reference shape), review-population filters (class, status, eligibility) that the naive read ignores, orphans that must be quarantined and valued rather than inner-joined away.
**Errs:** the wrong population computed confidently. **Organ:** the governing document's scope clause plus the register or naming convention that identifies membership, the row-count reconciliation that surfaces the drop. **Aim:** a figure about a population nobody asked about.

**D6 · Grain and aggregation.** Detail and rollup rows in one file (the rollup exceeding its sibling is the tell), subtotal furniture inside data regions, event headers fanned onto every covered line so summing repeats the quantity, registers that must collapse to the entity before joining, allocation splits at the wrong weight.
**Errs:** double aggregation, fan-out sums, whole-to-part attribution. **Organ:** the grain statement in the dictionary, the physical impossibility the fan-out creates (a loss exceeding the lot), the reconciling total at the correct grain. **Aim:** inflation by a clean integer factor or a fan-out mass.

**D7 · Keys, linkage and resolution.** The true key living in a different field than the label (an alternate-key rule, entity where populated else hash), the real date encoded inside a reference string, resolution reachable only through a prior-id chain in a second file, effective-dated joins where the natural as-of hides the far edge, multi-hop namespaces (partner code to crosswalk to catalog), dirty keys at realistic rates with at least one collision that punishes global normalisation.
**Errs:** single-key matching, the stale current row, the chain never walked. **Organ:** the linkage rule filed as field semantics, the chain's own arithmetic closing only when walked. **Aim:** entities merged, split or dropped, with the mass landing on a named wrong value.

**D8 · Time and clocks.** Timezone and DST against a filed cutoff, the settlement date standing where the order date is needed, watermark overlaps at a DST boundary, settlement periods that never land on a month end so every month-end level costs an unwind, an append-only history whose misparse silently resolves to the previous row.
**Errs:** the convenient clock. **Organ:** the standard's stated timezone and cutoff, the period definitions, the one timestamp that is a real clock. **Aim:** events in the wrong period, a count off by the boundary population.

**D9 · Self-validation, the meta-family.** These are not asks' primary devices, they are what keeps the other families alive against a strong solver, and every ask should sit behind at least one: a headline reconciliation engineered to pass on the broken read (the false clean), a trailer or control total that confirms the wrong parse, a published DQ table that genuinely passes because the defect sits where the checks do not look, an oracle made to lie both ways (name agreement that vetoes valid joins and blesses false ones), the rehearsed repair shipped as an artifact pointing the wrong direction, and at most one punish-the-repair device per build (a withdrawn correction artifact that catches excess diligence), because it is the only device that penalises thoroughness and two of them read as malice.
**The standing rule from the register era:** every control that still ties on the wrong path is certifying the wrong number, and that is the design working, not an accident to fix.

---

## Part 5. The nine laws every device obeys

These are the laws the register era converged on across every build that survived a blind panel, restated for the ask layer. A device that breaks one is either unfair, non-deterministic, or dead on contact with the opponent model, and the audit in Part 8 checks all nine.

1. **Unflagged, but adjudicated.** Discovery happens only through internal inconsistency: a cardinality that is wrong, a row that is physically impossible, a rollup exceeding its parts, a rate published beside its own reciprocal. No flag column, no status word, no file name, no prose anywhere narrates the defect, because a label is the answer standing next to the question. But the **rule that adjudicates the correct handling is filed**, stated generally, in-pack, at authority: the dictionary defines the key, the standard states the counting basis, the manifest declares supersession. A device needs both a discoverable population and a rule that authorises acting on it; the population is never announced, the rule always is. An inconsistency a default hygiene sweep surfaces (key uniqueness, exact duplicates, unmatched joins, fan-out, count ties) is not a discovery, it is a work order the field completes (task73 v2), so the device's inconsistency exists only at a cross-file or cross-grain cut nothing invites, with the adjudicating rule still filed at authority but its relevance one uninvited question away. A rule whose relevance the solver cannot miss is executed: in task105 v4 the strongest response landed every ask figure by carrying out the four filed device rules (balances moved at a hive-up kept out of the credit notes, blank-key credits tied through the invoice they credit, take-overs picked out by their set-up fee, a rent-free period clocked from the lease start), and task17 X0 stopped stumping once its full classification procedure was filed.
2. **Two antidotes, split across files.** One structural (a column or record the wrong path never reads) and one documentary (the filed clause), neither sufficient alone. This is also where the span floor comes from, because the evidence that forces the handling is deliberately not co-located with the data it governs.
3. **Silent on the wrong path.** The careless pipeline completes with no error and produces a plausible, internally consistent wrong number, and it reconciles everywhere it is habitually checked: counts tie, joins land, totals agree, with any offsetting engineered by construction. Anything that fails loudly (a parse error, a zero-row join, visible garbage) is texture, useful for realism and worth shipping, but it is not a device, because the opponent cleans loud failures reflexively. Reserve loud breakage for places where it cannot change any answer.
4. **Aimed, with magnitude.** Every mishandling lands on a specific wrong value, outside the ask's rounding bin by a stated distance, and every mis-repair lands on a decoy value with margin, never a near-tie. A near-tie converts difficulty into grading noise, and a tie is worse than either outcome, so tune away from it.
5. **Interior handling.** Over-cleaning costs the answer as much as under-cleaning. For every device, ship the genuine population a blanket exclusion destroys, so "distrust and drop everything suspicious" fails exactly like credulity. The correct knob value is interior, and each ask ladder in Part 6 carries one over-corrected stop to price it.
6. **The fairness guarantee, asserted.** The intended handling is unique, no second defensible rule reproduces the golden, and the handling reproduces truth exactly, asserted in the generator at plant time, not argued in prose. A device whose truth is unrecoverable from the shipped bytes is not hard, it is a determinism defect, and the register era's rule stands: an unrecoverable variant makes the answer a matter of interpretation and gets cut.
7. **Mechanism, not marker.** No batch id, source-system value, load stamp or single flag may isolate the device rows in one groupby. Blend benign rows into every batch the device touches, give every candidate classifier column a benign twin population, and check the shortcut yourself before shipping.
8. **No oracle.** Sweep the pack for anything that verifies a repair for free: a count identity, a manifest total equal to the repaired truth, name agreement, a round number that confirms the intended rule (the confirming bell), a column from which the answer inverts. Remove it, or engineer it to lie in both directions. Then keep **one referee**: a single independent corroborating file, byte-clean and never trapped, that arbitrates a designed disagreement without handing over any level. Every pack ships exactly one, chosen deliberately, recorded in the ledger.
9. **Authentic cause, shared causes.** Every device has an in-fiction root cause a real system produces, and one cause may feed several devices (a single migration yields the id-scheme backload, the stale snapshot and the frozen derived field). Fewer, deeper causes keep the pack coherent, keep the device count from reading as sabotage, and give the social layer something true to talk about without narrating any defect.

---

## Part 6. The per-ask ladder and the span floor

### An ask is a small ladder

Design every supplemental ask as three to five stopping points, each a complete pipeline a competent analyst would file, each landing on a **distinct** wrong value, only the last surviving the pack's own evidence. The canonical stops: the natural read, the half-handled device, the over-corrected read (law 5's stop), the right rule on the wrong population, the answer. Assert every stop's value and its distance from the golden, and keep every gap wider than the ask's rounding bin. The task63 ask-ladder file is the working model: per ask, a five-row table of stopping points and values, the file list, the column list, generated from the golden's own code path rather than written by hand, private, never shipped.

Ask shape rules ride along from the spec: **every figure inside an ask separately gradable and separately determinate**, unit and rounding stated inside the sentence that asks for it, the golden mid-bin, no ask wording that names a treatment, a device, or a trap word, and **the six realism tests in `../guide-to-prompt/SKILL.md`**, which a device-derived ask has to be checked against deliberately because its construction does not produce them for free. A multi-dimensional ask spanning ten units on three measures owes thirty determinate answers and every one of them is held to this.

### The span floor: eight files, ten to fifteen columns

**Every supplemental ask's correct computation touches at least eight shipped files and consumes ten to fifteen distinct columns, counted on the causal path from the golden's own code.** This is the standing floor for the layer, and it is what separates an ask from a lookup: the client's twelve targeted failure behaviours (head-of-file sampling, no cross-file reconciliation, format blind spots, join naivety, `guidelines/techniques.md`) are all behaviours an eight-file path exposes a solver to repeatedly, and a one-file ask exposes it to none of them.

**Span is causal or it is nothing.** For every file on an ask's path, misreading or dropping that file must be able to move that ask's answer, which the necessity matrix in Part 8 verifies mechanically. A file a solver could skip without consequence is decoration, its presence in the count is padding, and the audit will expose it. The honest ways to buy span:

- **Split the quantity.** Numerator parts in two files, the correction table in a third, eligibility in a fourth, the key resolution in a fifth, the calendar in a sixth. A quantity assembled from six sources cannot be skimmed.
- **Route through the resolution chain.** Fact file to correction table to register to crosswalk to manifest to dictionary to standard is seven hops that real warehouses genuinely have, and the chain is shared infrastructure every ask can cross while carrying its own primary device.
- **Separate the antidotes.** Law 2 already puts the structural antidote and the documentary antidote in different files, and the reconciling artifact is a third.

**The pack consequence, which is why this skill runs before `dataset-generation`.** At the 13-file median pack, an eight-file path means most of the pack participates in every ask. That is the hub-and-spoke schema: a small number of heavy files every ask crosses, per-ask satellites around them, and it has to be designed into the file roles before the spine is cut, because no pack built ask-blind will happen to support nine eight-file paths. Asks may share the backbone freely; **no two asks may share both their primary device and their file path**, or they are one ask graded twice.

---

## Part 7. Ask-level determinism

The judge holds every supplemental answer to the main call's bar: it must recompute from the shipped bundle and be uniquely forced, and one two-way-defensible answer fails the gate exactly as an ambiguous main call would (`determinism-check`, Gates A to E). The determinism work per ask:

- **Enumerate the readings the wording admits**, compute what each yields, and either prove convergence or pin the wording. Where a boundary case could split readings, use the convergence construction: align the data so every licensed reading selects the same rows, which closes the fork without a signpost.
- **Band by the margin you own.** Every designed wrong stop must sit outside any tolerance a graded criterion would reasonably grant, so a solver cannot land on stop 2 and be banded into credit. The margin is measured first, then the band is set inside it.
- **The device is forced by the organ, never by the ask.** The ask asks for the number; the dictionary's key definition is what makes deduplication the only defensible read; the version-of-record clause is what makes the vintage unique. If the only way to force a handling is to say it in the ask, the organ is missing and the device is not ready.
- **Verification extends the assertion regime.** The generator asserts, per ask: every stop's value, every delta, the bin distance, the file and column lists. Per device: the asks it moves with per-ask deltas, the main-call zero-count proof, the fairness guarantee. The independent verifier recomputes every ask answer and every ladder stop from the shipped bundle alone, and a stop it cannot reproduce does not exist. Budget for the ledger roughly doubling the build's assertion count, and treat that as the cost of nine committed answers rather than one.

---

## Part 8. The audit loop

Nothing outside the generator audits this layer before a solver round does, and a round grades the asks without explaining them, so the ask layer is audited by construction. Seven sweeps, all mechanical, all asserted:

1. **The lazy sweep.** For each ask, code the most natural competent path, the obvious files, no device handling, no organ read, and assert it lands on stop 1 of that ask's ladder, outside the bin. If the lazy path reaches the golden, the ask is a free criterion and the device is inert on it.
2. **The necessity matrix.** For each device, handle everything else correctly and mishandle only it, and record which ask answers move and by how much. A device that moves nothing is dead weight and comes out; a file whose misreading moves nothing on some ask's path is decoration and the span claim shrinks. The hazard table is this matrix's output, and it is rerun in full after every parameter change, because a tuning edit that silently kills a device costs exactly what a rung collision costs the main ladder.
3. **The pair simulation.** Two answer sheets, both swept the way the strongest solver works: the habitual hygiene battery applied, every filed rule the battery points at executed, and no device handling beyond that. The **cracker sheet** solves the main call correctly; the **mirror sheet** solves it *incorrectly*, at the ladder's most attractive stopping point, and is the second slot of the top two. Score both against the expected criteria and assert the pair average sits **at or under 40**, with each sheet's ask leakage near a fifth of the ask weight. This is the single sweep that tests what the layer exists for. Because every ask is decoupled, the two sheets should differ only in the recommendation criteria: an ask answer that moves between them is coupled, and it is re-routed or dropped.
4. **The over-cleaner.** Apply every plausible blanket hygiene rule (drop all duplicates, drop all flagged rows, drop everything the suspicious batch touched, trust no stale extract) and assert each lands on its designed over-corrected stop, not the golden. Paranoia must lose like credulity loses.
5. **The oracle and leak sweep.** Assert no un-repaired metric, free identity, count check or untouched column points at any golden ask answer, and that the one referee arbitrates its designed disagreement without leaking a level.
6. **The hygiene battery on the wrong path.** Per device, run the habitual battery (key uniqueness, exact duplicates, unmatched joins, fan-out, count ties) on the wrong path and assert it comes back clean. A device the battery surfaces is on the visible list in Part 4 and may only serve as a hazard or with its over-cleaning half.
7. **The separation count.** Assert zero device rows and zero hazard rows inside the main call's declared row population, and write the counts into the ledger.

Repair discipline: change one device per repair so the next matrix run is attributable, ship both halves of every patch (a new organ and the records it governs land together), and never repair by deleting an organ, because an unadjudicated device is a determinism defect wearing a difficulty costume.

---

## Part 9. Build order, the ledger and reuse

Where this skill sits in the pipeline, and what it hands each neighbour:

```
guide-to-prompt  ->  stumping (main ladder fixed)
    ->  THIS SKILL: ask sheet + device ledger, on paper
    ->  dataset-generation (pack built to carry both layers)
    ->  build, audit loop green  ->  determinism-check (self-run; judge rehearsal only if the author asks)
    ->  ask wording finalised against the golden  ->  submission-writeup
```

1. **Assign every ask its devices, by weight.** Typically three to five wide asks, all device-carried, none keyed to the call. Each is named with its primary device family (the silent list in Part 4 first, proven devices before new ones, no family repeated) and the hazards stacked on it.
2. **Compute the failure budget** (Part 3), lay the hazards, and write the correlated-weight sum into the design note.
3. **Design each ask's ladder and span on paper** (Part 6): stops, target values, the eight-file path, the organ pair, the root-cause fiction each device hangs from.
4. **Write the ask ledger into the design note.** Per ask: primary device, hazards crossed (at least one), file path, column list, stops with values, lazy delta, organ pair, **the named use (who acts on the answer and what they do differently)**, and the main-call insulation proof. Plus the main call's declared row population with the zero-counts, the hazard table, the referee's name, and the pair ceiling with both sheets' scores beside it. This ledger is what `dataset-generation` builds against, what the audit asserts, and what a determinism review reads to see the separation was designed rather than hoped.
5. **Hand off to `dataset-generation`.** The ledger scopes its mess-neutrality rule: every complication is either inert everywhere, or it is a ledgered device allowed to move exactly the asks in its row and nothing else, with the main call inert under all of it. The span floor shapes its file roles before the spine is chosen.
6. **After the build, run the Part 8 audit before the bundle goes to the portal**, and after the rubric generates, recompute the pair ceiling with the real weights.
7. **Word the asks last**, after the golden, against the ledger and the `stumping` Part 7 levers, then run the over-determination sweep across the full set.

**Reuse at this layer is free.** A device that worked in an earlier build can be spent again, in the next build and the one after: the mechanism, the organ's form, the ladder shape, the measured magnitude. Nothing rotates; reach for the proven ones first (`references/proven-in-production.md` Part 3 and the sort at the head of Part 4) rather than inventing an untested device for novelty. A main-call mechanism from a retired build can be demoted to an ask device too, and the clone check reads demotion as reuse. What is written fresh is the surface a reviewer compares, the file and column names, the fiction's nouns, the organ's wording and the ask wording, because the clone check's visible track reads exactly that. Inside one build no two asks share a primary device family (Part 3). None of this reaches the main recommendation: its driver is guarded by the fingerprint guard and the clone check, and no supplemental device carries the main call. Record which proven device each ask reuses in the ledger, so the portal result can be read against it.

---

## Part 10. Diagnosis

| Symptom | Diagnosis | Direction |
|---|---|---|
| Two responses land the main call | **A main-ladder failure, not an ask-layer one**: two responses on the call take both top slots at about 45 each before any ask | Back to `stumping`. No ask repair brings a pair of responses that both landed the call under 40 |
| The pair simulation clears 40, or the portal's top two average 40 or more with only one response on the call | The asks are leaking: primaries visible to the hygiene battery, one device per figure, devices inert, organs signposted or narrated, or spans decorative | Move primaries onto the silent list in Part 4, stack a hazard on every graded figure, grep the cut pack for each device's own vocabulary, run the necessity matrix, move organs behind joins, deepen the lazy deltas, and rerun the pair simulation with the battery applied. This is a Part 4/5 repair, never a main-ladder repair |
| A reviewer calls the ask set a litany, or an ask reads as written against a scoring sheet | A device ask was built device-first and never given a use, which its construction does not supply | Re-cut it to the quantity the decision needed anyway that happens to cross the same device. If none exists, the device sits in the wrong part of the pack: move the device, not the ask |
| An ask's answer differs between the cracker and mirror sheets | **The ask is coupled to the main call** | Re-route it off the corrected structure, or drop it |
| Two rigorous solvers split on one ask's figure | Ask-level determinism defect, the organ is missing or two readings survive | Fix the organ or build convergence. Never respond by making the ask harder |
| A device miss moves no ask outside its bin | Magnitude failure | Raise the device's mass or re-site the ask's golden mid-bin, then rerun the matrix |
| Mishandling a device moves the main call or its margin | **Separation breach, the highest-severity finding this skill has** | Stop everything, re-site the device off the main path or rebuild its rows, re-run the zero-count assertions, and only then return to difficulty |
| One discovery sweeps several asks | Primary-device collision, or a hazard doing all the work | Re-diversify the primaries; hazards may overlap asks, primaries may not |
| The rubric's ask criteria read as process ("describes the method") | Asks worded as instructions rather than quantities | Reword to determinate values with unit and rounding, regenerate |
| An ask cannot be computed without the main call or its decisive rung | Coupling | Re-route the ask through the backbone, off the ladder's structure |
| The pack reads as booby-trapped, or a reviewer flags intent | Too many root causes, devices without fictions | Consolidate devices under fewer authentic causes, cut the weakest |
| A graded criterion the golden itself would fail | Rounding-path or wording drift between golden and deliverable | The H5 repair in `reduce-house-fixes`, fix before anything is graded |
| Solvers find every device and the layer stops discriminating | Organs restated in multiple files, a marker column survived, or ask wording leaks vocabulary | Single-statement sweep, marker sweep, delete-on-sight sweep over the asks |

---

## Part 11. Pre-flight checklist

**Separation, run first**
- [ ] Every device and every hazard off the main call's path, proven by the zero-counts
- [ ] Litmus rerun with all devices deleted: the main task is still hard
- [ ] No ask is keyed to the call, inherits the corrected structure, or requires the decisive rung
- [ ] Every ask still enters the committed call as a component of its case, a reconciliation or an audit trail (H18), named in the ledger
- [ ] The main call's row population declared in the generator, with zero device rows and zero hazard rows inside it asserted
- [ ] Gate G flags unchanged and still true of the main mechanism

**Budget**
- [ ] Every ask device-carried and multi-dimensional, no inheriting ask unless the author asked for one, and no primary device family repeated
- [ ] Pair ceiling computed on paper, **at or under 40** against a bar of 50 (each top response's ask leakage about a fifth of the ask weight), recomputed from the generated rubric's real weights
- [ ] At most one response expected on the main call (the main ladder's job), because two take both top slots at about 45 each
- [ ] The ten-point margin understood as insurance against the on-platform verifier's inaccuracy and the post-submission regrade, not as caution
- [ ] Both sheets of the pair simulation run, with `r` **read off** the recommendation criteria that survive a wrong call rather than guessed, and no ask answer moving between the two sheets
- [ ] Hazard table written: three to five hazards, each moving several asks, per-ask deltas asserted
- [ ] Composed-mishandling deltas per ask outside the bin for every subset

**Devices**
- [ ] Every primary from the silent list in Part 4, or a visible-list device shipped with its over-cleaning half; proven devices reused before new ones are invented, re-skinned
- [ ] Every graded figure under at least two independent devices
- [ ] Every device unflagged, discovered only by internal inconsistency, with its adjudicating rule filed at authority
- [ ] Two antidotes per device, structural plus documentary, different files, neither sufficient alone
- [ ] Wrong paths silent, plausible and aimed; loud breakage reserved for answer-neutral texture
- [ ] Genuine population shipped against every device so over-cleaning fails; interior handling priced as a ladder stop
- [ ] Fairness guarantee asserted per device: unique handling, truth reproduced exactly
- [ ] No marker isolates device rows; oracle sweep clean; exactly one referee, byte-clean, named in the ledger
- [ ] At most one punish-the-repair device; every device hangs from an authentic root cause

**Asks**
- [ ] Every ask a three-to-five-stop ladder, stops distinct, values and distances asserted, golden mid-bin
- [ ] Every ask **multi-dimensional and internally correlated**, so a device-blind path loses the whole ask rather than one criterion, and none of them stacked simply to raise the count
- [ ] Eight-plus files and ten-to-fifteen columns per ask, counted causal from the golden's code, necessity-verified
- [ ] No two asks share both primary device and path; ask wording names quantities, never treatments, no trap vocabulary
- [ ] Every ask passes the six realism tests, and each device ask in particular has a **named use** and a quantity the decision needed anyway, rather than one reverse-engineered from its device
- [ ] Unit and rounding inside every value; every figure inside every ask separately gradable and determinate; readings enumerated, convergent or pinned
- [ ] Any inheriting ask the author asked for swept for over-determination and for teaching the ladder by repetition

**Audit**
- [ ] Lazy sweep, necessity matrix, **pair simulation (cracker and mirror sheets, battery applied)**, over-cleaner, oracle sweep, hygiene battery on every wrong path and the separation count all green in the generator
- [ ] Independent verifier recomputes every ask answer and every stop from the bundle alone
- [ ] Ask ledger complete in the design note; ask-ladder file generated from the golden's code path, unshipped
- [ ] Matrix rerun in full after the last parameter change

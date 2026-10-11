---
name: supplemental-stumping
description: Design the ask layer, the asks that carry about 55 to 60 per cent of the generated rubric, against the pass bar (the top two responses averaging under 50 per cent, built to 40). Every ask is designed against the careful solver's path: the cracker sheet (the response that landed the call, ran the hygiene battery and executed every filed rule) must miss every ask figure, so no device is adjudicated by a filed rule, a marker or a referee on the ask's own path and no ask is keyed to the call or to its construction. Carries the pair arithmetic including the one-cracker case, the two layers on every ask (the construction output on a segment, decoupled from the call, and one silent piece of realistic Layer 1 mess on a path the main call never reads), the span floor, ask-level determinism, the in-generator audit with the ask gate grade.py enforces, the ask sheet the design note carries, and the returned-task revision. Runs after stumping fixes the ladder and before dataset-generation cuts data; also when a round or a portal result shows the asks leaking.
---

# The Ask Layer

> The main ladder defends 30 to 40 points of the rubric; the asks defend about 55 to 60. A response that
> lands the main call banks about 45 before it answers an ask, and the second slot of the top two is the
> best response that missed the call. So every ask is designed for two excellent readers at once: the
> one that cracked the trap and the one that did not, and both have to miss about four-fifths of the ask
> weight. The record says where that fails: an ask whose device a filed sentence adjudicates, a referee
> that ties only under the golden, an ask keyed to the construction, a visual whose order and title fall
> with the wrong call. Fewer, harder, decoupled asks, each written against the careful solver's path.

**Navigation.** Part 0 the goal and the pair arithmetic · Part 1 design against the careful solver's
path · Part 2 two layers, silence and span · Part 3 ask-level determinism · Part 4 the audit and the ask
gate · Part 5 the ask sheet · Part 6 the returned-task revision · Part 7 diagnosis

**Prerequisites.** The pairing is fixed (`guide-to-prompt`), the ladder is fixed (`stumping`) and the
design note carries the default path and the stump sentence. The ask layer is designed on paper before
any data is cut, because the span floor is a schema decision the pack has to honour; the ask wording is
finalised last, after the golden. `references/proven-in-production.md` carries what the record paid for
every rule below; read its Part 2 (what killed an ask layer) before any device is chosen.

---

## Part 0. The goal and the pair arithmetic

The generated rubric puts 30 to 40 per cent on the recommendation and its critical components, 5 to 10 on
instruction following and about 55 to 60 on the asks. At the planning weights (38 / 7 / 55):

```
C  =  38 + 7 + 55 x Lc        the response that landed the call
S  =   r + 7 + 55 x Ls        the best response that missed it
(C + S) / 2  <=  40     when     55 x (Lc + Ls)  <=  28 - r
```

`L` is the share of ask weight a response still earns and `r` the recommendation weight that survives a
wrong call (about 5, read off the generated rubric once it exists). At `r` about 5 the pair may keep about
23 of its 110 ask points, **roughly a fifth each**. That is the pair ceiling; it is computed on paper
before any wording exists and recomputed from the real rubric when it generates.

**The three cases, and which layer carries each.**

- **No top response lands the call** (the measured outcome on the client's hardest tasks). The
  construction layer costs the pair everything and the device layer is margin.
- **One lands it, the cracker.** The construction layer hands the cracker its ask weight, so only the
  device layer holds the pair under 40. This is the case the layer is built for, because the record does
  not let you plan on the first: the top slot sat at or near 100 on task98 v3 and v4 and on task133 v1.
- **Two land it.** Both top slots sit at about 45 before an ask; no ask layer rescues it. That is the
  main ladder's failure (`stumping` Part 0).

**The second slot is the response that missed the call**, and it is where builds have lost the average:
task181 missed the call in both in-house rounds and still kept 65.2 and 59.0 of the proxy; the proxy was
never gated, and the portal returned 52 with the call held. Eight portal results in the window scored 50
to 100 with the main call stumped or deterministic. `grade.py`'s ask gate (Part 4) exists for this.

**Why 40.** The on-platform verifiers are inexact and the task is regraded after submission. Ten points
is the margin, and it is bought here, because the ladder's own margin is spent on determinism.

**Fewer, harder asks.** Difficulty is bought per ask, through span, device mass and ladder depth, never
through count. Ten shallow asks hand a strong solver ten small wins; three wide ones hand it three
probable losses. An ask spanning every segment on two measures is twenty-plus criteria that a device-blind
response loses together, which is the multi-dimensionality the spec asks for.

---

## Part 1. Design against the careful solver's path

### 1.1 The cracker sheet, written before any device is chosen

Write the response that landed the main call, as it actually works: the construction right, the hygiene
battery run (key uniqueness, exact duplicates, unmatched joins, fan-out, counts that tie), every filed
rule the battery or the documents point at executed, every control total reconciled, every published
figure matched. Then score it on every ask, figure by figure, chart by chart. **Every row must miss**,
outside the ask's rounding bin, and the sheet goes into the design note's `## Ask sheet` where
`precut.py` reads it. An ask the cracker gets is rebuilt, not accepted.

The mirror sheet is the same response at the ladder's most attractive wrong stop. Because every ask is
decoupled (1.3), the two sheets differ only in the recommendation criteria; an ask figure that moves
between them is coupled and is re-routed or dropped.

### 1.2 Four bans, each a measured death

1. **No device adjudicated by a filed rule on the ask's own path.** A rule whose relevance the solver
   cannot miss gets executed: task105 v4's strongest response filed the main call and every ask figure by
   carrying out the four filed device rules; task118 x3, 122, 123, 228, 229 and 133 loop 1 died the same
   way in-house. An ask's golden takes the handling the records support; a filed sentence may exist where
   the real organisation would have one, but it never adjudicates the device, and the device's
   inconsistency is visible only at a cross-file or cross-grain cut nothing invites.
2. **No marker.** No batch id, source-system value, load stamp, flag or single column isolates the device
   rows in one group-by. Blend benign rows into every batch the device touches and give every candidate
   classifier column a benign twin population.
3. **No referee or control that ties only under the golden handling.** A reconciling artifact that
   confirms the solver's handling for free is an oracle (task122 x2, 123, 118). The pack keeps **one
   referee**, byte-clean and never trapped, that arbitrates a designed disagreement without handing over
   any level; it is named in the ask sheet. Everything else that ties, ties under every handling.
4. **No ask keyed to the call or to its construction.** "For the option you recommend", a split or
   sensitivity of the committed figure, the ladder's own population walk, a chart ordered on the decision
   quantity: the cracker banks all of it (task133 v1 at 100 on the portal, task118 and 119 at design,
   task134 before its first round). An ask is decoupled in computation and inside the decision (1.3).

### 1.3 Decoupled in computation, inside the decision

`reduce-house-fixes` H18 binds every ask: independence of difficulty is the point, independence of
decision is a rejection. Every ask enters the committed call as a component of its case, a reconciliation
of an input to another total, or the trail that audits an input, and the ask sheet names which. The homes
that are both decoupled and inside the decision:

- the other measures the deliverable carries for every candidate, on which the call does not turn (the
  cost beside the forecast, the capacity beside the demand, the realised loss beside the provision),
  computed from rows outside the main call's population;
- the trail that audits an input the call consumes, worked through device-carrying rows the call never
  reads, back to the input's control total;
- a reconciliation of an input or candidate figure to another system's total, where the gap is made of
  the devices.

If the only asks that pass H18 for a decision are inheriting ones, the decision is too narrow to carry an
ask layer and the fix is upstream in the draw, never a second decision bolted on.

### 1.4 The visual is on the sheet too

A chart's ordering, its labels and its title are graded criteria, and they fall with the wrong call when
they are built on the decision quantity: task134's rating ask held on its clock device while the chart's
order and title named the same district on the wrong path. Order and title a visual on the ask's own
quantity, and score them as rows on the cracker sheet.

---

## Part 2. Two layers, silence and span

### 2.1 The construction layer

The ask's quantity is the decisive construction's output cut by a segment the stakeholder would ask for
anyway (by region, tier, period, product and quarter; the runner-up and the gap), so a response on the
wrong unit, population or method is wrong on every figure at once. It is keyed to the construction only by
being unanswerable without it, never by name, and it is never a split of the committed figure (1.2, ban 4).

### 2.2 The device layer, which is the client's Layer 1

Each ask also crosses **one primary device** on rows the main call's declared row population never
touches, plus at least one shared hazard, so the figure is wrong whenever the device is mishandled
whatever the solver concluded about the construction. A device is realistic system behaviour from
`../dataset-generation/references/layer1-messiness.md` (a migration, a cutover, a vendor feed, a
reporting lag, a superseded document, a unit set per source by agreement), never corruption, truncation,
a decoy figure or a defect placed to be caught. The test for every device: would this organisation's real
export look exactly like this if nobody had designed a task around it?

An ask is free of the main call's rules: it needs no filed rule to pin its handling, its golden may go
against the procedure where the records support a different handling, and its device may turn on reading
a field, code or unit correctly or on applying a rule correctly, which rule 3 bans only as the main call's
decisive step. Realism is the one rule it shares with the main call.

**Silent, never louder.** The top responses run the hygiene battery by reflex and then execute whatever
filed rule adjudicates what it surfaced, so a device the battery finds is a work order (task73 v2: every
rebuilt device executed by both top responses). The mess that scores completes and reconciles on the wrong
path everywhere it is habitually checked, with the inconsistency visible only at a cross-file or
cross-grain cut. Measured holds: a stored label taken before a silent switch (task98 v4, portal), an
event's quantity repeated on every covered line with the grain unstated (task20 DEC-6, portal), a clock
against a filed cutoff (task134, in-house). Devices the battery finds (exact duplicates, sentinels,
roll-up lines inside detail, displaced fields) serve only as hazards, or ship with the over-cleaning half
so the reflexive repair lands on its own wrong value.

**The families** (the card's Layer 1 vocabulary; one line each, instantiated fresh on the build's own
data): D1 duplication and identity (replays under fresh ids, keys recycled across entities, genuine
repeats a blanket dedup destroys) · D2 version and vintage (the version of record is the latest accepted,
a history loaded as a state, a vintage whose totals are invariant) · D3 meaning and units (units set per
source, quote conventions per row, scale pinned by one ledger figure) · D4 absence and sentinels (a
reporter or channel absent, blanks that mean nobody filed, sentinel dates) · D5 scope and population
(silently partial extracts, rows outside the decision population identifiable only structurally) · D6
grain and aggregation (detail and rollup in one file, an event fanned onto every covered line) · D7 keys
and linkage (the true key in another field, a prior-id chain, effective-dated joins with a far edge) · D8
time and clocks (a clock against a filed cutoff, settlement where the order date is needed) · D9
self-validation (a control that passes on the broken read; kept out of the ask paths under 1.2, ban 3,
except the one referee).

**Stack on every graded figure.** One primary device plus at least one shared hazard, each moving every
figure in its ask together, no primary family repeated across the set. Three to five hazards per build,
each moving several asks, each in the ask sheet's hazard table with the per-ask delta. Compose the deltas
for every subset of mishandlings and assert none lands inside the bin.

### 2.3 The span floor

Every ask's correct computation touches **at least eight shipped files and ten to fifteen distinct
columns**, counted on the causal path from the golden's own code, and the necessity matrix (Part 4) shows
each file moves the ask when misread. Span is bought by splitting the quantity across sources, routing
through the resolution chain (fact to correction table to register to crosswalk to manifest to
dictionary to standard) and separating the antidotes (a column the wrong path never reads, in one file,
and a second file that corroborates it). At the 13-file median pack an eight-file path means the hub-and-
spoke schema is designed into the file roles before the spine is cut. No two asks share both their primary
device and their file path.

### 2.4 The use test

A device ask is designed backwards, from a device to a quantity that crosses it, and that construction
does not land on something a person would want. Three tests, from `guide-to-prompt`: **use** (name who
acts on the answer; "nobody, it exercises the migration device" is not finished), **vocabulary** (the
stakeholder's words, never the analyst's, because analyst vocabulary is where a device leaks), **genre**
(the ask belongs in the file it sits under). The repair runs device-first then use-first: find the
quantity the decision already needs that happens to cross the device, and if none exists, move the device.

---

## Part 3. Ask-level determinism

Every supplemental answer recomputes from the shipped bundle and is forced by the records, never by the
procedure. Per ask: enumerate the readings the wording admits, compute each, and prove convergence or pin
the wording; band by the margin you own, so no designed wrong stop sits inside a tolerance a criterion
would grant; let the organ force the device, never the ask (if the only way to force a handling is to say
it in the ask, the organ is missing). The generator asserts per ask every stop's value, every delta, the
bin distance, the file and column lists; per device the asks it moves with per-ask deltas, the main-call
zero-count proof and the fairness guarantee (the intended handling unique, truth reproduced exactly). The
independent verifier recomputes every ask answer and every stop from the bundle alone.

Every ask is a small ladder of three to five stops (the natural read, the half-handled device, the
over-corrected read, the right rule on the wrong population, the answer), each a distinct wrong value
outside the bin. Over-cleaning costs the answer as much as under-cleaning: ship the genuine population a
blanket exclusion destroys, so the correct knob value is interior.

---

## Part 4. The audit and the ask gate

Seven sweeps, all mechanical, all asserted in the generator:

1. **The lazy sweep.** The most natural competent path per ask, no device handling, lands on stop 1,
   outside the bin.
2. **The necessity matrix.** Mishandle one device with everything else right, record which ask figures
   move and by how much; a device that moves nothing comes out, a file whose misreading moves nothing is
   decoration. Re-run in full after every parameter change.
3. **The pair simulation.** The cracker sheet and the mirror sheet (Part 1.1), both with the battery
   applied and every filed rule executed, scored against the expected criteria: the pair average at or
   under 40, each sheet's ask leakage near a fifth, every cracker row a miss.
4. **The over-cleaner.** Every plausible blanket hygiene rule lands on its designed over-corrected stop.
5. **The oracle sweep.** No un-repaired metric, free identity, count check or untouched column points at a
   golden ask answer; the one referee leaks no level.
6. **The hygiene battery on the wrong path**, per device, comes back clean.
7. **The separation count.** Zero device rows and zero hazard rows inside the main call's declared row
   population, counts written into the ask sheet.

**The ask gate, enforced by `grade.py`.** The in-house round grades every ask figure at half a unit of the
stated rounding (no relative band: task229's 0.5 per cent band hid a leak). When the solver misses the
call and still keeps 35 per cent or more of the ask weight, or cracks any ask item, `grade.py` exits 3
(ASKS LEAK) and the round does not pass; the repair is this layer's, in a fresh agent, and the next round
is a fresh sandbox. A round the solver lands sends the build to the ladder first (`build-pipeline`).

Repair discipline: one device per repair, both halves of every patch (a new organ and the records it
governs land together), and never a repair by deleting an organ, because an unadjudicated device is a
determinism defect wearing a difficulty costume.

---

## Part 5. The ask sheet

The design note's `## Ask sheet` carries, and `precut.py` reads: per ask its primary device family and
hazards, its file path and column count, its stops with values and the lazy delta, the named use, the H18
home (component, reconciliation or audit trail), and the realism sentence for its device; the main call's
declared row population with the zero-counts; the hazard table; the referee's name; the cracker sheet
with every row a miss; `Pair ceiling:` with the figure, at or under 40, recomputed from the real rubric
when it generates. This is what `dataset-generation` builds against and what the audit asserts.

Reuse at this layer is legal and never free: a device that held can be spent again on new data,
re-skinned, but a device reused across consecutive builds or a device set that repeats one build's set is
a template finding. Record which measured device each ask reuses.

---

## Part 6. The returned-task revision

A shipped task the author brings back with portal feedback is repaired on the fast path
(`build-pipeline`, Returned tasks): design, build, commit, ship, with the free mechanical gates only
(`precut.py`, the generator's checks, `verify`, two byte-identical rebuilds, `leak.py`, `guard.py`,
`voice-check.py`). No leak reader, solver round, judge or clone check runs for it. This Part is the ask
side of that path.

**When the main call held** (stumped and deterministic) and the asks carried the score: the repair edits
the ask paths' data alone (the devices, the rows they sit on, the ask goldens and their assertions). The
prompt, the card, the ladder, the main call's rows and every document under `target/` stay as they are;
the one document edit allowed is a field description for a new column in a file only the asks read. The
gate, asserted in `checks.py` against the shipped commit: every file the main call reads and no ask
touches is byte-identical; in a shared file every row inside the main call's declared population is
unchanged and the file gains no column; every main-call figure recomputes unchanged on the generator and
the verifier. A device that needs a main-call row, a rule the main call reads or a new shared column is
dropped, not argued. One asserted line per new device: the natural read lands off the golden, outside the
bin.

**When the main call fell too**, the designer's repair of the ladder comes first (`stumping` Part 8) and
the asks are redesigned against the new cracker sheet in the same pass, because a new decisive step moves
what the cracker holds.

Then, in order: rebuild, two builds byte-identical; refresh every place a moved figure is written
(`submission.md` through `submission-writeup`, the goldens, `metadata.json`); one line per device in the
ask sheet and one `## Tried and rejected` line for the round; re-cut `target.zip`; commit and push;
`pipeline.json` records the revision; Status `shipped` on main in its own commit. The author re-tests.

---

## Part 7. Diagnosis

| Symptom | Diagnosis | Direction |
|---|---|---|
| Two responses land the main call | a main-ladder failure | `stumping`; no ask repair reaches 40 |
| The solver missed the call and `grade.py` reads ASKS LEAK | the asks are free to the careful path: a filed rule adjudicates a device, a marker isolates it, a referee ties, or an ask is keyed to the construction | rewrite the cracker sheet, then move each failing device's adjudication off every sentence and column, make every control tie under both handlings, re-route keyed asks; a fresh round |
| The cracker sheet gets an ask | the ask inherits the construction or its device is readable | Part 1.2; re-route or rebuild |
| A chart's criteria fall with the wrong call | order, labels or title built on the decision quantity | Part 1.4 |
| An ask's answer differs between the cracker and mirror sheets | coupling | re-route off the corrected structure, or drop |
| Two rigorous solvers split on one ask's figure | an ask-level fork | fix the organ or build convergence; never respond by making the ask harder |
| A device miss moves no ask outside its bin | magnitude failure | raise the device's mass or re-site the golden mid-bin, re-run the matrix |
| Mishandling a device moves the main call or its margin | separation breach, the highest-severity finding here | stop; re-site the device off the main path; re-run the zero-counts |
| A reviewer calls the ask set a litany | a device ask with no use | the quantity the decision needed anyway that crosses the device, or move the device |
| The pack reads as booby-trapped | too many root causes | consolidate devices under fewer authentic causes, cut the weakest |
| Solvers find every device | organs restated, a marker survived, ask wording leaks vocabulary | single-statement sweep, marker sweep, grep the pack for each device's own words |

## Checklist

- [ ] Cracker sheet written first, every row a miss outside the bin; mirror sheet differs only on the recommendation criteria
- [ ] No device adjudicated by a filed rule on its path; no marker; one referee, byte-clean, named; no ask keyed to the call or its construction; every visual ordered and titled on the ask's own quantity
- [ ] Every ask decoupled in computation and inside the decision (H18 home named), with a named use
- [ ] Every ask a construction output on a segment plus one silent primary device and at least one hazard; no primary family repeated; every device realistic and from the Layer 1 library
- [ ] Eight-plus files and ten to fifteen columns per ask, necessity-verified; no two asks share device and path
- [ ] Pair ceiling at or under 40 on paper and again from the generated rubric
- [ ] Ask-level readings enumerated, convergent or pinned; every stop and delta asserted; the verifier recomputes every ask
- [ ] The seven sweeps green; zero device and hazard rows inside the main call's population
- [ ] The ask sheet complete in the design note; `precut.py` passes
- [ ] The round's `grade.py` gate read: ASKS LEAK sends the build back to this layer

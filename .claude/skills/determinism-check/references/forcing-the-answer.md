# Forcing the answer

What made the shipped builds deterministic, as construction rules. Determinism is built while the ladder
and the generator are written, not inspected after the cut. The verdicts that come back are almost all
ambiguity, not arithmetic (`underspecified_objective` 31 times over 18 builds, `semantic_fork` 6,
`solution_incorrect` 2), and they come from an axis nobody enumerated, not from a missing verifier
(task62's rounding path, task42's three readings of one clause 13.35 per cent apart). So the work is a
closed enumeration (Part 1) and a closure move per axis (Part 2), written as one line per axis in the
design note's `## Closure table`, which `stumping/precut.py` reads by axis number.

## Part 1. The 22 axes

Walk every row on every build, including rows that cannot move the answer today: they become
load-bearing when another parameter moves (task65 asserts the population moves composition and totals but
not the fee). A convention placed in the prompt is not closed; it hands over the insight (Part 6.1).

| # | Axis | The open question | Usual closure (builds) |
|---|---|---|---|
| 1 | Population | which records are in the set | estimand filed literally, unobserved members stated; C1 (35, 39, 59, 74) |
| 2 | Unit of account | row, entity, person, household, firm | the question names the unit; C4 at a factor (42, 77, 81) |
| 3 | Attribution window | which period a fact falls in | C1, records clear of the boundary (35, 63, 78) |
| 4 | As-of dating | state at the pull, the event month or period end | filed as-of date; static schedule across the window (42, 81) |
| 5 | Version basis | current version or as it stood at settlement | C1 or filed basis (41) |
| 6 | Denominator | what sits under the line | filed in the standard's own words; C4 (63, three divisors 15 to 17 per cent apart) |
| 7 | Weighting | pooled, equal by group, by billing unit | filed criterion or C4 (71, four bases 21 to 70 days) |
| 8 | Window length | how far back a rate is measured | C1 across lengths (37) or C3 |
| 9 | Boundary inclusivity | strict or not | C1, nothing on the edge (41, 66) |
| 10 | Rounding path | once, per line, per group, before a total | filed at authority (65, 7.6(e) rounds each source down); asserted (70) |
| 11 | Tie-break | two levels for level candidates | filed two-level rule, first level resolves nearly all (60) |
| 12 | Maturity and censoring | all cohorts or only fully observed | filed in one governing sentence or C1 (75, 79) |
| 13 | Order of operations | non-commuting steps | filed order; C4 (58, wrong order 20.47 per cent) |
| 14 | Row order | file order changes the result | C1, asserted over permutations (37, six orders) |
| 15 | Duplicate resolution | first, last, both, collapse | C1 (63, both filings carry one volume) or filed rule (42) |
| 16 | Identity normalisation | same entity across systems | the systems' own keys and crosswalks, C4 (74, normalised GTIN 347 of 347, raw misses 129) |
| 17 | Netting against gross | may two tails offset | filed scope; C4 (49) |
| 18 | Dimensional units | are the added quantities the same | units in the data; C4 (65, six of 24 materials, 22.4 per cent) |
| 19 | Code and status semantics | what a code means for the calculation | the code's own crosswalk or a governing definition (71, 39); never the stump |
| 20 | Integerisation | floor, round, remainders, order | C1 by construction (64, whole packages, six disciplines one cent) |
| 21 | Clause scope | year, test or record | filed scope, C1 (37) |
| 22 | Forward window contents | what the committed window holds | a shipped driver file for the uncovered span (50, 53, 62, 78) |

## Part 2. The closure moves, strongest first

**C1 Converge.** Build the records so every reading selects the same rows. Find the boundary the readings
disagree on and put nothing on it: a period-shaped clause disagrees at the far edge (a covered period
running past an exit) and in the gap between spans, so place every record wholly inside one span; a
date-shaped clause disagrees at the boundary, so keep every event a stated distance clear (task66, twelve
days). Example: task42's four readings of a period clause all return USD 6,468,921.99 on the same 5,416
lines and 1,829 households. Assert the figure **and** the row and entity counts. Never write "identical
either way" without the assertion (task42 shipped it while two keys differed by USD 20,958.71 on 113 lines).

**C2 Confirm a filed criterion on closed data.** The governing document files the criterion in general
terms; a closed record shows exactly one candidate satisfies it. Never recovery of an unfiled rule, which
is a hidden rule (banned as the decisive step, capped by the client, an open fork to a literal judge).
Example: task71, one weighting at 32 of 32 published cells, nearest rival 2 of 32. Five properties, each
checkable:
1. **Exhaustive family**: run all of it (task39, all 1,024 partitions of ten codes), state the count, report
   the **worst** miss.
2. **Zero tolerance**: the survivor exact on every case, rivals missing outright; "fits better" is a preference.
3. **One survivor**: two survivors pin nothing.
4. **Blind to the decisive move** for a stated structural reason (task56, the population is zero in every
   closed cycle; task81, no register change inside the pilot window), or a back-testing solver finds the answer.
5. **Rerunnable from the bundle** (task55, the verifier recovers the lead with no generator state).
Where lookup transfer threatens, add a twin pair (two cases identical on every visible column, outcomes
about 2x apart; at least sixteen builds shipped one).

**C3 Corridor.** For a quantity estimated rather than read: every admissible value returns the same
answer. It needs a real quantisation (a publication step grid, a filing increment, a purchase block), with
the estimate mid-cell and the whole admissible family inside it. Example: task40, no filer between 192
and 209, so every ceiling 193 to 209 gives the same provision to the cent ("forced without the number that
generates it being knowable"). Recompute the whole admissible family under shifted conventions (task71,
day counts moved two days either way; task75, four run-off implementations inside one block). State the
slack as a number; a corridor with no slack is a coin flip (task35, two asks within 1 per cent of a $0.1M
edge).

**C4 Separate.** Compute every cell of the cross product of independent choices, each distinct, each
mapped to the shipped sentence it violates, the nearest wrong cell at least 6 per cent away (builds ran
8.4 to 18.8 per cent). Under 6 per cent only when the near cell needs two errors in opposite directions
(task62 at 0.59, task65 at 1.4); otherwise move a rung, do not write a paragraph. Make the answer the
grid's extreme cell where possible (task76, task78), so half-applied corrections cannot cancel onto it.

## Part 3. Bins and the flip condition

A binned figure is deterministic only when nothing in the admissible family crosses the bin edge, and the
only way to know is to compute the distance. Every graded figure sits mid-bin on a non-round value, at
least about 7 per cent of a bin from the edge (task72), with its flip condition stated as a number: "the
Minimum would have to fall to 7,651 before 96 replicates carry it" (task79), not "the margin is
comfortable". Two independent estimators agreeing inside the bin is strong evidence (task54, 0.076 per
cent apart). The deliverable's display precision must not move a bin (task83, cells at two decimals land
every figure in the full-precision bin). The rounding path is an axis and the one most often missed:
task70 reproduced the invoice per collection point to the penny and missed by two pence per operating
date, so every summary artifact the generator emits rounds the way its lines do, one arithmetic with the
golden, asserted. In a bin of width w the clearance is at most w/2, so re-centring cannot absorb a
modelling spread (task47); pin the estimator or widen the gap. Measure a one-decimal figure's distance to
x.x5 (task55). Never grade an iteration count, a median of an even-sized set, or a percentage near a
one-decimal edge where a count would do (task57).

## Part 4. How determinism is lost

| Symptom | Repair |
|---|---|
| A semantic pin never operationalised: filed at the right level, naming no field, still several readings (task42, 13.35 per cent) | converge (C1), never a second pin: a pin naming the field turns the rung into a lookup and trades Gate C for Gate F |
| The deciding axis never enumerated (task62) | the Part 1 walk in writing before the cut |
| A decision metric in the requester's own voice while a filed policy ranks on another (runs reproduce every number and split only on which objective governs) | demote it to an attributed claim |
| A convention declared in the write-up, not closed | the ten-of-ten test: if a competent analyst could go the other way, it is a decision; pin or converge |
| An unasserted convergence claim (task42) | assert it in the generator and the verifier, or delete the sentence |
| A thin margin over a live estimation range: two rigorous solvers on the same method reach opposite answers | pin the estimator (task59, the rate struck on the settled cohorts together) or widen the margin |
| A figure reproducing only under a read the file's grain forbids (a delta feed averaged as a panel) | carry each entity's last value forward, recompute; it is `solution_incorrect` even when the winner holds |
| A corpus able to score the decisive move | give it a stated structural reason to be blind (C2.4) |
| The sign of a cohort claim flips under another window (task73, +217 against -72) | assert the sign across every admissible window |
| A window term on a nameable date with records near it | put the date in a gap in the records, assert the gap (task55) |
| Codings of a filed criterion on a real coded field (task57, three of seven tests with two readings) | enumerate the codings, measure the set difference before writing the clause |
| Inclusion readings of a delta or cumulative feed (task44) | converge or violate a shipped sentence; compute on reconciled values |
| Mid-period proration (task40) | move whole periods at boundaries |
| A strata choice straddling a rounding edge (task73) | a filed rounding convention, never a pinned strata |
| A rule at two authority levels agreeing on one side and diverging on the other (task60) | make the situation not arise and assert both readings equal; never patch the lower document |

## Part 5. Three ways to force an open method

The estimand is always filed literally; the method may stay open only when something forces it, and the
data separates every reasonable candidate with margin, asserted.
1. **The design forces it.** The estimand plus the data's structure rule out every other method
   (censoring visible in the records, a contaminated comparison group, a mix-driven rate, a binding
   constraint). Nothing says so; the analyst must see it. Preferred.
2. **A governing standard's general method,** stated as the field states it (an actuarial standard on
   development, a survey standard on weighting); the step it leaves open is the stump.
3. **A filed selection criterion** in general terms, never naming the method ("the basis that, applied
   at the same point in the last closed period, comes closest to that period's final figure on every unit,
   closeness the largest miss"), confirmed by C2. A recognisable organ: never in consecutive builds.
With the method itself filed, the decisive step is rule application and the stump is gone. With nothing
forcing it, two methods survive (`underspecified_objective`).

## Part 6. Pins, grids and assertions

### 6.1 Pin authority

Highest first: **0 the prompt** (states the question, each ask's unit and rounding; no convention, since it
outranks everything and hands the insight over); 1 governing standard, policy, regulatory terms; 2
charter, SOW, contract, rate schedule; 3 decision memo; 4 method notes on an export; 5 thread or notes.
No dictionary, field notes or manifest ships (`dataset-generation` §3). A pin sits at or above every sentence that could argue the other
way. Fatal: the **counter-pin** (another file states the opposite) and the **outranked pin** (a level-5
pin against a level-1 implication). Fix by moving the pin up, relabelling an artifact in-file for the
question it answers, deleting an outranking endorsement. Sweep the pack for sentences quotable against
the answer (the constraint's nouns; *defensible*, *added*, *raised*, *increased* near them) and qualify
every absolute claim with its grain (task64).

### 6.2 The fork grid

List every choice a competent analyst could make differently; the answer wins every cell or the choice is
pinned. Assert cell by cell, each losing cell named and mapped to the clause, gate or file convention it
violates; "wins 8 of 12" is a summary, and an unmapped cell is an open fork. Ten-of-ten test per
assumption. Pin the nuisance axis, never the decisive one. Before claiming N rival readings, test each
against a careful read of the clause; claiming rivals the wording excludes invites "the difficulty is
semantic" (task44).

### 6.3 Convergence construction

- Check every interval the answer touches at the far edge (an as-of join on entry ignores the exit) and
  in the gap (a backward as-of join gives the gap to the closed span).
- Where an ambiguity cannot close, make both handlings return the same winner ("reattributing the
  transferred units or dropping them returns the same winner").
- Integerisation on a forward quantity: align quantised units with capacity constants so floor, round,
  largest remainder and none coincide (task64, $6,700 across six tie-breaks before).
- Converge at the finest pool a solver could defend: de-mean inside each subgroup (task43, 5.4 per cent).
- Close silent sweep forks in the data: no event ending on a day another lands in the same unit (task57).
- Convergence is bought with sample density, separation with block size; tune them separately and re-sweep
  every separation after closing a fork, since a separation can be borrowed from the fork (task44).
- A threshold family (drop addresses held by more than t) must cross the answer somewhere: put the
  crossing at an unnatural t, every round t at least 10 per cent off, the corpus refusing the family; sweep
  string heuristics on an entity exactly like columns (task58).

### 6.4 The robustness sweep

State it with counts: "holds across N of N combinations, narrowest margin 1.16x"; "holds at floors 1, 5
and 25"; "holds with the largest rival excluded". Rival-killers are audited as hard as the answer: run the
seventeen rivals you claim and report the worst miss.

### 6.5 Construct the disagreement

A rung on two axes disagreeing needs the correlation built per candidate and asserted both ways;
independent draws leave it inert. Place inert instances where they change nothing, or the constructing
field is the giveaway column (task60, 29 spring executions, 16 load-bearing).

### 6.6 The assertion regime

Compute forward, never backward. Assert, 40 or more: each rung's winner by name and margin; the position
table; discriminator dominance; the calibration back-test and swept count; the fork grid cell by cell;
every C1 equality on figure and counts; the C3 corridor; every graded figure's bin distance and flip
condition; every closure-table axis, including those that cannot move the answer; the generation tells (no
headline total on a round boundary, no exactly round share); each load-bearing fact in one file; the input
gates. Ship an independent verifier on a code path sharing
nothing with the generator (task71, pyarrow against pandas; task83, the golden used only as expectations).

Generator disciplines, each from a build that shipped wrong without it:
- Assert the structure the design depends on in the shipped records, not in a variable (task56); apply the
  extract cut at source, never at pack-write time (task60).
- The ground truth is the projection a solver can make, not the realised value (task56); run the golden
  script against the shipped bundle first, as the first solver.
- Write the verifier before the mechanism; a verifier falling into the stump is the measurement (task60).
- Build the ladder by construction and let the seed decide texture only; one RNG stream per period, so a
  change in one period does not re-roll the graded one (task56, task69).
- Read shipped constants from the one definition the model implements; check rounding distance and
  adjacency of every ordered pair on every redraw (task60, task73).
- A column whose rows and total are computed differently, or a rank or share silent on rounded against
  unrounded, is charged by the rubric: rebuild both from the unrounded source and assert (task60).

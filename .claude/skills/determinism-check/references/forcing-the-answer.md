# Forcing the answer: what actually made 44 shipped builds deterministic

> **Source.** The **Justification** blocks of the shipped `submission.md` for tasks 35 to 46, 48 to
> 56, 58 to 60, 62 to 72, 74 to 81 and 83, where those builds argued forcedness and had to say out
> loud why no second answer survives. Read alongside them: the review record in every `DESIGN_NOTE.md` and
> `DATASET_NOTES.md` (the round logs, which carry the verdicts that came back), the two
> `determinism_check_report.md` files on disk (task29, task35), task83's repair note, and every
> verifier script in the 44 folders.
>
> **Why this file exists.** Determinism is a construction, not an inspection, and a build that runs it
> as a review after the data is cut comes back non-deterministic on the first pass. SKILL.md carries
> the gates a reviewer applies. This file carries what the 44 builds
> actually did to make one answer the only survivor, with the counts, so a builder has something to
> copy rather than a standard to be measured against.
>
> **What this file is not.** It does not repeat `stumping` Part 5, which owns the pin authority
> hierarchy, the fork grid as a concept, the convergence repair, the robustness sweep and the
> assertion regime. Read Part 5 first. This file adds the four things Part 5 does not have: the
> corpus as an authority tier of its own, the corridor, the bin arithmetic, and a closed enumeration
> of the axes that a fork grid has to cover. The twin pair is `stumping/references/proven-in-production.md`
> organ O1 and is not re-derived here.

---

## Part 0. What actually fails, counted

Three measurements over the corpus, and together they say where the effort belongs.

**The verdicts that came back are almost all about ambiguity, not arithmetic.** Across every design
note in the repo the taxonomy labels appear like this: `underspecified_objective` 31 times across 18
distinct builds, `semantic_fork` 6 times, and `solution_incorrect` twice. A build that fails
determinism in this house is not a build whose numbers are wrong. It is a build where a competent
solver did the analysis correctly and landed somewhere else, because a choice the author never
noticed was left to the solver.

**The machinery is already universal, so its absence is not the cause.** All 44 builds ship a
verifier or check script, and 36 of the 44 have verifiers whose text engages fork vocabulary at all
(forks, rivals, naive paths, rungs, grids, convergence, five mentions or more). That is a crude
measure and it is only offered as one: it says the habit of checking rivals is standard, not that any
particular build checked the right ones. Builds are not failing for want of a verifier. They fail
because a verifier can only assert the forks somebody thought of, which is a claim the primary
evidence carries on its own.

**The failure has a name in the corpus's own words.** task62's round log records the finding as "a
task42-family convention fork (a rounding path) that the fork grid never enumerated." task42's own
log records three defensible operationalisations of one clause landing 13.35 per cent apart. In both
cases the grid existed, the assertions ran, and the axis was simply not on the list.

So the work is a **closed enumeration** (Part 1) followed by a **closure move per axis** (Part 2),
and the thing that has to end up in the design note is not "the fork grid holds" but a line per axis
saying which move closed it.

---

## Part 1. The convention axis inventory

This is the enumeration, drawn from what actually turned out to be load-bearing across the 44. Walk
every row on every build, including the rows that look irrelevant, and write the disposition of each
into the design note. The rows you skip are where the review finds you, because the axis that decides
a build is rarely the axis its author found interesting.

| # | The axis | The question a solver has to answer and you did not | Where it decided a build |
|---|---|---|---|
| 1 | **Population** | which records are in the set at all | 35 (register is not a provision), 39 (793 movements never entered the TMS), 44, 59 (worksite against employer account), 60, 65 (permits against sources), 74 (one trading route or both), 77 |
| 2 | **Unit of account** | what one thing is: a row, an entity, a person, a household, a firm | 42 (client against period), 60 (row against concentrator), 63 (filed number against well month), 72, 77 (determination rows against people, 500 members hold two), 81 (register unit against firm), 45 (cabinets against positions) |
| 3 | **Attribution window** | which period a fact falls in when two are arguable | 35 (endorsement year against schedule year), 41, 51, 63, 78 |
| 4 | **As-of dating** | the entity's state at the pull, at the event month, or at the period end | 42 (effective-dated chart of accounts), 63 (well status at the pull against as of each month), 65, 80 |
| 5 | **Version basis** | the current version of a record or the version as it stood when the period settled | 41 (worth 12.5 per cent, and the rival reading is the one the Office's own monitoring runs on) |
| 6 | **Divisor and denominator** | what sits under the line when the standard names only the numerator | 63 (three defensible divisors, 15 to 17 per cent apart, worth 864,566 barrels), 71 |
| 7 | **Weighting** | pooled, equal-weighted by group, or weighted by the billing unit | 71 (four bases give 21, 42, 56 and 70 days), 43, 59, 35 |
| 8 | **Measurement window length** | how far back a rate is measured over | 35 (fifteen measurements, three weightings against five windows), 52, 67, 78 |
| 9 | **Boundary inclusivity** | inclusive or exclusive, strict or non-strict | 38, 41 (strict inequality on the deadline), 66, 70 |
| 10 | **Rounding path** | round once at the end, per line, per group, or before a total | 70 (fuel unrounded then rounded per collection point reproduces the invoice to the penny, per operating date misses by two pence), 65 (7.6(e) rounds each source down before the total), 45 |
| 11 | **Tie-break** | what happens when two candidates or two records are level | 38 (leadership ties to the higher or lower RSSD), 64 (branch identifier on a tie) |
| 12 | **Maturity and censoring** | all cohorts or only the fully observed ones | 75 (a file closed six months before the cut is not yet due), 79 |
| 13 | **Order of operations** | when two operations do not commute | 58 (divide, then set off, then floor; the floor and the division do not commute and the wrong order is worth 20.47 per cent) |
| 14 | **Row order** | whether the result depends on the order the file is read in | 37 (six row orders, same figure) |
| 15 | **Duplicate resolution** | first, last, both, or collapse | 42 (re-delivered months, three readings 100,000 dollars apart), 63, 69 |
| 16 | **Identity normalisation** | what counts as the same entity across two systems | 74 (normalised GTIN reproduces all 347 adjudications, raw string misses 129), 69, 81 |
| 17 | **Netting against gross** | whether two tails of a position may be set against each other | 49 (netting destroys exactly the tail the audit reports separately), 45 |
| 18 | **Dimensional units** | whether the quantities being added are the same quantity | 65 (six of twenty-four materials are in board feet, square feet, pounds of steam, megawatt hours, cubic feet or cubic yards, worth 22.4 per cent) |
| 19 | **Code and status semantics** | what a reason code, a flag or a status actually means for the calculation | 71 (six release codes, three block call-off and three do not, and the names mislead in both directions), 39 (ten refusal reason codes, 1,024 partitions, one survives) |
| 20 | **Integerisation** | floor, round, or hand out remainders, and in what order | 64 (six disciplines return the same cent, because the construction leaves no remainders) |
| 21 | **Scope of a stated clause** | whether a clause governs the year, the test, or the record | 37 (the held applications govern the year, so applying them to one condition and not the other is not available) |
| 22 | **Forward window contents** | what is inside the window being committed, when the decision is forward facing | 50 (the funded window reaches 621 to 796 of 1,965 units), 53, 62, 78 |

Twenty-two rows is not a long walk, and the corpus says it is the cheapest hour in the build. Two
notes on using it.

**A row that cannot move the answer still has to be dispositioned,** because it becomes load-bearing
the moment another parameter moves. task65 asserts that resolving the population moves the
composition and the totals and does not move the fee by a dollar, and that sentence is worth having
precisely because a reviewer will test it.

**A row you close by pinning in the prompt has not been closed.** The prompt outranks every shipped
file and no pin may live there, which is `stumping` Part 5.1. A convention stated in the prompt is a
convention the build did not have to earn.

---

## Part 2. The four closure moves, strongest first

Every one of the 44 closed its axes with some combination of these four. They are not
interchangeable and they are not equally strong.

### C1. Converge: build the records so every reading selects the same rows

The strongest close there is, because there is nothing left to argue about. You do not choose between
the readings, you make the disagreement have nothing to bite on.

- **task42.** Four readings of one period clause were tested: the whole covered period inside the
  enrolment, the covered period starting inside it, the covered period overlapping it at all, and the
  warrant clearing inside it. **All four return USD 6,468,921.99 on the same 5,416 lines and the same
  1,829 households**, because no certifiable payment's covered period runs past the enrolment that
  opened it and none clears in a gap between enrolments. The write-up says the right thing about it:
  "that is a property of the records rather than a convention anybody picked."
- **task66.** "On supply at the reference date", "on supply across the heating season the standard
  defines" and "on supply for the twelve months to the reference date" select exactly the same 13,745
  dwellings, and no service event in the whole extract falls within twelve days of a season boundary
  or of the reference date.
- **task41.** Applying the settlement basis to the portal export only, or the legacy extract only,
  returns the identical figure to the cent. So does a strict inequality on the deadline, so does
  taking the first accepted version rather than the last accepted in time, and so does reading the
  approved amount as a spending ceiling.
- **task64.** Six integerisation disciplines run end to end return $3,111,552.25 to the cent, and the
  reason is constructed rather than lucky: every plan volume is a whole number of packages, so there
  are no remainders for the disciplines to disagree about.
- **task37.** Reading the register in six different row orders gives 2,585 each time, and the pace
  measured over the whole registration, the last year, the last two or the last three, on months in
  force or on calendar months, and prorating a part year in whole months or as a fraction of days,
  gives 2,585 every time.
- **task81.** The zone schedule carries two reviews, one before the base year opened and one taking
  effect after the extract, so it is static across the whole measured window and reading it at the
  year end and reading it today select the same eleven areas.
- **task63.** Which of the two filings of a re-entered completion stands cannot move the figure,
  because both carry the same volume, so the only thing in play is that one of them stands rather
  than both.

**The construction, stated generally.** Find the boundary the readings disagree about, then build the
records so nothing sits on it. A period-shaped clause disagrees at the far edge (a covered period
running past an exit) and in the gap (between one span closing and the next opening), so place every
record wholly inside one span. A date-shaped clause disagrees at the boundary, so keep every event a
stated distance clear of it (task66 says twelve days, task70 says sixty seconds and twenty minutes,
task78 says six days).

**The one rule that is absolute here.** Never write "the figure is identical either way" without an
assertion behind it. task42's own write-up carried exactly that sentence about the warrant key while
the two keys differed by USD 20,958.71 on 113 lines, and the review found it. A convergence claim
that turns out to be false is worse than no claim, because it is evidence that the author never
controlled the fork.

### C2. Recover the rule from a closed corpus

This is the corpus's dominant device, it appears in more than half the 44, and it is a **seventh
authority tier that `stumping` Part 5.1 does not name.** The hierarchy there ranks documents, from
the governing standard down to the planning thread. A rule recovered by unique reproduction against a
closed record outranks all of them in practice, for two reasons: a document pin can be counter-pinned
or outranked by another document, and a corpus pin cannot be argued with, because the rival does not
merely lose an argument, it contradicts the record. And a corpus pin leaves nothing in the prompt.

The shape is always the same. The governing document states the quantity and is silent on the method.
A closed record of settled cases ships in the pack. Candidate methods are run forward against it, and
exactly one reproduces every case.

| Build | The rule that was written nowhere | The corpus, and what it did to the rivals |
|---|---|---|
| 35 | which adjustment year an endorsement falls in | endorsement year reproduces **1253 of 1253** component lines, schedule year 1086, worst miss 280 per cent |
| 37 | whether an enrolment is still on the roll when its cohort ends | **39,753 of 39,753** enrolments separate absolutely on whether the sponsor held the agreement in the month the cohort ended, no partial cases |
| 39 | whether a depot-side refusal stops the per diem clock | filed rules alone reproduce 163 of 209, the depot-side credit reproduces **209 of 209**, and of the **1,024** ways of splitting the ten reason codes exactly one reproduces the cases |
| 41 | what makes expenditure certifiable | **240 of 240** closed reviews, against nine rival readings of which the closest still gets 20 wrong |
| 42 | the period rule and the household grain | **432 of 432** filed amounts to the cent; the cash-basis rival misses 226 and the per-client rival 30, and the two bases disagree on 264 of the 432, so sampling a few cases cannot settle it |
| 45 | the carriers' per-van reorder-point floor | **9 of 9** filed purchases to the unit; full netting reproduces 1 and understates the other eight by 7 to 42 per cent, every miss in the same direction |
| 51 | the register's own reclassification rule | consistent with every one of **58,374** observed class samples; rivals contradict the ledger 155, 17, 78 and 262 times |
| 52 | what generates a handover event | 46 separate teaching days per coach, slowest coach binding, reproduces **200 of 200** settled changes on the exact day, and changing the number by one in either direction reproduces 2 |
| 53 | how an add-on attaches to the base | only the composed rule reproduces all **383** outcomes; scale alone, renewal alone and term position alone each predict adoptions that did not happen |
| 54 | which consignments a temperature deviation destroys | **48 of 48** closed investigations to the pack, against 2,032 packs on the ledger; the two obvious rivals get 0 of 48 each |
| 55 | the vat lead behind a printed sell-by | seven days is the **unique integer** under which every one of **4,462** lot codes equals its lot's vat day, and six and eight both fail on the first historical cycle |
| 63 | what "per well" divides by | the completed-and-unplugged divisor reproduces all **534** determinations to three decimals, the other two miss 83 and 77 outright |
| 66 | what a point of delivery is a record of | reproduces **364 of 364** decided challenge locations still standing; property type misses 184, homestead 146, and the best account reading still misses 43 |
| 68 | how export activity is measured | the matched like-for-like quantity basis reproduces every one of **17** settled assessments, and every rival fails somewhere under every possible bar |
| 71 | what the clearance share is a share of | client-group weighting reproduces **32 of 32** published cells, pooled misses 30, account-code 20, storage-night 31 |
| 72 | the scope rule together with the composition separation | reproduces the closed review's **six pieces to three decimals**; the raw basis misses all six, scope-only all six, mix-only five |
| 74 | what counts as the same garment across two stacks | normalised-GTIN equality reproduces all **347** adjudicated pairs, raw string misses 129, unpadded digits 64, company prefix 64 |
| 77 | whether a determination reaches a room's age group | the head-count reading misses **71 of the 214** compliance reviews, by as much as nine classrooms in one review |
| 78 | the period duty accumulation is measured over | measuring across the planned maintenance period reproduces all **2,387** settled claims; the four rivals miss 13.9 to 23.9 per cent of them |
| 79 | the follow-up capacity ceiling | three of six waves land on **11.500** cases per interviewer-week on three different rosters (440, 500 and 460 interviewer-weeks) and no wave exceeds it |
| 80 | the dating of a designation term | across all **70** settled site-years a return either serves the whole enrolled roster or at most 0.58 of it, with nothing in between |
| 81 | the aggregation measure | the pilot reproduces to the dollar under the correct measure and refuses the two rungs below it, on 46 of 161 settlements and on all 161 |

**The five properties a corpus pin needs, and every one of them is checkable.**

1. **Exhaustive family.** Run the whole family, not a favourite and a straw man. task39 ran 24
   rulesets over three axes and separately all 1,024 partitions of ten reason codes. task35 swept 15
   measurements and the judge independently swept 18,432 configurations. task41 ran nine named rivals.
   State the count you actually ran and report the **worst** miss, not the average.
2. **Zero tolerance.** The survivor reproduces every case exactly, and the rivals miss outright. "Fits
   better" is a fit comparison and a fit comparison is a preference. task63 puts it exactly right:
   "which is not a matter of fitting better, it is exact against every case."
3. **One survivor.** If two candidates both reproduce the corpus, the corpus has not pinned anything.
   task71 is the model: one basis at 32 of 32 and the nearest rival at 2 of 32.
4. **Blind to the decisive move.** The corpus must certify the rungs below the answer and be unable to
   score the last one, for a stated structural reason (`stumping` proven-in-production L1). task56's
   committed-use plan opened on the first day of the measured cycle so the population is zero in every
   closed cycle. task81's pilot window contains no register-number change so it settles at the
   identical figure under either unit of account, which the write-up calls the honest position: the
   pilot is evidence about method, not about entity. task72's closed review had no site change hands
   inside its window, so it is "arithmetically incapable of certifying anything about where this
   year's service belongs."
5. **Rerunnable by the reviewer from the bundle.** The closed cases and everything they need ship in
   `target/`. task55 says it plainly: the verifier recovers the seven-day vat lead independently from
   the bundle without reference to any generator state.

**The twin pair is how you prove the corpus cannot be shortcut,** and it is organ O1 in
`stumping/references/proven-in-production.md`. Two records identical on every column a lookup can
reach, with outcomes far apart, so no rate transferred by resemblance reproduces both. It appears in
at least sixteen of the 44 (35 at 2.20x, 38 at fifteen times, 42 at exactly 2x, 44 with six pairs, 45,
51 eight dollars apart, 52 with three pairs, 53, 54 at 25 packs against 51, 59 at a factor of 2.59, 63
at exactly 2.00x, 67, 71 published at 28 days and 14, 74, 77 at 1 against 9, 79). Build one.

### C3. The corridor: make the parameter unrecoverable and irrelevant

Use this when a quantity is genuinely estimated rather than read, so no pin and no corpus can fix its
exact value. Instead of recovering the number, make every admissible value of it return the same
answer, and say so.

- **task40.** No filer's linked employment falls between 192 and 209 in any quarter of 2028, so every
  ceiling from 193 to 209 returns identical division tables and an identical provision, to the cent.
  The write-up states the principle better than a rule could: "the figure is forced without the number
  that generates it being knowable, which is the difference between a convention and a recovered
  rule."
- **task71.** The schedule can only be published at 7, 10, 14, 21, 28, 35, 42, 56 or 70 days, so a
  solver whose crossing lands anywhere between 29 and 35 files the same answer. The curve crosses on
  day 32, four days clear of the 28 step and three clear of 35, and the whole weighting grid was
  recomputed under day-count conventions shifted by plus or minus two days.
- **task75.** The commit level of 2,149.74 sits 49.7 matters above the 2,100 block boundary and 50.3
  below 2,200, and four different implementations of the run-off convention (carrying the last
  observed hazard into the tail at 2,141.43, leaving open matters out of the at-risk set at 2,125.88,
  excluding the phased-launch year, and a reading running 25 matters higher) all stay inside the same
  block.
- **task46.** All thirteen reasonable variants of the roll land between 9,882 and 10,215 and file the
  same 10,000 at the 1,000 increment.

**How to build one.** The corridor needs a quantisation to sit inside: a step grid the schedule can
only publish on, a reporting increment the answer is filed at, a block size the obligation is bought
in. Pick the quantisation from the domain (it must be a real business fact, not a rounding you
invented), then engineer the gap so the estimate sits near the middle of its cell and the whole
admissible family lands in the same cell.

**The failure mode is the boundary-hugger, and the corpus has an instance.** task35's judge report
records both of the PDF's money asks sitting inside 1 per cent of a $0.1M rounding boundary that a
rival December convention crosses, with the verdict that the convention is genuinely pinned but there
is no cushion. A corridor with no slack is a coin flip wearing a proof. State the slack as a number.

### C4. Separate the grid: every cell distinct, and the nearest one far

The fallback, and the one every build runs whether or not it uses the other three. Enumerate the cross
product of the independent decisions, compute every cell, and assert each is distinct and each is far.
`stumping` Part 5.2 owns the method. What the corpus adds is the **distance**, which is the number a
builder actually needs, because "the grid separates" is not a target.

| Build | Grid size | Nearest wrong cell |
|---|---|---|
| 37 | 30 combinations | 8.4 per cent |
| 39 | 16 | 10.8 per cent |
| 41 | 16 | 12.50 per cent |
| 42 | 16 | 10.62 per cent |
| 45 | 10 named readings | 14.2 per cent |
| 49 | full grid | 9.6 per cent |
| 58 | 8 | 14.77 per cent |
| 59 | 11 cells | 9.0 per cent |
| 60 | every wrong reading lands above | 10.8 per cent |
| 62 | 56 figures | 0.59 per cent, and reaching it needs **two violations pointing in opposite directions** |
| 63 | full grid | 6.24 per cent |
| 64 | full sweep | no partial application within 0.9 per cent |
| 65 | 216 cells | 1.4 per cent, and reaching it takes **two errors pointing opposite ways** |
| 66 | full grid | 9.7 per cent among permitted cells (the one closer cell, at 6.4, is refused outright by the challenge record) |
| 74 | full grid | 12.2 per cent |
| 76 | 16 cells | 15.3 per cent, and the **answer is the minimum of the grid** |
| 77 | 32 cells | 11.5 per cent |
| 78 | 24 cells | 14.3 per cent, and the **answer is the lowest figure the grid produces** |
| 80 | full grid | 9.6 per cent |
| 81 | 8 cells | 18.8 per cent, and the unit of account is worth a factor of 1.643 |

**The working floor the corpus implies is about 6 per cent,** and the two builds that ship under it
(62 at 0.59, 65 at 1.4) both buy the margin with the same structural argument: the near cell is
reachable only by making two errors that point in opposite directions, which is not a path a competent
solver walks. If your nearest cell is under 6 per cent and you cannot make that argument, the grid has
not separated, and the repair is to move a rung rather than to write a paragraph.

**Make the answer the extreme cell where you can.** task76 and task78 both name the answer as the
extreme of their grid, which is what makes partial corrections safe: no combination of half-applied
corrections can cancel its way onto the answer from outside. task62 is the counter-case, bracketed
14.17 per cent below by the natural stop and 3.76 to 20.64 per cent above by the early channel stops,
which is why it needed the two-violations argument at all.

---

## Part 3. Bins, rounding and the flip condition

A figure filed to a bin is not deterministic because its underlying value is deterministic. It is
deterministic when the value sits far enough from the bin boundary that nothing in the admissible
family crosses it, and the only way to know that is to compute the distance.

**The instances, with the arithmetic stated the way it should be stated.**

- **task54.** 1,420.30 sits 4.7 packs from the nearest boundary at the nearest 10, and two independent
  estimators (the per-call hazard on the plan's pack-legs at 1,420.30, the observed 2,032 packs scaled
  by the pack-leg ratio at 1,421.38) agree to 0.076 per cent and round to the same figure.
- **task60.** 13,203 sits 0.34 of an attainment from the nearest rounding boundary.
- **task75.** 2,149.74 sits 49.7 above the 2,100 boundary and 50.3 below 2,200, and the obligation
  would move a block only if the covered caseload in the setting month reached 2,201.
- **task79.** The Minimum of 7,677 sits at the midpoint between what 96 replicates land (7,651) and
  what 97 land (7,703), so there is 0.34 per cent of slack on each side, and **the flip is stated
  explicitly**: the Minimum would have to fall to 7,651 before 96 replicates would carry it.
- **task49.** The sum of limits sits $12,427 above the bottom of its rounding bin and $12,573 below the
  top.
- **task72.** Every graded figure sits at least seven per cent of a rounding bin from its boundary, so
  no two correct analysts round them apart.
- **task83.** Pricing the plan from cells stated at two decimals lands every graded figure in the same
  bin as full precision, which is the check that the deliverable's own display precision cannot move a
  graded answer.
- **task65.** Chapter 7.6(e) rounds each source's fee down to the dollar before the total is taken, so
  the invoice run and the determination are the same arithmetic and there is no rounding path to argue
  about. That is the best kind of close: the rounding path is pinned by the governing document rather
  than asserted by the author.

**The rounding path is itself an axis, and it is the one most often missed.** task70 is the worked
case and it was found by a review rather than by the author: accrue fuel unrounded and round once per
collection point and both of the invoice's fuel lines reproduce to the penny, round it per operating
date and both miss by two pence. Two pence decided the committed figure. The build's fork grid had
never enumerated a rounding path, and that is exactly the class of finding Part 1 exists to prevent.

**State the flip condition as a number, not as a reassurance.** "The margin is comfortable" is a
sentence. "The Minimum would have to fall to 7,651 completed interviews before 96 replicates would
carry it" is a determinism asset, because a reviewer can check it and because it tells you what to
watch when a parameter moves.

---

## Part 4. The eight ways a build loses determinism, with the repair

Written as symptoms, because that is how they present.

**1. The semantic pin that was never operationalised.** A clause is pinned at the right authority
level, names no file, no table and no field, and still admits several readings that land far apart.
task42: chargeability pinned to "the period of the household's enrolment", three defensible
operationalisations 13.35 per cent apart, and a strong solver that reached every planted insight
diverged anyway. **Repair: converge (C1), never a second pin.** A clause naming the field closes the
fork and simultaneously turns the decisive rung into a two-line lookup, which trades a Gate C failure
for a Gate F one.

**2. The axis that was never enumerated.** The grid is built, the assertions run, and the axis that
decides the build is not on the list. task62's rounding path. **Repair: the Part 1 walk, in writing,
before the data is cut.**

**3. The objective planted in the requester's own voice.** The prompt asserts a decision metric as
fact while a shipped file ranks on a different one, so both readings are licensed and they pick
different winners. The tell is diverging runs that reproduce every number and split only on which
objective governs. **Repair: demote the planted metric to an attributed stakeholder claim so the
shipped policy stays governing.**

**4. The unpinned convention declared rather than closed.** A convention the prompt and files leave
open, written into the write-up as a choice the author made, is a fork you chose not to close.
**Repair: the ten-of-ten test.** If a competent analyst could reasonably go the other way, it is a
decision, not a convention, and a model that did 99 per cent of the analysis right and diverged only
there is `underspecified_objective`, not a stump.

**5. The unasserted convergence claim.** "Identical either way" written into the write-up with
nothing behind it. task42 shipped it while the two keys differed by USD 20,958.71 on 113 lines.
**Repair: assert it in the generator and again in the independent verifier, or delete the sentence.**

**6. The thin margin with a live estimation range.** A thin margin is not a defect on its own. It
fails when thinness meets real uncertainty: the decisive quantity has more than one valid estimation
method whose range straddles the line, or the input error band is wider than the lead. The behavioural
tell is two rigorous solvers on the same correct method reaching **opposite** answers. **Repair: pin
the estimator (task59's charter strikes the conversion rate on the settled cohorts taken together, so
the corpus supplies one figure rather than a family) or widen the margin.**

**7. The figure that reproduces only under a read the file's own grain forbids.** A median of roughly
one row per entity across many periods is the tell of a delta feed being averaged as a panel.
**Repair: reconstruct the full panel by carrying each entity's last-known value forward, then
recompute.** This is `solution_incorrect` even when the winner does not flip.

**8. The corpus that can score the decisive move.** Not a determinism failure but a stump failure, and
it presents in the same review. If the closed record can distinguish the answer from the rung below
it, a solver who back-tests finds the answer. **Repair: give the corpus a stated structural reason to
be blind, per C2 property 4.**

---

## Part 5. What to assert, and where

The corpus baseline, so you know what normal looks like: **44 of 44 builds ship a verifier or check
script**, and most of those verifiers engage fork vocabulary somewhere. The machinery is standard.
What separates a build that passes on the first pass from one that does not is whether the enumeration
behind the assertions was closed.

**In the generator, while the data is being cut**, because a fork found here costs a re-cut and the
same fork found later costs the build:

- every convergence equality from C1, one assertion per reading, stated as an equality on the figure
  **and** on the row and entity counts (task42 asserts the same 5,416 lines and the same 1,829
  households, not only the same dollar figure)
- the corpus recovery: the survivor at N of N, every rival's miss count, and the size of the family
  actually run
- the corridor: the admissible range of the parameter, and the answer identical across all of it
- every grid cell computed, each mapped to the shipped rule it violates, and the nearest cell's
  distance
- every graded figure's distance to its nearest bin boundary, and the flip condition as a number
- the axis dispositions from Part 1, including the axes that cannot move the answer

**In the independent verifier, reading only the shipped bundle**, on a code path that shares nothing
with the generator. task71 uses pyarrow tables and plain dictionaries where the generator used pandas
group-bys. task83's verifier states in its own docstring that it uses the golden strictly as an
expectation table and carries no generator state. If the verifier cannot recompute a figure from the
bytes, that figure does not exist.

**In the design note**, one line per Part 1 axis: the axis, the reading chosen, and which of C1 to C4
closed it. This is the artifact the next iteration reads, and it is the thing a review asks for that
no build currently has.

---

## Part 6. Per-build index

The axis that decided each build and how it was closed. Read it as what has been built and where, not
as a menu.

| Task | The axis that decided it | Closed by | Nearest wrong |
|---|---|---|---|
| 35 | attribution window (endorsement year) | corpus, 1253/1253 | basis table, six rival bases |
| 36 | population (RDC transfers) plus the day give-back | separation with no overlap, 0.68 to 0.86 against -0.04 to -0.03 | 3.21x lead, holds out every DC and service class |
| 37 | scope of a clause, and roll survivorship | corpus, 39,753/39,753 | 8.4 per cent over 30 combinations |
| 38 | what a direction actually removes | corpus, 33 closed directions, plus two twin pairs | 2.25x margin, narrowest variant 1.11x |
| 39 | population, then reason-code semantics | corpus, 209/209, 1 of 1,024 partitions | 10.8 per cent over 16 |
| 40 | the ceiling parameter | corridor, 193 to 209 identical to the cent | twelve rows reproduced exactly |
| 41 | version basis, then certifiability | corpus, 240/240, plus C1 on four readings | 12.50 per cent over 16 |
| 42 | unit of account (client against period) | corpus 432/432, plus C1 on four period readings | 10.62 per cent over 16 |
| 43 | the moderator | hole in the distribution, 2 named sources against 22 | sixteen readings return the same partition |
| 44 | which quarter the property is measured over | prior peak against spring, 132 items differing in both directions | 96 cells all same sign |
| 45 | the per-van floor | corpus, 9/9 filed purchases | 14.2 per cent |
| 46 | the rate curve's key | exposure age against build age, plus C1 | thirteen variants inside one 1,000 increment |
| 48 | the aggregate that can see the population | absolute separation, ordinary max 7 against ring min 10 | identical membership at seven thresholds |
| 49 | netting against gross | the audit reports both lines separately, so netting cannot reproduce either | 9.6 per cent |
| 50 | forward window contents | the funded window, five demand readings agreeing | roughly two to one |
| 51 | the reclassification rule | corpus, 58,374 class samples | 37 per cent |
| 52 | the unit of the clock | corpus, 200/200 to the day | plus or minus one reproduces 2 |
| 53 | the composed attach rule | corpus, all 383 outcomes | 1.35x under every variant |
| 54 | exposure shape against a rate | corpus, 48/48, plus two independent estimators agreeing to 0.076 per cent | 4.7 packs from the bin |
| 55 | the vat lead | corpus, unique integer over 4,462 lot codes | 11 per cent |
| 56 | the billing basis for a population the meter never sees | corpus blind by construction, 30 of 31 pipelines refuted | the one survivor sits 55.13 per cent below |
| 58 | order of operations (divide, set off, floor) | the security agreement, plus a twin pair | 14.77 per cent over 8 |
| 59 | population grain (worksite against account) | corpus back-test plus a twin pair at 2.59x | 9.0 per cent over 11 cells |
| 60 | unit of account, and duplicate filings | terms 2.1 plus the criterion filed at 4.2 | 10.8 per cent |
| 62 | forward window contents, three stops | filed clauses at every stop plus the exit history | 0.59 per cent, two opposite violations |
| 63 | divisor, then filing grain | corpus, 534/534, plus a twin pair at exactly 2.00x | 6.24 per cent |
| 64 | a constraint on a grouping no account-level pipeline builds | the meter pinning two sources to their ceilings | 0.9 per cent under full sweep |
| 65 | unit of assessment, then where activities stand | Chapter 7.6(a) and 7.2(f), plus 7.6(e) on rounding | 1.4 per cent over 216 cells |
| 66 | what a point of delivery records | corpus, 364/364 decided challenges | 9.7 per cent among permitted cells |
| 67 | what the minutes column is a share of | zero residual across the whole history | 0.17 of a duty at the boundary |
| 68 | how activity is measured | corpus, 17 settled assessments | 1.19x on the runner-up |
| 69 | distinct events against summed columns | the charter's own two sentences | worst swap costs 2 per cent of coverage |
| 70 | acceptance against label date, then the trunk | the carrier statement, 29/29, plus the rounding path | thresholds exact, closest day 40 clear |
| 71 | weighting, then code semantics | corpus 32/32, plus a step-grid corridor | 4 days clear of one step, 3 of the other |
| 72 | where service belongs | corpus reproducing six pieces to three decimals | 0.51 points, 4.5x the runner-up |
| 74 | identity normalisation, then whose property the scale is | corpus, 347/347 | 12.2 per cent |
| 75 | maturity, and what consumes an authorisation | the register against the intake extract | 49.7 and 50.3 inside the block |
| 76 | an absolute class, not a rate | 1,581 referrals, zero engagements | 15.3 per cent, answer is the minimum |
| 77 | rows against people, and pathway against trend | corpus, 214 reviews | 11.5 per cent over 32 cells |
| 78 | the period accumulation is measured over | corpus, 2,387/2,387 | 14.3 per cent, answer is the lowest cell |
| 79 | the capacity ceiling | corpus, three waves on 11.500 exactly | 0.34 per cent each side, flip stated |
| 80 | the dating of a designation | corpus, 70 settled site-years, signature exact | 9.6 per cent |
| 81 | unit of account (register unit against firm) | the site-set match, exact and unique on 203 pairs | 18.8 per cent over 8 cells |
| 83 | conditioning on treatment history | the holdout, a switch rather than a gradient | 5.1 stops on a month worth about 30 |

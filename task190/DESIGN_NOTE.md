# task190 design note

Architecture 3. Internal audit of a port authority's capital programme payments: how much misstatement
the year's payments hold, projected from a tested set that was drawn in euro rather than in items.

| | |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task190.json`, architecture v3, registered 2026-10-17, WARN |
| Owner | oviya13ya |
| Status | stage 2, design |

**This is the number's third architecture. If it is spent the number retires**, so the ground was chosen
for a decisive quantity that is determinate by construction rather than by a fit, and the ladder's
separation and the blind-response score are measured on paper below before a single file is cut.

## Draw

| | |
|---|---|
| Pairing | `accounting-audit-forensic` / `audit-testing-sampling`, filed against the client's Survey Research and Official Statistics because the deciding method is design-based estimation from a probability-proportional-to-size sample. A never-built pairing; the subdomain has never been drawn. |
| Objective | `anomaly-detection`. The object is a defect in a population of payments, separated from what the testing happened to catch, and the call is a monitoring decision: certify the population or send it to extended testing. |
| Shape | 12, drill-down to one leaf. Nine work programmes, two figures each (18), three directorate rollups (3), the authority total, the leading programme, the gap to materiality and the flip (4), the chart's named parts (5). 30 criteria. |
| Gap | 4, rule: which projection the tested set's own selection entitles. |
| Strategy | `population_selection`; Layer 2 family `field_method`; generators G16 decisive, G17 supporting, G10 in Layer 1. |
| Decision | `quantity_figure`, answer unit `currency`, question form how-much. |
| World | Carrowmore Port Authority, Ireland, EUR, year to 31 December 2026. People drawn from `guard.py names --geo Ireland --seed 190`: Tanya McCrea, Colm Shaffrey, Marc O'Reardon. |
| Deliverables | `projected_misstatement_2026.csv`, `misstatement_by_population_2026.png`. |
| Guard | No BLOCK, after five redraws (context artifact three times, gap, people, deliverables) and three differentiation lines. Two WARNs, `repeat.gate_g` and `overuse.gate_g`, answered in the card's notes: no other Gate G key is true of this build, and the variety is carried by the driver, which scores 0.08 against the whole corpus, the lowest this slot has drawn. `guard.py heart` WARN. |

**The data-native sentence.** The tested set was drawn by stepping a fixed amount of euro through the
payment population in value order, so a tested payment line stands for that amount of the population
rather than for one line, every line at or above it was certain of selection and stands only for itself,
and the amount itself is recorded in no file and has to be recovered from the tested set; the authority's
capital payments are the kind of population that design exists for, a handful of contractor certificates
holding most of the value and twenty-six thousand small lines holding the defects.

**Why this ground, written against the slot's own lineage.** Architecture 1 settled whether unobserved
members were in the population and failed the WHAT screen. Architecture 2 estimated a counterfactual
density and died three times on the same shape: the specifications always disagreed, and each pass bought
agreement another way (a smooth draw, then an algebraic cancellation) rather than earning it. The author's
four constraints for this draw follow from that, and each is answered here:

1. **No fitted counterfactual density.** Nothing is fitted. Once one integer is recovered the figure is an
   exact weighted sum over the tested items: no window, no bin width, no family, no polynomial order, no
   tolerance. There is no specification grid for a judge to sweep, because there are no specifications.
2. **The blind-response test, at the draw.** Measured on paper below, before any file exists.
3. **The insensitivity screen.** Answered below, and the answer is the inverse of architecture 2's: the
   figure is strictly proportional to the recovered interval, so it is maximally sensitive to the one
   thing the data pins exactly, rather than insensitive to what the candidates differ on.
4. **No sentence filed at authority without the author's approval.** Nothing is pinned at authority in this
   design as it stands. If the build needs one, its exact wording comes to the author before it ships.

**The decisive quantity, and why it is determinate by construction.** Let k be the amount of euro stepped
through the population. Each tested line below k was selected with probability equal to its own amount over
k, so a tainting of fraction f on such a line projects as f times k. Each line at or above k was certain,
so it projects at its own error. The population's misstatement is the sum of those two terms over the
tested set. Every term is an exact arithmetic function of shipped numbers and k, and k is an integer the
tested set pins two independent ways:

- **the certainty threshold:** the smallest amount above which every line in the population is in the
  tested set, which is k itself;
- **the value step:** order the population by the value the selection ran on, cumulate the amounts, and
  the tested lines below k sit one per k of cumulated value, so the book value between consecutive tested
  lines is k.

The two have to agree, and they do, exactly. Nothing is filed that says to do either.

**The insensitivity screen, answered.** Architecture 2's agreeing estimator agreed because it cancelled the
fitted level algebraically, so it was insensitive to exactly what the candidate specifications differed on
and every other candidate stayed standing. Here the question is not why one estimator among many agrees,
because there is no family: the figure is one sum. The thing that could still be argued is k, and the
figure is linear in k, so a solver who recovers a different k files a proportionally different figure. k is
therefore the whole of the analysis, and it is pinned exactly by two independent observables rather than
chosen. The candidates the design has to rule out are not variants of one estimator but three different
estimators (the factual sum, the book-value ratio, the size-banded ratio), and what rules them out is that
the tested set is visibly a size-biased draw: every line above a definite amount is in it, and below that
amount the share of lines tested rises exactly in proportion to amount. That is a property of the shipped
record, not a rule in a file.

**The field's own evaluation, measured before the ladder was fixed.** A monetary-unit sample is not
evaluated by the projection alone: the standard evaluation is the projected misstatement plus basic
precision plus an incremental allowance for the taintings found, compared against tolerable misstatement
as an upper limit. Basic precision is the interval times the reliability factor at the stated confidence
and is computed before any tainting is looked at, so a draw whose basic precision already exceeds
materiality is escalated by step one of a textbook evaluation with no projection and no insight at all.
The first sketch did exactly that: an interval of 520,000 against materiality of 750,000 gives basic
precision of 1,560,000, **2.08 times materiality**.

**Why that sizing was indefensible, which is the reason and not just the arithmetic.** The interval an
auditor draws is (tolerable misstatement less expected misstatement times the expansion factor) over the
reliability factor. **Sizing with no allowance for expected misstatement therefore forces basic precision
to equal materiality exactly**, at any materiality: the interval is materiality over the factor, so the
factor cancels. A sample sized that way rejects its population on any tainting at all, which is why no
auditor sizes one that way, and it is why the first sketch's interval could not have been drawn by the
body it was attributed to. Planning for expected misstatement is what opens the headroom the decision
needs, and the headroom is exactly the expected misstatement times the expansion factor.

### The design point

| | |
|---|---|
| Reliability factors | Poisson, one-sided upper bound, 95 per cent: RF(0) 3.00, then 4.75, 6.30, 7.76 and on, the table every audit text carries. Expansion factor 1.60. |
| Population | 59,500,000 EUR over 24,700 payment lines, nine work programmes |
| Tolerable misstatement | 1,160,000 EUR, 2.0 per cent of budgeted capital expenditure of 58,000,000. **Shipped.** |
| Expected misstatement allowed in planning | 387,500 EUR. **Not shipped, and the reason is below: the plan's own sizing formula would otherwise give the interval away exactly.** |
| Interval | (1,160,000 less 387,500 x 1.60) / 3.00 = **180,000**. Not shipped. |
| Selections | 330, on 273 distinct tested lines; the 31 certainty lines hold 74 per cent of the tested recorded value |
| Basic precision | 180,000 x 3.00 = **540,000, which is 0.466 of materiality**, so step one escalates nothing |
| Stated granularity | the nearest **50,000** EUR, set from the measured route spread below |

### Every recovery route, and what the record does with it

The figure is linear in the interval, so a route that recovers the interval differently files a
proportionally different figure. Ten routes, the figure each files, and whether the record admits it:

| Route | Interval | Figure | Stated | The record |
|---|---|---|---|---|
| the lattice: the only interval fitting every tested and every untested line | 180,000 | **799,422** | **800,000** | admits |
| the median gap between selections, line end to line end | 180,579 | 801,918 | 800,000 | refuses |
| the median gap, line start to line start | 181,006 | 803,754 | 800,000 | refuses |
| the median gap, midpoint to midpoint | 180,423 | 801,243 | 800,000 | refuses |
| the mean gap, midpoint to midpoint | 245,812 | 1,082,934 | 1,100,000 | refuses |
| book value over the count of distinct tested lines | 217,949 | 962,901 | 950,000 | refuses |
| book value over the count of tested lines below the interval | 245,868 | 1,083,173 | 1,100,000 | refuses |
| the certainty threshold, the smallest line certain of selection | 181,000 | 803,730 | 800,000 | refuses |
| the certainty bracket's lower end, the largest untested line | 79,325 | 365,722 | 350,000 | refuses |
| the certainty bracket's midpoint | 130,162 | 584,726 | 600,000 | refuses |

Over every route the figures run 365,722 to 1,083,173, a spread of 89 per cent across five stated cells,
so the routes genuinely disagree and the set was not narrowed to the ones that agree. **The record admits
exactly one of them.** And the five routes that land within two per cent of the interval span 799,422 to
803,754, 0.54 per cent, **all in one stated cell at the nearest fifty thousand**: so a solver who takes
the natural approximate route rather than the lattice still files the graded figure. That is what sets the
granularity. The underlying 799,422 sits 24,422 from its nearest rounding line, almost the whole half
cell, and **the nearest wrong cell is 50,000 away, 6.25 per cent of the figure**, which clears the six per
cent the judge asks for. The three far routes are each refused by the record, and `checks.py` asserts the
whole table rather than claiming agreement.

### What the lattice's feasible set is, stated precisely

It is not an invariance over a feasible set and not a unique value on a chosen grid. **On a one-euro grid
over 179,960 to 180,040, exactly one interval is feasible: 180,000**, and the search was run over that
whole range rather than at a chosen point, so the neighbouring intervals were excluded rather than assumed
away. The far routes in the table above sit at 79,325, 130,162, 217,949, 245,812 and 245,868 and are each
refused by the same test. At that
interval the starts that reproduce the realised pattern span **10.96 euro**, from 123,445.38 to
123,456.34, which contains the start the selection actually ran from. The constraint is that every one of
the 273 tested lines must contain a step of cumulated book value under one common start and none of the
24,427 untested lines may, and the untested lines are what make it unique: the tested lines alone narrow
the start to a six-euro window but admit many intervals. So the projection is a single value, and the
feasible set's size is 10.96 euro of start and one euro of interval.

### The programme table, and the blind responses

Nine programmes, each carrying the projected misstatement and the share of its book value that was
certain of selection. Measured at the design point: all five blind families score **4 of 18, 22 per
cent**, because four programmes currently read nil. **That is above the fifth the author set as the point
to act, so the construction is re-tuned at stage 3 to three nil programmes rather than four.**

### The stage 3 tuning targets, written before any file is cut

Two residual defects at the design point, both tuning rather than design, with the constraints to assert:

1. **The two paths to the headline disagree.** The rounded programme figures sum to 750,000 while the
   unrounded total of 799,422 rounds to 800,000. That is architecture 2's SF12 failure exactly, and it is
   not fixed by filing the WHAT, because the other path stays computable. The generator tunes each
   programme's taintings so **the sum of the stated programme figures equals the stated total**, asserted.
2. **Four nil programmes.** Re-tuned to three, each nil deep in its cell (underlying under 15,000 against
   a 25,000 half cell), with no programme carrying a nil certain share, which is what protects the pair.

With, as the rest of the tuning contract: every programme's underlying figure at least 5,000 from its
rounding edge against a route band of plus or minus 1,500; the headline's underlying at least 20,000 from
its edge; the largest programme by misstatement outside the top three by book value; and all five blind
families at 3 of 18 or fewer.

### Readability screen, test 6, written out

The author's ruling is taken: test 6 asks how the decisive step is **found**, not how much arithmetic
follows once it is found. The step here is recognising that the sample was drawn in euro rather than in
items, so a line at or above the interval stands only for itself while a tainting in a small line carries
a whole interval of untested euro. That is a reconceptualisation of what one tested row represents, not a
subtraction, a ratio or half of a reported figure, and the multiplication that follows being trivial is
what a correct estimator usually looks like. **Verdict: silent.** Having written it out, it does not fire.

### What may be filed at authority, and what may not

**The leak the author caught, and the rule it gives.** The first draft of the plan stated tolerable
misstatement, the confidence and the expected misstatement allowance. The reliability factor at 95 per
cent with none expected is 3.00 and the expansion factor is 1.60, both in every audit text, so any
domain-competent reader computes (1,160,000 less 387,500 x 1.60) / 3.00 and has the interval exactly from
the plan alone. **The sizing formula is the inverse of the recovery problem the task is about**, so stating
its inputs at authority states the answer. The expected-misstatement sentence is therefore cut from every
shipped document, and the allowance lives only in this note as the reason the sizing is defensible. Without
it a reader has (1,160,000 less an unknown times 1.60) / 3.00 and can only bound the interval below
**386,667**, which is 1,160,000 over 3.00 and still a factor of 2.1 above the true 180,000, so the
recovery is left intact. The general rule, going into the slot's record: **before filing
any figure at authority, invert every formula the field would apply to it and check what the inverse
yields.**

**The reliability factors: Gate B, decided.** The decision rests on a bound, and a bound needs a
reliability factor, which the pack ships nowhere. The decision is that **they are standard domain knowledge
and the pack ships nothing for them**, for three reasons. First, Gate B asks whether the pack holds the
data the answer needs; a published constant every text in the field carries is not data, and no pack is
expected to ship the normal distribution's quantiles either. Second, the alternative fails worse: a manual
that ships the factors has to say what they are for, and any sentence that does so names the interval or
says the population was tested by selecting from its monetary units, which is the premise of the decisive
step and the one thing that must stay unstated. Third, the decision does not depend on the richer parts of
the evaluation: the projection plus basic precision alone clears materiality by 15 per cent, and basic
precision needs only the factor 3.00. **No reliability table, no expansion factor and no evaluation
procedure appears in any shipped file**, asserted by word sweep in `checks.py`.

**The decision rule, and the ambiguity that had to go.** "Where the testing indicates that the population
may be misstated by more than tolerable misstatement" does not say whether the comparison is against the
projection or against a bound. On these figures the projection is 799,422 against materiality of
1,160,000, so a solver who gets the decisive step right and compares the projection itself **certifies**:
the wording would have thrown the call away after the analysis was done. It is reworded so the comparison
is a confidence statement, which can only be met by a bound, without naming an estimator, a factor or the
interval.

**The two documents, held for the author's approval and shipped only after it.**

The audit plan, section 4:

> **4.2 Capital programme payments.** Tolerable misstatement for the capital programme payments
> population is set at 1,160,000 euro for the year to 31 December 2026, being 2.0 per cent of budgeted
> capital expenditure, and the population is tested to a confidence of 95 per cent.
>
> **4.3 Conclusion on a tested population.** A population is accepted only where the testing shows, to
> the confidence at 4.2, that the population's misstatement does not exceed tolerable misstatement. Where
> the testing does not show that, the population is referred for extended testing before the financial
> statements are certified.

The audit manual, part 9, which files the estimand and nothing else:

> **9.1 What a tested population's misstatement means.** The misstatement of a tested population is the
> amount by which the population's recorded value exceeds the amount properly payable, taken over every
> payment line in the population and over the year in which the line was paid. It is an amount of euro and
> not a count of lines or of invoices. It is stated for each work programme and for the authority, each to
> the nearest fifty thousand euro, the authority's figure being the sum of the programme figures as stated.
>
> **9.2 Records.** No feed, schedule or register the authority keeps records a population's misstatement,
> and none can: the payment records carry what was paid, not what was properly payable, and the testing
> establishes the difference only for the lines tested. The head of internal audit is satisfied each
> year that the figure reported rests on the year's own payment records and the testing performed on them.

What those two documents between them do **not** say: the interval, the number of selections, how the
population was ordered or selected from, the expected misstatement allowance, any reliability or expansion
factor, any evaluation procedure, and anything about projecting, scaling, weighting or extrapolating a
finding. 4.2's two figures bound the interval below 386,667 and no further. 9.1 files population, outcome,
window, unit, segmentation and grain, and 9.2 says no column holds the answer.


## Default path

1. Read `capital_payment_lines_2026.csv` and `supplier_master.xlsx`, carry the ledger's supplier numbers
   onto the master's through `supplier_number_crosswalk.csv`, and take each payment line's work programme
   from the capital programme register.
2. Keep the lines in the capital programme payments population for the year to 31 December 2026: drop the
   two credit notes and the lines they reverse, collapse the batch the bank feed delivered twice on its
   delivery sequence, and take the prior year's lines out of the overlapping extract.
3. Read `internal_audit_testing_schedule_2026.pdf` and lift the tested lines out of the table inside it:
   the line reference, the amount recorded and the amount the testing found properly payable.
4. Compute the misstatement the testing found: for each tested line, recorded less properly payable. Total
   it. It is 41,307 euro, which cannot be the population's misstatement because only part of the
   population was tested.
5. Project it to the population on the ratio the files make obvious: the population's recorded value over
   the tested recorded value, 59,500,000 over 21,260,698, a factor of 2.799.
6. State the result by work programme and for the authority, and read the conclusion at plan 4.3.

**Ends on:** 115,600 euro, which is accepted at 4.3 and certifies the population, with Rail siding and
yard the programme carrying most of it.
**Golden:** 800,000 euro, which is not accepted at 4.3 and refers the population for extended testing,
with Terminal roof and cladding the programme carrying most of it.

The default path cleans every key correctly, reads every clause correctly and uses a projection that is
arithmetically sound. It files a figure seven times too small because it treats the tested lines as a
sample of lines when they are a sample of euro.

## Stump sentence

The default path scales the misstatement it found on the ratio of the population's recorded value to the
tested recorded value and files **115,600** euro, which certifies the population, because the 31 lines at
or above the recovered selection interval hold 81 per cent of the tested recorded value and are sound,
while every defect sits in a small day-work invoice that was selected with a probability equal to its own
amount over that interval and therefore stands for a whole interval of untested euro; the misstatement the
selection entitles is 800,000, which refers the population for extended testing.

## Three rules

- **Task type:** anomaly-detection, the client task type in Survey Research and Official Statistics
  that serves Anomaly Detection, worked as the house domain's `audit-testing-sampling`: whether an
  administrative population holds a defect that the testing only sampled, and how much of it.
- **Domain test:** the deciding quantity is the misstatement in a population projected from a sample,
  which audit estimates on the sample's own inclusion probabilities because the sample was drawn in euro
  and not in items, so a tainting projects at the selection interval and a line certain of selection
  stands only for itself. Swap the nouns to a utility sampling meter readings for a billing error rate and
  the design has no reason to exist: a utility samples meters, because meters are what it is testing, so
  inclusion is equal and the ratio projection is the right one. The proportional design exists only
  because what is being tested and what materiality is denominated in are the same unit, which is what
  makes this an audit sampling problem and not a counting one.
- **Swap:** "how many of the hospital's admissions in the year were recorded against the wrong tariff"
  reads as a count over the sampled admissions scaled by the admission count, because admissions are
  sampled as admissions; nothing makes a large admission certain of being audited and nothing makes a
  small one stand for many, so the quantity collapses into the count and the task has nothing to estimate.
- **Layer 1:** the authority's own systems produce all of it and none of it decides the call. The ledger
  carries one row per payment line and several lines per invoice; two credit notes reverse payments inside
  the year; the bank feed delivered one payment batch twice with its own delivery sequence; the supplier
  master numbers suppliers differently from the ledger and a crosswalk carries both; the testing schedule
  is a table inside a PDF; the prescribed prior-year sample and the current year's sit in one overlapping
  extract; the capital programme register states values in thousands where every other file is in euro to
  the cent; the authority's financial year is the calendar year while the funder's grant claim runs to 31
  March.
- **Layer 2:** `field_method`. The methodological choice is what one tested payment line stands for: itself,
  a share of the lines, a share of the recorded value, or a fixed amount of euro fixed by how the
  selection was made.
- **Decisive step:** recognising that the tested set is a sample of euro and not of lines, so every line at
  or above the selection interval was certain and stands only for itself while a tainting below it carries
  a whole interval, and recovering that interval from the tested set.
- **Not semantics:** plan 4.2, plan 4.3 and manual 9.1 fix the population, the outcome, the window, the
  unit, the segmentation and the grain, and the field dictionary gives every column, so nothing turns on a
  reading. A solver who reads every field and every clause correctly still has to decide what the tested
  lines represent, and the misstatement found, the recorded-value ratio, the stratum ratio and the
  interval each give a different number: 41,307, 115,600, 163,525 and 800,000.
- **Not rule application:** no shipped sentence names a selection interval, a selection count, an inclusion
  probability, a projection, an extrapolation, a weighting or a stratum, and none describes how the
  population was ordered or selected from. A word sweep over every shipped file asserts it. Executing
  every stated rule leaves the solver holding a population, a tested set, a definition of misstatement and
  a question about what the tested set stands for.
- **Analyst test:** a strong analyst who carries the supplier numbers through the crosswalk, resolves the
  payment lines onto invoices, drops the credit notes and the re-delivered batch, lifts the table out of
  the PDF correctly and reads 9.1 exactly projects on the recorded-value ratio and files **115,600** (the
  `Ends on:` figure), where the misstatement the selection entitles is 800,000. `checks.py` runs that route
  on the generator's clean truth and asserts it files 115,600, then changes the decisive step alone and
  asserts 800,000.
- **Estimand:** manual 9.1: "The misstatement of a tested population is the amount by which the
  population's recorded value exceeds the amount properly payable, taken over every payment line in the
  population and over the year in which the line was paid. It is an amount of euro and not a count of
  lines or of invoices. It is stated for each work programme and for the authority, each to the nearest
  fifty thousand euro, the authority's figure being the sum of the programme figures as stated." Population,
  outcome, window, unit, segmentation and grain are all there; how the amount is arrived at for the lines
  that were not tested is nowhere stated, and that is the analysis.
- **No decoy:** nothing is planted to be caught. No scorecard, league table, ranked artifact, draft paper,
  memo or stakeholder figure ships; no block is copied; no screen, flag or indicator ships that the solver
  is meant to distrust. The tested set is a real sample of the population and every amount in it is the
  authority's own record; the defect is a wrong labour rate applied across small day-work invoices, which
  is a thing that happens and not a thing placed to be found.
- **No certified replay:** no past figure for this quantity ships. The prior year's extract holds its own
  tested lines and their findings, and no route on the ladder reproduces any closed or certified number
  from them; the prior year's own misstatement is not stated anywhere.
- **Lesson:** when a sample was drawn with probability proportional to size, what one sampled row stands
  for is fixed by the design and not by the row count or the value share, so the right projection is the
  one the design entitles and the ratio that the file makes obvious is wrong by the ratio of the sampled
  rows' mean size to the size-biased mean. No build on file teaches it: the corpus has survival behind a
  join, grain against a decided unit and conditioned yield, but no build turns on the inclusion
  probabilities of a designed sample recovered from the sample itself.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| below 0 the misstatement found, 41,307 | 9.1 defines misstatement, so a solver totals what the testing found | the schedule carries recorded and properly payable, so the difference is a column pair | yes, the first arithmetic | none ships | the battery reconciles the schedule to the ledger, not this | yes, one subtraction | readable |
| 0 the recorded-value ratio, 115,600 | nothing names a projection; 9.2 says the testing establishes the difference only for the lines tested, which makes the solver ask how to get from part to whole | the population's recorded value and the tested recorded value are both sums of one column | yes, the opponent's default when handed a sample and a population | none | no | yes, one ratio | readable |
| 1 the stratum ratio, 163,525 | nothing names a stratum | no column marks a line as certain of selection | yes, the obvious correction once the big tested lines are noticed | none | no | one ratio on two groups | readable |
| 2 **each tainting at the recovered interval, 800,000 (decisive)** | no shipped sentence names a selection interval, a selection count, an inclusion probability, a projection, a weighting or a stratum, and none says how the population was ordered or selected from, asserted by word sweep | no column, key or flag marks a line as certain, as proportional, or as standing for anything; the schedule carries a line reference, an amount recorded and an amount properly payable | no: the reflexes are the subtraction, the ratio and the stratified ratio, and each files a named wrong figure | none ships; no corpus, twin or colleague voice scores any projection | the battery reconciles the schedule to the ledger and finds the re-delivered batch, never what a tested line represents | no: the interval has to be recovered from the pattern of which lines were tested and which were not before anything can be multiplied | silent |

**Test 6, written out.** The test asks how the decisive step is **found**, not how much arithmetic follows
once it is found. The step here is recognising that the sample was drawn in euro rather than in items, so a
line at or above the interval stands only for itself while a tainting in a small line carries a whole
interval of untested euro. That is a reconceptualisation of what one tested row represents, not a
subtraction, a ratio or half of a reported figure, and the multiplication that follows being trivial is
what a correct estimator usually looks like. Written out, it does not fire. **Verdict: silent.**

## Semantic fork table

| id | Term or convention | Golden reading | Alternative | Ruled out by |
|---|---|---|---|---|
| SF1 | "the population" | every capital programme payment line paid in the year to 31 December 2026 | the invoices rather than the lines; capital and revenue together | 9.1 says every payment line in the population and the register names the capital programmes; `same call`: the figure is identical read on lines, asserted |
| SF2 | "misstated" | recorded value less the amount properly payable, overstatements only | any difference in either direction; absolute values | 9.1 says the amount by which the recorded value exceeds the amount properly payable; the testing found no understatement, asserted |
| SF3 | the window | 1 January to 31 December 2026, by the date the line was paid | the funder's year to 31 March; the date the invoice was received | 9.1 says the year in which the line was paid; the register states the authority's year; `same call` on the receipt date, asserted |
| SF4 | the unit | one amount of euro | a count of lines or of invoices | 9.1: an amount of euro and not a count of lines or of invoices |
| SF5 | the segmentation | the nine work programmes on the capital programme register | the three directorates; the supplier | 9.1 says for each work programme; the register carries the programme on every line |
| SF6 | the grain | the nearest fifty thousand euro per programme, the authority's figure their sum | the unrounded sum rounded once | 9.1 files both, and the construction makes the two agree: the stated programme figures sum to the stated total, asserted |
| SF7 | the credit notes | excluded, both the credit note and the line it reverses | the line kept, or the credit note kept as a negative | the dictionary gives `reverses_line_ref`; `same call`: neither is in the tested set, asserted |
| SF8 | the re-delivered batch | one payment line however many times the feed delivered it | each delivery a line | the dictionary states the feed's delivery sequence and that a line is one payment; `same call`, asserted |
| SF9 | the supplier numbers | the ledger's numbers carried onto the master's through the crosswalk | the ledger's numbers read as the master's | the crosswalk is complete and one-to-one over the window, asserted; the figure never reads a supplier |
| SF10 | the overlapping extract | the current year's tested lines only | both years' | the extract header states both years and the schedule states its own year; `same call` on the figure, asserted |
| SF11 | the register's thousands | converted to euro | read as euro | the register's own column header and the dictionary; `same call`: the figure never reads the register's values, asserted |
| SF12 | "shows, to the confidence at 4.2" | a bound on the misstatement at that confidence | the projection itself compared with tolerable misstatement | 4.3 says the testing must show that the misstatement does not exceed tolerable misstatement, which a point estimate does not show; and the crudest bound at that confidence already exceeds it, asserted |
| SF13 | "the programme carrying most of it" | the programme with the largest stated misstatement | the largest by recorded value, or by the misstatement found | the deliverable asks for the misstatement; the three rankings name different programmes, asserted |

## Ladder

**Measured on a real selection, not modelled.**

A synthetic population in four classes (contractor certificates, subcontractor interim payments, day-work
variation invoices, sundries) and a real monetary-unit selection at 180,000 from a random start. The
defect is a wrong day-work labour rate applied across small variation invoices in six programmes; eleven
of them fall in the sample, and one certificate carries a separate 24,000 error.

| Rung | The analysis | Figure | Upper limit | Decision | Step |
|---|---|---|---|---|---|
| below 0 | the misstatement found in the tested lines | 41,307 | 588,229 | certify | |
| 0 | the errors found scaled on the population's book value over the tested book value | **115,600** | 692,239 | certify | x2.80 |
| 1 | certainty lines at their own error, the rest on their stratum's book value | 163,525 | 759,335 | certify | x1.41 |
| 2 | **each tainting at the recovered interval, certainty lines at their own error** | **799,422** | **1,649,650** | **extended testing** | x4.89 |

The incremental allowance on the golden is 310,228, which is 0.40 of its sample projection, and the
allowance on each wrong rung is modelled at that same 0.40 of its own sample part, so every rung is tested
at the golden's own conservatism. **No wrong rung reaches extended testing**: the nearest one's upper limit
is 759,335, **65 per cent of materiality, a 35 per cent margin**, while the golden clears materiality by
**42 per cent**. Basic precision alone is 0.466 of materiality.

**The decision is robust to how the bound is built, which matters because the bound's construction is not
filed.** The crudest defensible one-sided bound at the stated confidence is the projection plus basic
precision, because basic precision is by definition the bound when nothing is found: 799,422 plus 540,000
is **1,339,422, which clears materiality by 15 per cent**. So a solver who knows only the single most
standard constant in the field, the factor 3.00 at 95 per cent, reaches the right decision, and every
richer bound clears it by more. The nearest wrong rung fails under every bound: 163,525 plus 540,000 is
703,525, 61 per cent of materiality. Every rung walks one way, the decisive move is
the largest, and the golden is the extreme.


**Position and dominance.** On every rung below the decisive one the programme carrying most of the
misstatement is Rail siding and yard, fourth of nine by recorded value, while the golden names Terminal
roof and cladding: the default path does not merely mis-size the figure, it names a different programme.
The recorded-value ranking names Deepwater berth renewal, the ranking by misstatement found names Rail
siding and yard, and the ranking by tested lines names Deepwater berth renewal, so three natural rankings
give three answers and none is the golden's.

**The grid.** The wrong answers are the rungs and the refused recovery routes, not fit variants: the
misstatement found (41,307), the recorded-value ratio (115,600), the stratum ratio (163,525), and the
figures the refused intervals give (365,722, 584,726, 962,901, 1,082,934, 1,083,173). Every single-error
cell files a feasible figure and none files the golden.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | every capital programme payment line paid in the year | 9.1 files it literally; SF1 asserted |
| 2 | Unit of account | one amount of euro | 9.1; SF4 |
| 3 | Attribution window | the date the line was paid | 9.1; SF3 asserted, and the receipt date gives the same figure |
| 4 | As-of dating | the ledger extracted 14 January 2027, the testing completed 26 February 2027, the year closed 31 December 2026 | the extract headers state it; the schedule carries its own completion date |
| 5 | Version basis | the bank feed's second delivery of the duplicated batch is the same payment | the dictionary's delivery sequence; SF8 |
| 6 | Denominator | none: the figure is an amount, not a rate | 9.1 states an amount of euro; each programme's recorded value ships beside it as a separate figure |
| 7 | Weighting | the weight a tested line carries is fixed by how the selection was made, and is the analysis | not closed by a sentence, and must not be: this is the decisive step |
| 8 | Window length | none: the figure is a level over one closed year | 9.1 |
| 9 | Boundary inclusivity | a line at or above the interval was certain of selection | recovered, not filed; the lattice fixes the interval and no population line sits within 1,000 euro of it, asserted |
| 10 | Rounding path | the nearest fifty thousand euro per programme, the authority's figure their sum | 9.1 files both; SF6 asserts the two agree by construction |
| 11 | Tie-break | the programme carrying most of the misstatement is named; Terminal roof and cladding leads the runner-up by at least one stated cell | asserted, with the unrounded figures not overlapping |
| 12 | Maturity and censoring | nothing is censored: the year is closed, every line is recorded, the testing is complete and no finding arrives later | asserted that the schedule holds no open or pending finding |
| 13 | Order of operations | each tested line's contribution is computed, then summed by programme, then rounded | asserted: sum-then-round and round-then-sum agree, which is SF6 |
| 14 | Row order | no step depends on file order, and the lattice recovery is invariant to re-ordering the population for presentation because it runs on the ledger's own sequence | asserted over six permutations of the presentation order |
| 15 | Duplicate resolution | one payment line per ledger row; the re-delivered batch collapses on the delivery sequence | the dictionary; SF8 |
| 16 | Identity normalisation | the crosswalk carries the ledger's supplier numbers onto the master's | complete and one-to-one over the window, asserted |
| 17 | Netting against gross | gross: credit notes and the lines they reverse are both excluded, nothing else nets | the dictionary; SF7 |
| 18 | Dimensional units | every amount is euro to the cent except the capital programme register, which states values in thousands | the register's column header and the dictionary; SF11, and the figure never reads it |
| 19 | Code and status semantics | `line_status`, `reverses_line_ref`, `delivery_sequence`, `programme_code` as the dictionary gives them | dictionary semantics; SF7, SF8, SF5 |
| 20 | Integerisation | the figure is an amount rounded to the nearest fifty thousand once | SF6; the underlying sits 24,422 from its line against a route band of plus or minus 1,500 |
| 21 | Clause scope | plan 4.2 sets materiality and the confidence, plan 4.3 the conclusion, manual 9.1 the estimand, manual 9.2 that no record holds it | the documents' own headings; asserted that no other clause bears on the figure |
| 22 | Forward window contents | the extended testing the conclusion may require has not been performed | the call is the conclusion on a closed population, with its reason below |

**Why the call is retrospective on its figure and forward on its consequence.** The misstatement is the
authority's own for a closed year, which is what an audit conclusion is about; the conclusion it drives,
whether the population goes to extended testing before the statements are certified, is work not yet done.
A figure about an open year would be a projection of a projection and no audit states one.

## Literal reader

A reader who executes the prompt, plan 4.2, plan 4.3 and manual 9.1 word for word, inferring nothing, has
the population, the outcome, the window, the unit, the segmentation, the grain, the comparison and the
conclusion rule all fixed, and 9.2 tells them no record holds the answer. Every reading of every term gives
the golden (SF1 to SF13, each asserted). The only thing the text does not give is what the tested lines
stand for, which is the analysis. Three constructions a reader may build instead are analyses rather than
readings, which is why the ladder and not the fork table carries them, and the seven recovery routes the
record refuses are measured in `## Draw` and asserted rather than argued.

## Oracles

Every control in the pack reads the same on the wrong path and on the golden. The capital programme
register's values in thousands reconcile to the ledger under every rung because they are sums of recorded
value and not of misstatement, to the authority's own stated residue. The prior year's extract holds its
own tested lines and findings and states no misstatement for its population, so no rung reproduces a
closed number from it. The funder's grant claim covers a different window and a different population and
ties under every rung. The supplier master carries approval categories and no figure. No corpus scores a
projection, no document ranks the programmes, and nothing in the pack states a misstatement for any
population in any year.

## Ask sheet

Three families, each multi-dimensional, each decoupled from the call and each carrying its own silent
device against the careful solver's path.

| Ask | Figures | The device |
|---|---|---|
| A1, per quarter of the year: the payment runs released, those released after the cut-off in force, and the net value of the payments reversed | 4 x 3 = 12 | the release cut-off moved from 15:00 to 14:00 on 1 July 2026 and the tolerance register carries both effective dates, so a solver using one cut-off for the year misses two quarters; one run lands exactly on the cut-off in force and the register says a run at the cut-off is within it |
| A2, per supplier risk category: the suppliers approved into it during the year, those removed from it, and those approved in then removed again | 5 x 3 = 15 | the approval register chains per supplier and carries superseded rows the dictionary rules out of the history; a category was relabelled on 1 October and the scale map carries both codings |
| A3, per month: the payment lines the testing schedule covers, whether any schedule line is absent from the ledger and if so how many, and whether any ledger line appears twice on the schedule and if so how many | 12 + 2 + 2 = 16 | the schedule is a table inside a PDF and its line references carry the ledger's supplier prefix, so the join needs the crosswalk; the re-delivered batch puts one ledger line on the schedule twice |

Every A3 ask is worded so that "none" is a grammatical answer, per H23.

Pair ceiling: 38

Mirror leakage: 21.0 per cent of ask weight

| Ask | The cracker, a response that answers the call correctly and takes each ask's obvious reading | What it never reaches | Verdict |
|---|---|---|---|
| A1 | one cut-off applied to the whole year | the cut-off moved on 1 July and the register carries both effective dates, so the second half is counted against the wrong one, and a run sitting exactly on the cut-off is within it | miss |
| A2 | every row of the approval register, each move counted | the superseded rows the dictionary rules out of a supplier's history, and the category relabelled on 1 October, which the scale map resolves | miss |
| A3 | the schedule joined to the ledger on its own line reference | the schedule's references carry the ledger's supplier prefix, so the join needs the crosswalk, and the re-delivered batch puts one ledger line on the schedule twice | miss |



## Pre-ship check

To be completed at stage 3. The free gates owed: generator `checks.py` including the three-rules block and
the analyst test on the clean truth, `verify.py` on the cut pack alone, two byte-identical rebuilds,
`figures_check.py`, the realism sweep, `golden-realism`, `reduce-house-fixes`, `leak.py`, `guard.py`
surface and heart, and the input gates. The two tuning targets in `## Draw` are asserted in `checks.py`
before the bundle is declared ready, together with the ten-route table and the lattice's feasible set.


## Tried and rejected

- Ranking the lines by the share of alerts that prove real (the yield reading): `guard.py nearest`
  measured the driver at 0.15 against task446 v2, which already builds a yield carried onto a
  population with a different base rate. Dropped at the draw, before any data was cut.
- The seed's own architecture, a filed scorecard ranking the divisions on confirmed movement per 1,000
  accounts: a stated score deciding the call, which the 10/10 rules ban, and a ranked artifact Gate G
  forbids shipping. No scorecard ships.
- Clause 9.2, which said the bank maintains no ranking of its business lines: it was there to keep a
  ranked artifact out of the pack, but the isolated reader quoted it as a sentence placed on purpose to
  reassure, which is a tell. Removed, and the Gate G guarantee is now carried by an assertion over
  every shipped PDF instead of by a sentence in one of them.
- A register in which every case is confirmed, every identifier sequential and no case amended past a
  second version: the reader called the pack plausibly real but slightly too orderly. The register now
  carries the cases that were put to the head of financial crime and not accepted, with no confirmed
  month, identifiers numbered as cases were opened with the gaps the register's own deletions leave,
  and ten cases amended twice. No graded figure moves: `figures.json` is byte-identical across the
  change, and SF14 asserts the wider reading of the disposition field names the same three lines.
- Clause 6.2's closing phrase, "the expectation is taken over the cases the line's own closed record
  implies", and clause 6.3's definition of that closed record: both were added by the first
  determinism repair, to close a fork between the expectation and a single realisation. Two isolated
  readers then quoted the pair as naming the method, one of them saying the stump had become "did you
  read 6.2" rather than "did you find the pitfall", and the determinism judge marked Gate F borderline
  for the same reason. That is the failure the house rules name: a determinism repair that files the
  HOW. Removed. The expectation is now carried by "expected to be carrying" alone, the realisation
  reading is ruled out because the register holds no unseen case (asserted), and the window the
  construction needs is closed by convergence over 36 windows and the register entire rather than by a
  clause. Clause 6.3 keeps the look-back span as a fact of the bank's governance, which says nothing
  about using it.
- The contract register's note that "the ledger holds the ticket under both references and the hours
  are owed once", and the ledger's own note column saying a row was "reissued under the credit note
  series": a filed rule adjudicating an ask's device, and a narration of it, which the ask layer's
  first two bans forbid. Both removed. Each credit note now names the ticket it reverses, so the
  reissued pair reverses more hours than that ticket was billed and only an internal inconsistency
  finds it.
- A register whose typologies were uniform across the eight lines, whose annual case counts barely
  moved, whose confirmation lag was uniform on nought to two months everywhere and whose amendments
  multiplied an amount by 1.08: the isolated reader read all four as generated. The mix is now what
  each line actually sees, the monthly count is a Poisson draw on a yearly and a seasonal factor, the
  confirmation lag runs with the line's own detection lag, and an amendment moves an amount either way.
- **Architecture 1, the whole of it, is spent.** Three consecutive judge SEND_BACK verdicts and a Gate
  F graded moderate to borderline then moderate to low. The reason is structural rather than a list of
  fixes. `determinism-check` requires the estimand to say that the population holds cases the bank has
  no record of yet, and requires the method to be forced, which here means every estimation route
  converging: it now does, over 36 windows of two years or more and the register entire. Once both
  hold, the only analytical step left is deciding to nowcast rather than count, and clause 6.2 has to
  announce that to be literal. Every Gate F repair reopened a determinism fork and every determinism
  repair closed the stump, twice round. Three isolated readers built the nowcast and landed the call at
  80 to 90 per cent confidence, so the portal's top two would both land it. The slot re-roots at stage
  1 with a new driver; the stock-from-arrivals-and-time-unseen driver is not reused.
- **Architecture 2, the WHAT screen run on four candidate decisive steps before this one.** Correcting
  the monitoring's output with the sensitivity and specificity measured on an assurance sample: dropped
  at the draw, because task446 v2 ships that driver in this same domain and task448 ships its stratified
  form, which the re-root brief bans. Estimating the undetected caseload from a below-the-line review
  sample: the same two cards, plus the sample's own arms announce the step. The excess of deposits over
  a counterfactual named in the estimand as "the number that would otherwise have been made there":
  dropped because naming the counterfactual that way excludes the band count by the clause's own words,
  which turns the decisive step into rule application and fails the analyst test. Ranking the eight
  segments rather than sizing the figure: dropped because a three-of-eight set pays a response that
  gets two members right, and the ladder cannot keep the top two off a set the way it keeps them off a
  figure. The step that survived settles none of the estimand's five parts, which `## Three rules`
  answers line by line.
- **The first cut of architecture 2's deposit-size record, spent at stage 4.** The law had one shape over
  5,000 to 16,000 and a different one below 5,000, so a fit window starting at 4,000 or 3,000 crossed the
  kink and gave 440 and 512 against the filed 400, and the per-bin integer rounding left enough scatter for
  an unweighted log fit at 100-dollar steps to read 421 and a one-sided fit to read 311. The design note
  asserted convergence it had not measured. Replaced by one shape end to end, a gentle decay of the same
  rate in every segment, with each 500-dollar block's count exact and the pile on round figures spread
  evenly inside it, so every family, window and step width lands on the same eight figures. The sweep is
  now run and asserted rather than claimed.
- **The pooled book profile as a wrong cell.** It gave 370 against 400 on the old record, and the note
  carried it as a single-error cell. On a record with one shape it converges with the rest, and it is now
  reported as one of the 199 estimators rather than as a rival.
- **Rating events drawn independently.** 205 of 805 follow-on events started from a band the customer was
  not in and 318 moved a rating to itself, which the solver's-eye reader read as generated and which gave
  "moved out of the band" more than one reading. The events now chain, so the ask has one answer.
- **A machine estate defined only by the service log.** The deposit feed invented machine ids the log never
  held, so "any machine with no service record" had no forced answer. The estate now ships as
  `deposit_machine_register.csv` with install and withdrawal dates, the feed takes deposits only at a
  machine in service that day, and the answer is the register's own.
- **Amounts drawn from evenly spaced quantiles of a fixed curve.** Every bin count was the curve's own
  value, so variance over mean was 0.11 bank-wide at 100-dollar bins and the eight segments gave
  chi-square per degree of freedom of 0.004 to 0.026, each with a tail probability below 1e-26. The
  determinism judge named this as the reason the method fork looked tight: the 199-estimator agreement and
  the 180-specification agreement were both bought by the absence of sampling noise, not by the design.
  Replaced by drawing each deposit independently from its segment's own density, so every bin count is a
  genuine sample, which `## Dispersion and granularity, measured` reports on the shipped pack. The dispersion sweep that was to find a ceiling is therefore dead: there is no ceiling to find,
  because block-level dispersion bought no chi-square at all (chi-square tracks the dispersion parameter
  squared, so the honest value needs the parameter at 1, which is a sample) and cost convergence at 0.02.
- **Block-exact generation with an evenly spread round-figure pile.** It was what made 199 estimators
  agree, and that is the defect above, restated. Recorded here so it is not reached for again.
- **Splitting generated by adding a band deposit on top of an existing day.** It put a surplus below the
  threshold with no matching deficit above, which both readers found: a real splitting process moves mass,
  so the takes that would have been reported are missing. Replaced by replacing a take: a deposit at or
  just above the threshold is taken out of the record and paid in instead as two deposits on the same day,
  the larger inside the band. The dollars balance to the cent and 10,000 to 11,000 carries a deficit of the
  same size as the band's surplus.
- **Raising the record's volume to beat the noise.** Measured at 2x, 4x and 8x with the construction
  scaled alongside: the bank figure's span across the judge's grid falls only from 44 per cent of the
  figure to 29 per cent, because the residue is specification bias (OLS on counts extrapolates the
  baseline low, log-OLS with curvature extrapolates it high) and bias scales with the figure, not with its
  square root. Flattening the baseline's curvature over the fit window, measured at 2x, 4x and 8x the
  decay length, does not remove it either.
- **Grading something derived instead of the level.** Measured across the 165 clean specifications: the
  rise over the prior year spans 125 to 244, the ratio 1.46 to 2.58, every segment's share of the bank
  figure spans 5 to 21 points, the largest segment splits 113 to 52 between two segments, and a
  significance call on each segment's own trade gives 4 to 10 distinct answer sets at every bar from 1.5
  to 5. The specification bias does not cancel in a difference, a ratio, a share or a ranking, so none of
  these is determinate either.
- **An averaging estimator the pack files nowhere (architecture 2's last stand, and what spent it).** The
  golden was the average of the band's surplus below the threshold and the deficit above it, and the
  determinism judge reproduced it under that estimator and no other: the surplus alone gave unrounded bank
  figures from 71 to 786 and the deficit alone from 207 to 858, while the average gave 450 in all 186 of
  its complete specifications. The reason it agreed is the finding: being the half difference of two
  observed counts less a half slope correction of 2.7 to 58 deposits, it cancels the fitted profile's level
  algebraically, so it is insensitive to exactly what the specifications differ on and every other
  estimator is still standing. The refusal rule the build used, failing to reconcile within a fifth, is in
  no shipped file, so the 141 standing specifications could not be reproduced from the bundle at all. The
  general lesson, and the reason this slot is now barred from the whole family: a decisive step that is an
  estimation choice over a fitted counterfactual density cannot be both forced and silent, because the
  specifications always disagree and nothing filable chooses between them without becoming rule
  application. Three passes each moved the artifact instead of removing it (a smooth draw, then an
  algebraic cancellation), which is what spending an architecture looks like.
- **A per-segment table that book size alone reproduces.** On architecture 2's shipped pack a flat rate on
  the paid-in column matched 7 of 8 segment cells at about 0.82 per cent, and at 0.91 per cent it matched 6
  of 8 with the bank figure landing on exactly the golden, only the top two segments wrong. Raising one
  segment's propensity was not enough to break it. The replacement is not a tuning: the blind-response
  test now runs at the draw, before any file exists, on the widest graded component, and the component's
  shape changes if it fails.
- **Two paths to one headline, asserted to agree on one family.** Summing the rounded segment figures gave
  the golden in 186 of 186 specifications while rounding the unrounded sum gave it in 93, so SF12's
  assertion that both paths agree was true on the author's family and false on the judge's. A two-path
  assertion is only worth what the family behind it is worth.
- **A handbook sentence ordered to state a role, which stated the method.** Filing "the whole of that band
  is what the figure estimates, so no part of it evidences what the band would have held absent the
  practice" was the instruction; the clause that followed it, "that has to come from the segment's trade
  outside the band", told the solver where to build the counterfactual. A sentence filed to close one thing
  closes more than it was asked to, so any sentence filed at authority now goes to the author in its exact
  wording before it ships.

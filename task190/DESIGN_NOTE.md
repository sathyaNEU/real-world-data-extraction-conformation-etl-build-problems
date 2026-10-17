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
| Shape | 12, drill-down to one leaf. Nine work programmes, two figures each (18), the authority's figure and the programme carrying most (2), the referral decision (1), the chart's nine bars and the mark on the largest (10), and the three ask families' 41 figures. 72 graded figures, plus instruction-following. |
| Gap | 4, rule: which projection the tested set's own selection entitles. |
| Strategy | `population_selection`; Layer 2 family `field_method`; generators G16 decisive, G17 supporting, G10 in Layer 1. |
| Decision | `quantity_figure`, answer unit `currency`, question form how-much. |
| World | Carrowmore Port Authority, Ireland, EUR, year to 31 December 2026. People drawn from `guard.py names --geo Ireland --seed 190`: Tanya McCrea, Colm Shaffrey, Marc O'Reardon. |
| Deliverables | `projected_misstatement_2026.csv`, `misstatement_by_population_2026.png`. |
| Guard | No BLOCK, after five redraws (context artifact three times, gap, people, deliverables) and three differentiation lines. Two WARNs, `repeat.gate_g` and `overuse.gate_g`, answered in the card's notes: no other Gate G key is true of this build, and the variety is carried by the driver, which scores 0.07 against the whole corpus on `guard.py check` and 0.05 against every card driver on `guard.py heart`, the lowest this slot has drawn. `guard.py heart` WARN. |

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
| Population | 59,469,739.92 EUR over 26,648 payment lines, nine work programmes |
| Tolerable misstatement | 1,160,000 EUR, 2.0 per cent of budgeted capital expenditure of 58,000,000. **Shipped.** |
| Expected misstatement allowed in planning | 387,500 EUR. **Not shipped, and the reason is below: the plan's own sizing formula would otherwise give the interval away exactly.** |
| Interval | (1,160,000 less 387,500 x 1.60) / 3.00 = **180,000**. Not shipped. |
| Selections | 330, on 271 distinct tested lines; the 31 certainty lines hold 15,826,525 EUR, 75 per cent of the tested recorded value of 21,043,847.13 |
| Basic precision | 180,000 x 3.00 = **540,000, which is 0.466 of materiality**, so step one escalates nothing |
| Stated granularity | the nearest **50,000** EUR, set from the measured route spread below |

### Every recovery route, and what the record does with it

The figure is linear in the interval, so a route that recovers the interval differently files a
proportionally different figure. Ten routes, the figure each files, and whether the record admits it:

| Route | Interval | Figure | Stated | The record |
|---|---|---|---|---|
| the lattice: the only interval fitting every tested and every untested line | 180,000 | **811,170.09** | **800,000** | admits |
| the median gap between selections, line end to line end | 180,116 | 811,692.98 | 800,000 | refuses |
| the median gap, midpoint to midpoint | 180,239 | 812,248.27 | 800,000 | refuses |
| the certainty threshold, the smallest line certain of selection | 180,726 | 814,441.81 | 800,000 | refuses |
| the median gap, line start to line start | 180,827 | 814,895.43 | 800,000 | refuses |
| recorded value over the count of distinct tested lines | 219,446 | 988,931.41 | 1,000,000 | refuses |
| recorded value over the count of tested lines below the interval | 247,791 | 1,116,668.39 | 1,100,000 | refuses |
| the mean gap, midpoint to midpoint | 247,823 | 1,116,814.17 | 1,100,000 | refuses |
| the certainty bracket's midpoint | 132,907 | 598,944.79 | 600,000 | refuses |
| the certainty bracket's lower end, the largest untested line | 85,088 | 383,447.76 | 400,000 | refuses |

Over every route the figures run 383,447.76 to 1,116,814.17, a spread of 191 per cent across five stated
cells, so the routes genuinely disagree and the set was not narrowed to the ones that agree. **The record
admits exactly one of them.** And the five routes that land within two per cent of the interval span
811,170.09 to 814,895.43, 0.46 per cent, **all in one stated cell at the nearest fifty thousand**: so a
solver who takes the natural approximate route rather than the lattice still files the graded figure. That
is what sets the granularity. The underlying 811,170.09 sits 13,830 inside its cell against a half cell of
25,000, and **the nearest wrong answer a defensible route produces is 988,931.41, 21.9 per cent away**,
which is the measurement C4 asks for: route to route, not against the adjacent cell of the stated grid.
The five far routes are each refused by the record, and `checks.py` asserts the whole table, both the
family that agrees and the distance to the nearest route that does not, rather than claiming agreement.

### What the lattice's feasible set is, stated precisely

It is not an invariance over a feasible set and not a unique value on a chosen grid. **On a one-euro grid
over 178,000 to 182,000, exactly one interval is feasible: 180,000**, and the search was run over that
whole 4,001-euro range rather than at a chosen point, so the neighbouring intervals were excluded rather
than assumed away; `checks.py` re-sweeps the inner band of plus or minus 40 euro exhaustively on every
rebuild. The five far routes in the table above sit at 85,088, 132,907, 219,446, 247,791 and 247,823 and
are each refused by the same test. At that interval the starts that reproduce the realised pattern span
**23.76 euro**, from 121,746.57 to 121,770.33, which contains the start the selection actually ran from.
The constraint is that every one of the 271 tested lines must contain a step of cumulated recorded value
under one common start and none of the 26,377 untested lines may. **Measured, and it corrects what the
first draft of this section claimed:** the tested lines alone already pin both the start window and the
interval, to the same 23.76 euro and the same single value over the whole 4,001-euro band, so the untested
lines confirm the recovery rather than carrying it and a solver who sweeps only the tested side gets there.
So the projection is a single value, and the feasible set's size is 23.76 euro of start and one euro of
interval.

### The programme table, and the blind responses

Nine programmes, each carrying the projected misstatement and the share of its recorded value that was
certain of selection. The five families are a constant in every cell, nil in every cell, and one obvious
rate applied to recorded value, to the tested-line count, or to the misstatement the testing found.
Measured at the draw, before any file existed: all five score **4 of 18, 22 per cent**, because four
programmes read nil, which is above the fifth the author set as the point to act, so the construction was
tuned to three nils. Measured again on the cut pack by `checks.py`: **all five score 3 of 18, 17 per
cent**, and those three cells are the three nil misstatements. No blind family reaches a non-nil
misstatement or any certain share at all, because both graded figures per programme need the recovered
interval.

### The tuning contract, and what the cut pack measures against it

Two residual defects at the design point, both tuning rather than design, with the constraint asserted
against each and the measurement beside it:

1. **The two paths to the headline have to agree.** Both are computable, so if the stated programme
   figures and the rounded total disagree the task has two defensible headlines, and filing the WHAT does
   not fix it because the other path stays computable. That was architecture 2's SF12 failure. The
   generator tunes each programme's taintings so **the sum of the stated programme figures equals the
   stated total**: measured, the nine stated figures sum to 800,000 and the unrounded 811,170.09 rounds to
   800,000, asserted both ways.
2. **Four nil programmes at the design point, three in the pack.** Measured: Deepwater berth renewal, Quay
   3 reconstruction and the Dredging programme, each nil exactly rather than merely deep in its cell, and
   none of them carrying a nil certain share, which is what protects the pair. The two largest are nil
   because they are paid on contractor certificates and carry no day-work defect at all; the Dredging
   programme carries 31 defective day-work lines that the selection happened to miss, which is what a
   probability sample does and is the honest reason its figure is nil.

The rest of the tuning contract, with the measured value beside each: every programme's underlying figure
at least 9,000 inside its stated cell (worst 10,688, at Rail siding and yard) against a per-programme
route band of at most 1,214 euro across the five near routes; the headline's underlying at least 11,000
from its edge (measured 13,830, against a headline route band of 3,725); the largest programme by
misstatement outside the top three by recorded value (Rail siding and yard, fourth of nine); the stated
figures taking at least five distinct values (measured six: nil, 50,000, 100,000, 150,000, 200,000 and
250,000); and all five blind families at 3 of 18 or fewer (measured 3).

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
projection or against a bound. On these figures the projection is 811,170.09 against materiality of
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
   it. It is 15,445.38 euro, which cannot be the population's misstatement because only part of the
   population was tested.
5. Project it to the population on the ratio the files make obvious: the population's recorded value over
   the tested recorded value, 59,469,739.92 over 21,043,847.13, a factor of 2.826.
6. State the result by work programme and for the authority, and read the conclusion at plan 4.3.

**Ends on:** 43,648.52 euro, which is accepted at 4.3 and certifies the population, with Security and
access systems the programme carrying most of it.
**Golden:** 800,000 euro, which is not accepted at 4.3 and refers the population for extended testing,
with Rail siding and yard the programme carrying most of it.

The default path cleans every key correctly, reads every clause correctly and uses a projection that is
arithmetically sound. It files a figure nineteen times too small because it treats the tested lines as a
sample of lines when they are a sample of euro.

## Stump sentence

The default path scales the misstatement it found on the ratio of the population's recorded value to the
tested recorded value and files **43,648.52** euro, which certifies the population, because the 31 lines at
or above the recovered selection interval hold 75 per cent of the tested recorded value and are sound,
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
  interval each give a different number: 15,445.38, 43,648.52, 129,201.54 and 800,000.
- **Not rule application:** no shipped sentence names a selection interval, a selection count, an inclusion
  probability, a projection, an extrapolation, a weighting or a stratum, and none describes how the
  population was ordered or selected from. A word sweep over every shipped file asserts it. Executing
  every stated rule leaves the solver holding a population, a tested set, a definition of misstatement and
  a question about what the tested set stands for.
- **Analyst test:** a strong analyst who carries the supplier numbers through the crosswalk, resolves the
  payment lines onto invoices, drops the credit notes and the re-delivered batch, lifts the table out of
  the PDF correctly and reads 9.1 exactly projects on the recorded-value ratio and files **43,648.52** (the
  `Ends on:` figure), where the misstatement the selection entitles is 800,000. `checks.py` runs that route
  on the generator's clean truth and asserts it files 43,648.52, then changes the decisive step alone and
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
| below 0 the misstatement found, 15,445.38 | 9.1 defines misstatement, so a solver totals what the testing found | the schedule carries recorded and properly payable, so the difference is a column pair | yes, the first arithmetic | none ships | the battery reconciles the schedule to the ledger, not this | yes, one subtraction | readable |
| 0 the recorded-value ratio, 43,648.52 | nothing names a projection; 9.2 says the testing establishes the difference only for the lines tested, which makes the solver ask how to get from part to whole | the population's recorded value and the tested recorded value are both sums of one column | yes, the opponent's default when handed a sample and a population | none | no | yes, one ratio | readable |
| 1 the stratum ratio, 129,201.54 | nothing names a stratum | no column marks a line as certain of selection | yes, the obvious correction once the big tested lines are noticed | none | no | one ratio on two groups | readable |
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

A population of 26,648 payment lines in four classes (contractor certificates, subcontractor interim
payments, day-work variation invoices, sundries) and a real monetary-unit selection at 180,000 from a
random start. The defect is a wrong day-work labour rate applied across small variation invoices in seven
of the nine programmes; the two largest by recorded value, Deepwater berth renewal and Quay 3
reconstruction, are paid almost entirely on contractor certificates and carry none of it, and **no
certificate is overstated: every line certain of selection was found sound**, which is what makes the
recorded-value ratio fail. Six programmes carry a tainting in the sample; the Dredging programme's 31
defective lines were all missed by the selection, so its projection is nil. A first draft put an error on
one certificate and it inverted two rungs, because the ratio route scales that error by the
whole-population factor while the stratum route takes it at face: the line is in
`## Tried and rejected`.

The figures in the table below are the measured ones at the design point the generator carries. Every one
is asserted in `checks.py` against the clean truth, and `verify.py` recomputes each from the bundle alone
on its own code path, recovering the interval itself rather than being told it.

| Rung | The analysis | Figure | Upper limit | Decision | Step |
|---|---|---|---|---|---|
| below 0 | the misstatement found in the tested lines | 15,445.38 | 561,623.53 | certify | |
| 0 | the errors found scaled on the population's recorded value over the tested recorded value | **43,648.52** | 601,107.92 | certify | x2.83 |
| 1 | certainty lines at their own error, the rest on their stratum's recorded value | 129,201.54 | 720,882.15 | certify | x2.96 |
| 2 | **each tainting at the recovered interval, certainty lines at their own error** | **811,170.09** | **1,698,967.57** | **extended testing** | x6.28 |

The incremental allowance on the golden is 347,797.48, which is 0.43 of its projection, and the allowance
on each wrong rung is modelled at 0.40 of its own sample part, so every rung is tested at the conservatism
the golden itself earns. **No wrong rung reaches extended testing**: the nearest one's upper limit is
720,882.15, **62 per cent of materiality, a 38 per cent margin**, while the golden clears materiality by
**46 per cent**. Basic precision alone is 0.466 of materiality. Every certainty line was found sound, so
the certainty part of each rung is nil and the allowance falls entirely on the sampled part.

**The decision is robust to how the bound is built, which matters because the bound's construction is not
filed.** The crudest defensible one-sided bound at the stated confidence is the projection plus basic
precision, because basic precision is by definition the bound when nothing is found: 811,170.09 plus
540,000 is **1,351,170.09, which clears materiality by 16 per cent**. So a solver who knows only the
single most standard constant in the field, the factor 3.00 at 95 per cent, reaches the right decision,
and every richer bound clears it by more. The nearest wrong rung fails under every bound: 129,201.54 plus
540,000 is 669,201.54, 58 per cent of materiality. Every rung walks one way, the decisive move is the
largest, and the golden is the extreme.


**Position and dominance.** On every rung below the decisive one the programme carrying most of the
misstatement is Security and access systems, seventh of nine by recorded value, while the golden names
Rail siding and yard, fourth of nine: the default path does not merely mis-size the figure, it names a
different programme. The recorded-value ranking and the tested-lines ranking both name Deepwater berth
renewal, the ranking by misstatement found and the stratum ratio both name Security and access systems,
and no natural ranking of the pack reaches the golden's answer. The golden's leader leads its runner-up by
a full stated cell, 250,000 against 200,000, and by 50,257 unrounded, so the two do not overlap.

**The grid.** The wrong answers are the rungs and the refused recovery routes, not fit variants: the
misstatement found (15,445.38), the recorded-value ratio (43,648.52), the stratum ratio (129,201.54), and
the figures the refused intervals give (383,447.76, 598,944.79, 811,692.98, 812,248.27, 814,441.81,
814,895.43, 988,931.41, 1,116,668.39 and 1,116,814.17). Every single-error cell files a feasible figure.
Four of the refused intervals round into the golden's stated cell, which is the granularity doing its job
rather than a leak: they are the approximate recoveries of the same interval. The five that do not land at
400,000, 600,000, 1,000,000 and 1,100,000, none of them the golden.

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
| 9 | Boundary inclusivity | a line at or above the interval was certain of selection | recovered, not filed; the lattice fixes the interval and no population line sits at it, the nearest being 726 euro above and 71,054 euro below, so "at or above" and "above" give the same certainty set, asserted |
| 10 | Rounding path | the nearest fifty thousand euro per programme, the authority's figure their sum | 9.1 files both; SF6 asserts the two agree by construction |
| 11 | Tie-break | the programme carrying most of the misstatement is named; Rail siding and yard leads the runner-up by at least one stated cell, 250,000 against 200,000 | asserted, with the unrounded figures 50,257 apart and not overlapping |
| 12 | Maturity and censoring | nothing is censored: the year is closed, every line is recorded, the testing is complete and no finding arrives later | asserted that the schedule holds no open or pending finding |
| 13 | Order of operations | each tested line's contribution is computed, then summed by programme, then rounded | asserted: sum-then-round and round-then-sum agree, which is SF6 |
| 14 | Row order | no step depends on file order, and the lattice recovery is invariant to re-ordering the population for presentation because it runs on the ledger's own sequence | asserted over six permutations of the presentation order |
| 15 | Duplicate resolution | one payment line per ledger row; the re-delivered batch collapses on the delivery sequence | the dictionary; SF8 |
| 16 | Identity normalisation | the crosswalk carries the ledger's supplier numbers onto the master's | complete and one-to-one over the window, asserted |
| 17 | Netting against gross | gross: credit notes and the lines they reverse are both excluded, nothing else nets | the dictionary; SF7 |
| 18 | Dimensional units | every amount is euro to the cent except the capital programme register, which states values in thousands | the register's column header and the dictionary; SF11, and the figure never reads it |
| 19 | Code and status semantics | `line_status`, `reverses_line_ref`, `delivery_sequence`, `programme_code` as the dictionary gives them | dictionary semantics; SF7, SF8, SF5 |
| 20 | Integerisation | the figure is an amount rounded to the nearest fifty thousand once | SF6; the underlying sits 13,830 inside its cell against a headline route band of 3,725 and a per-programme band of at most 1,214 |
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
readings, which is why the ladder and not the fork table carries them, and the nine recovery routes the
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
| A1, per quarter of the year: the payment runs released, those released past the cut-off in force, and the value those carried | 4 x 3 = 12 | three devices, each measured: the cut-off moved from 15:00 to 14:00 on 1 July 2026 and the register carries both effective dates, so one cut-off for the year undercounts both later quarters; a run released past midnight ends each quarter, so grouping on the opening date rather than the release moves the counts; and one run was rejected by the bank and re-released, so the log carries it twice. A run released exactly at the cut-off is within it, which the register states |
| A2, per supplier risk category: the suppliers approved into it during the year, those removed from it, and those approved in then removed again | 5 x 3 = 15 | the approval register chains per supplier and carries superseded rows the dictionary rules out of the history; a category was relabelled on 1 October and the scale map carries both codings |
| A3, per month: the payment lines the testing schedule covers, whether any schedule line is absent from the ledger and if so how many, and whether any ledger line appears twice on the schedule and if so how many | 12 + 2 = 14 | the schedule is a table inside a PDF and its line references carry the ledger's supplier prefix, so the join needs the crosswalk; the re-delivered batch puts one ledger line on the schedule twice |

Every A3 ask is worded so that "none" is a grammatical answer, per H23.

Pair ceiling: 37.1

Mirror leakage: 22.0 per cent of ask weight

Measured by: `generator/ceiling.py`, which builds both responses as code, scores them against the graded
figures in `figures.json` on the cut pack and prints the pair ceiling and the mirror leakage; it exits
non-zero if the ceiling reaches 50. `generator/checks.py` measures the five blind families on the same
pack and runs each cracker reading in the table above against the golden.

**What the script changed, and it is the reason the line exists.** The paper figures were a pair ceiling
of 38 and a mirror leakage of 21.0, and neither was measured. Written as code and run on the cut pack, the
first run gave a pair ceiling of 45.1 and **a mirror leakage of 46.3**, which fails its gate outright: the
A1 and A2 devices each moved two or three cells out of twelve and fifteen, so a response that reached the
call banked nearly half the ask weight. Four things were rebuilt until the script read 37.1 and 22.0.

- **A1 turns on three devices rather than one.** The cut-off moved on 1 July, so one cut-off for the year
  undercounts both later quarters; a run released past midnight ends each quarter, so grouping on the
  opening date rather than the release moves the quarter counts; and one run was rejected by the bank and
  re-released, so the log carries it twice and the count needs de-duplicating.
- **A1's third figure was nil in three quarters of four**, so anyone took it. The net value reversed is
  replaced by the value the runs past the cut-off carried, which is non-nil in every quarter and inherits
  both the cut-off and the quarter device, asserted.
- **A2's cracker reading is now the scale map rather than the superseded rows.** Ignoring the October
  relabelling is wrong in almost every cell; the superseded rows moved three.
- **Nine of the nineteen cells in the widest graded component were free to every response**, because the
  payments recorded per programme is a plain sum of the pack. That column is out of the graded table and
  out of the prompt: both figures per programme, the misstatement and the share of recorded value certain
  of selection, now need the recovered interval, so neither is free. The cracker's take in that band fell
  from 12 of 19 to 3 of 19, which is the three nil programmes it reaches by filing a figure nineteen times
  too small.

Measured after all four: the cracker takes 9 of the 41 ask figures and 3 of the 19 component cells and
scores 21.0; a response that answers the call correctly and still takes each ask's obvious reading scores
53.2; the pair is **37.1**, under the 40 the house builds to.


| Ask | The cracker, a response that answers the call correctly and takes each ask's obvious reading | What it never reaches | Verdict |
|---|---|---|---|
| A1 | one cut-off applied to the whole year | the cut-off moved on 1 July and the register carries both effective dates, so the second half is counted against the wrong one, and a run sitting exactly on the cut-off is within it | miss |
| A2 | every row of the approval register, each move counted | the superseded rows the dictionary rules out of a supplier's history, and the category relabelled on 1 October, which the scale map resolves | miss |
| A3 | the schedule joined to the ledger on its own line reference | the schedule's references carry the ledger's supplier prefix, so the join needs the crosswalk, and the re-delivered batch puts one ledger line on the schedule twice | miss |



## Pre-ship check

**The pack.** 18 files, four formats (11 csv, 2 xlsx, 3 pdf, 1 md), the spine
`capital_payment_lines_2026.csv` at 26,874 rows (26,648 population lines plus the two credit notes and the
re-delivered batch), every file carrying a source, a date and a licence in `metadata.json` and asserted
complete against the cut directory, two declared distractors (the funder's
grant claim on a claim year to 31 March, and the revenue expenditure summary, which is the other
population the plan tests) plus the prior year's lines, which the two-year testing extract needs and whose
own misstatement is stated nowhere.

**Layer 1, every item produced by the authority's own systems and none of it deciding the call.** The
ledger carries one row per payment line and several lines per invoice; two payments were reversed inside
the year and the credit notes that reverse them ship beside them; the bank feed delivered one payment run
twice with its own delivery sequence; the supplier master numbers suppliers differently from the ledger
and a crosswalk carries both, which the testing schedule's references need; the schedule is a table inside
a PDF; the prior year's tested lines and the current year's sit in one overlapping extract; the capital
programme register states approved budgets in thousands where every other file is in euro to the cent; the
authority's financial year is the calendar year while the funder's claim runs to 31 March; one line was
queried and re-tested, so the schedule carries it twice, and it carries no exception, so no figure the
report states turns on it.

**What is filed at authority, and nothing more.** Plan 4.2 (tolerable misstatement and the confidence),
plan 4.3 (the conclusion, as a confidence statement that only a bound satisfies), manual 9.1 (the
estimand) and manual 9.2 (that no record holds the answer). Asserted by word sweep over every shipped
file: no selection interval, no selection count, no inclusion probability, no reliability or expansion
factor, no basic precision, no incremental allowance, no upper limit, no expected-misstatement allowance,
and nothing about projecting, scaling, weighting, extrapolating or monetary units.

**The free gates.**

| Gate | Result |
|---|---|
| `precut.py task190` | 50 checks, 0 FAIL, 0 WARN |
| `voice-check.py task190` | PASS, 974 characters |
| generator `checks.py` | 121 assertions: the three-rules block R1 to R3c on the clean truth, the analyst test executed, the ladder's conclusions at 4.3, the determinism block (the whole route table, the lattice, its neighbouring band and the interval's boundary), SF1 to SF13, the five blind families, the input gates including every file's licence record, and the asks |
| `verify.py` (reads `target/` and `figures.json` only, own code path, recovers the interval itself) | 0 failed |
| two consecutive rebuilds | `target/` and `golden/` byte-identical |
| `figures_check.py task190` | every figure in blocks 1 to 4 present in `figures.json` |
| `leak.py task190 --asof 2027-02-26` | REVIEW, every line answered below |
| `guard.py check` / `heart` | no BLOCK; WARN on the two answered gate_g repeats (`repeat.gate_g` against task468, `overuse.gate_g` at 7 of the last 12); nearest driver 0.07 on `check`, 0.05 against card drivers on `heart` |
| `guard.py surface` | no BLOCK; no persona the card never planned, and only two of the three carded names ship; eight pairs promoted for the author's adjudication, five on corpus-wide surface idiom (shared file names, the `pdf+png` deliverable pair, `quantity_figure`) and three on the same-driver signature, gap `rule` plus pattern G16 plus Gate G `method_or_model_selection`, against task185, task457 and task80, each already answered by a differentiation line on the card |

**The leak report's lines, answered.** REVIEW on six lines, each read and each answered.

- **Block 3, "golden figure 4.3 appears" in the plan.** The sweep matched the clause number 4.3, not a
  figure: the text it quotes is the heading "4.3 Conclusion on a tested population". Tolerable
  misstatement is in the plan by design and approved, and the write-up no longer repeats the figure in a
  graded block, so the sweep that first flagged 1,160,000 as a golden figure now passes. No golden figure
  appears in any shipped file, asserted by word sweep in `checks.py`.
- **Block 3, the plan carries 14 of 14 and the provenance note 9 of 14 of the call's distinctive words.**
  The call is asked in the manual's own words because 9.1 is the estimand: payment, population,
  misstatement, programme, tested, year, euro. The question cannot be asked without them, and neither
  document carries the figure, the interval, a projection or any step of the method.
- **Block 4, 5 of 25 stump-paragraph terms in the manual and 4 of 25 in the schedule.** The matches are
  tested, amount, carries, stated, payment and nothing, which are the vocabulary of any audit working
  paper. Read for whether either document names the move: neither names a selection interval, a selection
  count, an inclusion probability, a projection, a weighting or a stratum, and neither says how the
  population was ordered or selected from, asserted.
- **Block 9, nine ISO dates after the as-of in the capital programme register.** They are the programmes'
  scheduled completion dates, the latest 2028-03-31. A capital programme register carries the dates the
  works are due to finish, so dates beyond the audit as-of are what the file is for; none of them bears on
  the figure, and the register's values are the only thing the figure could read from it and it does not
  read them (SF11).
- **Block 10, container metadata.** INFO; `scrub_producer_metadata.py` reports the pack clean, with no
  producer signature and no out-of-band timestamp.

**Golden realism.** The schedule is sorted by the misstatement indicated and then by programme name, the
order the chart uses; recorded value to the cent as the ledger holds it, the misstatement whole because
9.1 states it to the nearest fifty thousand, the share to one decimal; the authority row carries its own
certain share rather than a blank. The chart's title is the finding, the axis names its unit and its
grain, the three nil programmes are explained in a footer from the pack's own facts, and the source strip
carries the testing completion date. Every programme's recorded value is a non-round figure: nine totals
each within a euro of a round million was the first draft's clearest tell and the contractor certificates
were round too, so both were redrawn.


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
- **An error on one contractor certificate.** It was put there so the Dredging programme would not read
  nil, and it inverted two rungs: the recorded-value ratio scales a certainty line's error by the whole
  population factor (2.8x) while the stratum route takes it at face, so at an error of 62,400 the ratio
  route filed 216,123 against the stratum route's 182,462 and the ladder ran backwards. The arithmetic is
  that the inversion happens whenever the certainty error exceeds about 2.9 times the proportional
  findings, and keeping it below that left too little room to also hold the rungs 1.15x apart. Replaced by
  putting the defect in a seventh programme's day-work instead, so no certainty line carries an error at
  all. That is better in three ways: the ladder is monotone by construction, the story is cleaner (the big
  certificates get the most scrutiny and were sound, which is exactly why the recorded-value ratio fails),
  and the two largest programmes reading nil is a fact a reader can check rather than a coincidence.
- **Computing the golden from the designer's exact tainting fractions.** The schedule ships the amount
  recorded and the amount properly payable, both to the cent, so a solver's fraction is theirs and not the
  designer's. The generator and the independent verifier disagreed by up to 34 cents until the fraction
  was recomputed from the rounded payable, which is now what the population carries.
- **Shipping the ledger extract sorted by payment date.** The selection cumulates the population in the
  ledger's own sequence, and sorting the extract by date destroyed that order, so the interval was no
  longer recoverable and the verifier could not reproduce the figure at all. The extract now ships in the
  ledger's posting sequence with a `ledger_sequence` column, which is how a ledger extract comes out and
  which survives a solver re-sorting the file.
- **Nine programme totals each within a euro of a round million.** The first draft scaled each programme
  to a round target and the contractor certificates were round too, which is the clearest realism tell in
  the pack and would have been the first thing a reader quoted. Both were redrawn off round numbers, which
  moved the cumulative values and forced the design point to be re-tuned from scratch.
- **The claim that the untested lines are what make the interval unique.** The note asserted that the
  tested lines alone narrow the start but admit many intervals, so the untested side carried the recovery.
  Measured on the cut pack it is false: the tested lines alone pin both the interval and the same
  23.76-euro start window over a 4,001-euro band. The claim was replaced by the measurement, and the
  untested side is now described as a confirmation. Nothing in the design changed; an unmeasured sentence
  about the mechanism did.
- **A closure row asserting a clearance nothing asserted.** Axis 9 claimed no population line sits within
  1,000 euro of the interval, "asserted", and no assertion existed; the nearest line is 726 euro above it.
  The row now states the measured gaps and two assertions were added to `checks.py`, so the boundary
  reading cannot move the certainty set and the claim is executed rather than written.

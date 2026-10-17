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

## Author override of the judge's disposition

Architecture 3's first determinism judge returned **NOT_DETERMINISTIC, SEND_BACK**. By the letter of
`build-pipeline` that spends the architecture and retires the number, because a SEND_BACK spends an
architecture and this is task190's third. The author overrode the disposition to **FIX_NOW**. The
reasoning and the condition are recorded here verbatim, because an author override of a judge's
disposition that nobody can find later is worse than no override.

> **The test I applied.** An architecture is spent when the decisive step cannot be saved, and the mark of
> that is when the only way to close the fork is to file the HOW. That is what killed architecture 1 of
> task194 this morning. It is not what is happening here. Every fix the judge asks for files the WHAT: what
> the sample is, how it was drawn, what the terms in its own working papers mean. None of them files the
> estimator. And the judge's own gates say the decisive step is alive: Gate F high, with every easy route
> accepting the population; Gate G pass; Gate H pass with the decisive step analytical and no decoy; the
> headline reproducing at 800,000, refer, Rail siding and yard 250,000. The proof is in the cold reader: it
> saw the certainty stratum perfectly well, called it out at about 100,000, and still used a value-weighted
> ratio estimator, got about 130,000 and accepted the population. Telling a solver how the sample was drawn
> does not tell it how to project from a sample drawn that way, and that gap is the whole build.
>
> **The condition, and it is hard.** If the re-judge after this pass is not APPROVE, task190 retires,
> without further argument and without another override. This is the only one.

The eight fixes the override carries are worked in the order they bind: the sampling design filed as a fact
about the sample; the reliability factors shipped; the terms the graded components use defined; the
allowance and the upper limit made to reproduce from the shipped table; tolerable misstatement stated as a
judgement with the derivation deleted; the four ask forks pinned in the asking sentences; the whole-euro
marker taken off the certainty lines; and the payment-run realism done with the run pins in one pass.

## What is filed and what is open, after the override

**Filed, as facts about the sample and not as a method.** The testing schedule's basis of selection states
that the lines tested were selected with probability proportional to recorded value by stepping one
interval of 180,000 euro through the population's cumulated recorded value from a random start; that the
single interval was used for the whole population and was **common to every work programme**, none having
an interval of its own; that a line recorded at 180,000 or more spans a whole interval and was therefore
certain of selection; and that a line below the interval was selected with probability equal to its
recorded amount over the interval. Manual 9.3 defines selection interval, certain of selection, tainting,
basic precision, incremental allowance and upper misstatement limit. Manual 9.5 ships the Poisson
reliability factors at 95 per cent for nil to twenty overstatements.

**Open, and it is the decisive step.** No shipped sentence says how to get from the tested lines to the
population. The estimator is the analysis: the misstatement the testing found, the findings scaled on
recorded value, the certainty lines at their own error with the rest scaled on their stratum, or each
tainting at the interval with the certainty lines at their own error. `checks.py` asserts by word sweep,
with the PDFs' content streams decompressed, that no shipped file projects, extrapolates, scales up,
grosses up or multiplies a tainting.

**Why filing the design does not file the answer, measured rather than argued.** The cold reader had the
certainty stratum without being told it, named it at about 100,000, and still filed a value-weighted ratio
estimate of about 130,000 and accepted the population. Knowing how a sample was drawn and knowing what one
of its rows stands for are different pieces of knowledge, and only the second decides the call.

**What filing the interval closed.** The per-programme-interval route, which gave an authority figure a
quarter again as large and which nothing in the earlier pack refuted, is closed by the one clause that the
interval was common to every programme. `checks.py` computes that route and asserts it lands on a
different stated figure, so the closure is executed rather than claimed.

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

### The selection interval, filed rather than recovered

Earlier passes of this build left the interval to be recovered from the tested set and enumerated ten
routes a solver might recover it by, one of which the record admitted. The first determinism judge refused
that: the pack did not hold the interval, the decision rested on it through basic precision, and the
recovery the note claimed was not one either isolated thread performed. The interval is now filed. The
route table, the lattice feasibility search and the granularity argument built on the route spread are all
retired with it, and the generator's determinism block now asserts the two things that matter instead:
that the filed interval and the filed start reproduce the shipped selection exactly, and that the
per-programme-interval route the working paper rules out lands on a different figure.

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
| below 0 | the misstatement found in the tested lines | 21,004.93 | 569,406.90 | certify | |
| 0 | the errors found scaled on the population's recorded value over the tested recorded value | **57,577.47** | 620,608.46 | certify | x2.74 |
| 1 | certainty lines at their own error, the rest on their stratum's recorded value | 156,183.24 | 758,656.54 | certify | x2.71 |
| 2 | **each tainting at the filed interval, certainty lines at their own error** | **840,096.72** | **1,607,781.54** | **extended testing** | x5.38 |

The incremental allowance on the golden is 227,684.83, which is 0.27 of its projection, and the allowance
on each wrong rung is modelled at 0.40 of its own sample part, so every rung is tested at the conservatism
the golden itself earns. **No wrong rung reaches extended testing**: the nearest one's upper limit is
758,656.54, **65 per cent of materiality, a 35 per cent margin**, while the golden clears materiality by
**39 per cent**. Basic precision alone is 0.466 of materiality. Every certainty line was found sound, so
the certainty part of each rung is nil and the allowance falls entirely on the sampled part.

**The decision is robust to how the bound is built, which matters because the bound's construction is not
filed.** The crudest defensible one-sided bound at the stated confidence is the projection plus basic
precision, because basic precision is by definition the bound when nothing is found: 840,096.72 plus
540,000 is **1,380,096.72, which clears materiality by 19 per cent**. So a solver who knows only the
single factor the manual's own table gives at nil overstatements, 3.00, reaches the right decision,
and every richer bound clears it by more. The nearest wrong rung fails under every bound: 129,201.54 plus
540,000 is 696,183.24, 60 per cent of materiality. Every rung walks one way, the decisive move is the
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
| A1, per quarter of release: the value the runs released past the cut-off then in force carried. Both conventions are pinned in the asking sentence. The plain count of runs released was cut first, then the count past the cut-off: each was free to the cracker and no device reached either | 4 x 1 = 4 | three devices, each measured: the cut-off moved from 15:00 to 14:00 on 1 July 2026 and the register carries both effective dates, so one cut-off for the year undercounts both later quarters; a run released past midnight ends each quarter, so grouping on the opening date rather than the release moves the counts; and one run was rejected by the bank and re-released, so the log carries it twice. A run released exactly at the cut-off is within it, which the register states |
| A2, per supplier risk category: the suppliers raised into it, those removed from it, and those raised in then removed. "Removed from it" is pinned in the asking sentence, against the removed-into reading | 5 x 3 = 15 | the **grain** primary: an approval decision is taken on a trading group and recorded against the parent only, so a decision reaches every member the master names. Nothing says a row covers more than the number on it; a reader finds it by seeing a member hold a current risk category with no approval row to account for it, and then intersecting the register against the master's parent column. Hazards beside it: the superseded rows the dictionary rules out of the history, and the October relabelling the scale map resolves | the approval register chains per supplier and carries superseded rows the dictionary rules out of the history; a category was relabelled on 1 October and the scale map carries both codings |
| A3, per month of payment: the distinct ledger lines the testing schedule covers, whether any schedule line is missing from the ledger and if so how many, and whether any ledger line is on it twice and if so how many. "Distinct" and the month of payment are pinned in the asking sentence | 12 + 2 = 14 | two primaries. **Scope:** the working paper is internal audit's paper for the year, so plan 4.4's revenue expenditure sample sits on it under its own cost centres and its own ledger prefix; seventeen rows resolve to no capital line, are counted in no month, and nothing flags them. **Clock:** the paper carries the date the run was released, as the payment run log records it, while the ledger carries the date of the run that paid the line, and the two differ for the seven runs whose release ran past midnight, two of which cross a month end | the schedule is a table inside a PDF and its line references carry the ledger's supplier prefix, so the join needs the crosswalk; the re-delivered batch puts one ledger line on the schedule twice |

Every A3 ask is worded so that "none" is a grammatical answer, per H23.

Pair ceiling: 38.1

Mirror leakage: 12.0 per cent of ask weight

Measured by: `generator/ceiling.py`, which builds both responses as code, scores each on its OWN ask
readings against the graded figures in `figures.json` on the cut pack, and exits non-zero unless the
cracker keeps nothing, the mirror keeps under 35 per cent and the pair sits at or under 40. **It currently
exits non-zero on all three.**

**The measurement is failing and the asks are open work.** The first version of this script scored both
responses on the same ask readings, both rows taking the mirror's A1 stops and the mirror's A2 reading,
and hardcoded the third ask to nil for both, so the ask component of the ceiling and the whole of the
mirror leakage were one reading counted twice; the two labels were crossed against
`supplemental-stumping` Part 1.1 as well. Scored properly, with each response on its own readings and the
third ask actually scored:

| Response | call | components | instruction | A1 | A2 | A3 | score |
|---|---|---|---|---|---|---|---|
| the cracker, which lands the call, runs the hygiene battery and executes every filed rule | 4/4 | 19/21 | 2/2 | 0/4 | 5/15 | 1/6 | **56.0** |
| the mirror, which stops at the recorded-value ratio and takes each obvious reading | 0/4 | 6/21 | 2/2 | 0/4 | 3/15 | 0/6 | **20.1** |

**Why the cracker keeps everything, which is the diagnosis and not a wording problem.** Every device on
every ask is adjudicated by a filed sentence or found by the hygiene battery, so a careful solver executes
it: the cut-off register carries both effective dates, the run log carries the release timestamp and marks
the re-released run, the scale map resolves the October relabelling, `event_status` marks the superseded
rows, and A3's twelve monthly counts come straight off the schedule's own `paid_date` column and need no
join at all, which is why even the mirror takes 12 of 14 there. There is not one silent primary in the
set. `supplemental-stumping` Part 5 names this exactly: a pin says what to compute and never makes
computing it correctly hard, so every pin has to be paired with a silent primary underneath it. The asks
need silent primaries, which is design work on the ask data, not a re-worded sheet, and it is open.

**The cracker sheet.** One row per ask, the cracker being the response that lands the call, runs the
hygiene battery and executes every filed rule and column description. Measured by
`generator/ceiling.py` on the cut pack.

| Ask | What the cracker does | What it never reaches | Verdict |
|---|---|---|---|
| A1 | reconciles the run log to the ledger it was given and rebuilds the value it can tie | the log records the whole run and the capital extract holds only its capital part, so every value figure is short by the revenue part, which ties to the revenue expenditure summary month by month | miss |
| A2 | reads the approval register as it stands, one decision against one supplier number | a decision is taken on a trading group and recorded against the parent only, so the suppliers raised into or removed from a category are the group's members, which only the master's parent column and a member holding a category with no row of its own reveal | miss |
| A3 | splits the paper's reference, joins to the ledger and runs the unmatched-join sweep | five rows are certified valuations recorded at invoice level, so each covers every line on its invoice; the sweep reports them as missing from the ledger, which is wrong, and the quarters are short by the lines they carry | miss |

Measured: the cracker gets **no ask whole**, keeping 4 of 8 on A1, 5 of 15 on A2 and 1 of 6 on A3, which
is 10 of the 29 ask figures against a measured ceiling of 12, and the pair reads 38.1.

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

**The leak report's lines, answered.** REVIEW on eight lines, no LEAK, each read against this pass's
pack.

- **Block 3, five lines.** One matches the clause number 4.3, not a figure, in the heading "4.3
  Conclusion on a tested population". The others are the plan and the provenance note carrying the call's
  distinctive words, because the call is asked in manual 9.1's own vocabulary: payment, population,
  misstatement, programme, tested, year, euro. The question cannot be asked without them and no shipped
  file carries the figure, asserted by word sweep with the PDF content streams decompressed and with a
  positive control proving the sweep can read each PDF before any absence is asserted.
- **Block 4, the manual and the schedule share the design note's vocabulary.** Deliberate, and the
  author's override is why: the manual defines selection interval, certain of selection, tainting, basic
  precision, incremental allowance and upper misstatement limit, and the schedule states the basis of
  selection. Read for whether either names the move: neither says how to get from the tested lines to the
  population, and `checks.py` sweeps for projecting, extrapolating, scaling up, grossing up and
  multiplying a tainting and finds none.
- **Block 9, dates after the as-of in the capital programme register.** The programmes' planned
  completion dates, now spread from 2027 into 2029. A capital register carries the dates the works are
  due to finish, and the figure never reads the register's values (SF11).
- **Block 10, container metadata.** INFO; the pack is clean.

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
- **The interval left to be recovered from the tested set.** Ten routes were enumerated, one admitted by
  the record, and the granularity was set from the spread of the five that agreed. The first determinism
  judge refused it: the pack did not hold the interval, the call rested on it through basic precision, and
  neither isolated thread performed the recovery the note claimed, the cold reader instead taking
  materiality over the reliability factor and filing a figure twice the golden. The design is now filed as
  a fact about the sample and the estimator alone is open. The route table, the lattice search and the
  granularity argument built on the route spread are retired with it.
- **The whole-euro contractor certificates.** Every line certain of selection was a whole number of euro
  and the only whole-euro line above 100,000, so `cents == 0 and amount >= 100,000` selected the certainty
  set exactly, with no false positives and none missed. Both isolated threads found the certainty set that
  way rather than from the interval. Measured: 31 of 31 certainty lines whole euro against 1.04 per cent of
  the lines below the interval. The certificates now carry cents and about one sundry line in nine is
  invoiced at a round euro, a half euro or a round five euro across every size band.
- **The paper cracker sheet, and the first code that replaced it.** The sheet claimed every ask figure
  missed and reported a pair ceiling of 37.1 with 22.0 per cent mirror leakage. Written as code the two
  responses were scored on the same ask readings, both rows taking `the_cracker` for A1 and `a2_unmapped`
  for A2, and the third ask was hardcoded to nil for both, so the ask component of the ceiling and the
  whole of the leakage were one reading counted twice. The labels were also crossed against
  `supplemental-stumping` Part 1.1. Scored properly the cracker takes 41 of 41 and the pair ceiling is
  69.3. The asks need silent primaries, which is open work and not a re-wording.
- **The word sweep that could not see the PDFs.** `_sweep` read every shipped file as raw bytes, so it
  never saw inside the three PDFs' Flate-compressed content streams, which is exactly where the authority
  sentences live. Every R3c claim rested on it. It now decompresses the streams through `verify.pdf_text`.
- **Tolerable misstatement derived from budgeted capital expenditure.** The plan called 1,160,000 two per
  cent of budgeted capital expenditure while the register summed to a figure giving 1,189,620, a
  contradiction of 29,620 that the call did not turn on. The derivation is deleted and the figure is stated
  as the head of internal audit's judgement, which is what an audit plan does.
- **The register's approved budget equal to the year's spend.** Each programme's budget was the year's own
  recorded value rounded to the thousand, so the register reconciled to the ledger exactly and the budget
  carried no information. It now carries the board's approval figure, which differs from the spend.
- **Pins alone against the cracker.** The four ask conventions were pinned in the asking sentence, which
  is where a pin belongs, and the measured pair ceiling moved only from 69.3 to 67.8 with the mirror
  leakage from 51.2 to 46.3. The cracker still takes 41 of 41. That is the skill's own rule arriving
  empirically: a pin says what to compute and never makes computing it correctly hard, so a pin without a
  silent primary under it buys determinism and no difficulty. The primaries are open work and the four
  families the author named for them are unspent in this world.
- **A3's monthly figure read off the schedule's own date column.** Twelve of the ask's fourteen figures
  were a group-by on `paid_date` with no join at all, which is why even the mirror took twelve of them.
  Pinning the count to distinct ledger lines costs the mirror one figure and nothing else. The ask needs
  re-routing through the resolution chain rather than strengthening, which is open.
- **Two visible devices tried against the cracker, and what they measured.** A3's scope primary (plan
  4.4's revenue sample on the same working paper) and its clock primary (the paper's release date against
  the ledger's run date) together took the mirror from 46.3 to **26.8 per cent of ask weight, which passes
  its bar**, and the pair ceiling from 67.8 to 62.0. Neither moved the cracker, which still takes 41 of
  41. The reason is general and belongs on the slot's record: **a device a careful reader can resolve from
  a column description cannot suppress the cracker, because the cracker reads the dictionary.** The scope
  device is found by the unmatched-join sweep, which is a battery check, and the clock device is resolved
  by reading two honest date definitions. Both are legitimate mirror devices and neither is a primary in
  the sense the cracker test means. What suppresses the cracker has to be discoverable only from an
  internal inconsistency that nothing invites, and the candidate designed for it is below.
- **The grain device, built, and the two figures it cost to build it safely.** Five tested items are
  certified valuations the paper records at invoice level, so each row covers every payment line on its
  invoice rather than one line. It is the first device in this build that costs the cracker anything:
  A3 fell from 14 of 14 to **8 of 14**, because the unmatched-join sweep reports the five invoice rows as
  missing from the ledger, which is wrong, and the monthly counts are short by the lines those invoices
  carry. Every line on the five invoices was found sound, so the projection is identical read at line or
  at invoice level, and `checks.py` asserts the tested set, the certainty set, every per-programme figure
  and the unrounded total identical with the device deleted. What it cost: the lines tested and the value
  tested are read off the paper, and the invoice rows make both ambiguous, so neither is stated as a
  figure any more and the three wrong rungs are no longer quoted to the cent in the recommendation. That
  is the right trade, because a graded figure a judge cannot rebuild is the commonest finding in the
  record, but it is a trade and it is recorded as one.
- **The earlier draft of that device, which would have moved the call.** The paper would identify
  a handful of tested items by their invoice reference rather than their line reference, in the same
  shape, so those rows resolve to the ledger's `invoice_ref` and cover two or three payment lines each.
  A response that reports every unresolved row as missing is then wrong on the absent count, and one that
  counts a line per paper row undercounts the months. It is silent: only reconciling the paper's recorded
  amount against the ledger, where one paper row equals the sum of two lines, reveals it. It was not built
  because it changes which lines the paper identifies as tested, which moves the main call, and the
  separation rule and the author's standing instruction both say a device that moves the call is the
  gravest finding. Building it needs the invoice-level rows to cover lines that are already in the tested
  set, so the tested set is unchanged, and that construction has to be measured before it is cut.
- **The band weights at the favourable end of every permitted range.** `ceiling.py` weighed the call at
  0.12, the critical components at 0.18, instruction-following at 0.10 and the asks at 0.60. Every one is
  legal under the house spec, but the recommendation side sat at the bottom of its range and the asks at
  the top, which gave a response that lands the call a floor of **40.0** against `supplemental-stumping`
  Part 0's **45.0**, and so flattered the pair by 2.5 points in the field the gate reads. The bar of 40
  was derived on Part 0's numbers, so the gate now computes on Part 0's numbers: 38 for the recommendation
  and the components, 7 for instruction-following, 55 for the asks. Measured with the script rather than
  argued on paper, the cracker may keep at most **10** of the 41 ask figures for the pair to reach 40; on
  the old weights it was 11.
- **Dropping the figures the grain device made ambiguous, rejected for naming the quantity instead.** The
  invoice-level rows made the lines tested and the value tested ambiguous, and the first fix was to stop
  stating them. The better fix is to name the quantity in the asking sentence, the ledger lines the
  testing covered and their recorded value, which is one determinate answer that a response counting the
  paper's rows gets wrong. The device then bites on a graded figure instead of costing one, and the three
  wrong rungs are quoted to the cent again. Measured: the cracker loses 2 of the 21 component cells.
- **Ask figures the cracker kept that no device could protect, cut rather than defended.** The bar is a
  share of ask weight, not a count, so a figure every strong response banks for free is worth less than
  nothing: it dilutes every criterion beside it. Of the 31 the cracker still kept, twelve were free by
  construction. **A1's plain count of runs released** was a row count per quarter after the duplicate
  sweep and the pinned basis, so it is cut: A1 is now two figures per quarter, both of which need the
  cut-off register and the run log's own value. **A3's twelve monthly counts** were a group-by in which
  only four months carried a device, so they fold into four quarters of payment, and now every quarter
  contains a device-touched month. Measured: the ask set falls from 41 criteria to 29, the cracker from 31
  of 41 to 20 of 29, A3 from 8 of 14 to **1 of 6**, and the pair from 51.0 to **47.6**. The floors hold:
  56 graded criteria against a floor of 25, and the ask weight is unchanged at 55 per cent.
- **An overnight release scored as inside the cut-off, which the fold exposed.** A run released at 01:30
  on the day after its run date was compared against that morning's clock, so the latest run of the
  quarter counted as the earliest. Minutes now run from the run's own date, so a release that crossed
  midnight is past that date's cut-off by construction, which is both the correct reading and what makes
  the quarter basis worth pinning.
- **A2's grain device, and the measurement that closed the pass.** An approval decision is taken on a
  trading group and the register records it against the parent the submission came in under; the master
  names the parent each supplier belongs to, and the members carry no row of their own. A response that
  reads one row as one supplier undercounts every category. Measured: A2 fell from 15 of 15 to **5 of 15**
  and the pair from 47.6 to **38.1**, which is the first measurement in this build to clear its bar. The
  discovery route is the one the shape promises: a member holds a current risk category with no approval
  row to account for it, which shows only by intersecting the register against the master's parent column,
  and no battery sweep performs that intersection.
- **The realism tail, cleared before the hand-back rather than after.** Supplier names are now a mix of
  family firms, trade names and place names with varied suffixes rather than a town-plus-trade grid; the
  crosswalk's numbers were issued in blocks as trades migrated, so they step from the ledger's by no
  stride; the supersessions are no longer symmetric pairs, with some arriving the same day, some weeks
  late and a couple whose effective date disagrees with the row they replace; the funder's claim has the
  shape a claim has, eligible expenditure by how long the programme has been running, the grant at the
  funder's 45 per cent intervention rate, and the two newest programmes with nothing yet to claim; and the
  revenue summary's maintenance line is seasonal on the spring and autumn shutdowns. It was cleared first
  because the next isolated reader sees a pack whose prompt and documents have moved, and a reader
  rediscovering a known item spends the pass on a list already in hand.
- **The mirror modelled rather than measured, which flattered the pair twice over.** Two of its scores
  were assumptions with nothing behind them. Its nine certain-share cells were credited only to the
  response that lands the call, which was true while the interval had to be recovered and false the moment
  the interval was filed: any response that reads the working paper computes all nine. And its
  instruction-following was scored 1 of 2, where the rubric spec says instruction-following covers the
  requested files and output-shape asks, all of which a wrong-rung response produces. Corrected, the
  honest pair was **44.7**, not 38.1. Two cuts brought it back: the deliverable's second column is now the
  misstatement as a share of the programme's recorded value, which moves with the estimator, in place of
  the certain share, which every route banked; and A1's count of runs past the cut-off was cut after its
  plain run count, because the cut-off register files both effective dates so the cracker applies them.
  **Measured against `supplemental-stumping` Part 0: the mirror's recommendation side is 6.5 of the 38
  points, above Part 0's r of about 5, and 13.5 before the asks against Part 0's 12**, so the model is now
  slightly more generous to the mirror than Part 0 assumes rather than harsher. The six component criteria
  it earns are named: the three nil programmes, Deepwater berth renewal, Quay 3 reconstruction and the
  Dredging programme, on both columns, where nil is nil under any route.
- **The prose of Part 1.1 and the script that enforces it disagree, and the disagreement is worth
  filing.** The prose scores "each ask figure and chart criterion" and then says "every row misses or the
  ask is rebuilt", which reads as a per-figure zero; `precut.py` reads the rows of the cracker table in
  the design note, at whatever granularity the author wrote them, and checks each ends in a miss. Read as
  a per-figure zero the prose makes the pair ceiling redundant, which cannot be its purpose, so it is a
  design-iteration instruction and the ship gates are Part 7's two numbers. `ceiling.py` gates on those
  two and prints the figure keep beside them, because every figure the cracker takes costs pair points.

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
| Selections | 331, on 274 distinct tested lines; 31 certainty lines hold 81 per cent of the tested book value |
| Basic precision | 180,000 x 3.00 = **540,000, which is 0.466 of materiality**, so step one escalates nothing |
| Stated granularity | the nearest **50,000** EUR, set from the measured route spread below |

### The ladder, measured on a real selection

A synthetic population in four classes (contractor certificates, subcontractor interim payments, day-work
variation invoices, sundries) and a real monetary-unit selection at 180,000 from a random start. The
defect is a wrong day-work labour rate applied across small variation invoices in six programmes; eleven
of them fall in the sample, and one certificate carries a separate 24,000 error.

| Rung | The analysis | Figure | Upper limit | Decision | Step |
|---|---|---|---|---|---|
| below 0 | the misstatement found in the tested lines | 41,306 | 588,229 | certify | |
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
the 274 tested lines must contain a step of cumulated book value under one common start and none of the
24,426 untested lines may, and the untested lines are what make it unique: the tested lines alone narrow
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
433,333, which leaves the recovery intact. The general rule, going into the slot's record: **before filing
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
> establishes the difference only for the lines tested. The head of internal audit satisfies himself each
> year that the figure reported rests on the year's own payment records and the testing performed on them.

What those two documents between them do **not** say: the interval, the number of selections, how the
population was ordered or selected from, the expected misstatement allowance, any reliability or expansion
factor, any evaluation procedure, and anything about projecting, scaling, weighting or extrapolating a
finding. 4.2's two figures bound the interval below 433,333 and no further. 9.1 files population, outcome,
window, unit, segmentation and grain, and 9.2 says no column holds the answer.


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

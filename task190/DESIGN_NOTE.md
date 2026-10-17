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

**The ladder's arithmetic, on paper.** Materiality 750,000 EUR on a population of about 62,400,000 EUR in
about 26,000 payment lines; k about 520,000; about 18 certainty lines holding about 16,000,000; about 107
tested lines below k.

| Rung | The analysis | Figure | Decision it files | Worth |
|---|---|---|---|---|
| below 0 | report the misstatement actually found in the tested lines | about 165,000 | certify | no projection at all; no competent analyst stops here |
| 0 | scale the errors found on the population's book value over the tested book value | **about 320,000** | certify | the default path; the tested book value is dominated by the certainty lines, which are sound |
| 1 | band the tested lines by size and scale each band on its own book-value ratio | about 620,000 | certify | the right instinct about size bias, applied with the wrong weight; within the lowest band the inclusion chance still rises with amount |
| 2 | take the certainty lines at their own error and scale only the rest by book value | about 700,000 | certify | the certainty stratum handled correctly and the rest still wrong |
| 3 | **recover k and project each tainting at it, certainty lines at their own error** | **about 1,160,000** | extended testing | the golden; the extreme of the ladder, and the only rung that crosses materiality |

Every rung walks one way, each is defensible and reproducible from the raw files, and only the decisive
move reverses the decision. The decisive move is +460,000, the largest single step; the default path is
3.6x away from the golden. The figures above are design targets and are pinned in `figures.json` at stage
3, mid-cell on non-round values with each flip condition stated as a number.

**The blind-response test, measured at the draw.** The widest graded component is the nine programmes
times two figures. The blind move is one rate on one size column, the programme's book value. It is
designed to fail: four of the nine programmes carry no tainting at all, so their projected misstatement is
nil and any non-zero rate misses them; among the five that do, the taintings are placed so the projected
misstatement is not monotone in book value, with the largest misstatement in a programme that is seventh
of nine by size. The second figure per programme is the share of the programme's book value that was
certain of selection, which depends on the programme's own size distribution and is not any rate times
anything. **The target to assert in `checks.py`: at the best single rate on book value, a blind response
matches at most 2 of the 18 cells, and at most 0 of the 9 misstatement cells without also missing every
nil.** This is measured on the cut pack before the bundle is declared ready, and if it fails the asks' shape
changes rather than the data.

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

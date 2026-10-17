# task194 design note

Placing a scarce improvement team when the unit standing worst is partly standing worst by chance.

## Draw

**Architecture 2.** Architecture 1 was sent back at stage 4 and is spent; its identity, fate and driver are
in the card's `lineage` and its dead end is the last entry under `## Tried and rejected`. The world is kept
whole: Mid-Rivers Health Network, four hospitals in regional Australia, the hospital-acquired complication
indicator on specification 4.0, the episode extract, the quarterly series, the activity plan, the unit
register and the closed placement register. What is re-chosen is the quantity the call rests on.

**Card:** `healthcare-delivery-health-economics` / `provider-quality-risk-adjustment`, objective
`anomaly-detection`, shape 14, decision `pick_one_of_n`, gap `objective`, Gate G
`decomposition_attribution`, strategy `composition_mix`, Layer 2 family `field_method`, pattern
`own:internal-against-external-standardisation`, generators G6, G14, G11, G2, calibration form `none`,
context artifact `monitoring_export`, forum `executive_team`, forcing event `budget_or_appropriation`,
question form `which`, role family `portfolio_manager`, people Maureen Watts and Joseph Hunter.
`guard.py check` clears every BLOCK; nearest driver on file 0.06 (task464 v1). Six axes were redrawn
against live BLOCKs while sibling builds registered beside this one: the context artifact twice
(`published_series` against task191, then `filed_standard` against task240, settling on the dashboard
export), the forum, the forcing event twice, the role family, and the decisive gap, which moved from
`population` to `objective` because gap, generator and decision type together were spent in four earlier
builds.

**The two WARNs, answered.** `overuse.objective`: anomaly detection is four of the last twelve, and this
draw is in it because the question is whether a unit's reported excess is the unit or the measurement
system, which is the objective's own work; the Gate G mechanism, the strategy, the Layer 2 family, the gap
and the generators are all different from every other anomaly-detection build on file.
`repeat.question_form`: "which" repeats task240 across the last two prompts, and it is the only honest
opening for a pick of one unit from twelve; the prompt's shape, deliverables and sentence structure are
drawn independently of it.

**The quantity the call rests on is measured, not fitted.** Every graded figure is a count summed from the
record: a unit's observed complications, the complications the comparison population's own rates give its
patients, and the difference between them on the quarter's planned activity. Nothing in the call requires a
functional form to be chosen, which is the failure that spent architecture 1.

**Data-native sentence.** Specification 4.0's stratum rates were set on FY2023-24 network activity and
clause 3.1 says they are not re-estimated between specifications, while the network's own rate has since
moved in opposite directions across the complication groups; because the twelve candidate units differ
several-fold in case mix, a ratio against those published rates carries each unit's composition as well as
its practice, and the units it penalises most are the ones whose patients sit where the standard has gone
most out of date.

**Sources read.** `references/client/two-layer-task-design.md`: the client's two-layer standard, which this
draw answers with the published standard as Layer 1 furniture and the comparison's construction as Layer 2.
`strategies.md` Part 4 and Part 6: `composition_mix` is drawn here because the composition that moves the
answer is a risk-stratum mix the pack publishes a rate table for, not a segment share a column names, and
no build on file carries that. `guard.py mechanisms --objective anomaly-detection`: the anomaly-detection
drivers on file turn on a count read before its records arrive, a selected extreme against the record of
extremes, a shared driver with lagged response, and a detection threshold that moves; none turns on the
standard the excess is measured against.

**Kept from architecture 1, which the judge confirmed sound:** the eight-placement register with its spread
of standing, the charter sentence fixing a unit's position as its own closed quarters rather than any one
of them, the eligible row set and the separation key pinned, the realism work on casemix, weekday,
holidays, length of stay and comorbidity, the measured cracker, and the series tying to the extract on all
215 unit-quarters with no shipped file ranking the candidates.

**Two defects carried forward as stage 3 work, not inherited:** the four hospital-level adjusted rates are
still edge-fragile, one at 0.019 of a bin and another flipping on a single complication either way; and the
activity summary equals a de-duplication on one key in all 90 unit-months while the dictionary states
another, which gives supplementary answer 6 two defensible series. Both are closed before any reader sees
the pack.

## Default path

The pipeline a competent analyst builds from the prompt's words and the files' own grain. Figures are
measured at stage 2 on the built panel; the names below are what the design puts at each step.

1. Read `episode_outcomes_extract.csv`, apply specification 4.0's denominator and its four exclusions, join
   `drg_risk_bands.csv` and `hac_stratum_rates.csv`, and compute every unit-quarter's observed and expected
   complications; the result ties to `unit_indicator_series.csv` row for row and to the dashboard export.
2. Apply charter clause 4.2 through `unit_register.csv` and `improvement_placements.csv`: twelve eligible
   units.
3. Take each unit's observed complications less its expected complications over the specification period,
   and scale that excess to the quarter's planned separations under clause 3.4.
4. Rank the twelve on that excess and read the top.
5. Put the improvement team with the unit at the top of that ranking.

**Ends on:** Alderbrook General Surgery (cost centre 41220).
**Golden:** Alderbrook Orthopaedics (cost centre 41230), 40.0 avoidable complications on its 2,305
planned separations. The unit the default path names carries minus 3.7.

## Stump sentence

A competent solver reconciles to the published indicator, ranks the eligible units on the complications
each records above the expectation the published stratum rates give it, and places the improvement team
with Alderbrook General Surgery (cost centre 41220), which is the unit whose patients sit where the
published standard has gone most out of date rather than the unit whose own patients are having the most
complications they should not be having; on the comparison the charter asks for, that unit is carrying
minus 3.7 avoidable complications and the unit that is carrying 40.0 sits fourth on the ranking it read.

## Three rules

- **Task type:** `provider-quality-risk-adjustment`, which the client taxonomy lists under Anomaly
  Detection & Diagnostics: separating a provider's own signal from what the measurement system produces is
  the task type's own work, and the pack ships the episode-level raw material the risk model runs on.
- **Domain test:** the deciding quantity is a provider's excess over the outcome its own case mix implies.
  Provider profiling obtains it by standardising, either indirectly against a published external standard
  or against the rates the comparison population itself achieves, and the two agree only while the external
  standard still matches that population. Indirect standardisation, stratum-specific rates and the case-mix
  distribution are the field's own instruments and all three ship.
- **Swap:** "Which of our twelve machines should the calibration crew spend the quarter with, and how many
  out-of-tolerance parts is it producing that it should not be?" Machines calibrated against a fixed
  reference run one uniform process, so there is no case mix for a standard to mis-state and the published
  excess is the excess: the question becomes a sort. The task only works where the outcome is risk adjusted
  against a published table and the units differ in the patients they treat.
- **Layer 1:** episode records at two grains; a national complication list revision mid-period; two wards
  amalgamated into one cost centre; a comorbidity score keyed on part of the episodes at a rate that moves
  with the month; three cost centres realigned to another hospital site while the register carries only the
  current alignment; wards off the clinical information system whose complications reach the warehouse only
  as the episode record's own category; fiscal quarters against the calendar year the hospital-level ask
  uses; tables inside PDFs. Every item is what these systems produce and each is asserted neutral (R2).
- **Layer 2:** `field_method`. The methodological choice that flips the call is what the excess is measured
  against: the expectation the published stratum rates give a unit's patients, or the expectation the
  network's own rates over the same period give them.
- **Decisive step:** rebuild the expectation from the rates the comparison population itself achieves,
  because the published rates are a fixed FY2023-24 standard, the network's own rates have since moved by
  different amounts in different complication groups, and the candidate units' case mixes differ
  several-fold, so a ratio against the published rates carries composition as well as practice.
- **Not semantics:** every field, code, unit and definition read correctly still leaves the easy route on
  the published excess. The extract's fields are plain, the specification files the denominator, the
  exclusions, the published rates, the reporting periods and the forward activity basis, and the charter
  files the population, the outcome, the window, the unit and the comparison. A solver who reads every one
  of them correctly, and whose observed and expected counts tie to the published series row for row, still
  ranks on the published excess and names Alderbrook General Surgery.
- **Not rule application:** no filed rule, formula or procedure builds the comparison the charter asks for.
  Specification 3.1 files the published rates and says in the same sentence that they are not re-estimated
  between specifications; nothing in the pack computes what the network's own units achieve, by stratum or
  at all, and no file carries a second rate table. Executing every stated rule gives each unit a published
  ratio and stops there.
- **Analyst test:** a strong analyst who applies charter 4.2 and 4.4, reads every field and every code
  correctly and reconciles to the published series row for row ranks the eligible units on the excess the
  indicator reports and places the team with Alderbrook General Surgery (41220).
- **Estimand:** the complications the unit's planned activity for the quarter carries above the
  complications that patients of the same risk band and age band ordinarily have, charter clause 4.3,
  with the population in clause 4.2, the activity basis in clause 4.4, the reporting period in
  specification 3.3 and the indicator's denominator and exclusions in specification 4.0 clauses 2.1 to 2.4.
- **No decoy:** nothing is planted to be caught. The published stratum rates are the real published rates
  and are correct for the indicator they define; the indicator series, the dashboard and the activity
  summary are each correct for the question they answer and reproduce from the extract to the row. No block
  of readings is copied or backfilled, no memo argues a candidate, no stakeholder figure is wrong, and the
  difficulty survives deleting every wrong number because there is none.
- **No certified replay:** the pack carries no corpus of settled decisions and no achieved-reduction
  column; the calibration form is `none`. The comparison the charter asks for is a construction the analyst
  makes from 290,000 episode records, not a figure a file reproduces.
- **Lesson:** a standardised ratio is a comparison with whatever standard produced its denominator, and
  when that standard is fixed at a vintage the comparison population has moved away from unevenly, ranking
  providers on it ranks their case mix as much as their practice. No build on file teaches it: the
  anomaly-detection drivers on file turn on when a record arrives, how an extreme was selected, a shared
  driver with a lagged response, or a detection threshold that moves.

**The WHAT screen (`stumping` 1.2).** The decisive step settles none of the five parts. Population: charter
4.2, the twelve eligible units. Outcome: specification 2.1 to 2.4, episodes recording a complication.
Window: the assessment quarter for the activity, the specification period for the rates, both filed.
Unit: complications, counted at the unit. Comparison: charter 4.3, against the complications that patients
of the same risk band and age band ordinarily have. What stays open is which
frequency answers "ordinarily have", and the data force it under `determinism-check` section 1's first
licence, the design forcing the method with the data separating the candidates. The separation is measured,
not asserted: the network's own rate runs from 0.886 to 1.319 of the published rate across the six risk
bands, a factor of 1.49 crossing 1.00 in both directions; the twelve candidates' surgical share of in-scope
episodes runs from 0.075 to 0.851 with three carrying none at all; and on the record one unit's own practice
is flat across a case-mix shift while the published basis moves its avoidable count by a factor of five
(`## Literal reader`). Both candidate frequencies are measured sums over the record, neither is a fitted
form, and no free parameter is chosen, so the collinearity that spent architecture 1 cannot arise.

## Tried and rejected

- Ranking units by the fall in their adjusted rate rather than by complications avoided: the charter would
  have to file a rate, and then the whole decision is a one-column sort on each unit's own standing, with the
  planned activity and the register idle. Dropped at the draw; the charter files complications.
- Giving the closed placements a hot quarter the placement was decided on (a selection shock of 0.15), so the
  register's own falls were inflated by reversion as well: it put the share a placement removes 10 per cent
  apart depending on whether the decision quarter stayed in the unit's pre-placement record, which is a fork
  on a graded figure. Replaced by placements decided on units' standing, with the decision quarter at the
  unit's own level (asserted), so the register prices the programme the same way under every reading of its
  pre-placement window.
- Block-correcting each unit's quarterly deviations so the trailing four, eight and ten quarter windows all
  returned the unit's level exactly: it left the panel with a lag-1 autocorrelation of -0.28, which licenses
  an AR(1) counterfactual below the unit's level and forks every figure. Replaced by one uniform shift per
  unit (autocorrelation -0.107 over 156 pairs, what de-meaning a ten-quarter record implies).
- A monthly reconciliation ask whose gap was the activity summary's own vintage: it needed the summary to be
  short for the acute units too, which breaks the referee the call's own reconciliation leans on. Replaced by
  A3 on the non-acute units, where the summary stays exact and the replay is the device.

- **This pass, the reader's and the judge's findings in one generator pass.** The judge's recomputation
  confirmed the structure and asked for four things; the reader found a data defect and a realism list. The
  register's ten readings were brought from a 10.75 per cent spread to 2.9 per cent by levelling the network's
  own quarterly position and holding the comparison units still across each placement's two quarters, with
  the two operations writing disjoint unit-quarters so they no longer undo each other, and by choosing the
  embed-quarter counts once on the narrowest reading band rather than twice on different objectives. What
  "avoided" means is filed as a difference between two counts in charter 4.3, the standing's window in
  specification 3.3, and the in-progress placement in charter 4.2. The shared-admission path recomputed the
  length of stay, so no episode now separates before it was admitted. Ask 1's basis is pinned in the asking
  sentence and ask 3's missing units are declared in `unit_register.csv`.
- **Rejected: grading the twelve per-unit figures as the effect-free excess** to take the register's reading
  out of them. The prompt would then have to ask for the complications a unit's planned activity carries
  above its own standing, which files the decisive step. Kept the avoided counts and centred each unit's
  planned volume so all twelve round the same way under every reading instead.
- **Rejected: a cross-site patient index collision as texture.** Two episodes in different hospitals shared a
  patient number and an admission date, which reads as one duplicated episode and puts ask 1's episode count
  in play. Issued the index in blocks by site instead, which is what a master index does.

- **This pass, the judge's SEND_BACK closed on the register rather than by filing a method.** The judge
  found three pricings of the embed defensible on a register that carried no sampling noise: its own fit was
  chi-square 0.006 on six degrees of freedom and the likelihood ratio over the constant-drop shape was 1.8 to
  1. The repair widened the closed placements' standing from a unit at its expected number to one at nearly
  twice it, which is what makes a share of excess and a constant drop predict different falls, and let the
  quarters before each placement and the assessment quarters carry their own scatter instead of being forced.
  The three competing shapes now sit 1.4e7, 2.0e4 and 2.1e4 to one against the register's own fit, measured
  and asserted. The charter files the baseline's population and window and nothing about the shape of the
  fall.
- **Rejected: filing the effect model in the charter**, which the judge offered. It closes the fork and
  spends the stump in the same sentence: with the shape filed, every remaining step is arithmetic the
  specification already prescribes.
- **Rejected: more closed placements at the same spread of standing.** Volume moves a chi-square linearly
  and the gap needed was two orders of magnitude; what moved it was the second constraint inside the record,
  the spread of the placements themselves, which is the lesson task190 landed on from the other side.
- **Rejected: the unweighted and expected-weighted means of the per-placement shares as readings that have
  to converge.** One closed placement was made with a unit running at its expected number, so it has no
  standing excess to take a share of; those two estimators cannot be formed at all, and the register's own
  structure is what rules them out rather than a sentence.
- **Rejected: the two-constraint levelling** (holding both the unweighted and the pooled movement of the
  comparison units flat). With placed units an order of magnitude apart in size, the slope it needs pushes
  small units down and large units up by 0.1 of a ratio across the panel. One pooled constraint, and one
  difference-in-differences reading rather than two, leaves every unit's own record where it was.

- **This pass, the two routes the coordinator found.** A solver who meets an undefined per-placement share
  drops that placement and averages the rest, and that route is formable. Measured on the previous pack it
  gave 0.50719 against a pooled 0.52947 and the expected-weighted version gave 0.55306, both outside the
  window the twelve counts allow (0.51834 to 0.53955), moving six of the twelve. Rather than narrow the
  route set, the placement that was running at its expected number was raised to a tenth above it, so every
  share can be formed and all eight routes are asserted. The price was paid on the fit, as offered: the
  constant-percent shape went from 2.7e5 to one down and back up to 2.7e5 to one once the register was
  re-searched, and the headroom improved rather than fell, from 4.5 complications to 6.6.
- **Rejected: keeping a negative per-placement share alongside the two mean routes.** A placement that shows
  a rise is the right texture, but on a placement carrying 16 complications of standing excess it moves the
  unweighted mean of the shares by about 0.011, which is a third of a bin on the answer against the slack the
  eight routes leave. The register keeps the scatter in the form the window allows: one placement at 0.022
  that took off almost none of the excess it was carrying, one at 1.232 that took off more than all of it,
  and standardised residuals from -0.92 to +0.84.

- **Architecture 1 is spent: the fitted-counterfactual family is closed for this slot.** Its decisive
  quantity was the fall a scarce intervention causes, read off a closed register of past interventions. The
  judge sent it back NOT_DETERMINISTIC on `competing_defensible_answer` with margin fragility, and the
  reason is structural rather than a shortage of data. A power on the standardised ratio, where observed
  equals expected times the ratio raised to g, fits the register at chi-square 3.34 on seven degrees of
  freedom against 3.30 for a share of standing excess: **a likelihood ratio of 1.02 to 1**, and it gives 19
  against 21 for the recommended unit with a gap of 7 rather than 8. Near a standardised ratio of 1 the two
  forms agree to first order and they diverge only at high ratios, so separating them would need placements
  at ratios of three or four, which no hospital unit carries. The register's own assessment quarters were
  also **under-dispersed at 0.47 per degree of freedom against 1.65 for the rest of the record**, about
  three and a half times too clean, so every likelihood ratio the build reported was inflated and fixing
  the dispersion makes the separation worse rather than better. Three of the eight pooling routes also
  moved ten of twelve counts once enumerated properly (the mean excluding one placement 0.765, the
  geometric mean 0.480, the mean with the baseline lagged a quarter 0.537). Both forms named the same unit,
  so the call was robust and only the graded counts were not. **The rule this slot now carries: a graded
  quantity is either measured from the record or it is not graded.** A fitted quantity needs a forced
  functional form, a functional form can only be forced by the data when the plausible domain separates the
  candidates, and that has to be checked at the draw by listing the forms a competent analyst would try and
  asking whether any two agree to first order over the domain the world allows.
- **Rejected at the draw: making the window of a unit's position the decisive step.** It is the obvious
  replacement once the fitted fall is gone, and it is dead on the `stumping` 1.2 screen: the window is one
  of the estimand's five parts, so filing it makes the computation follow from the clause and leaving it
  unfiled makes the call indeterminate. The latest-quarter trap stays in the build as a rung, ruled out by
  charter 4.3, and is not the decisive step.
- **Rejected at the draw: judging each unit's excess against its own sampling error.** Measured and in the
  domain, but the ways of accounting for the error (a Poisson limit, a shrunk estimate, an
  over-dispersion-adjusted funnel) are again a family of forms with a free parameter, which is the disease
  that spent architecture 1 in another dress.

